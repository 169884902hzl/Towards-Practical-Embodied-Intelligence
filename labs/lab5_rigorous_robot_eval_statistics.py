# lab5_rigorous_robot_eval_statistics.py
# 运行方式: python labs/lab5_rigorous_robot_eval_statistics.py
import math
import random


def _validate_paired_binary(paired_a: list[int], paired_b: list[int]) -> None:
    if len(paired_a) == 0 or len(paired_a) != len(paired_b):
        raise ValueError(f"Paired trial lists must be non-empty and of equal length (got {len(paired_a)} vs {len(paired_b)}).")
    if any(x not in (0, 1) for x in paired_a) or any(y not in (0, 1) for y in paired_b):
        raise ValueError("Trial outcomes must be binary integers in {0, 1}.")


def wald_ci(successes: int, total: int, z: float = 1.95996) -> tuple[float, float, float]:
    """计算传统正态近似 Wald 95% 区间（展示其在小样本或极端成功率 p_hat -> 0/1 下越界或坍缩为零宽度的缺陷）"""
    if total <= 0 or successes < 0 or successes > total:
        raise ValueError(f"Invalid counts: successes={successes}, total={total}")
    p_hat = successes / total
    half_width = z * math.sqrt(p_hat * (1.0 - p_hat) / total)
    return p_hat * 100.0, (p_hat - half_width) * 100.0, (p_hat + half_width) * 100.0


def wilson_score_ci(successes: int, total: int, z: float = 1.95996) -> tuple[float, float, float]:
    """计算二项分布成功率的 Wilson Score 95% 渐近置信区间（二次方程反演，永不越界，小样本覆盖率显著优于 Wald）"""
    if total <= 0 or successes < 0 or successes > total:
        raise ValueError(f"Invalid counts: successes={successes}, total={total}")
    p_hat = successes / total
    z2 = z * z
    denom = 1.0 + z2 / total
    center = (p_hat + z2 / (2.0 * total)) / denom
    half_width = (z * math.sqrt((p_hat * (1.0 - p_hat) + z2 / (4.0 * total)) / total)) / denom
    return p_hat * 100.0, max(0.0, (center - half_width) * 100.0), min(100.0, (center + half_width) * 100.0)


def minimum_sample_size_wilson_halfwidth(p_est: float = 0.80, target_half_width: float = 0.10, z: float = 1.95996) -> int:
    """给定预期成功率 p_est 与目标 Wilson 置信区间半宽 target_half_width，规划最小独立评测次数 N_min"""
    if not (0.0 < p_est < 1.0) or target_half_width <= 0.0:
        raise ValueError("p_est must be in (0, 1) and target_half_width > 0.")
    z2 = z * z
    for n in range(1, 100000):
        denom = 1.0 + z2 / n
        half_width = (z * math.sqrt((p_est * (1.0 - p_est) + z2 / (4.0 * n)) / n)) / denom
        if half_width <= target_half_width:
            return n
    return 100000


def mcnemar_exact_binomial_p(paired_a: list[int], paired_b: list[int]) -> tuple[int, int, float]:
    """
    计算配对初始位姿下策略 A 与策略 B 的双侧精确 McNemar 二项检验 p 值:
    n10: A 成功且 B 失败的配对数; n01: A 失败且 B 成功的配对数
    """
    _validate_paired_binary(paired_a, paired_b)
    n10 = sum(1 for a, b in zip(paired_a, paired_b) if a == 1 and b == 0)
    n01 = sum(1 for a, b in zip(paired_a, paired_b) if a == 0 and b == 1)
    n_discordant = n10 + n01
    if n_discordant == 0:
        return 0, 0, 1.0
    k = min(n10, n01)
    tail_prob = sum(math.comb(n_discordant, i) * (0.5 ** n_discordant) for i in range(k + 1))
    return n10, n01, min(1.0, 2.0 * tail_prob)


