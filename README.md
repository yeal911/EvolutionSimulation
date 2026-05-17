# Evolution Simulation / 进化模拟器

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PySide2](https://img.shields.io/badge/PySide2-GUI-green.svg)](https://wiki.qt.io/Qt_for_Python)
[![pyqtgraph](https://img.shields.io/badge/pyqtgraph-Real--time%20Plotting-orange.svg)](http://www.pyqtgraph.org/)

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

### Overview

Evolution Simulation is a Python-based multi-threaded ecosystem simulator inspired by evolutionary biology and **Richard Dawkins' *The Selfish Gene***. It models a four-tier food chain — **Plants → Sheep → Wolves → Tigers** — running on a 500×500 grid world. Each individual carries a 10-digit gene that controls traits such as lifespan, fighting capability, attack/defense tendency, breeding times, running speed, **camouflage, greenbeard badge, attractiveness, and territory/nest tendency**. Through inheritance, mutation, natural selection, and spatial competition, populations evolve over time.

### Features

- **Gene Inheritance & Mutation**
  - Each individual has a 10-digit gene (0~99 per digit).
  - Parents mutate before recombination; offspring have a 10% chance of additional mutation.
  - **10 traits** are mapped from genes: lifespan, fight capability, attack tendency, defense tendency, breeding times, speed, **camouflage, greenbeard badge, attractiveness, territory/nest tendency**.

- **Multi-Species Food Chain**
  - **Plants**: Producers, replenished each cycle (affected by environmental harshness).
  - **Sheep**: Herbivores, feed on plants.
  - **Wolves**: Carnivores, hunt sheep and occasionally wolves.
  - **Tigers**: Apex predators, hunt sheep and wolves.

- **Survival Pressure Mechanisms**
  - **Hunger**: Increases each cycle; starves after exceeding threshold.
  - **Aging**: Natural death when age exceeds gene-determined lifespan.
  - **Combat**: Predator-prey encounters resolved by fight capability; the weaker may flee based on speed and distance.
  - **Breeding Constraints**: Gender, age window, maximum breeding limits, **female mate choice (sexual selection)**.

- **10 New Evolutionary Mechanisms** (see detailed list below)

- **Real-Time Visualization** (10 enhanced views)
  - Built with **PySide2 + pyqtgraph**.
  - Live population count curves.
  - Birth/death statistics per cycle.
  - Gene attribute trends per species.
  - **2D world map, density heatmap, gene histograms, food web, pedigree tree, strategy matrix, 3D fitness landscape, event log**.

- **Data Export**
  - Export cycle summaries and individual life histories to Excel (`.xls`).

### Architecture

```
EvolutionSimulation/
├── src/
│   ├── gene/
│   │   └── Gene.py              # Gene definition & mutation + similarity (kin selection)
│   ├── population/
│   │   ├── Population.py        # Abstract base: fight, breed, PD game, mate choice
│   │   ├── Plant.py             # Plant species
│   │   ├── Sheep.py             # Sheep species (new traits)
│   │   ├── Wolf.py              # Wolf species (new traits)
│   │   └── Tiger.py             # Tiger species (new traits)
│   ├── thread/
│   │   ├── PopulationThread.py  # Core evolution loop + all new mechanisms
│   │   ├── PlantThread.py
│   │   ├── SheepThread.py
│   │   ├── WolfThread.py
│   │   └── TigerThread.py
│   ├── dreamland/
│   │   └── Dreamland.py         # 500×500 world grid + terrain + rich slots + environment
│   ├── tool/
│   │   ├── CycleInfo.py         # Per-cycle statistics (expanded)
│   │   └── Recorder.py          # Data logging & Excel export (expanded)
│   ├── event/
│   │   └── EventLogger.py       # Global event log singleton
│   ├── nest/
│   │   └── Nest.py              # Nest object (extended phenotype)
│   ├── parasite/
│   │   └── Parasite.py          # Parasite object
│   ├── visualization/
│   │   ├── WorldMapView.py      # 2D spatial map with terrain & trails
│   │   ├── HeatmapWidget.py     # Population density heatmap
│   │   ├── GeneHistogram.py     # Gene frequency distribution
│   │   ├── FoodWebGraph.py      # Food web network graph
│   │   ├── PhylogenyGraph.py    # Pedigree tree
│   │   ├── StrategyMatrix.py    # PD strategy payoff matrix
│   │   ├── FitnessLandscape3D.py # 3D fitness landscape
│   │   └── EventLogWidget.py    # Real-time event log with filtering
│   ├── main/
│   │   ├── main.py              # GUI entry (PySide2) with all tabs
│   │   ├── main1.py             # Matplotlib test script
│   │   └── test.py              # CLI test entry
│   └── ui/
│       └── main.ui              # Qt Designer UI file
└── README.md
```

### Quick Start

#### Requirements

```bash
pip install PySide2 pyqtgraph openpyxl xlwt numpy PyOpenGL
```

#### Run GUI

```bash
python EvolutionSimulation/src/main/main.py
```

#### Run CLI Test

```bash
python EvolutionSimulation/src/main/test.py
```

---

## 10 Evolutionary Mechanisms Implemented

| # | Mechanism | Implementation |
|---|-----------|----------------|
| 1 | **Kin Selection / Hamilton's Rule** | `Gene.similarity()` computes genetic distance. In `Population.fight()`, if similarity ≥ 0.7, animals spare kin. |
| 2 | **Reciprocal Altruism / Prisoner's Dilemma** | `Population.play_pd_game()` implements PD with 4 strategies: Always Cooperate, Always Defect, Tit-for-Tat, Random. Reputation tracking. |
| 3 | **Evolutionarily Stable Strategy (ESS)** | The 4 PD strategies compete within each species. Strategy frequencies shift over cycles. |
| 4 | **Sexual Selection / Mate Choice** | Females evaluate males via `_evaluate_mate()` using `attractiveness * 0.6 + fightCapability * 0.4`. Rejections are logged. |
| 5 | **r/K Selection Theory** | `Dreamland.updateEnvironment()` cycles through stable/mild/harsh/recovering phases. Plant growth adjusts. High-breeders vs high-quality offspring trade-off emerges. |
| 6 | **Mimicry & Camouflage** | `camouflage` gene (digit 6). Prey with high camouflage have reduced detection probability in `searchFood()`. |
| 7 | **Parasitism** | `Parasite` class attaches to hosts, drains hunger each cycle. Hosts clear parasites based on immune proxy (`gene[3]`). |
| 8 | **Territorial Behavior** | `territoryTendency` gene (digit 9). Animals defend `richSlots` (gold-bordered on map), driving away intruders. |
| 9 | **Greenbeard Effect** | `greenbeardBadge` gene (digit 7 // 10). Animals with matching badges avoid fighting. Direct demonstration of gene → marker + behavior. |
| 10 | **Extended Phenotype** | `Nest` class. High `territoryTendency` animals build nests providing breeding/defense bonuses. Nests persist after death. |

---

## 10 Visualization Enhancements Implemented

| # | Enhancement | File | Description |
|---|-------------|------|-------------|
| 1 | **2D Spatial World Map** | `WorldMapView.py` | Real-time rendering of 500×500 grid. Terrain colors, rich slots (gold border), individuals as colored dots (size = fight capability, opacity = age), nest markers (brown), movement trails. |
| 2 | **Population Density Heatmap** | `HeatmapWidget.py` | 50×50 grid heatmap showing overcrowded/barren regions. |
| 3 | **Gene Frequency Distribution** | `GeneHistogram.py` | 10 histograms (one per gene digit) showing population distribution per cycle. |
| 4 | **Pedigree Tree** | `PhylogenyGraph.py` | Traces the highest-generation individual and its parents. |
| 5 | **Food Web Network Graph** | `FoodWebGraph.py` | Nodes = species; edge thickness = predation count. Animated over time. |
| 6 | **Individual Movement Trails** | `WorldMapView.py` | Faint trajectory lines rendered from `moveHistory` on the world map. |
| 7 | **Fitness Landscape 3D** | `FitnessLandscape3D.py` | X/Y = gene dimensions 0 & 1; Z = fitness proxy (lifespan + fightCapability). Requires `PyOpenGL`. |
| 8 | **Strategy Coexistence Matrix** | `StrategyMatrix.py` | 4×4 payoff heatmap for PD strategies. Shows which strategies dominate. |
| 9 | **Real-Time Event Log** | `EventLogWidget.py` | `QListWidget` with color-coded events: Fight (red), Breed (green), Altruism (blue), SexualSelection (pink), Nest (brown), Territory (yellow), Parasite (purple), PD (teal). Filter by type. |
| 10 | **Export Animation** | `Recorder.py` + data | All data exported to Excel. Use `matplotlib.animation` or `imageio` externally to generate time-lapse GIFs from exported data. |

### New Gene Curves in Original UI
- **Camouflage** (red-pink)
- **Attractiveness** (yellow-orange)
- **Territory Tendency** (green)

Added to Tiger/Wolf/Sheep gene tabs alongside original 7 curves.

---

<a name="chinese"></a>
## 中文

### 项目概述

进化模拟器是一个基于 Python 的多线程生态系统模拟器，灵感来源于进化生物学和 **理查德·道金斯的《自私的基因》**。它在 500×500 的网格世界中模拟了一条四级食物链：**植物 → 羊 → 狼 → 虎**。每个个体携带一个 10 位基因，控制寿命、战斗力、攻击/防御倾向、繁殖次数、奔跑速度、**保护色、绿胡子徽章、吸引力、领地/筑巢倾向**等性状。通过遗传、变异、自然选择和空间竞争，种群随时间不断演化。

### 功能特性

- **基因遗传与变异**
  - 每个个体拥有 10 位基因（每位 0~99）。
  - 繁殖前父母各自先变异，子代重组后有 10% 概率再次变异。
  - 基因映射**十大性状**：寿命、战斗力、攻击倾向、防御倾向、繁殖次数、速度、**保护色、绿胡子徽章、吸引力、领地/筑巢倾向**。

- **多物种食物链生态**
  - **植物**：生产者，受环境严酷度影响每周期补充量。
  - **羊**：食草动物，以植物为食。
  - **狼**：食肉动物，捕食羊和狼。
  - **虎**：顶级掠食者，捕食羊和狼。

- **生存压力机制**
  - **饥饿度**：每周期递增，超过阈值饿死。
  - **寿命**：超过基因决定的寿命后自然死亡。
  - **战斗**：捕食者与猎物相遇，按战斗力决胜负；弱势方可尝试逃跑。
  - **繁殖限制**：受性别、年龄段、最大繁殖次数约束，**雌性拥有择偶权（性选择）**。

- **10 种全新进化机制**（详见下方列表）

- **实时可视化**（10 项增强）
  - 基于 **PySide2 + pyqtgraph** 构建。
  - 实时种群数量曲线、出生/死亡统计、基因属性趋势。
  - **2D 世界地图、密度热力图、基因直方图、食物网、系谱树、策略矩阵、3D 适应度景观、事件日志**。

- **数据导出**
  - 支持导出周期汇总和个体全生命周期数据到 Excel（`.xls`），包含所有新属性。

### 项目架构

```
EvolutionSimulation/
├── src/
│   ├── gene/
│   │   └── Gene.py              # 基因定义与变异 + 相似度计算（亲缘选择）
│   ├── population/
│   │   ├── Population.py        # 抽象基类：战斗、繁殖、囚徒博弈、择偶
│   │   ├── Plant.py             # 植物
│   │   ├── Sheep.py             # 羊（新性状）
│   │   ├── Wolf.py              # 狼（新性状）
│   │   └── Tiger.py             # 虎（新性状）
│   ├── thread/
│   │   ├── PopulationThread.py  # 核心演化循环 + 全部新机制
│   │   ├── PlantThread.py
│   │   ├── SheepThread.py
│   │   ├── WolfThread.py
│   │   └── TigerThread.py
│   ├── dreamland/
│   │   └── Dreamland.py         # 500×500 世界地图 + 地形 + 富饶区 + 环境波动
│   ├── tool/
│   │   ├── CycleInfo.py         # 周期统计（扩展）
│   │   └── Recorder.py          # 数据记录与 Excel 导出（扩展）
│   ├── event/
│   │   └── EventLogger.py       # 全局事件日志单例
│   ├── nest/
│   │   └── Nest.py              # 巢穴对象（延伸表现型）
│   ├── parasite/
│   │   └── Parasite.py          # 寄生物对象
│   ├── visualization/
│   │   ├── WorldMapView.py      # 2D 空间地图（含地形与轨迹）
│   │   ├── HeatmapWidget.py     # 种群密度热力图
│   │   ├── GeneHistogram.py     # 基因频率分布直方图
│   │   ├── FoodWebGraph.py      # 食物网网络图
│   │   ├── PhylogenyGraph.py    # 系谱树
│   │   ├── StrategyMatrix.py    # 囚徒困境策略收益矩阵
│   │   ├── FitnessLandscape3D.py # 3D 适应度景观
│   │   └── EventLogWidget.py    # 实时事件日志（带过滤）
│   ├── main/
│   │   ├── main.py              # GUI 入口（集成全部标签页）
│   │   ├── main1.py             # Matplotlib 测试脚本
│   │   └── test.py              # 命令行测试入口
│   └── ui/
│       └── main.ui              # Qt Designer UI 文件
└── README.md
```

### 快速开始

#### 环境依赖

```bash
pip install PySide2 pyqtgraph openpyxl xlwt numpy PyOpenGL
```

#### 启动 GUI

```bash
python EvolutionSimulation/src/main/main.py
```

#### 启动命令行测试

```bash
python EvolutionSimulation/src/main/test.py
```

---

## 已实现的 10 种进化机制

| 编号 | 机制 | 实现方式 |
|:---:|:---|:---|
| 1 | **亲缘选择 / 汉密尔顿法则** | `Gene.similarity()` 计算基因距离。`Population.fight()` 中相似度 ≥ 0.7 时放过同类。 |
| 2 | **互惠利他 / 迭代囚徒困境** | `Population.play_pd_game()` 实现囚徒博弈，四种策略：永远合作、永远背叛、以牙还牙、随机。追踪声誉。 |
| 3 | **进化稳定策略 (ESS)** | 四种 PD 策略在种群内竞争，策略频率随周期变化。 |
| 4 | **性选择 / 配偶选择** | 雌性通过 `_evaluate_mate()` 评估雄性，公式：`吸引力×0.6 + 战斗力×0.4`。拒绝事件被记录。 |
| 5 | **r/K 选择理论** | `Dreamland.updateEnvironment()` 循环四种环境相位（稳定/轻度/严酷/恢复），植物生长量随之调整。 |
| 6 | **拟态与保护色** | 保护色基因（第6位）。高保护色猎物在 `searchFood()` 中降低被捕食概率。 |
| 7 | **寄生** | `Parasite` 类附着宿主，每周期吸取饥饿值。宿主依据免疫代理（`gene[3]`）清除寄生虫。 |
| 8 | **领地行为** | 领地倾向基因（第9位）。高倾向个体守卫 `richSlots`（地图金色边框），驱赶入侵者。 |
| 9 | **绿胡子效应** | 绿胡子徽章基因（第7位 // 10）。相同徽章的个体避免战斗。直接展示基因→标记+行为。 |
| 10 | **延伸的表现型** | `Nest` 类。高领地倾向动物消耗饥饿值筑巢，提供繁殖/防御加成。巢穴在个体死后仍然存在。 |

---

## 已实现的 10 项可视化增强

| 编号 | 增强项 | 文件 | 说明 |
|:---:|:---|:---|:---|
| 1 | **2D 空间世界地图** | `WorldMapView.py` | 实时渲染 500×500 网格。地形着色、富饶区金色边框、个体用彩色圆点表示（大小=战斗力，透明度=年龄）、巢穴标记（棕色）、移动轨迹线。 |
| 2 | **种群密度热力图** | `HeatmapWidget.py` | 50×50 网格热力图，显示拥挤/荒芜区域。 |
| 3 | **基因频率分布图** | `GeneHistogram.py` | 10 个直方图（每个基因位一个），展示种群分布。 |
| 4 | **系谱 / 进化树** | `PhylogenyGraph.py` | 追溯代数最高的个体及其父母。 |
| 5 | **食物网网络图** | `FoodWebGraph.py` | 节点=物种；边粗细=捕食次数。随时间动画变化。 |
| 6 | **个体移动轨迹** | `WorldMapView.py` | 利用 `moveHistory` 在地图上渲染淡色轨迹。 |
| 7 | **适应度景观 3D 图** | `FitnessLandscape3D.py` | X/Y = 基因维度 0 & 1；Z = 适应度代理（寿命+战斗力）。需要 `PyOpenGL`。 |
| 8 | **策略共存矩阵** | `StrategyMatrix.py` | 4×4 收益热力图，展示哪种 PD 策略占优。 |
| 9 | **实时事件日志** | `EventLogWidget.py` | `QListWidget` 彩色编码事件：战斗(红)、繁殖(绿)、利他(蓝)、性选择(粉)、筑巢(棕)、领地(黄)、寄生(紫)、囚徒博弈(青)。支持按类型过滤。 |
| 10 | **导出动画** | `Recorder.py` + 数据 | 所有数据导出到 Excel。可外部使用 `matplotlib.animation` 或 `imageio` 生成时间轴 GIF。 |

### 原始 UI 新增基因曲线
- **保护色**（红粉色）
- **吸引力**（黄橙色）
- **领地倾向**（绿色）

已添加到虎/狼/羊的基因标签页中，与原有 7 条曲线并列显示。

---

## License

MIT License — feel free to extend, simulate, and evolve! 🧬
