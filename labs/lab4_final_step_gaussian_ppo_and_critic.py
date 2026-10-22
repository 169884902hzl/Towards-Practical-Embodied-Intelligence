# lab4_final_step_gaussian_ppo_and_critic.py
# 运行方式: python labs/lab4_final_step_gaussian_ppo_and_critic.py
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def gaussian_chunk_log_prob(a_sampled: torch.Tensor, mu: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    """
    计算高斯化去噪/流匹配步在动作块 a[:, :, :] 上的闭式对角高斯联合对数似然:
    对动作块的全部时间步和动作维求和；PPO 的重要性采样比率使用联合密度，不能对维度取平均。
    """
    diff = (a_sampled - mu) / (std + 1e-8)
    log_p_per_dim = -0.5 * (diff.pow(2) + 2.0 * torch.log(std + 1e-8) + math.log(2.0 * math.pi))
    return log_p_per_dim.sum(dim=(1, 2))


def analytic_gaussian_kl(
    mu_rl: torch.Tensor,
    std_rl: torch.Tensor,
    mu_ref: torch.Tensor,
    std_ref: torch.Tensor | None = None,
) -> torch.Tensor:
    """
    计算当前策略分布 N(mu_rl, std_rl^2) 与参考分布 N(mu_ref, std_ref^2) 的闭式高斯 KL 散度:
    在动作块全部维度求和，再对 batch 求平均。std_ref=None 表示共享协方差。
    """
    s_rl = std_rl + 1e-8
    s_ref = (std_ref + 1e-8) if std_ref is not None else s_rl.detach()
    kl_per_dim = torch.log(s_ref / s_rl) + (s_rl.pow(2) + (mu_rl - mu_ref).pow(2)) / (2.0 * s_ref.pow(2)) - 0.5
    return kl_per_dim.sum(dim=(1, 2)).mean()


def compute_bellman_td_target(
    rewards: torch.Tensor,
    next_values: torch.Tensor,
    dones: torch.Tensor,
    gamma: float = 0.99,
) -> torch.Tensor:
    """
    标准单步 Bellman 时序差分 (TD) 目标:
    当回合终止 (dones == 1) 时截断对下一状态的 Value 自举。
    """
    bootstrap_mask = 1.0 - dones
    return rewards + gamma * bootstrap_mask * next_values


def gaussian_ppo_update_step(
    mu_new, std_new, mu_ref_frozen, a_actions, old_log_probs, advantages,
    v_pred, td_targets, std_ref_frozen=None, clip_eps: float = 0.2, kl_beta: float = 0.05
) -> dict:
    new_log_probs = gaussian_chunk_log_prob(a_actions, mu_new, std_new)
    ratio = torch.exp(new_log_probs - old_log_probs)
    surr1 = ratio * advantages
    surr2 = torch.clamp(ratio, 1.0 - clip_eps, 1.0 + clip_eps) * advantages
    loss_policy = -torch.min(surr1, surr2).mean()
    loss_kl = analytic_gaussian_kl(mu_new, std_new, mu_ref_frozen.detach(), std_ref=std_ref_frozen)
    loss_critic = F.smooth_l1_loss(v_pred, td_targets.detach())
    total_loss = loss_policy + kl_beta * loss_kl + 0.5 * loss_critic
    return {
        "total_loss": total_loss,
        "policy_loss": round(loss_policy.item(), 4),
        "kl_div": round(loss_kl.item(), 4),
        "critic_loss": round(loss_critic.item(), 4),
        "mean_ratio": round(ratio.mean().item(), 4),
    }


def compare_bptt_vs_truncated_grad_norm(steps_k: int = 10, stiff_lip: float = 8.0) -> tuple[float, float]:
    """
    SYNTHETIC：在线性不稳定速度场 v_theta(a) = L_v * a + theta 下，
    对比朴素 K 步欧拉 ODE 反向传播 (BPTT) 与单步截断求导的参数梯度范数:
    - Naive BPTT: 反向传播连乘 K 步雅可比 (1 + L_v * dt)^K，逼近 Grönwall 最坏界 exp(L_v)；
    - Single-Step Detach: 相同前向轨迹，只保留最后一步参数梯度；其尺度为 dt，而非普遍常数。
    这是一个选定的正斜率反例，不代表机器人接触动力学或所有流策略都不稳定。
    """
    torch.manual_seed(0)
    theta_bptt = nn.Parameter(torch.full((7,), 0.01))
    theta_trunc = nn.Parameter(torch.full((7,), 0.01))
    dt = 1.0 / steps_k

    # 1. Naive K-step ODE BPTT: 真实前向积分 a_{k+1} = a_k + dt * (L_v * a_k + theta)
    a = torch.zeros(4, 7)
    for _ in range(steps_k):
        v = stiff_lip * a + theta_bptt
        a = a + dt * v
    a.sum().backward()

    # 2. Same forward dynamics; only the backward path is truncated.
    a2 = torch.zeros(4, 7)
    for k in range(steps_k):
        if k == steps_k - 1:
            a2 = a2.detach()
        v2 = stiff_lip * a2 + theta_trunc
        a2 = a2 + dt * v2
    a2.sum().backward()
    assert torch.allclose(a, a2), "Detaching must not change the forward trajectory"
    return theta_bptt.grad.norm().item(), theta_trunc.grad.norm().item()


if __name__ == "__main__":
    torch.manual_seed(0)
    B, H, D = 8, 50, 7
    mu_ref = torch.zeros(B, H, D)
    std_ref = torch.full((B, H, D), 0.08)
    mu_rl = (torch.randn(B, H, D) * 0.01).requires_grad_(True)
    std_rl = torch.full((B, H, D), 0.08)
    a_act = (mu_ref + std_ref * torch.randn(B, H, D)).detach()
    old_lp = gaussian_chunk_log_prob(a_act, mu_ref, std_rl).detach()
    adv = torch.tensor([1.2, -0.8, 0.9, 1.5, -1.1, 0.4, 0.7, -0.5])
    rewards = torch.tensor([1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0])
    next_v = torch.full((B,), 0.6)
    dones = torch.tensor([0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])

    td_tgt = compute_bellman_td_target(rewards, next_v, dones)
    v_pred = torch.full((B,), 0.5, requires_grad=True)
    stats = gaussian_ppo_update_step(
        mu_rl, std_rl, mu_ref, a_act, old_lp, adv, v_pred, td_tgt, std_ref_frozen=std_ref
    )
    stats["total_loss"].backward()

    expected_lp = torch.distributions.Normal(mu_rl, std_rl).log_prob(a_act).sum((1, 2))
    assert torch.allclose(gaussian_chunk_log_prob(a_act, mu_rl, std_rl), expected_lp, atol=1e-4)
    expected_kl = torch.distributions.kl_divergence(
        torch.distributions.Normal(mu_rl, std_rl), torch.distributions.Normal(mu_ref, std_ref)
    ).sum((1, 2)).mean()
    assert torch.allclose(analytic_gaussian_kl(mu_rl, std_rl, mu_ref, std_ref), expected_kl, atol=1e-4)

    grad_bptt, grad_trunc = compare_bptt_vs_truncated_grad_norm(steps_k=10, stiff_lip=8.0)
    assert math.isfinite(mu_rl.grad.norm().item()), "Gradient on mu_rl must be finite!"
    assert td_tgt[1].item() == 0.0, "Terminal episode flag must mask out next_value bootstrap!"
    assert grad_bptt > grad_trunc * 50.0, "Expected multi-step BPTT gradient amplification under stiff field"

    print(
        f"[Lab 4 | SYNTHETIC; no robot success rates] PPO Step Stats: { {k: v for k, v in stats.items() if k != 'total_loss'} } | "
        f"Grad norm on mu_rl: {mu_rl.grad.norm().item():.4f} | "
        f"Stiff K=10 Grad Norm (Naive BPTT: {grad_bptt:.1f} vs Single-Step Truncated: {grad_trunc:.2f})"
    )
