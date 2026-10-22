<p align="center">
  <a href="../README.md"><b>🏠 English Survey Portal</b></a> |
  <a href="../README_zh.md"><b>🏠 中文综述门户</b></a> |
  <a href="./00_Must_Read_60_Leaderboard.md"><b>🏆 Top-60 Must-Read</b></a> |
  <a href="./01_Foundations_Compliant_Control_and_RL.md"><b>Stage 1</b></a> |
  <a href="./02_VLA_WAM_and_Flow_RL.md"><b>Stage 2A</b></a> |
  <a href="./03_Tactile_RTC_and_Verification_Recovery.md"><b>Stage 2B</b></a> |
  <a href="./04_Datasets_Scaling_Laws_and_Statistical_Eval.md"><b>Stage 3</b></a> |
  <a href="./05_Contact_Rich_Manipulation_and_Generalist_EI.md"><b>Stage 4A</b></a> |
  <a href="./06_Glossary_Templates_and_Checklists.md"><b>Stage 4B & Labs</b></a>
</p>

---

## 具身智能与富接触操作必读论文总榜（2022–2026.10 精选 60 篇分级导读）

**证据等级**：`[已验证事实]` 全部论文标题照抄 arXiv 官方元数据（由 `tools/build_references.py` 生成的 `references.bib` 统一维护）；`[论文报告]` 核心机制与数字对照各论文摘要；`[方法论综合]` 按“入门奠基 $\rightarrow$ 流匹配/扩散强化学习 $\rightarrow$ 视触觉与富接触操作 $\rightarrow$ 实时执行与验证恢复 $\rightarrow$ 世界模型与全身控制 $\rightarrow$ 数据缩放律与统计评测”六大模块分级，并标注每篇论文在富接触操作研究中的定位。

> [!tip] 如何使用这份必读榜单？
> - **新手入门（第 1–2 周）**：只读 **模块一（Tier 0 奠基必读 Top 10）**，配合本教程阶段 1 与阶段 4 的 `Lab 1`、`Lab 2` 跑通代码，切勿一上来陷入上百篇 2026 新论文的海洋。
> - **视触觉与流匹配在线 RL 进阶（第 3 周）**：精读 **模块二（Flow/Diffusion RL 12 篇）** + **模块三（视触觉与富接触 16 篇）** + **模块四中的 `RTC` / `KI`**。其中标有 `直接竞品/必引基线` 的论文必须在 Related Work 与实验表格中正面回应。
> - **长程在线验证、失败恢复与双臂 DLO 进阶（第 4 周）**：精读 **模块四（实时执行、验证恢复与 DLO 12 篇）** + **模块六（统计评测协议）**。

---

### 一、入门怎么读：三阶段 30 天精读路径

| 周期 | 目标人群与阶段 | 必读论文组合（共 20 篇核心） | 配套动手实验 |
|---|---|---|---|
| **第 1 周（建立物理闭环直觉）** | 零基础 / 刚转入具身智能 | `#01 ACT`、`#02 Diffusion Policy`、`#03 RT-2`、`#05 Octo`、`#06 OpenVLA`、`#07 UMI` | 跑通 `LeRobot` 下的 ACT / Diffusion Policy 仿真推箱与插孔 |
| **第 2 周（掌握现代流匹配 VLA 底座）** | 准备复现主流 VLA | `#09 π0`、`#10 π0.5`、`#11 Knowledge Insulation`、`#12 RTC`、`#49 Qwen-RobotManip`、`#50 REKI` | 运行本教程 **`Lab 1`（`openpi` + `KI`）** 与 **`Lab 2`（`RTC` 软掩码流修复）** |
| **第 3 周（攻克视触觉与流匹配 RL）** | 视触觉表征与流匹配在线 RL 深入 | `#08 HIL-SERL`、`#13 DPPO`、`#15 πRL`、`#18 DSRL`、`#21 RECAP`、`#25 T3`、`#29 RDP`、`#33 T-Rex`、`#34 SimpleTouch`、`#39 UniVTAC`、`#40 ForceBench` | 运行本教程 **`Lab 3`（两阶段流与受控模态消融合成实验）** 与 **`Lab 4`（高斯块策略梯度与欧拉链求导分析）** |
| **第 4 周（闭环验证恢复与顶会级评测）** | 在线验证恢复与严格统计评测 | `#43 FAVOR`、`#44 DiVeR`、`#45 SAFE`、`#47 E-TTS`、`#48 Harness VLA`、`#56 Curse of Precision`、`#58 RoboArena`、`#59 TRI LBM`、`#60 Kress-Gazit` | 运行本教程 **`Lab 5`（Wilson 95% CI + McNemar 精确检验）** |

---

### 二、模块一：奠基必读 Top 12（Tier 0 · 具身智能通用语言）

这 12 篇论文定义了现代具身智能的**动作块（Action Chunking）、连续去噪/流匹配生成、VLA 架构、无本体采集、真机 RL 与实时异步闭环**，是所有后续研究的共同底座。

