# lab1_openpi_ki_and_latency_profiler.py
# 运行方式: python labs/lab1_openpi_ki_and_latency_profiler.py
import time
import torch
import torch.nn as nn
import torch.nn.functional as F


class KnowledgeInsulatedFlowVLA(nn.Module):
    """
    演示 pi0.5 + Knowledge Insulation (Driess et al., arXiv:2505.23705):
    1. VLM 主干提取多模态 KV 特征，并受离散 FAST 动作 token 交叉熵损失监督；
    2. 连续 Flow Matching 动作专家通过 .detach() (stop_gradient) 读取 VLM 特征，
       验证连续流损失的梯度隔离；本例随机初始化，不测量预训练语义保留。
    """
    def __init__(self, d_vlm: int = 256, d_expert: int = 128, chunk_size: int = 50, action_dim: int = 14, fast_vocab: int = 512):
        super().__init__()
        self.chunk_size = chunk_size
        self.action_dim = action_dim
        self.vlm_backbone = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_vlm, nhead=8, dim_feedforward=512, dropout=0.0, batch_first=True),
            num_layers=2,
        )
        self.fast_token_head = nn.Linear(d_vlm, fast_vocab)
        self.kv_proj = nn.Linear(d_vlm, d_expert)
        self.action_in_proj = nn.Linear(action_dim + 1, d_expert)
        self.expert_decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=d_expert, nhead=4, dim_feedforward=256, dropout=0.0, batch_first=True),
            num_layers=2,
        )
        self.velocity_out = nn.Linear(d_expert, action_dim)

    def encode_vlm_kv(self, obs_tokens: torch.Tensor) -> torch.Tensor:
        return self.vlm_backbone(obs_tokens)

    def predict_velocity(self, a_tau: torch.Tensor, tau: torch.Tensor, vlm_hidden: torch.Tensor, insulate_grad: bool = True) -> torch.Tensor:
        kv_source = vlm_hidden.detach() if insulate_grad else vlm_hidden
        memory = self.kv_proj(kv_source)
        tau_expand = tau.view(-1, 1, 1).expand(-1, a_tau.size(1), 1)
        x = self.action_in_proj(torch.cat([a_tau, tau_expand], dim=-1))
        h = self.expert_decoder(tgt=x, memory=memory)
        return self.velocity_out(h)

    def compute_joint_loss(
        self, obs_tokens: torch.Tensor, a_gt: torch.Tensor, fast_targets: torch.Tensor,
        insulate_grad: bool = True, fast_weight: float = 1.0,
    ) -> dict:
        B, H, D = a_gt.shape
        vlm_hidden = self.encode_vlm_kv(obs_tokens)
        fast_logits = self.fast_token_head(vlm_hidden[:, :fast_targets.size(1), :])
        loss_fast = F.cross_entropy(fast_logits.reshape(-1, fast_logits.size(-1)), fast_targets.reshape(-1))
        a0 = torch.randn_like(a_gt)
        tau = torch.rand(B, device=a_gt.device)
        tau_view = tau.view(B, 1, 1)
        a_tau = (1.0 - tau_view) * a0 + tau_view * a_gt
        u_target = a_gt - a0
        v_pred = self.predict_velocity(a_tau, tau, vlm_hidden, insulate_grad=insulate_grad)
        loss_flow = F.mse_loss(v_pred, u_target)
        return {"total_loss": fast_weight * loss_fast + loss_flow, "loss_fast": loss_fast.item(), "loss_flow": loss_flow.item()}

    @torch.no_grad()
    def sample_action_chunk(self, obs_tokens: torch.Tensor, steps: int = 10) -> tuple[torch.Tensor, dict]:
        self.eval()
        B = obs_tokens.size(0)
        if obs_tokens.is_cuda:
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        vlm_hidden = self.encode_vlm_kv(obs_tokens)
        if obs_tokens.is_cuda:
            torch.cuda.synchronize()
        t_vlm = (time.perf_counter() - t0) * 1000.0

        t1 = time.perf_counter()
        a = torch.randn(B, self.chunk_size, self.action_dim, device=obs_tokens.device)
        dt = 1.0 / steps
        for k in range(steps):
            tau = torch.full((B,), k * dt, device=obs_tokens.device)
            a = a + dt * self.predict_velocity(a, tau, vlm_hidden, insulate_grad=True)
        if obs_tokens.is_cuda:
            torch.cuda.synchronize()
        t_flow = (time.perf_counter() - t1) * 1000.0
        return a, {"vlm_prefill_ms": round(t_vlm, 2), "flow_euler_ms": round(t_flow, 2), "total_ms": round(t_vlm + t_flow, 2)}


def verify_knowledge_insulation_gradients(device: str = "cpu") -> dict:
    """SYNTHETIC gradient routing check, not a pretrained VLM retention benchmark.

    Random labels stand in for a discrete auxiliary objective; no FAST tokenizer,
    pretrained language model, semantic benchmark, or robot data is loaded.
    """
    torch.manual_seed(42)
    model = KnowledgeInsulatedFlowVLA().to(device)
    obs = torch.randn(2, 16, 256, device=device)
    actions = torch.randn(2, 50, 14, device=device)
    targets = torch.randint(0, 512, (2, 8), device=device)
    parameters = tuple(model.vlm_backbone.parameters())

    def norm(grads):
        return sum(g.square().sum().item() for g in grads if g is not None) ** 0.5

    hidden = model.encode_vlm_kv(obs)
    discrete_loss = F.cross_entropy(model.fast_token_head(hidden[:, :8]).reshape(-1, 512), targets.reshape(-1))
    discrete_grads = torch.autograd.grad(discrete_loss, parameters)
    joint = model.compute_joint_loss(obs, actions, targets, insulate_grad=True, fast_weight=1.0)
    joint_grads = torch.autograd.grad(joint["total_loss"], parameters)
    assert all(torch.allclose(a, b, atol=1e-6) for a, b in zip(discrete_grads, joint_grads))

    norms = {}
    for insulated in (True, False):
        loss = model.compute_joint_loss(obs, actions, targets, insulate_grad=insulated, fast_weight=0.0)
        grads = torch.autograd.grad(loss["total_loss"], parameters, allow_unused=True)
        norms[insulated] = norm(grads)
    assert norms[True] == 0.0 and norms[False] > 0.0
    assert norm(discrete_grads) > 0.0, "The auxiliary objective must still train the backbone"
    return {"flow_to_backbone_KI": norms[True], "flow_to_backbone_no_KI": norms[False],
            "auxiliary_to_backbone": norm(discrete_grads), "joint_matches_auxiliary": True}


if __name__ == "__main__":
    torch.manual_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = KnowledgeInsulatedFlowVLA().to(device)
    obs = torch.randn(1, 16, 256, device=device)
    model.sample_action_chunk(obs, steps=2)  # warm-up
    chunk, timing = model.sample_action_chunk(obs, steps=10)
    assert chunk.shape == (1, 50, 14)
    print(f"[Lab 1 | SYNTHETIC, not semantic retention] {verify_knowledge_insulation_gradients(device)}")
    print(f"Local runtime only ({device}, torch {torch.__version__}): {timing}; not comparable to pretrained VLA latency")
