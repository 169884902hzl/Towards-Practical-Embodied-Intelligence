# Executable teaching labs

These are **SYNTHETIC teaching examples, not real results**. No robot data, pretrained weights or published-method evaluations are loaded. Use Python 3.11 and the pinned dependency in [requirements.txt](../requirements.txt).

| Script | What it actually checks | Figure |
|---|---|---|
| [Lab 1](lab1_openpi_ki_and_latency_profiler.py) | Flow-gradient isolation while an auxiliary discrete loss still updates the backbone; local runtime timing | [Mechanism diagram](../assets/ei_tutorial/lab1_ki_and_latency_plot.svg) |
| [Lab 2](lab2_rtc_soft_masked_inpainting.py) | Paper soft mask, clipped guidance and endpoint VJP on a synthetic linear field; boundary **action** differences | [Mechanism diagram](../assets/ei_tutorial/lab2_rtc_trajectory_inpainting_plot.svg) |
| [Lab 3](lab3_cascade_tactile_flow.py) | Configurable two-stage rollout and matched-network input-dropout ablation at three training correlations; no assumed winner | [Ablation design](../assets/ei_tutorial/lab3_two_stage_modality_ablation_plot.svg) |
| [Lab 4](lab4_final_step_gaussian_ppo_and_critic.py) | Joint Gaussian chunk ratio, analytic KL divergence and Bellman TD target; identical forward dynamics with full/truncated derivatives | [Analytic synthetic example](../assets/ei_tutorial/lab4_flow_rl_convergence_plot.svg) |
| [Lab 5](lab5_rigorous_robot_eval_statistics.py) | Wilson/Wald intervals, exact McNemar, paired stratified bootstrap and interval half-width planning on arbitrary Method A/B/C/D records | [Generated synthetic statistics](../assets/ei_tutorial/lab5_statistical_eval_wilson_mcnemar_plot.svg) |

Run from the repository root:

```bash
python labs/lab1_openpi_ki_and_latency_profiler.py
python labs/lab2_rtc_soft_masked_inpainting.py
python labs/lab3_cascade_tactile_flow.py
python labs/lab4_final_step_gaussian_ppo_and_critic.py
python labs/lab5_rigorous_robot_eval_statistics.py
```

Lab 1 latency depends on the machine; Lab 2 differences and Lab 3 MSE depend on the chosen synthetic data and numerical setup. They are not fixed claims about robot performance. Lab 4's positive-slope field is a deliberately chosen unstable example, not a universal variance theorem. Lab 5's significance illustrates a calculation and says nothing about real methods.

Rebuild the teaching diagrams and derived statistics without PyTorch or plotting dependencies:

```bash
python tools/build_lab_figures.py
python tools/build_lab_figures.py --check
python tools/check_public_release.py
```

Labs 1-3 figures contain no measured curves; Lab 4 values are analytic; Lab 5 shares its data and statistics functions with the figure builder. The complete code is also embedded in [the tutorial](../docs/06_Glossary_Templates_and_Checklists.md).