| 编号 | 推荐度 | 论文简称与年份 | 完整标题与 arXiv / 来源 | 核心贡献（一句话精髓） | 开源状态 | 核心定位与适用场景 |
|---|---|---|---|---|---|---|
| **#01** | ★★★★★ | **`ACT / ALOHA`** (RSS 2023) | *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* ([arXiv:2304.13705](https://arxiv.org/abs/2304.13705)) | 提出 Action Chunking ($H$ 步动作块预测) + CVAE 潜变量 + Temporal Ensembling，奠定双臂精细模仿学习基石 | 代码/硬件全开源 | 双臂操作与动作块基石 |
| **#02** | ★★★★★ | **`Diffusion Policy`** (RSS 2023 / IJRR) | *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion* ([arXiv:2303.04137](https://arxiv.org/abs/2303.04137)) | 将条件扩散去噪引入机器人动作生成，解决多峰动作分布（Multimodality）下 MSE 回归均值坍缩问题 | 代码/权重全开源 | 连续生成式策略第一基准 |
| **#03** | ★★★★☆ | **`RT-2`** (CoRL 2023) | *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control* ([arXiv:2307.15818](https://arxiv.org/abs/2307.15818)) | 正式提出 **VLA** 概念，将末端动作离散化为文本 Token 与互联网 VLM 协同微调，实现涌现语义泛化 | 闭源 | VLA 概念开山之作 |
| **#04** | ★★★★★ | **`Open X / RT-X`** (ICRA 2024) | *Open X-Embodiment: Robotic Learning Datasets and RT-X Models* ([arXiv:2310.08864](https://arxiv.org/abs/2310.08864)) | 联合 21 家机构构建 22 种本体、100 万+轨迹数据集，开启跨本体（Cross-Embodiment）预训练时代 | 数据集开源 | 跨本体数据对齐必引 |
| **#05** | ★★★★☆ | **`Octo`** (RSS 2024) | *Octo: An Open-Source Generalist Robot Policy* ([arXiv:2405.12213](https://arxiv.org/abs/2405.12213)) | 首套完全开源、支持语言与目标图像双条件、采用轻量扩散动作头的跨本体通用策略 | 代码/权重/数据全开源 | 轻量通用扩散策略对照 |
| **#06** | ★★★★★ | **`OpenVLA`** (CoRL 2024) | *OpenVLA: An Open-Source Vision-Language-Action Model* ([arXiv:2406.09246](https://arxiv.org/abs/2406.09246)) | 基于 `Llama-2-7B` + `DINOv2` + `SigLIP` 的开源 VLA 标杆，验证 LoRA 微调与量化部署流程 | 代码/权重/数据全开源 | 离散自回归 VLA 标准基线 |
| **#07** | ★★★★★ | **`UMI`** (RSS 2024) | *Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots* ([arXiv:2402.10329](https://arxiv.org/abs/2402.10329)) | 用手持 3D 打印夹爪 + GoPro 鱼眼 SLAM 实现无机器人本体的野外数据采集与零样本跨机械臂迁移 | 硬件/代码全开源 | 低成本采集与相机中心坐标标杆 |
| **#08** | ★★★★★ | **`HIL-SERL`** (2024.10) | *Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning* ([arXiv:2410.21845](https://arxiv.org/abs/2410.21845)) | 真机强化学习工程圣经：结合少量演示初始化 SAC 缓冲池、在线人工干预纠偏与高 UTD，1–2.5 小时真机插装达近 100% 成功率 | 代码全开源 (`serl`) | 真机在线 RL 与干预机制必引 |
| **#09** | ★★★★★ | **`π0 / openpi`** (2024.10) | *$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control* ([arXiv:2410.24164](https://arxiv.org/abs/2410.24164)) | 将 `PaliGemma-3B` 与 300M 连续流匹配动作专家（Flow Matching Action Expert, 10 步欧拉积分 50Hz）结合 | `openpi` 开源 | 流匹配 VLA 核心基座模型 |
| **#10** | ★★★★★ | **`π0.5`** (2025.04) | *$\pi_{0.5}$: a Vision-Language-Action Model with Open-World Generalization* ([arXiv:2504.16054](https://arxiv.org/abs/2504.16054)) | 提出异构协同训练（预训练期离散 FAST Token + 后训练期连续流动作专家）与高层语义子目标到低层动作块的两阶段推理 | `openpi` 开源 | 异构协同训练与两阶段推理基座 |
| **#11** | ★★★★★ | **`Knowledge Insulation`** (2025.05) | *Knowledge Insulating Vision-Language-Action Models: Train Fast, Run Fast, Generalize Better* ([arXiv:2505.23705](https://arxiv.org/abs/2505.23705)) | 揭示连续流专家高方差梯度会破坏 VLM 预训练语义，提出对 VLM KV-Cache 施加 `stop_gradient` + 离散 Token 辅助监督 | 机制完全公开 (`openpi` 可复现) | 冻结/绝缘慢速 VLM 前缀的理论依据 |
| **#12** | ★★★★★ | **`RTC`** (2025.06 & 2025.12) | *Real-Time Execution of Action Chunking Flow Policies* ([arXiv:2506.07339](https://arxiv.org/abs/2506.07339)) & *Training-Time Action Conditioning for Efficient Real-Time Chunking* ([arXiv:2512.05964](https://arxiv.org/abs/2512.05964)) | 提出已承诺前缀锁定 $a_{0:d}$ 与软掩码指数衰减流修复引导（Soft-Masked Flow Inpainting），消除动作块切换停顿与边界跳变 | 官方实现公开 | 实时动作块前缀锁定与软掩码修复底座 |