def bootstrap_paired_diff_ci(
    paired_a: list[int],
    paired_b: list[int],
    n_boot: int = 10000,
    seed: int = 42,
    strata_sizes: list[int] | None = None,
) -> tuple[float, float, float]:
    """支持分层 (Stratified) 或全局的 10,000 次配对 Bootstrap 重采样，计算差值 (A - B) 的 95% 置信区间"""
    _validate_paired_binary(paired_a, paired_b)
    rng = random.Random(seed)
    n = len(paired_a)
    diffs = [(a - b) * 100.0 for a, b in zip(paired_a, paired_b)]
    if strata_sizes is None:
        strata_sizes = [n]
    if n_boot < 40 or any(not isinstance(x, int) or x <= 0 for x in strata_sizes) or sum(strata_sizes) != n:
        raise ValueError("Use n_boot >= 40 and positive strata sizes summing to the number of trials.")

    boot_means = []
    for _ in range(n_boot):
        total_val = 0.0
        offset = 0
        for s_len in strata_sizes:
            stratum = diffs[offset:offset + s_len]
            for _ in range(s_len):
                total_val += stratum[rng.randrange(s_len)]
            offset += s_len
        boot_means.append(total_val / n)
    boot_means.sort()
    mean_diff = sum(diffs) / n
    return mean_diff, boot_means[int(0.025 * n_boot)], boot_means[int(0.975 * n_boot)]


def synthetic_trial_data() -> dict[str, list[int]]:
    """Arbitrary paired binary outcomes; not measurements of any robot or policy."""
    return {
        "Method A": [1]*22 + [0]*28,
        "Method B": [1]*29 + [0]*21,
        "Method C": [1]*34 + [0]*16,
        "Method D": [1]*32 + [0]*2 + [1]*12 + [0]*4,
    }


if __name__ == "__main__":
    # [Synthetic Evaluation Example] N = 50 组配对初始位姿（5 个子条件分层，每层 10 次）下的合成教学评测数据
    print("SYNTHETIC — not real results; A/B/C/D are arbitrary teaching labels, not published methods.")
    n_trials = 50
    strata = [10, 10, 10, 10, 10]
    trials = synthetic_trial_data()
    method_a, method_b, method_c, method_d = trials.values()

    _, wald_lo_10, wald_hi_10 = wald_ci(10, 10)
    _, wilson_lo_10, wilson_hi_10 = wilson_score_ci(10, 10)
    n_min_10pp = minimum_sample_size_wilson_halfwidth(p_est=0.80, target_half_width=0.10)
    n10_check, n01_check, p_check = mcnemar_exact_binomial_p(method_d, method_c)
    assert (n10_check, n01_check) == (12, 2) and abs(p_check - 0.012939) < 1e-4

    print(
        f"[Small-Sample Boundary Check (10/10 = 100%)] Wald 95% CI: [{wald_lo_10:.1f}%, {wald_hi_10:.1f}%] (Degenerate!) "
        f"vs Wilson 95% CI: [{wilson_lo_10:.1f}%, {wilson_hi_10:.1f}%]"
    )
    print(f"[Sample Size Planning] Minimum trials for p_est=80% with Wilson half-width <= ±10%: N_min = {n_min_10pp}")
    print("| 合成对比策略 (Synthetic Paired Protocol, N=50) | 成功率 (%) | Wilson 95% CI | vs Method D Δ (95% Stratified Boot CI) | McNemar (n10/n01, p-value) |")
    print("|---|---|---|---|---|")
    for name, arr, is_ref in [
        ("Method A (Synthetic)", method_a, False),
        ("Method B (Synthetic)", method_b, False),
        ("Method C (Synthetic)", method_c, False),
        ("**Method D (Synthetic)**", method_d, True),
    ]:
        sr, lo, hi = wilson_score_ci(sum(arr), len(arr))
        if is_ref:
            print(f"| {name} | **{sr:.1f}%** ({sum(arr)}/{len(arr)}) | `[{lo:.1f}%, {hi:.1f}%]` | Reference | — |")
        else:
            diff, d_lo, d_hi = bootstrap_paired_diff_ci(method_d, arr, strata_sizes=strata)
            n10, n01, p_val = mcnemar_exact_binomial_p(method_d, arr)
            print(f"| {name} | {sr:.1f}% ({sum(arr)}/{len(arr)}) | `[{lo:.1f}%, {hi:.1f}%]` | **+{diff:.1f} pp** (`[+{d_lo:.1f}, +{d_hi:.1f}]`) | {n10}/{n01}, **p = {p_val:.4g}** |")
