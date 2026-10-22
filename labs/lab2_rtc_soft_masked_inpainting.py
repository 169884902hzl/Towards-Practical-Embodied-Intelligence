# lab2_rtc_soft_masked_inpainting.py
# 运行方式: python labs/lab2_rtc_soft_masked_inpainting.py
import math
import torch


def build_rtc_soft_mask(
    horizon: int,
    delay_d: int,
    exec_s: int,
    decay_rate: float = 0.25,
    mode: str = "rtc_paper",
    device: str = "cpu",
) -> torch.Tensor:
    """
    构造 Real-Time Chunking (RTC) 软掩码权重 W in [0, 1]^H (Black et al., arXiv:2506.07339, Eq. 5):
    - [0, d): 已承诺前缀 (Committed Prefix)，权重 W_i = 1.0 (严格对齐上一动作块对应步)
    - [d, H - s): 过渡融合区，默认采用论文精确指数衰减 W_i = c_i * (exp(c_i) - 1) / (e - 1)，
      其中 c_i = (H - s - i) / (H - s - d + 1)；亦支持 'exp' 或 'cosine' 核对比
    - [H - s, H): 自由远期规划区，权重 W_i = 0.0
    """
    if not (0 <= delay_d <= horizon - exec_s and 0 <= exec_s < horizon):
        raise ValueError("Require 0 <= delay_d <= horizon - exec_s and 0 <= exec_s < horizon")
    if mode not in ("rtc_paper", "exp", "cosine"):
        raise ValueError("Unknown mask mode")
    w = torch.zeros(horizon, 1, device=device)
    w[:delay_d] = 1.0
    transition_end = horizon - exec_s
    span = float(transition_end - delay_d + 1)
    for i in range(delay_d, min(horizon, transition_end)):
        if mode == "rtc_paper":
            c_i = float(transition_end - i) / span
            w[i, 0] = c_i * (math.exp(c_i) - 1.0) / (math.e - 1.0)
        elif mode == "exp":
            w[i, 0] = math.exp(-decay_rate * float(i - delay_d))
        else:
            progress = (i - delay_d) / float(transition_end - delay_d)
            w[i, 0] = 0.5 * (1.0 + math.cos(math.pi * progress))
    return w


def rtc_guided_euler_rollout(
    velocity_fn,
    a_prev_shifted: torch.Tensor,
    horizon: int = 50,
    action_dim: int = 7,
    delay_d: int = 8,
    exec_s: int = 16,
    steps: int = 10,
    beta_clip: float = 5.0,
    use_rtc: bool = True,
    mask_mode: str = "rtc_paper",
) -> torch.Tensor:
    """
    执行单次 Action Chunk 生成，对比 Naive 独立采样 vs RTC 软掩码伪逆引导 (arXiv:2506.07339):
    v_RTC(a^tau, tau) = v_theta(a^tau, tau) + min(beta, (1 - tau) / (tau * r_tau^2)) * (d a1_hat / d a^tau)^T [W * (a_prev - a1_hat)]
    其中 a1_hat = a^tau + (1 - tau) * v_theta(a^tau, tau), r_tau^2 = (1 - tau)^2 / (tau^2 + (1 - tau)^2)。
    """
    if steps <= 0 or beta_clip <= 0:
        raise ValueError("steps and beta_clip must be positive")
    a = torch.randn(horizon, action_dim, device=a_prev_shifted.device, dtype=a_prev_shifted.dtype)
    dt = 1.0 / steps
    w = build_rtc_soft_mask(horizon, delay_d, exec_s, mode=mask_mode, device=a.device) if use_rtc else torch.zeros(horizon, 1, device=a.device)

    for k in range(steps):
        tau = k * dt
        if use_rtc and delay_d > 0:
            a_var = a.detach().requires_grad_(True)
            v = velocity_fn(a_var, tau)
            a1_hat = a_var + (1.0 - tau) * v
            weighted_residual = (w * (a_prev_shifted - a1_hat)).detach()
            (vjp_term,) = torch.autograd.grad(
                outputs=a1_hat, inputs=a_var, grad_outputs=weighted_residual, retain_graph=False
            )
            r_tau_sq = ((1.0 - tau) ** 2) / (tau ** 2 + (1.0 - tau) ** 2)
            guidance_scale = beta_clip if tau == 0.0 else min(beta_clip, (1.0 - tau) / (tau * r_tau_sq))
            v = v.detach() + guidance_scale * vjp_term
        else:
            v = velocity_fn(a, tau)
        a = a + dt * v

    if use_rtc and delay_d > 0:
        a[:delay_d] = a_prev_shifted[:delay_d]
    return a


if __name__ == "__main__":
    torch.manual_seed(42)
    H, D = 50, 7
    t_grid = torch.linspace(0, 1, H).unsqueeze(-1)
    a_prev_shifted = torch.sin(2 * math.pi * t_grid).repeat(1, D)
    target_new = a_prev_shifted + 0.42 + 0.12 * t_grid.repeat(1, D)
    # 合成线性速度场；终点预测的 Jacobian 非零，无真实机器人或空间耦合。
    velocity_fn = lambda a_tau, tau: (target_new - a_tau) / max(1.0 - tau + 0.15, 0.20)

    for d in [4, 8, 12]:
        torch.manual_seed(42 + d)
        chunk_naive = rtc_guided_euler_rollout(velocity_fn, a_prev_shifted, H, D, delay_d=d, exec_s=16, use_rtc=False)
        # ACT 风格 Temporal Ensembling (无流引导，仅对新旧块做指数平均，在多峰分布下易发生模式平均)
        chunk_te = 0.45 * a_prev_shifted + 0.55 * chunk_naive
        chunk_te[:d] = a_prev_shifted[:d]
        torch.manual_seed(42 + d)
        chunk_rtc = rtc_guided_euler_rollout(
            velocity_fn, a_prev_shifted, H, D, delay_d=d, exec_s=16, use_rtc=True, mask_mode="rtc_paper"
        )
        # 比较第 d 步切换边界处相对于已承诺前缀末端 a_prev_shifted[d - 1] 的单步动作跳变范数 ||a_d - a_{d-1}||_2
        jump_naive = torch.norm(chunk_naive[d] - a_prev_shifted[d - 1]).item()
        jump_te = torch.norm(chunk_te[d] - a_prev_shifted[d - 1]).item()
        jump_rtc = torch.norm(chunk_rtc[d] - a_prev_shifted[d - 1]).item()
        red_pct = (1.0 - jump_rtc / jump_naive) * 100.0
        assert torch.allclose(chunk_rtc[:d], a_prev_shifted[:d]), "Committed prefix must be strictly locked!"
        assert torch.isfinite(chunk_rtc).all(), "Guided rollout must remain finite"
        print(
            f"[Lab 2 | SYNTHETIC, not robot results] Delay d={d:2d} steps | Boundary Step Jump ||a_d - a_{{d-1}}||_2 -> "
            f"Naive: {jump_naive:.2f}, Temporal-Ensemble: {jump_te:.2f}, RTC: {jump_rtc:.2f} (-{red_pct:.1f}%)"
        )