---

### 三、模块二：流匹配与扩散 VLA 强化学习必读榜（12 篇 · 核心算法演进）

这 12 篇论文完整回答了“**为什么 Flow/Diffusion 策略难做 RL，以及 2024–2026 社区演化出的 7 条破局路线各有什么优劣**”。

| 编号 | 推荐度 | 论文简称与路线 | 完整标题与 arXiv 编号 | 核心机制与优劣边界 | 在视触觉流匹配 RL 中的定位 |
|---|---|---|---|---|---|
| **#13** | ★★★★★ | **`DPPO`** (路线1: 去噪 MDP) | *Diffusion Policy Policy Optimization* ([arXiv:2409.00588](https://arxiv.org/abs/2409.00588)) | 将 $K$ 步去噪展开为双层 MDP，每步高斯转移均可解析算 $\log p$ 并用 PPO 优化，通常只微调最后几步去噪层 | 证明“只对尾部去噪步做高斯 PPO”有效性的核心先驱 |
| **#14** | ★★★★★ | **`ReinFlow`** (路线2: 注入流噪声) | *ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning* ([arXiv:2505.22094](https://arxiv.org/abs/2505.22094)) | 在确定性欧拉积分步注入可学习时间条件高斯噪声网络 $\sigma_\psi(a^\tau,\tau,o)$，使离散流轨迹具有精确闭式转移似然 | 可学习探索噪声的直接参考；与只在末端步注入噪声的做法（`Lab 4`）形成对照 |
| **#15** | ★★★★★ | **`πRL`** (路线2: 全模型流 RL) | *$\pi_\texttt{RL}$: Online RL Fine-tuning for Flow-based Vision-Language-Action Models* ([arXiv:2510.25889](https://arxiv.org/abs/2510.25889)) | 提出 `Flow-Noise`（带可学习噪声网络的离散时间 MDP，可精确计算对数似然）与 `Flow-SDE`（ODE 转 SDE 的双层 MDP），对 $\pi_0/\pi_{0.5}$ 做在线 RL | 证明 3B 级流 VLA 可做在线 RL；全步建模计算图较重，适合并行仿真 |
| **#16** | ★★★★☆ | **`RLinf`** (路线2: 开源训练栈) | *RLinf: Flexible and Efficient Large-Scale Reinforcement Learning via Macro-to-Micro Flow Transformation* ([arXiv:2509.15965](https://arxiv.org/abs/2509.15965)) | 支持 `OpenVLA`、$\pi_0$、$\pi_{0.5}$ 大规模在线 PPO/GRPO 的开源工程框架（`RLinf-VLA`） | 代码开源，可直接作为 RL 训练基础设施参考 |
| **#17** | ★★★★☆ | **`RoboFFT`** (路线2: 2026.10 全参数) | *RoboFFT: Finetuning generative robot policy via online reinforcement learning with forward process* ([arXiv:2609.32236](https://arxiv.org/abs/2609.32236)) | 2026.10 最新全参数流 VLA 在线 RL 方案，通过分阶段梯度稳定策略缓解全参数更新崩溃 | 2026.10 最新流 VLA RL 文献对照 |
| **#18** | ★★★★★ | **`DSRL`** (路线3: 初始噪声空间 RL) | *Steering Your Diffusion Policy with Latent Space Reinforcement Learning* ([arXiv:2506.15799](https://arxiv.org/abs/2506.15799)) | 冻结扩散/流策略权重，用 SAC 在初始高斯噪声空间 $a^0 \sim \mathcal{N}(0,I)$ 上做引导，完全免除 BPTT 穿链 | 必须对比的强基线：指出其局限在于初始噪声 $a^0$ 在动作块起点决定，无法响应块内突发触觉冲击 |
| **#19** | ★★★★☆ | **`NSL`** (路线3: 非参数噪声优化) | *Noise Space Learning for VLA Adaptation* ([arXiv:2610.13943](https://arxiv.org/abs/2610.13943)) | 在推理期通过 Critic 梯度直接在线更新初始噪声潜变量 $a^0$ | 潜空间引导家族 2026 扩展引用 |
| **#20** | ★★★★★ | **`ResFiT`** (路线4: 动作空间残差 RL) | *Residual Off-Policy RL for Finetuning Behavior Cloning Policies* ([arXiv:2509.19301](https://arxiv.org/abs/2509.19301)) | 冻结预训练流/扩散基座，在末端输出动作空间叠加轻量 MLP 残差策略 $\Delta a_\phi$ 并用异策略 RL 训练 | 审稿人常问对比：解释为什么流空间尾步微调比纯外部 $\Delta a$ 加法残差更能保持动作块内部平滑与多峰几何 |
| **#21** | ★★★★★ | **`RL Token / RLT`** (路线4: Token 残差) | *RL Token: Bootstrapping Online RL with Vision-Language-Action Models* ([arXiv:2604.23073](https://arxiv.org/abs/2604.23073)) | 仅训练约 1M 参数的轻量残差策略头，读取 3B VLA 内部特征输出高频修正动作，15 分钟真机 RL 收敛 | 轻量真机后训练标杆 |
| **#22** | ★★★★★ | **`π*0.6 / RECAP`** (路线5: 优势条件化) | *$\pi^{*}_{0.6}$: a VLA That Learns From Experience* ([arXiv:2511.14759](https://arxiv.org/abs/2511.14759)) | 用分布式价值 Critic 评估经验优势 $I_t=\mathbb{I}(A^\pi > \epsilon)$，将其作为条件标签直接回灌至標準流匹配监督损失 | 离线/多轮迭代经验学习里程碑 |
| **#23** | ★★★★☆ | **`VaM` & `PA-RL`** (路线6: 后验流引导) | *Value as Memory: Online Value-Guided Post-training for General Robot Policies* ([arXiv:2610.22368](https://arxiv.org/abs/2610.22368)) & *Policy Agnostic RL: Offline RL and Online RL Fine-Tuning of Any Class and Backbone* ([arXiv:2412.06685](https://arxiv.org/abs/2412.06685)) | 在 ODE 积分过程中叠加 Critic 对动作的梯度 $\nabla_a Q(s,a)$ 引导速度场流向高价值区域 | 测试期 Critic 梯度引导路线代表 |
| **#24** | ★★★★★ | **`RL-100` & `ConRFT`** (路线7: 真机 100% 栈) | *RL-100: Performant Robotic Manipulation with Real-World Reinforcement Learning* ([arXiv:2510.14830](https://arxiv.org/abs/2510.14830)) & *ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy* ([arXiv:2502.05450](https://arxiv.org/abs/2502.05450)) | 系统结合离线预训练、一致性正则与在线真机交互安全护栏，在多项真机精密操作上逼近 100% 成功率 | 真机安全 RL 闭环与干预价值设计的工程参考 |

