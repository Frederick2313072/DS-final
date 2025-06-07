# 透视全球数学教育的棱镜：基于IMO六十年数据的探索性分析

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data Source](https://img.shields.io/badge/Data-TidyTuesday-purple.svg)](https://tidytues.day)

> **摘要：** 本研究运用探索性数据分析方法，对1959年至2024年间覆盖157个国家和地区的21,707条IMO参赛记录进行了系统性、多维度的定量分析，揭示全球数学教育的发展趋势、竞争格局演变和地区间差异。

## 📋 目录

- [项目概览](#-项目概览)
- [主要发现](#-主要发现)
- [数据集描述](#-数据集描述)
- [项目结构](#-项目结构)
- [环境配置](#-环境配置)
- [快速开始](#-快速开始)
- [分析流程](#-分析流程)
- [可视化结果](#-可视化结果)
- [研究方法](#-研究方法)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)
- [致谢](#-致谢)

## 🎯 项目概览

国际数学奥林匹克竞赛（IMO）作为全球最具声望的中学数学竞赛，为评估和比较各国数学教育水平提供了独特的视角。本项目通过数据科学方法对IMO历史数据进行深入分析，探索全球数学教育的演变规律。

### 研究目标

1. **描绘全球参与格局**：分析IMO参赛国家、地区和人数的历史演变
2. **评估国家竞争力**：建立多维度评价体系，识别数学教育的领先者
3. **解析题目设计哲学**：研究6道题目的难度分布和区分度特征
4. **探索地区教育差异**：揭示全球数学教育发展的不平衡现象

## 🔍 主要发现

### 🌏 全球竞争格局
- **亚洲崛起**：中国、韩国等东亚国家在近三十年表现突出
- **多极竞争**：美国、俄罗斯等传统强国维持领先地位
- **动态演化**：从欧洲主导到全球多极化竞争的转变

### 📊 题目设计规律
- **位置效应显著**：P1/P4作为"入门题"，P3/P6为"挑战题"
- **科学分层**：遵循"入口-区分-挑战"的三层难度模式
- **稳定评价**：相对比例制保证了跨年度评价的一致性

### 🌍 地区发展差异
- **参与广度**：欧洲参与度最高，体现深厚数学传统
- **表现优异**：大洋洲平均分领先，亚洲整体上升趋势明显
- **发展挑战**：非洲和南美洲在参与度和表现上相对落后

## 📊 数据集描述

### 数据来源
- **原始数据**：[TidyTuesday IMO Dataset](https://tidytues.day)
- **时间跨度**：1959-2024年（65年历史数据）
- **覆盖范围**：157个国家和地区，21,707条参赛记录

### 数据字段
| 字段 | 描述 | 类型 |
|------|------|------|
| `year` | 比赛年份 | int |
| `contestant` | 参赛者姓名 | string |
| `country` | 参赛者国家 | string |
| `p1-p6` | 各题得分(0-7分) | int |
| `total` | 总分(0-42分) | int |
| `individual_rank` | 个人排名 | int |
| `award` | 奖项等级 | string |

## 📁 项目结构

```
DS-final/
├── data/                           # 数据文件
├── fig/                           # 生成的图表
├── src/                           # 源代码
├── style/                         # LaTeX样式文件
├── notebooks/                     # Jupyter分析笔记本
│   ├── 0_data_preprocessing.ipynb # 数据预处理
│   ├── 1_country_performance.ipynb # 国家表现分析
│   ├── 2_award_analysis.ipynb     # 奖项分布分析
│   ├── 3_problem_difficulty.ipynb # 题目难度分析
│   └── 4_country_trends.ipynb     # 国家趋势分析
├── main.tex                       # 研究报告
├── requirements.txt               # Python依赖
└── README.md                      # 项目说明
```

## 🛠 环境配置

### 系统要求
- **操作系统**：Linux/macOS/Windows
- **Python版本**：3.12+
- **内存**：建议8GB以上

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/Frederick2313072/DS-final.git
cd DS-final

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 核心依赖包
```
pandas>=2.0.0          # 数据处理
numpy>=1.24.0          # 数值计算
matplotlib>=3.7.0      # 基础绘图
seaborn>=0.12.0        # 统计可视化
jupyter>=1.0.0         # 交互式分析
scikit-learn>=1.3.0    # 机器学习
```

## 🚀 快速开始

### 1. 数据预处理
```bash
jupyter notebook 0_data_preprocessing.ipynb
```

### 2. 运行分析
```bash
# 按顺序执行分析笔记本
jupyter notebook 1_country_performance.ipynb
jupyter notebook 2_award_analysis.ipynb
jupyter notebook 3_problem_difficulty.ipynb
jupyter notebook 4_country_trends.ipynb
```

### 3. 生成报告
```bash
# 编译LaTeX报告（需要XeLaTeX环境）
xelatex main.tex
```

## 📈 分析流程

### 阶段一：数据预处理
- **数据清洗**：处理缺失值和异常值
- **标准化**：统一国家名称和地区分类
- **特征工程**：创建地区标签和衍生指标
- **数据验证**：确保数据完整性和一致性

### 阶段二：探索性分析
- **描述统计**：总体数据概览和分布特征
- **相关性分析**：各题得分间的关联关系
- **异常检测**：识别数据中的特殊模式

### 阶段三：多维度分析
- **国家表现**：排名、得分、奖牌数等指标
- **题目难度**：各题得分分布和区分度
- **奖项分布**：评奖标准和比例稳定性
- **地区比较**：洲际间的教育发展差异

### 阶段四：可视化展示
- **趋势图**：时间序列变化趋势
- **对比图**：国家和地区间横向对比
- **分布图**：得分、奖项等数据分布
- **热力图**：相关性和模式识别

## 🎨 可视化结果

### 核心图表

1. **数据概览图** (`fig/data_overview.png`)
   - 年度参赛趋势、总分分布特征
   - 奖项构成比例、各题平均得分

2. **国家表现分析图** (`fig/country_analysis.png`)
   - 平均分排名前15、金牌总数排名前15
   - 总分与排名关系、顶尖国家历年趋势

3. **题目难度分析图** (`fig/problem_difficulty.png`)
   - 各题得分分布（小提琴图）
   - 零分率与满分率对比、难度历年变化趋势

4. **奖项分析图** (`fig/award_analysis.png`)
   - 各奖项人数占比、获奖人数历年变化
   - 不同奖项在各题表现、分数线历年趋势

5. **地区分析图** (`fig/regional_analysis.png`)
   - 各地区参与人数、地区平均分对比
   - 奖牌分布情况、地区表现历年趋势

## 🔬 研究方法

### 数据科学方法论
- **探索性数据分析（EDA）**：Tukey的数据探索哲学
- **数据可视化**：遵循图形语法原则
- **统计建模**：描述性统计和相关性分析

### 技术栈
- **数据处理**：Pandas + NumPy
- **可视化**：Matplotlib + Seaborn
- **开发环境**：Jupyter Notebook
- **文档生成**：LaTeX + XeLaTeX

### 质量保证
- **数据验证**：交叉验证数据源准确性
- **可重现性**：完整记录分析流程
- **代码规范**：遵循PEP 8编码标准

## 🤝 贡献指南

欢迎贡献代码、提出问题或建议！请遵循以下流程：

1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 **Pull Request**

### 贡献方向
- 🐛 **Bug修复**：报告或修复发现的问题
- 📊 **新分析**：添加新的分析维度或方法
- 🎨 **可视化优化**：改进图表设计和信息传达
- 📖 **文档完善**：补充或改进项目文档
- 🧪 **测试用例**：添加测试确保代码质量

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

### 数据来源
- **TidyTuesday社区**：提供高质量的IMO数据集
- **IMO官方组织**：维护竞赛历史记录

### 技术支持
- **开源社区**：Python数据科学生态系统
- **学术机构**：南开大学提供研究环境

---

## 📞 联系方式

- **作者**：徐媛
- **学号**：2313072
- **机构**：南开大学
- **项目主页**：https://github.com/Frederick2313072/DS-final

---

<div align="center">

**如果本项目对您有帮助，请考虑给个 ⭐ Star！**

*透过数据看世界，用科学解教育*

</div>
