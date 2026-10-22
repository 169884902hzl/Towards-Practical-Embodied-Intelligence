# Contributing to Towards Practical Embodied Intelligence

Thank you for your interest in contributing to **Towards Practical Embodied Intelligence**! Whether you are adding a newly released Embodied AI paper, fixing a mathematical derivation, contributing a benchmark evaluation protocol, or extending our executable PyTorch labs, please follow the engineering and academic rigor guidelines below.

---

## 1. Academic Evidence & Citation Audit Rules (Mandatory)

1. **Exact arXiv ID & Title Verification**:
   - Before adding or updating any paper link, verify that the `arXiv:YYMM.NNNNN` identifier resolves to the exact paper title and author list via the official arXiv page or API (`http://export.arxiv.org/api/query?id_list=YYMM.NNNNN`).
   - Never guess or extrapolate an arXiv ID from a release date or preprint title. If a paper is published only on a project website or OpenReview without an arXiv preprint, link directly to its official project/OpenReview URL.
2. **Five-Tier Evidence Tagging**:
   - **`[Verified Fact]` / `[已验证事实]`**: Directly verifiable open-source code, checkpoints, dataset schemas, licenses, or mathematical identities.
   - **`[Paper-Reported]` / `[论文报告]`**: Quantitative metrics reported within the original paper's evaluation protocol (must specify benchmark, split, and baseline context; do not compare numbers across incompatible protocols without an explicit disclaimer).
   - **`[Official Claim]` / `[官方宣称]`**: Capabilities demonstrated in official technical blogs or videos without third-party reproducible weights/code.
   - **`[Principled Inference]` / `[合理推论]`**: Mechanistic analysis or architectural synthesis derived from multiple verified papers.
   - **`[Open Question]` / `[尚不确定]`**: Unresolved empirical boundaries requiring further real-robot experiments.
3. **Statistical Rigor for Benchmark Claims**:
   - When contributing real-robot or simulation evaluation tables, report trial counts $N$, **95% Wilson score confidence intervals**, and (for paired initial states) **exact two-sided McNemar $p$-values** or stratified bootstrap confidence intervals (see [`labs/lab5_rigorous_robot_eval_statistics.py`](./labs/lab5_rigorous_robot_eval_statistics.py)).

---

## 2. Bilingual & Multi-Entry Synchronization

This repository maintains synchronized English and Chinese entry points alongside a modular textbook and interactive HTML workbench:
- **Survey Portals**: [`README.md`](./README.md) (English) and [`README_zh.md`](./README_zh.md) (Chinese)
- **Modular Tutorial Volumes**: [`docs/00_Must_Read_60_Leaderboard.md`](./docs/00_Must_Read_60_Leaderboard.md) through [`docs/06_Glossary_Templates_and_Checklists.md`](./docs/06_Glossary_Templates_and_Checklists.md)
- **Single-File Complete Edition**: [`docs/Full_Tutorial_CN.md`](./docs/Full_Tutorial_CN.md)
- **Interactive HTML Workbench**: [`index.html`](./index.html) (rendered with local KaTeX in [`assets/katex/`](./assets/katex/))

Synthetic examples must use neutral labels, never published-method names or real-robot performance claims.

When updating a core paper citation, mathematical formula, or code lab in [`labs/`](./labs/), please keep the corresponding section in `docs/` and `index.html` synchronized.

---

## 3. Pre-Submission Verification Checklist

Before opening a Pull Request, run the verification suite locally:

```bash
# 1. Install minimal dependencies
python -m pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu

# 2. Run all 5 executable PyTorch code labs (includes built-in assertions)
python labs/lab1_openpi_ki_and_latency_profiler.py
python labs/lab2_rtc_soft_masked_inpainting.py
python labs/lab3_cascade_tactile_flow.py
python labs/lab4_final_step_gaussian_ppo_and_critic.py
python labs/lab5_rigorous_robot_eval_statistics.py

# Offline documentation and figure checks
python tools/check_public_release.py
python tools/build_references.py --check
python tools/build_lab_figures.py --check
```

Ensure that:
- All markdown code fences (` ``` `) are properly closed across `README*.md` and `docs/*.md`.
- All SVG diagrams under `assets/ei_tutorial/` use a pure white background (`#FFFFFF`), parse as valid XML, and contain no text clipping or internal codenames.
- No local machine paths (e.g., drive-qualified or home-directory paths) or credentials are committed.