---

### 四、模块三：视触觉硬件、预训练表征与富接触 VLA 必读榜（16 篇 · 核心方法与评测基准）

| 编号 | 推荐度 | 论文简称与年份 | 完整标题与 arXiv 编号 | 核心机制与关键指标 | 在视触觉流匹配 RL 中的定位 |
|---|---|---|---|---|---|
| **#25** | ★★★★★ | **`T3`** (CoRL 2024) | *Transferable Tactile Transformers for Representation Learning Across Diverse Sensors and Tasks* ([arXiv:2406.13640](https://arxiv.org/abs/2406.13640)) | 传感器特定编码器 + 共享 Transformer 主干 + 任务特定解码器的跨传感器触觉预训练框架（ViT 在 $224\times224$、patch 16 时输出 1 CLS + $14\times 14$ 空间 Token） | 常用冻结触觉编码器；“保留空间 Token vs 全局池化”是值得做的消融 |
| **#26** | ★★★★★ | **`Sparsh`** (CoRL 2024 / Meta) | *Sparsh: Self-Supervised Touch Representations for Vision-Based Tactile Sensing* ([arXiv:2410.24090](https://arxiv.org/abs/2410.24090)) | 在 46 万+ 视触觉图像上全面评测 MAE、DINO、I-JEPA 自监督预训练，发布 `TacBench` 六项触觉下游任务 | 视触觉自监督表征权威基准，Related Work 必引 |
| **#27** | ★★★★☆ | **`UniTouch`** (CVPR 2024) | *Binding Touch to Everything: Learning Unified Multimodal Tactile Representations* ([arXiv:2401.18084](https://arxiv.org/abs/2401.18084)) | 将触觉表征对齐到预训练视觉-语言-音频语义空间，配备传感器特定 Token 实现零样本跨传感器迁移 | 多模态语义触觉对齐代表 |
| **#28** | ★★★★☆ | **`3D-ViTac` & `AnySkin`** (CoRL 2024) | *3D-ViTac: Learning Fine-Grained Manipulation with Visuo-Tactile Sensing* ([arXiv:2410.24091](https://arxiv.org/abs/2410.24091)) & *AnySkin: Plug-and-play Skin Sensing for Robotic Touch* ([arXiv:2409.08276](https://arxiv.org/abs/2409.08276)) | `3D-ViTac` 将密集触觉点云与三维视觉点云统一于 3D 空间支持双臂精细操作；`AnySkin` 提供即插即用免标定磁敏电子皮肤 | 3D 视触觉与触觉硬件代表 |
| **#29** | ★★★★★ | **`RDP`** (RSS 2025) | *Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation* ([arXiv:2503.02881](https://arxiv.org/abs/2503.02881)) | 慢速视觉潜空间扩散规划 + 快速触觉/力控潜空间译码的慢快双层架构 | 慢快视触觉架构的代表性先驱 |
| **#30** | ★★★★☆ | **`ImplicitRDP` & `FA-RDP`** (2025.12–2026.02) | *ImplicitRDP: An End-to-End Visual-Force Diffusion Policy with Structural Slow-Fast Learning* ([arXiv:2512.10946](https://arxiv.org/abs/2512.10946)) & *FA-RDP: A Frequency-Adaptive Reactive Diffusion Policy for Contact-Rich Manipulation* ([arXiv:2607.28596](https://arxiv.org/abs/2607.28596)) | 端到端联合注意力的慢快视触觉扩散策略与力自适应调制扩展 | 慢快视触觉家族最新演进必引 |
| **#31** | ★★★★☆ | **`FACTR` & `ACP`** (2024.10–2025.02) | *FACTR: Force-Attending Curriculum Training for Contact-Rich Policy Learning* ([arXiv:2502.17432](https://arxiv.org/abs/2502.17432)) & *Adaptive Compliance Policy: Learning Approximate Compliance for Diffusion Guided Control* ([arXiv:2410.09309](https://arxiv.org/abs/2410.09309)) | `FACTR` 通过课程式随机遮挡视觉迫使策略关注力反馈（克服本体/视觉捷径病）；`ACP` 联合预测参考位姿与动态刚度矩阵 | 力感知注意力课程与学习型阻抗控制必引 |
| **#32** | ★★★★☆ | **`ForceVLA` & `ForceVLA2`** (2025.05 & 2026.03) | *ForceVLA: Enhancing VLA Models with a Force-aware MoE for Contact-rich Manipulation* ([arXiv:2505.22159](https://arxiv.org/abs/2505.22159)) & *ForceVLA2: Unleashing Hybrid Force-Position Control with Force Awareness for Contact-Rich Manipulation* ([arXiv:2603.15169](https://arxiv.org/abs/2603.15169)) | 将六维力/力矩通过 Force-Aware MoE 路由注入 VLA 动作专家，同时预测末端位姿与目标接触力 | 六维力控 VLA 代表工作 |
| **#33** | ★★★★★ | **`T-Rex`** (2026.06) | *T-Rex: Tactile-Reactive Dexterous Manipulation* ([arXiv:2606.17055](https://arxiv.org/abs/2606.17055)) | 可变速率 Mixture-of-Transformers 架构 + 时序触觉 VQ-VAE 编码器；配套 100 小时按运动原语采集的触觉数据集 | 12 项力控/柔性体任务上平均成功率比最强基线高 30% 以上；触觉反应式 VLA 的核心对照 |
| **#34** | ★★★★★ | **`SimpleTouch`** (2026.10) | *SimpleTouch: Can Vision-Language-Action Models Master Contact-Rich Manipulation Without Tactile Policy Pretraining?* ([arXiv:2610.02784](https://arxiv.org/abs/2610.02784)) | 在 $\pi_{0.5}$ 上增加触觉专家，使用冻结触觉编码器的全部 Token，以动作监督 + 多时域未来触觉潜变量预测单阶段训练 | 检验“是否必须做触觉策略预训练”的轻量强基线 |
| **#35** | ★★★★☆ | **`N0-VTLA` & `TacVLA`** (2026.03–07) | *$N_0$-VTLA: Scaling Vision-Tactile-Language-Action Model with Latent Tactile Tokens* ([arXiv:2607.23782](https://arxiv.org/abs/2607.23782)) & *TacVLA: Contact-Aware Tactile Fusion for Robust Vision-Language-Action Manipulation* ([arXiv:2603.12665](https://arxiv.org/abs/2603.12665)) | `N0-VTLA`：大规模视触觉预训练 + 预测式触觉通路 + 优势条件化离线 RL（`ALTER`）；`TacVLA`：接触感知门控，仅在检测到接触时激活触觉 Token | 视触觉 VLA 的两条代表路线（规模化预训练 vs 微调期门控融合） |
| **#36** | ★★★★☆ | **`PACE`** (CoRL 2026) | *PACE: Temporal-Role Tactile Conditioning for Chunk-Based Insertion Policies* ([arXiv:2610.16308](https://arxiv.org/abs/2610.16308)) | 把共享触觉流分成三种时间角色：持续接触状态调制动作块生成、突发接触事件修正已生成动作块、接触后果预测在训练中塑形表征 | 五项真机插装平均 90.7%；动作块策略中触觉条件化方式的直接参考 |
| **#37** | ★★★★☆ | **`FACT`** (2026.10) | *FACT: A Multimodal Force-Action-Track Foundation Model for Human-to-Robot Dexterity* ([arXiv:2610.19155](https://arxiv.org/abs/2610.19155)) | 人类触觉数据 `EgoForce` + 机器人示范联合预训练；轨迹引导粗规划器 + 力-动作联合精修器 | 力感知灵巧操作与人-机数据联合训练的代表工作 |
| **#38** | ★★★★☆ | **`Spark-0` & `PRISM`** (2026.10) | *Spark-0: Scaling Spatially Aligned Tactile Pretraining for Robot Dexterous Manipulation* ([arXiv:2610.22342](https://arxiv.org/abs/2610.22342)) & *PRISM: Precision Forcing for Generalist Vision-Language-Action Policies* ([arXiv:2610.14704](https://arxiv.org/abs/2610.14704)) | `Spark-0`：用触觉手套接触图监督视觉 Token 的空间对齐触觉预训练（1,000 小时 `HumanTouch`）；`PRISM`：针对“流时间饥饿”（Flow-Time Starvation）按精度需求重加权流匹配监督，无需新传感器 | 触觉作为预训练监督 / 精密任务监督分配的两种思路 |
| **#39** | ★★★★★ | **`UniVTAC`** (2026.02) | *UniVTAC: A Unified Simulation Platform for Visuo-Tactile Manipulation Data Generation, Learning, and Benchmarking* ([arXiv:2602.10093](https://arxiv.org/abs/2602.10093)) | 支持三种常用视触觉传感器的仿真数据合成平台，提供 `UniVTAC Encoder` 与 8 任务 `UniVTAC Benchmark` | 视触觉策略仿真评测的公开基准 |
| **#40** | ★★★★★ | **`ForceBench`** (2026.10) | *ForceBench: Benchmarking Force Integration for Robotic Manipulation* ([arXiv:2610.19604](https://arxiv.org/abs/2610.19604)) | 统一协议下评测六轴腕部力融合设计的仿真基准：8 任务、1,600 条示范、共享 $\pi_{0.5}$ 骨干上比较 1 个无力基线与 6 种融合设计 | `Prompt Fusion` 最优（仿真 35.31% vs 基线 23.25%），时序设计在装配任务上低于基线；消融表应包含无力基线与简单融合基线 |

