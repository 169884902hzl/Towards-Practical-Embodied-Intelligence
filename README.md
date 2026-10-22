# **Towards Practical Embodied Intelligence** [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<p align="center">
  <a href="https://169884902hzl.github.io/Towards-Practical-Embodied-Intelligence/"><img src="https://img.shields.io/badge/Live_Workbench-GitHub_Pages-2563eb?style=flat-square&logo=github" alt="Live Interactive Workbench"/></a>
  <a href="https://github.com/169884902hzl/Towards-Practical-Embodied-Intelligence/actions/workflows/ci.yml"><img src="https://github.com/169884902hzl/Towards-Practical-Embodied-Intelligence/actions/workflows/ci.yml/badge.svg" alt="Labs & Docs CI"/></a>
  <a href="https://github.com/169884902hzl/local-domain-expert-vault"><img src="https://img.shields.io/badge/Companion_Vault-local--domain--expert--vault-059669?style=flat-square&logo=obsidian" alt="Companion Research Vault"/></a>
  <a href="./labs/"><img src="https://img.shields.io/badge/PyTorch_Labs-5_Executable_Scripts-ee4c2c?style=flat-square&logo=pytorch" alt="5 PyTorch Labs"/></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License"/></a>
</p>

<p align="center">
  <b>English</b> | <a href="./README_zh.md"><b>简体中文 (Chinese Portal & Deep-Dive Tutorial)</b></a> | <a href="https://169884902hzl.github.io/Towards-Practical-Embodied-Intelligence/"><b>🌐 Launch Online Interactive Workbench</b></a>
</p>

As **Embodied Intelligence (EI)** rapidly evolves from single-task visuomotor imitation to generalist **Vision-Language-Action (VLA)** models, **World Action Models (WAM)**, **Online Reinforcement Learning for Flow/Diffusion Policies**, **Visuotactile & Contact-Rich Manipulation**, **Whole-Body Humanoid Control**, and **Real-Time Asynchronous Execution**, this repository provides a **dual-layer open-source resource**:
1. **A Structured Survey & Literature Index (`README.md` / `README_zh.md`)**: Curating 60+ milestone papers, 17 dataset, simulator and benchmark entries, and categorized 2023–2026 frontier research across RSS, CoRL, ICRA, IROS, ICLR, NeurIPS, CVPR, and IJRR.
2. **A Comprehensive Textbook-Grade Tutorial & Executable Code Labs ([`docs/`](./docs/) & [`labs/`](./labs/))**: Over 6,900 lines of mathematical explanations and bounded derivations, 44 teaching figures (25 SVG + 19 JPG), 35 self-test exercises with full solutions, and 5 self-contained PyTorch code labs.

This repository is continuously maintained and updated. Contributions via Pull Requests or Issues are warmly welcome.

<p align="center">
  <img src="assets/ei_tutorial/hero_closed_loop.svg" width="96%" alt="Embodied Intelligence Closed-Loop System Overview"/>
</p>

---

## 🔗 Quick Navigation

