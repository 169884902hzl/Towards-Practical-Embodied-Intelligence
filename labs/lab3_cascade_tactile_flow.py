# lab3_cascade_tactile_flow.py
"""Synthetic teaching examples: a two-rate flow and a controlled input-dropout ablation.

No pretrained tactile encoder, robot experiment, or published-method reproduction.
Run: python labs/lab3_cascade_tactile_flow.py
"""
import copy
import torch
from torch import nn
from torch.nn import functional as F


class CascadeTactileFlow(nn.Module):
    """Generic two-stage flow; dimensions and integration schedule are configurable."""
    def __init__(self, horizon=12, action_dim=2, context_dim=8, tactile_dim=4):
        super().__init__()
        self.horizon = horizon
        self.action_dim = action_dim
        self.slow = nn.Sequential(nn.Linear(action_dim + context_dim + 1, 32), nn.SiLU(), nn.Linear(32, action_dim))
        self.fast = nn.Sequential(nn.Linear(action_dim + context_dim + tactile_dim + 1, 32), nn.SiLU(), nn.Linear(32, action_dim))

    def rollout(self, context, tactile, slow_steps=2, fast_steps=2):
        if slow_steps <= 0 or fast_steps <= 0:
            raise ValueError("Both stages need at least one integration step")
        batch = context.shape[0]
        a = torch.randn(batch, self.horizon, self.action_dim, device=context.device)
        total_steps = slow_steps + fast_steps
        dt = 1.0 / total_steps
        ctx = context[:, None].expand(-1, self.horizon, -1)
        tac = tactile[:, None].expand(-1, self.horizon, -1)
        for k in range(total_steps):
            tau = k * dt
            t = torch.full((batch, self.horizon, 1), tau, device=a.device)
            v = self.slow(torch.cat((a, ctx, t), -1)) if k < slow_steps else self.fast(torch.cat((a, ctx, tac, t), -1))
            a = a + dt * v
        return a


def run_synthetic_shortcut_ablation():
    """Matched networks and inputs; only training-time proprioceptive dropout differs.

    q and target have partial, adjustable correlation during training. At test time
    q is independent random noise, not a fixed zero. Results depend on this chosen
    distribution and cannot establish robot insertion success or universal ranking.
    """
    rows = []
    for rho in (0.0, 0.5, 0.9):
        torch.manual_seed(42)
        method_a = nn.Sequential(nn.Linear(2, 16), nn.SiLU(), nn.Linear(16, 1))
        method_b = copy.deepcopy(method_a)
        optimizers = [torch.optim.AdamW(model.parameters(), lr=0.01) for model in (method_a, method_b)]
        for _ in range(60):
            signal = torch.randn(64, 1)
            tactile = signal + 0.2 * torch.randn_like(signal)
            q = rho * signal + (1 - rho * rho) ** 0.5 * torch.randn_like(signal)
            inputs = torch.cat((tactile, q), -1)
            for model, optimizer, drop in zip((method_a, method_b), optimizers, (False, True)):
                model_input = inputs.clone()
                if drop:
                    model_input[:, 1:] = F.dropout(model_input[:, 1:], p=0.5, training=True)
                optimizer.zero_grad()
                F.mse_loss(model(model_input), signal).backward()
                optimizer.step()
        with torch.no_grad():
            target = torch.randn(256, 1)
            test_inputs = torch.cat((target + 0.2 * torch.randn_like(target), torch.randn_like(target)), -1)
            a = F.mse_loss(method_a(test_inputs), target).item()
            b = F.mse_loss(method_b(test_inputs), target).item()
        assert torch.isfinite(torch.tensor([a, b])).all()
        rows.append({"train_correlation": rho, "test_correlation": 0.0, "method_a_mse": a, "method_b_mse": b})
    return rows


if __name__ == "__main__":
    torch.manual_seed(42)
    model = CascadeTactileFlow(horizon=12)
    out = model.rollout(torch.randn(2, 8), torch.randn(2, 4))
    assert out.shape == (2, 12, 2) and torch.isfinite(out).all()
    print("SYNTHETIC — not real results; no published methods or robot success rates.")
    print("Two-rate rollout shape:", tuple(out.shape))
    for row in run_synthetic_shortcut_ablation():
        print(row)