---

### 五、模块四：实时执行、在线验证、失败恢复与双臂 DLO 必读榜（8 篇 · 核心机制与代表方法）

| 编号 | 推荐度 | 论文简称与年份 | 完整标题与 arXiv 编号 | 核心机制与关键发现 | 在验证恢复与 DLO 中的定位 |
|---|---|---|---|---|---|
| **#41** | ★★★★☆ | **`REACT` & `Chronos Policy`** (2026.10) | *REACT: Rolling Denoising and Dual Decoupling for Reactive Robot Control with VLA Models* ([arXiv:2610.12007](https://arxiv.org/abs/2610.12007)) & *Chronos Policy: Learning Robot Policies on Physical Time* ([arXiv:2610.13929](https://arxiv.org/abs/2610.13929)) | `REACT` 维护各块流时间错开的持久动作缓冲区，每个控制步用最新观测对整个视野去噪、执行最干净的块并在尾部补噪声；`Chronos Policy` 以观测采集时间与期望执行时间为条件（时间感知 RoPE） | 实时动作块执行的最新机制 |
| **#42** | ★★★★☆ | **`TacitVLA` & `ERVLA`** (2026.06–10) | *TacitVLA: Reasoning Vision-Language-Action Models Without Reasoning Latency* ([arXiv:2610.17540](https://arxiv.org/abs/2610.17540)) & *ERVLA* ([arXiv:2606.03784](https://arxiv.org/abs/2606.03784)) | `TacitVLA` 将多步显式 CoT 蒸馏至单次前向隐状态；`ERVLA` 通过双解码器解耦慢速文本推理与快速动作生成，消除推理延迟 | 零额外 Token 延迟推理代表 |
| **#43** | ★★★★★ | **`FAVOR`** (2026.10) | *Future Anchored Verification and Online Recovery for World Action Models* ([arXiv:2610.06280](https://arxiv.org/abs/2610.06280)) | 把 WAM 行动前预测的未来帧作为锚点：`Anchor Verifier` 标记破坏任务的偏离，`Anchor-Guided Recovery` 用 VLM 生成纠正指令引导 WAM 回到预期轨迹 | 面向 WAM 的验证恢复；摘要报告增益较小（LIBERO 97.85% → 98.10%） |
| **#44** | ★★★★★ | **`DiVeR`** (2026.10) | *DiVeR: Decision-Critical Verifier Learning for VLA Test-Time Scaling* ([arXiv:2610.04933](https://arxiv.org/abs/2610.04933)) | 用采样动作表征的离散度估计决策关键性，并据此重加权验证器训练（无需步级标注），提升 verifier-guided test-time scaling | 测试期“采样-验证-选优”路线的代表 |
| **#45** | ★★★★★ | **`SAFE` & `FAIL-Detect`** (2025.03–06) | *SAFE: Multitask Failure Detection for Vision-Language-Action Models* ([arXiv:2506.09937](https://arxiv.org/abs/2506.09937)) & *Can We Detect Failures Without Failure Data? Uncertainty-Aware Runtime Failure Detection for Imitation Learning Policies* ([arXiv:2503.08558](https://arxiv.org/abs/2503.08558)) | `SAFE` 从 VLA 内部特征学习单一失败概率标量并跨任务泛化（NeurIPS 2025）；`FAIL-Detect` 只用成功数据做序列 OOD 检测，并用保形预测给出统计保证（RSS 2025） | 在线失败检测的两种代表方案 |
| **#46** | ★★★★★ | **`E-TTS`** (2026.06) | *E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation* ([arXiv:2606.27268](https://arxiv.org/abs/2606.27268)) | 无需微调基座 VLA，通过多视角测试期集成、多尺度历史聚合与**基于自身置信度的自适应动作块视界截断**显著降低碰撞与失败率 | 测试期自适应视界缩短与安全缩放标杆 |
| **#47** | ★★★★★ | **`Harness VLA`** (2026.07) | *Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents* | 将冻结 VLA 封装为受控接触原语，由上层带记忆规划器与解析原语库负责语义重绑定、抓取交接与失败重试 | 双臂线束/装配中“规划器 + 冻结 VLA 原语 + 验证恢复”工程样板 |
| **#48** | ★★★★☆ | **`Bimanual DLO MPC` & `Visuomotor DLO`** (2026.02–09) | *Online Material Estimation for Conditioned Diffusion Policy in Shaping Deformable Linear Objects* ([arXiv:2609.12634](https://arxiv.org/abs/2609.12634)) & *WireCraft: A Simulation Benchmark for Industrial DLO Manipulation* ([arXiv:2606.18097](https://arxiv.org/abs/2606.18097), [arXiv:2606.04206](https://arxiv.org/abs/2606.04206)) | 结合数据驱动雅可比/状态转移模型与带防过度拉伸约束的 MPC 及视觉-运动策略，实现双臂柔性线缆高精度形状控制与绕障 | 双臂 DLO 建模与控制必引 |