- [📚 Deep-Dive Tutorial & PyTorch Code Labs](#-deep-dive-tutorial--pytorch-code-labs)
- [🏅 Our Recent Publications & Research Infrastructure](#-our-recent-publications--research-infrastructure)
- [📖 Survey & Review Papers](#-survey--review-papers)
- [📊 Datasets, Simulators & Benchmarks](#-datasets-simulators--benchmarks)
- [🏆 Top-60 Must-Read Embodied AI Canon](#-top-60-must-read-embodied-ai-canon)
- [🗂️ Categorized Frontier Papers (2023–2026)](#️-categorized-frontier-papers-20232026)
  - [1. Vision-Language-Action (VLA) Foundation Models](#1-vision-language-action-vla-foundation-models)
  - [2. World Action Models (WAM) & Video-Action Pretraining](#2-world-action-models-wam--video-action-pretraining)
  - [3. Reinforcement Learning for Flow Matching & Diffusion VLAs](#3-reinforcement-learning-for-flow-matching--diffusion-vlas)
  - [4. Visuotactile Sensing, Compliant Control & Contact-Rich Manipulation](#4-visuotactile-sensing-compliant-control--contact-rich-manipulation)
  - [5. Real-Time Action Chunking (RTC), Latency & Edge Acceleration](#5-real-time-action-chunking-rtc-latency--edge-acceleration)
  - [6. Online Verification, Failure Detection & Closed-Loop Recovery](#6-online-verification-failure-detection--closed-loop-recovery)
  - [7. 3D Spatial Grounding, Dexterous Hands, Whole-Body Control & Deformable Objects](#7-3d-spatial-grounding-dexterous-hands-whole-body-control--deformable-objects)

---

## 📚 Deep-Dive Tutorial & PyTorch Code Labs

Unlike traditional paper lists that only provide links, this repository includes a full textbook-grade tutorial series ([`docs/`](./docs/)) and executable PyTorch implementations ([`labs/`](./labs/)):

| Module | Document / Code Path | Core Topics Covered | Figures / Labs |
|:---:|:---|:---|:---:|
| **Part 0** | [**Must-Read 60 Paper Leaderboard**](./docs/00_Must_Read_60_Leaderboard.md) | 4-week 30-day reading roadmap; 60 annotated foundational & 2026 frontier papers across 6 tracks | 6 Curated Tables |
| **Stage 1** | [**Foundations, Compliant Control & RL**](./docs/01_Foundations_Compliant_Control_and_RL.md) | Observation/State/Action contracts, $SE(3)$ kinematics, Cartesian impedance/admittance/hybrid force-position control, BC, ACT, Diffusion Policy, Flow Matching, PPO/GRPO/SAC/`HIL-SERL`/IQL/Cal-QL, 25 Q&A solutions | 6 referenced figures |
| **Stage 2A** | [**VLA, WAM & Flow/Diffusion RL**](./docs/02_VLA_WAM_and_Flow_RL.md) | RT-1 $\rightarrow$ OpenVLA $\rightarrow$ $\pi_0 \rightarrow \pi_{0.7}$ (6 generations), VLM backbones and memory (`Qwen-RobotManip` / `REKI`), WAM (`DreamZero`, `Fast-WAM`, `OpenWAM`, `V-JEPA 2`), 7 RL paradigms for Flow/Diffusion VLAs (`DPPO`, `ReinFlow`, $\pi_{\texttt{RL}}$, `RLinf`, `DSRL`, `ResFiT`, `RECAP`, `RL-100`) | 20 referenced figures |
| **Stage 2B** | [**Tactile VLA, RTC & Verification-Recovery**](./docs/03_Tactile_RTC_and_Verification_Recovery.md) | Optical/magnetic tactile hardware (`GelSight`, `ViTai`, `AnySkin`), pretrained tactile encoders (`T3`, `Sparsh`, `UniTouch`), contact-rich VLAs (`T-Rex`, `SimpleTouch`, `PACE`, `FACT`), `Real-Time Chunking (RTC)`, `Knowledge Insulation`, online verification & recovery (`FAVOR`, `DiVeR`, `SAFE`, `E-TTS`) | 1 referenced figures |
| **Stage 3** | [**Datasets, Scaling Laws & Statistical Rigor**](./docs/04_Datasets_Scaling_Laws_and_Statistical_Eval.md) | Open X, DROID, LIBERO, ManiSkill3, LeRobot v3, AgiBot World (1M+ trajectories), *The Curse of Precision* ($\log N \propto \frac{1}{P-c}$), Wilson 95% CI, sample size planning, paired McNemar's test & blind A/B evaluation (`RoboArena`, `TRI LBM`) | 5 referenced figures |
| **Stage 4A** | [**Contact-Rich, Bimanual DLO & Generalist EI**](./docs/05_Contact_Rich_Manipulation_and_Generalist_EI.md) | Contact-rich taxonomy, bimanual deformable linear object (DLO) state representations, 6 failure modes & recovery loops, tri-frequency Generalist EI architecture & 90:9:1 data pyramid | 5 referenced figures |
| **Stage 4B** | [**Glossary, Checklists & 5 Executable Labs**](./docs/06_Glossary_Templates_and_Checklists.md) | Unified terminology dictionary, paper audit templates, 10 advanced Q&A solutions, edge quantization/pruning (`BitVLA`, `TurboVLA`), 2027–2030 forecast, and 5 runnable PyTorch scripts | 8 referenced figures |
| **Full Edition** | [**Single-File Complete Tutorial (CN)**](./docs/Full_Tutorial_CN.md) \| [**🌐 Live Interactive Workbench**](https://169884902hzl.github.io/Towards-Practical-Embodied-Intelligence/) ([Source](./index.html)) | Complete 6,900-line master document & interactive browser workbench with 44 white-bg diagrams/plots and 1,186 local paper summaries | All 44 Figures |

---

## 🏅 Our Recent Publications & Research Infrastructure

<details open>
<summary>📚 Show/Hide Our Open-Source Research Infrastructure & Publications</summary>

- **[2026 · IEEE CASE (Accepted, Paper ThCT6.3)]** [**Active Observation for Robust Visual Servoing in Robotic Manipulation**](https://hzl666.xyz/projects/active-observation/) (**Zhilun Hu**, Yuqi Cheng, Yuxiang Tan, Wen-pan Li, and Weiming Shen, *2026 IEEE International Conference on Automation Science and Engineering (CASE)*): Uses an active camera arm and target–gripper relative visual servoing with a two-stage viewpoint strategy and occlusion-triggered exploration to preserve or recover shared visual feedback during grasping under severe occlusion. [[Official Program (ThCT6.3)](https://ras.papercept.net/conferences/scripts/rtf/CASE26_ContentListWeb_4.html)] [[Project Page](https://hzl666.xyz/projects/active-observation/)] [[Publications](https://hzl666.xyz/publications/)]
- **[2026 · Open-Source Infrastructure]** [**Local Domain Expert Vault (`local-domain-expert-vault`, v1.0)**](https://github.com/169884902hzl/local-domain-expert-vault): A local-first Obsidian + Zotero + Multi-Agent (`Claudian` / `Gemini` / `DeepSeek` / `Codex`) **Research Governance Workbench** that maintains our 1,186-entry public paper index (`wiki/topics/`, `wiki/concepts/`, `wiki/entities/`), anchored claim graphs (`paper_primitives.v1`), arXiv OAI-PMH mirror-first scouting, and fail-closed adversarial review gates powering this survey and tutorial. [[GitHub Repository](https://github.com/169884902hzl/local-domain-expert-vault)] [[Academic Homepage](https://hzl666.xyz/)]

</details>

---

## 📖 Survey & Review Papers

<details open>
<summary>📚 Show/Hide Embodied AI & Robot Learning Survey Papers</summary>

- **A Survey on Vision-Language-Action Models for Embodied AI** [[arXiv:2405.14093](https://arxiv.org/abs/2405.14093)]
- **What Matters in Building Vision-Language-Action Models for Generalist Robots** [[arXiv:2412.14058](https://arxiv.org/abs/2412.14058)]
- **Towards a Unified Understanding of Robot Manipulation: A Comprehensive Survey** [[arXiv:2510.10903](https://arxiv.org/abs/2510.10903)]
- **Robot Learning as an Empirical Science: Best Practices for Policy Evaluation** (*Kress-Gazit et al., 2024*) [[arXiv:2409.09491](https://arxiv.org/abs/2409.09491)]
- **A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation** (*TRI LBM, 2025*) [[arXiv:2507.05331](https://arxiv.org/abs/2507.05331)]
- **A Survey on Robotic Manipulation of Deformable Objects: Recent Advances, Open Challenges and New Frontiers** [[arXiv:2312.10419](https://arxiv.org/abs/2312.10419)]

</details>

---

## 📊 Datasets, Simulators & Benchmarks

| Name | Venue / Org | Date | Description & Resources | Modality & Embodiment |
|:---:|:---:|:---:|:---|:---:|
| **Open X-Embodiment** | ICRA | 2024 | 1M+ real robot trajectories across 22 robot embodiments from 21 institutions [[paper](https://arxiv.org/abs/2310.08864)] [[code](https://github.com/google-deepmind/open_x_embodiment)] [[dataset](https://robotics-transformer-x.github.io/)] | RGB-D, Proprio, Language (22 Robots) |
| **DROID** | RSS | 2024 | 76k trajectories (350 hours) across 564 diverse in-the-wild scenes on Franka Panda [[paper](https://arxiv.org/abs/2403.12945)] [[code](https://github.com/droid-dataset/droid)] [[dataset](https://droid-dataset.github.io/)] | Stereo RGB-D, Wrist Cam, Proprio, Lang |
| **BridgeData V2** | CoRL | 2023 | 60k+ trajectories across 24 environments on low-cost WidowX 250 6-DoF arm [[paper](https://arxiv.org/abs/2308.12952)] [[code](https://github.com/rail-berkeley/bridge_data_v2)] [[dataset](https://rail-berkeley.github.io/bridgedata/)] | RGB, Proprio, Language, Goal Image |
| **AgiBot World Colosseo** | AgiBot | 2025 | 1,000,000+ real-world bimanual mobile manipulation trajectories across 100+ real scenarios [[paper](https://arxiv.org/abs/2503.06669)] [[code](https://github.com/OpenDriveLab/AgiBot-World)] [[dataset](https://huggingface.co/agibot-world)] | Multi-Cam RGB-D, Visuotactile, Bimanual |
| **Galaxea Open-World** | Galaxea | 2025 | 500+ hours of synchronized mobile bimanual manipulation trajectories across 50 scenes [[paper](https://arxiv.org/abs/2509.00576)] [[dataset](https://opengalaxea.github.io/GalaxeaVLA/)] | RGB-D, Whole-Body Bimanual Proprio |
| **RoboMIND** | Peking Univ | 2024 | 107k real & simulated trajectories spanning single-arm, bimanual, humanoid, and dexterous hands [[paper](https://arxiv.org/abs/2412.13877)] [[code](https://huggingface.co/datasets/x-humanoid-robomind/RoboMIND)] [[dataset](https://x-humanoid-robomind.github.io/)] | Multi-Embodiment RGB-D + Proprio |
| **RH20T** | ICRA | 2024 | 110k contact-rich manipulation episodes with synchronized 6-axis Force/Torque sensing [[paper](https://arxiv.org/abs/2307.00595)] [[dataset](https://rh20t.github.io/)] | RGB-D, **6-Axis F/T**, Proprio |
| **LIBERO / LIBERO-Plus** | NeurIPS | 2023/2025 | 130 lifelong learning manipulation tasks (Spatial, Object, Goal, Long) + OOD robustness suite [[paper](https://arxiv.org/abs/2306.03310)] [[code](https://github.com/Lifelong-Robot-Learning/LIBERO)] | Sim RGB, Proprio, Language |
| **CALVIN** | IEEE RA-L | 2022 | Long-horizon language-conditioned manipulation benchmark (5 consecutive subtasks `ABC->D`) [[paper](https://arxiv.org/abs/2112.03227)] [[code](https://github.com/mees/calvin)] | Sim RGB-D, Tactile, Language |
| **ManiSkill3** | RSS / SAPIEN | 2024/2025 | GPU-parallelized simulation benchmark (30,000+ FPS) supporting rigid, articulated, and deformable tasks [[paper](https://arxiv.org/abs/2410.00425)] [[code](https://github.com/haosulab/ManiSkill)] | GPU Sim RGB-D, Point Cloud, Force |
| **RoboTwin / RoboTwin 2.0** | CVPR / CoRL | 2025/2026 | Generative digital-twin benchmark for coordinated bimanual manipulation & clutter-to-real (`C2R`) [[paper](https://arxiv.org/abs/2506.18088)] [[code](https://github.com/RoboTwin-Platform/RoboTwin)] | Bimanual Sim & Real RGB-D |
| **RoboCasa** | RSS | 2024 | Large-scale everyday household simulation environment powered by MimicGen trajectory synthesis [[paper](https://arxiv.org/abs/2406.02523)] [[code](https://github.com/robocasa/robocasa)] | Sim Kitchen Mobile Bimanual |
| **UniVTAC** | arXiv | 2026 | Unified visuotactile benchmark and dataset for tight-tolerance insertion, snap-fit, and blind assembly [[paper](https://arxiv.org/abs/2602.10093)] | RGB + **Optical Tactile** + Proprio |
| **ForceBench** | arXiv | 2026 | Comprehensive benchmark for force-aware robotic manipulation with systematic baseline ablations [[paper](https://arxiv.org/abs/2610.19604)] | RGB + **6-Axis Force/Torque** |
| **RoboArena** | Multi-Inst | 2025 | Distributed real-world double-blind A/B evaluation platform with Bradley-Terry Elo ranking [[paper](https://arxiv.org/abs/2506.18123)] [[project](https://robo-arena.github.io/)] | Real-World Distributed Evaluation |
| **Newton / Isaac Lab** | NVIDIA/DeepMind | 2025/2026 | Open-source GPU differentiable physics engine (`MuJoCo Warp` / XPBD / MPM) for rigid & deformable bodies [[project](https://github.com/newton-physics/newton)] [[isaac-lab](https://github.com/isaac-sim/IsaacLab)] | GPU Differentiable Physics |
| **LeRobot (v3)** | HuggingFace | 2024–2026 | Unified PyTorch framework & `LeRobotDataset v3` format for ACT, Diffusion, $\pi_0$, $\pi_{0.5}$, SmolVLA [[code](https://github.com/huggingface/lerobot)] [[datasets](https://huggingface.co/lerobot)] | Unified Training & Eval Stack |

<p align="center">
  <img src="assets/ei_tutorial/benchmark_sota_comparison_2026.svg" width="96%" alt="2024-2026 Embodied Foundation Models Quantitative Benchmark & Latency Comparison"/>
</p>

---

## 🏆 Top-60 Must-Read Embodied AI Canon

> For the complete 60-paper annotated tables with 4-week study plans, see [**`docs/00_Must_Read_60_Leaderboard.md`**](./docs/00_Must_Read_60_Leaderboard.md). Below are the **12 Foundational Tier-0 Papers** every researcher should read first:

| # | Paper | Venue | Year | Key Contribution | Links |
|:---:|:---|:---:|:---:|:---|:---:|
| **01** | **ACT / ALOHA** | RSS | 2023 | Action Chunking with Transformers ($H$-step prediction) + CVAE + Temporal Ensembling | [[paper](https://arxiv.org/abs/2304.13705)] [[code](https://github.com/tonyzhaozh/act)] |
| **02** | **Diffusion Policy** | RSS / IJRR | 2023 | Conditional denoising diffusion over action chunks to capture multimodal distributions | [[paper](https://arxiv.org/abs/2303.04137)] [[code](https://github.com/real-stanford/diffusion_policy)] |
| **03** | **RT-2** | CoRL | 2023 | Co-finetuning web VLMs with discretized robotic action tokens for semantic transfer | [[paper](https://arxiv.org/abs/2307.15818)] |
| **04** | **Open X-Embodiment** | ICRA | 2024 | Cross-embodiment dataset (22 robots, 1M+ episodes) and RT-X generalist policies | [[paper](https://arxiv.org/abs/2310.08864)] [[code](https://github.com/google-deepmind/open_x_embodiment)] |
| **05** | **Octo** | RSS | 2024 | Open-source cross-embodiment generalist policy with language & goal-image conditioning | [[paper](https://arxiv.org/abs/2405.12213)] [[code](https://github.com/octo-models/octo)] |
| **06** | **OpenVLA** | CoRL | 2024 | 7B open-source VLA (`Llama-2` + `DINOv2` + `SigLIP`) with LoRA & quantization recipes | [[paper](https://arxiv.org/abs/2406.09246)] [[code](https://github.com/openvla/openvla)] |
| **07** | **UMI** | RSS | 2024 | Embodiment-free handheld fisheye SLAM gripper for low-cost in-the-wild data collection | [[paper](https://arxiv.org/abs/2402.10329)] [[code](https://github.com/real-stanford/universal_manipulation_interface)] |
| **08** | **HIL-SERL** | arXiv | 2024 | Sample-efficient real-world RL with human-in-the-loop interventions reaching ~100% SR in 1–2.5h | [[paper](https://arxiv.org/abs/2410.21845)] [[code](https://github.com/rail-berkeley/serl)] |
| **09** | **$\pi_0$ (openpi)** | Physical Intelligence | 2024 | VLM backbone (`PaliGemma-3B`) + 300M Flow Matching Action Expert for 50Hz continuous control | [[paper](https://arxiv.org/abs/2410.24164)] [[code](https://github.com/Physical-Intelligence/openpi)] |
| **10** | **$\pi_{0.5}$** | Physical Intelligence | 2025 | Heterogeneous co-training (discrete FAST tokens + continuous flow expert) for open-world generalization | [[paper](https://arxiv.org/abs/2504.16054)] [[code](https://github.com/Physical-Intelligence/openpi)] |
| **11** | **Knowledge Insulation** | Physical Intelligence | 2025 | Stopping continuous flow gradients (`stop_gradient`) from corrupting pretrained VLM representations | [[paper](https://arxiv.org/abs/2505.23705)] |
| **12** | **Real-Time Chunking (RTC)** | Physical Intelligence | 2025 | Committed prefix locking ($a_{0:d}$) + soft-masked flow inpainting for zero-pause asynchronous execution | [[paper](https://arxiv.org/abs/2506.07339)] [[follow-up](https://arxiv.org/abs/2512.05964)] |

---

## 🗂️ Categorized Frontier Papers (2023–2026)

### 1. Vision-Language-Action (VLA) Foundation Models

<details open>
<summary>📚 Show/Hide VLA Foundation Models</summary>

- **[2026.10]** **VLA-$\Delta$**: Learning Physical State Transition for Vision-Language-Action Models [[paper](https://arxiv.org/abs/2610.21306)]
- **[2026.10]** **ObjDream**: Guiding Vision-Language-Action Models with Object-Level Understanding and Future State Prediction [[paper](https://arxiv.org/abs/2610.20223)]
- **[2026.10]** **TacitVLA**: Reasoning Vision-Language-Action Models Without Reasoning Latency [[paper](https://arxiv.org/abs/2610.17540)]
- **[2026.10]** **REKI**: Registering Knowledge in VLAs [[paper](https://arxiv.org/abs/2610.22178)]
- **[2026.10]** **EvoMem-VLA**: State-Evolution Memory for Long-Horizon Robot Manipulation [[paper](https://arxiv.org/abs/2610.05418)]
- **[2026.09]** **SAVLA**: Symmetry-Aware Vision-Language-Action Models for Robotic Manipulation [[paper](https://arxiv.org/abs/2609.16641)]
- **[2026.08]** **StreamPI**: Streaming Multimodal Temporal Modeling for Vision-Language-Action Models [[paper](https://arxiv.org/abs/2608.26067)]
- **[2026.07]** **LaMem-VLA**: Dual Latent Memory in Vision-Language-Action Models for Robotic Manipulation [[paper](https://arxiv.org/abs/2607.07608)]
- **[2026.06]** **Qwen-RobotManip**: Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models [[paper](https://arxiv.org/abs/2606.17846)]
- **[2026.06]** **ERVLA**: Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation [[paper](https://arxiv.org/abs/2606.03784)]
- **[2026.04]** **$\pi_{0.7}$**: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities [[paper](https://arxiv.org/abs/2604.15483)]
- **[2026.03]** **MEM**: Multi-Scale Embodied Memory for Vision Language Action Models [[paper](https://arxiv.org/abs/2603.03596)]
- **[2025.10]** **Gemini Robotics 1.5**: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer [[paper](https://arxiv.org/abs/2510.03342)]
- **[2025.07]** **GR-3**: GR-3 Technical Report [[paper](https://arxiv.org/abs/2507.15493)]
- **[2025.06]** **SmolVLA**: A Vision-Language-Action Model for Affordable and Efficient Robotics [[paper](https://arxiv.org/abs/2506.01844)] [[code](https://github.com/huggingface/lerobot)]
- **[2025.03]** **Gemini Robotics**: Bringing AI into the Physical World [[paper](https://arxiv.org/abs/2503.20020)]
- **[2025.03]** **GR00T N1 / N1.5**: Open Foundation Model for Generalized Humanoid Robot Skills [[code](https://github.com/NVIDIA/Isaac-GR00T)]
- **[2025.02]** **OpenVLA-OFT**: Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success (RSS 2025) [[paper](https://arxiv.org/abs/2502.19645)] [[code](https://github.com/moojink/openvla-oft)]
- **[2025.01]** **FAST**: Efficient Action Tokenization for Vision-Language-Action Models [[paper](https://arxiv.org/abs/2501.09747)]

</details>

---

### 2. World Action Models (WAM) & Video-Action Pretraining

<details open>
<summary>📚 Show/Hide World Action Models (WAM)</summary>

- **[2026.10]** **OpenWAM**: An Open Framework for Composable World-Action Models [[paper](https://arxiv.org/abs/2610.07922)]
- **[2026.10]** **Long-WAM**: Scaling the Context of World-Action Models [[paper](https://arxiv.org/abs/2610.10528)]
- **[2026.03]** **Fast-WAM**: Do World Action Models Need Test-time Future Imagination? [[paper](https://arxiv.org/abs/2603.16666)]
- **[2026.03]** **EVA**: Aligning Video World Models with Executable Robot Actions via Inverse Dynamics Rewards [[paper](https://arxiv.org/abs/2603.17808)]
- **[2026.02]** **DreamZero**: World Action Models are Zero-shot Policies [[paper](https://arxiv.org/abs/2602.15922)]
- **[2025.06]** **V-JEPA 2**: Self-Supervised Video Models Enable Understanding, Prediction and Planning [[paper](https://arxiv.org/abs/2506.09985)] [[code](https://github.com/facebookresearch/vjepa2)]
- **[2025.05]** **DreamGen**: Unlocking Generalization in Robot Learning through Video World Models [[paper](https://arxiv.org/abs/2505.12705)]

</details>

---

### 3. Reinforcement Learning for Flow Matching & Diffusion VLAs

<details open>
<summary>📚 Show/Hide RL for Flow & Diffusion Policies</summary>

- **[2026.10]** **NSL**: Noise Space Learning for VLA Adaptation [[paper](https://arxiv.org/abs/2610.13943)]
- **[2026.10]** **VaM**: Value as Memory: Online Value-Guided Post-training for General Robot Policies [[paper](https://arxiv.org/abs/2610.22368)]
- **[2026.09]** **RoboFFT**: Finetuning generative robot policy via online reinforcement learning with forward process [[paper](https://arxiv.org/abs/2609.32236)]
- **[2026.04]** **RL Token (RLT)**: Bootstrapping Online RL with Vision-Language-Action Models [[paper](https://arxiv.org/abs/2604.23073)]
- **[2025.11]** **$\pi^*_{0.6}$ (RECAP)**: a VLA That Learns From Experience [[paper](https://arxiv.org/abs/2511.14759)]
- **[2025.10]** **$\pi_{\texttt{RL}}$**: Online RL Fine-tuning for Flow-based Vision-Language-Action Models [[paper](https://arxiv.org/abs/2510.25889)]
- **[2025.10]** **RL-100**: Performant Robotic Manipulation with Real-World Reinforcement Learning [[paper](https://arxiv.org/abs/2510.14830)]
- **[2025.09]** **ResFiT**: Residual Off-Policy RL for Finetuning Behavior Cloning Policies [[paper](https://arxiv.org/abs/2509.19301)]
- **[2025.09]** **RLinf**: Flexible and Efficient Large-scale Reinforcement Learning via Macro-to-Micro Flow Transformation [[paper](https://arxiv.org/abs/2509.15965)] [[code](https://github.com/RLinf/RLinf)]
- **[2025.06]** **DSRL**: Steering Your Diffusion Policy with Latent Space Reinforcement Learning [[paper](https://arxiv.org/abs/2506.15799)]
- **[2025.05]** **ReinFlow**: Fine-tuning Flow Matching Policy with Online Reinforcement Learning [[paper](https://arxiv.org/abs/2505.22094)]
- **[2025.02]** **ConRFT**: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy [[paper](https://arxiv.org/abs/2502.05450)]
- **[2024.12]** **PA-RL**: Policy Agnostic RL: Offline RL and Online RL Fine-Tuning of Any Class and Backbone [[paper](https://arxiv.org/abs/2412.06685)]
- **[2024.10]** **HIL-SERL**: Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning [[paper](https://arxiv.org/abs/2410.21845)] [[code](https://github.com/rail-berkeley/serl)]
- **[2024.09]** **DPPO**: Diffusion Policy Policy Optimization [[paper](https://arxiv.org/abs/2409.00588)] [[code](https://github.com/irom-princeton/dppo)]

</details>

---

### 4. Visuotactile Sensing, Compliant Control & Contact-Rich Manipulation

<details open>
<summary>📚 Show/Hide Tactile & Contact-Rich Manipulation Papers</summary>

- **[2026.10]** **ForceBench**: Benchmarking Force Integration for Robotic Manipulation [[paper](https://arxiv.org/abs/2610.19604)]
- **[2026.10]** **FACT**: A Multimodal Force-Action-Track Foundation Model for Human-to-Robot Dexterity [[paper](https://arxiv.org/abs/2610.19155)]
- **[2026.10]** **PRISM**: Precision Forcing for Generalist Vision-Language-Action Policies [[paper](https://arxiv.org/abs/2610.14704)]
- **[2026.10]** **PACE**: Temporal-Role Tactile Conditioning for Chunk-Based Insertion Policies (CoRL 2026) [[paper](https://arxiv.org/abs/2610.16308)]
- **[2026.10]** **Spark-0**: Scaling Spatially Aligned Tactile Pretraining for Robot Dexterous Manipulation [[paper](https://arxiv.org/abs/2610.22342)]
- **[2026.10]** **SimpleTouch**: Can Vision-Language-Action Models Master Contact-Rich Manipulation Without Tactile Policy Pretraining? [[paper](https://arxiv.org/abs/2610.02784)]
- **[2026.07]** **$N_0$-VTLA**: Scaling Vision-Tactile-Language-Action Model with Latent Tactile Tokens [[paper](https://arxiv.org/abs/2607.23782)]
- **[2026.07]** **FA-RDP**: A Frequency-Adaptive Reactive Diffusion Policy for Contact-Rich Manipulation [[paper](https://arxiv.org/abs/2607.28596)]
- **[2026.06]** **T-Rex**: Tactile-Reactive Dexterous Manipulation [[paper](https://arxiv.org/abs/2606.17055)]
- **[2026.03]** **TacVLA**: Contact-Aware Tactile Fusion for Robust Vision-Language-Action Manipulation [[paper](https://arxiv.org/abs/2603.12665)]
- **[2026.03]** **ForceVLA2**: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation (CVPR 2026) [[paper](https://arxiv.org/abs/2603.15169)]
- **[2026.02]** **UniVTAC**: A Unified Simulation Platform for Visuo-Tactile Manipulation Data Generation, Learning, and Benchmarking [[paper](https://arxiv.org/abs/2602.10093)]
- **[2026.02]** **GAP (Gradient Adjustment with Phase-guidance)**: When would Vision-Proprioception Policies Fail in Robotic Manipulation? (ICLR 2026) [[paper](https://arxiv.org/abs/2602.12032)]
- **[2025.12]** **ImplicitRDP**: An End-to-End Visual-Force Diffusion Policy with Structural Slow-Fast Learning (RA-L 2026) [[paper](https://arxiv.org/abs/2512.10946)]
- **[2025.05]** **ForceVLA**: Enhancing VLA Models with a Force-aware MoE for Contact-rich Manipulation (NeurIPS 2025) [[paper](https://arxiv.org/abs/2505.22159)]
- **[2025.03]** **Reactive Diffusion Policy (RDP)**: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation (RSS 2025) [[paper](https://arxiv.org/abs/2503.02881)] [[code](https://github.com/xiaoxiaoxh/reactive_diffusion_policy)]
- **[2025.02]** **FACTR**: Force-Attending Curriculum Training for Contact-Rich Policy Learning [[paper](https://arxiv.org/abs/2502.17432)]
- **[2024.10]** **Sparsh**: Self-supervised touch representations for vision-based tactile sensing (CoRL 2024) [[paper](https://arxiv.org/abs/2410.24090)] [[code](https://github.com/facebookresearch/sparsh)]
- **[2024.10]** **3D-ViTac**: Learning Fine-Grained Manipulation with Visuo-Tactile Sensing (CoRL 2024) [[paper](https://arxiv.org/abs/2410.24091)]
- **[2024.10]** **ACP**: Adaptive Compliance Policy: Learning Approximate Compliance for Diffusion Guided Control [[paper](https://arxiv.org/abs/2410.09309)]
- **[2024.09]** **AnySkin**: Plug-and-play Skin Sensing for Robotic Touch [[paper](https://arxiv.org/abs/2409.08276)]
- **[2024.06]** **T3**: Transferable Tactile Transformers for Representation Learning Across Diverse Sensors and Tasks [[paper](https://arxiv.org/abs/2406.13640)] [[code](https://github.com/alanzjl/t3)]
- **[2024.01]** **UniTouch**: Binding Touch to Everything: Learning Unified Multimodal Tactile Representations [[paper](https://arxiv.org/abs/2401.18084)]

</details>

---

### 5. Real-Time Action Chunking (RTC), Latency & Edge Acceleration

<details open>
<summary>📚 Show/Hide Real-Time Execution & Acceleration Papers</summary>

- **[2026.10]** **Chronos Policy**: Learning Robot Policies on Physical Time [[paper](https://arxiv.org/abs/2610.13929)]
- **[2026.10]** **REACT**: Rolling Denoising and Dual Decoupling for Reactive Robot Control with VLA Models (CoRL 2026) [[paper](https://arxiv.org/abs/2610.12007)]
- **[2026.07]** **TurboVLA**: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM [[paper](https://arxiv.org/abs/2607.27205)]
- **[2026.07]** **FabriVLA**: A Lightweight Vision-Language-Action Model with Conformal Action Chunk Uncertainty [[paper](https://arxiv.org/abs/2607.08575)]
- **[2025.12]** **Training-Time RTC**: Training-Time Action Conditioning for Efficient Real-Time Chunking [[paper](https://arxiv.org/abs/2512.05964)]
- **[2025.06]** **BitVLA**: 1-bit Vision-Language-Action Models for Robotics Manipulation [[paper](https://arxiv.org/abs/2506.07530)]
- **[2025.06]** **Real-Time Chunking (RTC)**: Real-Time Execution of Action Chunking Flow Policies (NeurIPS 2025) [[paper](https://arxiv.org/abs/2506.07339)]
- **[2025.05]** **Knowledge Insulation (KI)**: Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better [[paper](https://arxiv.org/abs/2505.23705)]
- **[2025.02]** **VLA-Cache**: Efficient Vision-Language-Action Manipulation via Adaptive Token Caching (NeurIPS 2025) [[paper](https://arxiv.org/abs/2502.02175)]
- **[2024.11]** **DeeR-VLA**: Dynamic Inference of Multimodal Large Language Models for Efficient Robot Execution (NeurIPS 2024) [[paper](https://arxiv.org/abs/2411.02359)]

</details>

---

### 6. Online Verification, Failure Detection & Closed-Loop Recovery

<details open>
<summary>📚 Show/Hide Verification, Failure Detection & Recovery Papers</summary>

- **[2026.10]** **FAVOR**: Future Anchored Verification and Online Recovery for World Action Models [[paper](https://arxiv.org/abs/2610.06280)]
- **[2026.10]** **DiVeR**: Decision-Critical Verifier Learning for VLA Test-Time Scaling [[paper](https://arxiv.org/abs/2610.04933)]
- **[2026.08]** **Active Observation**: Active Observation for Robust Visual Servoing in Robotic Manipulation (*Hu et al., IEEE CASE 2026 Accepted, Paper ThCT6.3*) [[program](https://ras.papercept.net/conferences/scripts/rtf/CASE26_ContentListWeb_4.html)] [[project](https://hzl666.xyz/projects/active-observation/)]
- **[2026.07]** **Harness VLA**: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents [[paper](https://arxiv.org/abs/2607.08448)]
- **[2026.06]** **E-TTS**: A New Embodied Test-Time Scaling Framework for Robotic Manipulation (ECCV 2026) [[paper](https://arxiv.org/abs/2606.27268)]
- **[2025.06]** **SAFE**: Multitask Failure Detection for Vision-Language-Action Models (NeurIPS 2025) [[paper](https://arxiv.org/abs/2506.09937)]
- **[2025.03]** **FAIL-Detect**: Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies (RSS 2025) [[paper](https://arxiv.org/abs/2503.08558)]

</details>

---

### 7. 3D Spatial Grounding, Dexterous Hands, Whole-Body Control & Deformable Objects

<details open>
<summary>📚 Show/Hide 3D VLA, Dexterous Manipulation, WBC & DLO Papers</summary>

- **[2026.10]** **VioLA**: Learning Generalist Humanoid Control Policies from Human Data [[paper](https://arxiv.org/abs/2610.12435)]
- **[2026.09]** **Online Material Estimation for DLOs**: Online Material Estimation for Conditioned Diffusion Policy in Shaping Deformable Linear Objects [[paper](https://arxiv.org/abs/2609.12634)]
- **[2026.07]** **The Curse of Precision**: A Data Scaling Law for High-Precision Robotic Manipulation (ICRA 2026) [[paper](https://arxiv.org/abs/2607.23108)]
- **[2026.06]** **DLO-Lab & DeformX**: DLO-Lab: Benchmarking Deformable Linear Object Manipulations with Differentiable Physics; DeformX: A Versatile Co-Simulation Framework for Deformable Linear Objects (ICML 2026) [[DLO-Lab](https://arxiv.org/abs/2606.04206)] [[DeformX](https://arxiv.org/abs/2606.22116)]
- **[2026.06]** **WireCraft**: A Simulation Benchmark for Industrial DLO Manipulation (CoRL 2026) [[paper](https://arxiv.org/abs/2606.18097)]
- **[2025.11]** **SONIC**: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control [[paper](https://arxiv.org/abs/2511.07820)]
- **[2025.08]** **BeyondMimic**: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion [[paper](https://arxiv.org/abs/2508.08241)]
- **[2025.05]** **DexUMI**: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation [[paper](https://arxiv.org/abs/2505.21864)]
- **[2025.03]** **PointVLA**: Injecting the 3D World into Vision-Language-Action Models [[paper](https://arxiv.org/abs/2503.07511)]
- **[2025.02]** **ASAP**: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills (RSS 2025) [[paper](https://arxiv.org/abs/2502.01143)] [[code](https://github.com/LeCAR-Lab/ASAP)]
- **[2025.01]** **SpatialVLA**: Exploring Spatial Representations for Visual-Language-Action Model (RSS 2025) [[paper](https://arxiv.org/abs/2501.15830)]
- **[2024.10]** **HOVER**: Versatile Neural Whole-Body Controller for Humanoid Robots (ICRA 2025) [[paper](https://arxiv.org/abs/2410.21229)]
- **[2024.10]** **DexMimicGen**: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning (ICRA 2025) [[paper](https://arxiv.org/abs/2410.24185)]
- **[2023.10]** **MimicGen**: A Data Generation System for Scalable Robot Learning using Human Demonstrations (CoRL 2023) [[paper](https://arxiv.org/abs/2310.17596)] [[code](https://github.com/NVlabs/mimicgen)]

</details>

---

## 💻 Quick Start: Running the 5 PyTorch Code Labs & Teaching Figures

All 5 code labs in [`labs/`](./labs/) are self-contained and require only `Python >= 3.10` and `torch==2.9.0`:

```bash
python labs/lab1_openpi_ki_and_latency_profiler.py
python labs/lab2_rtc_soft_masked_inpainting.py
python labs/lab3_cascade_tactile_flow.py
python labs/lab4_final_step_gaussian_ppo_and_critic.py
python labs/lab5_rigorous_robot_eval_statistics.py
```

### Synthetic teaching diagrams and derived statistics (not robot measurements)

<p align="center">
  <img src="assets/ei_tutorial/lab1_ki_and_latency_plot.svg" width="49%" alt="Lab 1: Knowledge Insulation & Latency"/>
  <img src="assets/ei_tutorial/lab2_rtc_trajectory_inpainting_plot.svg" width="49%" alt="Lab 2: Real-Time Chunking Soft-Masked Inpainting"/>
</p>
<p align="center">
  <img src="assets/ei_tutorial/lab3_two_stage_modality_ablation_plot.svg" width="49%" alt="Lab 3: Two-Stage Rollout & Controlled Modality Ablation"/>
  <img src="assets/ei_tutorial/lab4_flow_rl_convergence_plot.svg" width="49%" alt="Lab 4: Online RL Post-Training for Flow VLAs"/>
</p>
<p align="center">
  <img src="assets/ei_tutorial/lab5_statistical_eval_wilson_mcnemar_plot.svg" width="72%" alt="Lab 5: Wilson 95% CI & Paired McNemar Evaluation"/>
</p>