---

### 六、模块五：VLM 基座、世界动作模型（WAM）与灵巧手/全身控制必读榜（7 篇 · 架构视野）

| 编号 | 推荐度 | 论文简称与年份 | 完整标题与 arXiv 编号 | 核心机制与关键发现 | 精读价值 |
|---|---|---|---|---|---|
| **#49** | ★★★★★ | **`Qwen-RobotManip` & `REKI`** (2026.06–10) | *Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models* ([arXiv:2606.17846](https://arxiv.org/abs/2606.17846)) & *REKI: Registering Knowledge in VLAs* ([arXiv:2610.22178](https://arxiv.org/abs/2610.22178)) | `Qwen-RobotManip`：基于 `Qwen-VL` 主干通过表征/运动/行为对齐整合约 38,100 小时多源预训练语料；`REKI`：2.4B VLA 配合流匹配动作专家，在专家缓存中维护持久化寄存器 Token 提供近期记忆 | `Qwen` 系 VLM 基座的代表；比较时注意预训练语料规模差异 |
| **#50** | ★★★★★ | **`π0.7`** (2026.04) | *$\pi_{0.7}$: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities* ([arXiv:2604.15483](https://arxiv.org/abs/2604.15483)) | 引入四路上文元数据协议（语言+机器人ID+任务规范+数据源质量标签）与 **14B 扩散视觉子目标生成器**，实现杂乱演示消歧与无机器人数据新技能迁移 | 多模态上下文控制与视觉子目标规划标杆 |
| **#51** | ★★★★☆ | **`GR-3` & `Gemini Robotics 1.5`** (2025.07–10) | *GR-3 Technical Report* ([arXiv:2507.15493](https://arxiv.org/abs/2507.15493)) & *Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer* ([arXiv:2510.03342](https://arxiv.org/abs/2510.03342)) | `GR-3` (字节 Seed, 4B Flow VLA) 展示图文数据+人类 VR 轨迹+真机轨迹协同训练在长程柔性衣物折叠上的泛化；`Gemini Robotics 1.5` 展示具身思考与跨本体迁移 | 工业界旗舰 VLA 技术报告代表 |
| **#52** | ★★★★★ | **`DreamZero` & `Fast-WAM`** (2026.02–03) | *World Action Models are Zero-shot Policies* ([arXiv:2602.15922](https://arxiv.org/abs/2602.15922)) & *Fast-WAM: Do World Action Models Need Test-time Future Imagination?* ([arXiv:2603.16666](https://arxiv.org/abs/2603.16666)) | `DreamZero` (14B 视频扩散 WAM) 验证联合预测未来视频与动作的物理泛化，但单步需 850 ms；`Fast-WAM` 证明训练期保留视频预测、**测试期跳过像素去噪直接解码动作可将延迟压缩至 190 ms（~5.3 FPS）且不掉点** | VLA vs WAM 范式融合必读双子星 |
| **#53** | ★★★★☆ | **`OpenWAM`、`V-JEPA 2` & `DreamGen`** (2025.05–2026.10) | *OpenWAM: An Open Framework for Composable World-Action Models* ([arXiv:2610.07922](https://arxiv.org/abs/2610.07922)), *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning* ([arXiv:2506.09985](https://arxiv.org/abs/2506.09985)) & *DreamGen: Unlocking Generalization in Robot Learning through Video World Models* ([arXiv:2505.12705](https://arxiv.org/abs/2505.12705)) | `V-JEPA 2` 在百万小时视频上学习非生成式潜空间物理预测器（免像素渲染开销）；`DreamGen` 用视频世界模型合成伪轨迹扩充策略训练；`OpenWAM` 提供全开源 WAM 基座 | 世界模型潜空间规划与合成数据代表 |
| **#54** | ★★★★☆ | **`MimicGen`、`DexMimicGen` & `DexUMI`** (CoRL 2023–2025) | *MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations* ([arXiv:2310.17596](https://arxiv.org/abs/2310.17596)), *DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning* ([arXiv:2410.24185](https://arxiv.org/abs/2410.24185)) & *DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation* ([arXiv:2505.21864](https://arxiv.org/abs/2505.21864)) | `MimicGen` 从 10–20 条人工演示自动几何变换合成数万条仿真轨迹；`DexUMI` 用外骨骼手套 + 指尖相机无机器人采集灵巧手数据 | 轨迹自动倍增与灵巧手采集核心工具 |
| **#55** | ★★★★☆ | **`HOVER`、`ASAP`、`BeyondMimic` & `SONIC`** (2024.10–2025.11) | *HOVER* ([arXiv:2410.21229](https://arxiv.org/abs/2410.21229)), *ASAP* ([arXiv:2502.01143](https://arxiv.org/abs/2502.01143)), *BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion* ([arXiv:2508.08241](https://arxiv.org/abs/2508.08241)) & *SONIC* ([arXiv:2511.07820](https://arxiv.org/abs/2511.07820)) | 现代人形机器人全身控制（WBC）标准工具箱：统一命令空间蒸馏、`Delta Action` 真实物理残差对齐、引导扩散全身追踪 | 灵巧手与人形全身控制标准栈 |

---

### 七、模块六：数据缩放律与严格统计评测方法必读榜（5 篇 · 顶会实验设计铁律）

| 编号 | 推荐度 | 论文简称与年份 | 完整标题与 arXiv 编号 | 核心定律与实验设计规范 | 为什么写论文前必须精读 |
|---|---|---|---|---|---|
| **#56** | ★★★★★ | **`The Curse of Precision`** (ICRA 2026) | *The Curse of Precision: A Data Scaling Law for High-Precision Robotic Manipulation* ([arXiv:2607.23108](https://arxiv.org/abs/2607.23108)) | 在固定成功率下，所需示范数 $N$ 随目标精度 $P$ 逼近极限 $c$ 呈超指数增长：$\log N \propto \frac{1}{P-c}$；$c$ 是整个系统（传感器、专家策略等）的涌现属性 | 为“提升系统组件（如加腕部相机、更好的专家）以降低 $c$”提供定量依据 |
| **#57** | ★★★★☆ | **`Data Scaling Laws` & `AgiBot World`** (ICLR 2025 / 2025.03) | *Data Scaling Laws in Imitation Learning for Robotic Manipulation* ([arXiv:2410.18647](https://arxiv.org/abs/2410.18647)) & *AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems* ([arXiv:2503.06669](https://arxiv.org/abs/2503.06669)) | 证明跨场景泛化误差关于“环境数 $\times$ 物体数”呈幂律下降，而单场景重复采集超过 50–100 条即饱和；提供百万级真机双臂数据集 | 指导真机数据采集预算分配 |
| **#58** | ★★★★★ | **`RoboArena`** (2025.06) | *RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies* ([arXiv:2506.18123](https://arxiv.org/abs/2506.18123)) | 建立多高校分布式真机双盲随机 A/B 对战评测与 Bradley-Terry Elo 排名体系，消除评测者主观摆位偏置 | 顶会真机盲测与公平对比标杆 |
| **#59** | ★★★★★ | **`TRI LBM Evaluation`** (2025.07) | *A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation* ([arXiv:2507.05331](https://arxiv.org/abs/2507.05331)) | 丰田研究院示范如何用大规模试验次数、分布内/分布外严格切分、配对置信区间与细粒度失败阶段归因检验大型行为模型 | 实验章节图表与统计显著性写作范本 |
| **#60** | ★★★★★ | **`Kress-Gazit Best Practices`** (2024.09) | *Robot Learning as an Empirical Science: Best Practices for Policy Evaluation* ([arXiv:2409.09491](https://arxiv.org/abs/2409.09491)) | 机器人学习实验设计红宝书：系统规定初始状态分布记录、成败判据、安全中断计数、盲测交错与置信区间报告准则 | 投稿 RSS / CoRL / ICRA / TRO 前必查的自检清单 |
