#!/usr/bin/env python3
"""Idempotently strengthen the teaching organization of chapters 6--8.

The script keeps every original cell (including its id, outputs, execution count,
and student answer areas), inserts teaching/navigation cells, and applies only the
small set of source corrections requested for the return-probability-risk chain.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REVISION = "course-org-2026-07-ch06-08-v1"


def lines(text: str) -> list[str]:
    text = text.strip() + "\n"
    return text.splitlines(keepends=True)


def generated_id(marker: str) -> str:
    return hashlib.sha1(f"{REVISION}:{marker}".encode("utf-8")).hexdigest()[:12]


def markdown_cell(marker: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "id": generated_id(marker),
        "metadata": {"course_org_revision": REVISION, "course_org_marker": marker},
        "source": lines(source),
    }


def code_cell(marker: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": generated_id(marker),
        "metadata": {"course_org_revision": REVISION, "course_org_marker": marker},
        "outputs": [],
        "source": lines(source),
    }


def task_card(
    marker: str,
    prerequisite: str,
    question: str,
    prediction: str,
    hint: str,
    boundary: str,
    title: str = "本节任务卡",
) -> dict[str, Any]:
    return markdown_cell(
        marker,
        f"""
### {title}

- **前置检索**：{prerequisite}
- **核心问题**：{question}
- **先预测，后运行**：{prediction}
- **手算 / Python提示**：{hint}
- **解释边界**：{boundary}
""",
    )


NAVIGATION: dict[str, str] = {
    "06_收益率与财富路径.ipynb": r"""
### 本章导航：从一列价格到一条财富路径

小林在第5章完成了价格、股息与日期的数据清洗。现在他必须回答：**10,000元究竟变成了多少，这个结果使用了哪一种收益口径，追加资金以后还能不能用同一种方法解释？**

学习路径：`一期比例变化 → 总回报与连乘 → 对数记账 → 长期增长 → 年化 → 外部现金流 → 可测试函数`

| 主线 | 本章推进 |
|---|---|
| 金融概念线 | 区分价格收益、总回报、资产表现与个人财富结果 |
| 数学模型线 | 从比率和连乘走到对数、几何平均与递推 |
| Python能力线 | 从逐期计算走到`shift`、`pct_change`、`cumprod`与函数测试 |

- **本章产出**：一张带口径、频率、现金流假设和边界检查的收益—财富审计卡。
- **下章用途**：本章只描述已经发生的一条路径；第7章将追问未来有哪些可能结果以及如何表达它们的权重。

![无文字概念图：价格变化、股息和追加资金汇成不同财富路径](assets/course/06_returns_wealth.png)

**读图说明**：先沿金色财富筹码的时间方向观察，再分别寻找价格涨跌、股息流入和外部追加三种变化来源。图中路径表示计算关系，不表示真实收益承诺。
""",
    "07_概率分布与抽样.ipynb": r"""
### 本章导航：从一条历史路径到许多可能结果

第6章告诉小林“过去发生了什么”，却没有告诉他未来会出现哪一种收益。小林将用三张情景卡建立一个**明确标注假设**的随机模型，再观察有限样本为什么会偏离模型中心。

学习路径：`结果 → 事件 → 随机变量 → 概率 → 总体与样本 → 模拟 → 稳定性 → 尾部 → 抽样分布`

| 主线 | 本章推进 |
|---|---|
| 金融概念线 | 把不确定性拆成情景、损失事件与尾部事件 |
| 数学模型线 | 从加权平均走到方差、分位数、大数定律和中心极限定理 |
| Python能力线 | 使用可复现随机生成器、布尔统计、重复抽样与经验分布 |

- **本章产出**：一份把模型假设、理论量、一次样本和模拟误差分开的随机实验报告。
- **下章用途**：第8章将使用本章的标准差、分位数和尾部样本构造多种风险观察窗口。

![无文字概念图：从情景容器反复抽样并形成分布](assets/course/07_probability_sampling.png)

**读图说明**：从左到右区分“装有固定权重的模型容器”“一次有限抽样”和“许多次抽样形成的整体形状”。颜色多少是教学假设，不是市场概率预测。
""",
    "08_风险度量与压力测试.ipynb": r"""
### 本章导航：用多副镜头观察同一组损失

小林已经能描述收益分布，但“风险多大”仍不是一个单一问题。本章用起伏、从峰值下跌、尾部阈值、极端情景和资本存续五副镜头检查同一组收益。

学习路径：`离散程度 → 财富路径与回撤 → 尾部阈值与严重度 → 模型比较 → 时间变化 → 压力情景 → 杠杆存续`

| 主线 | 本章推进 |
|---|---|
| 金融概念线 | 区分日常波动、路径损失、尾部损失、情景脆弱性与生存风险 |
| 数学模型线 | 使用标准差、路径极值、分位数、条件平均和分段边界 |
| Python能力线 | 构造滚动指标、历史尾部、自定义风险函数和边界测试 |

- **本章产出**：一份每个指标都说明对象、期限、单位、假设与遗漏风险的资产风险体检。
- **下章用途**：单项资产风险仍没有回答资产之间如何共同变化；第9章将进入相关性与分散化。

![无文字概念图：波动、回撤、尾部、冲击与杠杆五种风险视角](assets/course/08_risk_lenses.png)

**读图说明**：不要寻找“唯一最危险”的区域；依次观察围绕中心的摆动、从峰顶到谷底的落差、被隔离的红色尾部、外部冲击以及杠杆后的资本耗尽。
""",
}


TASKS: dict[str, dict[str, dict[str, str]]] = {
    "06_收益率与财富路径.ipynb": {
        "## AI学习状态": {
            "title": "章前定位任务卡",
            "prerequisite": "不看前文，写出简单收益率需要哪两个价格；回忆第5章为什么必须先排序日期并核实复权。",
            "question": "本章的每个收益数字需要附带哪些口径信息，才不会被误读？",
            "prediction": "先列出你认为最终报告至少要写明的三项信息，再与章末审计卡比较。",
            "hint": "用100→110→99作为全章手算锚点；代码中始终保留日期索引和原始列。",
            "boundary": "本章讨论已实现路径的计算，不把历史年化结果当作未来预测。",
        },
        "## 6.1 简单收益率": {
            "prerequisite": "回忆第1章收益率是相对哪一个基数计算的；确认价格已经按时间升序排列。",
            "question": "为什么100→110→99的两期百分比相加为0，终值却不是100？",
            "prediction": "先手算第二期收益的分母，并在运行代码前写下最终累计收益。",
            "hint": "先写`prices[i] / prices[i-1] - 1`，再对照`shift()`与`pct_change()`；第一行没有前一期，因此是`NaN`而不是0。",
            "boundary": "简单收益无单位，但必须写起止时点；`pct_change()`不会检查复权，也不会自动加入股息。",
        },
        "## 6.2 总回报与累计财富": {
            "prerequisite": "回忆第1—2章现金流正负号，并说明股息为什么也是投资者收到的现金流。",
            "question": "价格几乎没变但收到股息时，价格收益和投资者总回报为什么不同？",
            "prediction": "手算100买入、期末仍为100、收到2元股息时的两种收益率。",
            "hint": "逐列建立价格收益、总回报和两条财富路径；`cumprod()`对应逐期乘以`1 + R`。",
            "boundary": "当前总回报模型假设股息按教学时点再投资，暂不含税费、滑点和真实除息细节。",
        },
        "## 6.3 对数收益率": {
            "prerequisite": "回忆高等数学中对数把乘法变成加法，以及指数函数如何把结果变回原尺度。",
            "question": "为什么跨期对数收益可以相加，而简单收益通常需要连乘？",
            "prediction": "判断+10%与−10%的对数收益绝对值是否相等，并预测两者之和的正负。",
            "hint": "优先使用`np.log1p(R)`和`np.expm1(sum_r)`；输入必须满足`R > -1`。",
            "boundary": "对数收益只是记账与建模变换，不创造额外收益；其和不能直接当成简单累计百分比报告。",
        },
        "## 6.4 算术平均不等于长期增长率": {
            "prerequisite": "回忆累计财富依赖`(1+R_1)(1+R_2)`，以及几何平均要复现相同终值。",
            "question": "两期算术平均固定时，收益差距扩大为什么会降低等效复合增长？",
            "prediction": "比较`[5%, 5%]`与`[50%, -40%]`的100元终值，运行前判断哪条路径的几何平均更低。",
            "hint": "令两期收益为`m-d`与`m+d`，直接计算精确式`sqrt((1+m-d)*(1+m+d))-1`。",
            "boundary": "这是一个确定性的两期复合实验；此处不引入随机分布，也不据此预测未来风险。",
        },
        "## 6.5 年化必须说明频率和样本长度": {
            "prerequisite": "回忆几何平均和复合增长，并区分月、年这两个时间单位。",
            "question": "把三个月的增长换算成年等效尺度，为什么不等于预测未来一年？",
            "prediction": "先比较“月均收益×12”和逐月连乘的大小，再判断两天赚1%机械年化是否可信。",
            "hint": "函数参数显式命名`n_periods`和`periods_per_year`，输出同时打印样本长度与频率。",
            "boundary": "年化是尺度换算；必须连同样本区间、频率、现金流和费用口径报告。",
        },
        "## 6.6 定投引入现金流，不能只看资产收益率": {
            "prerequisite": "回忆第2章现金流时点，并写出“先增长、后追加”的一期财富递推。",
            "question": "相同三个收益数字改变顺序后，为什么有外部追加资金的终值会改变？",
            "prediction": "比较`[-30%,40%,10%]`与`[10%,40%,-30%]`，指出每笔新增资金随后经历了哪些收益。",
            "hint": "保留普通循环并逐期打印`增长前财富、收益、追加额、期末财富`；再把追加时点改为期初做变式。",
            "boundary": "下跌并非天然有利；结论还依赖后续恢复、持续现金流、费用以及资本是否已经耗尽。",
        },
        "## 6.7 编程练习：累计财富": {
            "prerequisite": "回忆第0章函数输入输出与第6.2节财富连乘。",
            "question": "怎样把收益定义和破产边界写进一个可测试函数？",
            "prediction": "先决定空收益列表、收益等于−100%、含非有限值时函数应返回还是报错。",
            "hint": "A级补一轮递推，B级完成整个函数，C级验证一维、有限值、`return > -1`且不修改输入。",
            "boundary": "测试通过只证明实现符合已写规则，不证明输入数据可靠或历史表现可持续。",
        },
        "## 本章总结与小项目": {
            "title": "章末整合任务卡",
            "prerequisite": "闭卷写出价格收益、总回报、累计财富、几何平均和年化各自回答的问题。",
            "question": "能否为同一份数据制作一张不混淆收益口径与个人现金流的审计卡？",
            "prediction": "先找出四句收益陈述中缺失的起止时点、股息、频率或现金流说明，再运行完整报告。",
            "hint": "最终表格每个字段同时给出名称、公式/代码、单位、频率、输入列和关键假设。",
            "boundary": "一条历史路径只说明发生过什么；它不能直接给出未来结果及其概率。",
        },
    },
    "07_概率分布与抽样.ipynb": {
        "## AI学习状态": {
            "title": "章前定位任务卡",
            "prerequisite": "回忆第6章历史平均和最终财富是由一条已经实现的路径计算出来的。",
            "question": "怎样在不冒充预测的前提下表达未来可能结果？",
            "prediction": "先用自己的话区分“模型中所有可能结果”和“实际抽到的一小组结果”。",
            "hint": "全章沿用三情景`[-20%, 5%, 30%]`与权重`[0.2, 0.5, 0.3]`作为手算锚点。",
            "boundary": "教学概率是明确给定的假设参数，不是对真实市场概率的估计。",
        },
        "## 7.1 随机变量：给结果赋数值": {
            "prerequisite": "回忆第1章“情景不是预测”和第6章一期收益率的含义。",
            "question": "结果、事件、随机变量、概率、总体和样本分别是什么？",
            "prediction": "判断7.5%的期望收益是否必须是三个情景之一，并先手算概率加权和。",
            "hint": "先逐行算`结果×概率`再求和；代码中先显示情景表，最后才使用向量乘法。",
            "boundary": "期望是模型中心而非个人保证；总体是概率模型描述的全部可能性，不等于一张巨大数据表。",
        },
        "## 7.2 模拟不是“制造事实”": {
            "prerequisite": "指出三情景模型中哪些是结果数组，哪些是概率数组。",
            "question": "从指定概率模型抽样能回答什么，又不能证明什么？",
            "prediction": "预测抽10次是否必然恰好出现2、5、3次三种结果，再比较10、100、10,000次频率。",
            "hint": "拆解`rng.choice(outcomes, size, p)`三个输入；先打印前12次抽样，再汇总次数和比例。",
            "boundary": "随机种子用于复现计算，不会令假设更真实；模拟不能替代数据和机制检验。",
        },
        "## 7.3 大数定律：样本平均逐渐稳定": {
            "prerequisite": "回忆第7.2节每一次抽样仍可能亏损，以及第6章算术平均的计算。",
            "question": "样本量增加时，累计样本均值会怎样变化？",
            "prediction": "判断累计均值是否单调靠近期望，并比较三个随机种子的早期路径。",
            "hint": "用`cumsum()/arange()`计算累计均值，并打印样本量10、100、1,000、5,000的检查点。",
            "boundary": "大数定律不消除单次尾部损失；真实市场也可能不满足固定权重与相互独立。",
        },
        "## 7.4 分位数与尾部": {
            "prerequisite": "先把一组收益从小到大排序，并回忆布尔条件如何筛出小于阈值的元素。",
            "question": "不用假设正态分布，怎样描述最差的一小部分结果？",
            "prediction": "预测均值和标准差接近的两个模型，其1%分位和极端事件比例是否也必须接近。",
            "hint": "先用`np.quantile`和布尔筛选；读对数纵轴时比较数量级，不比较柱形的表面高度。",
            "boundary": "分位数是尾部入口而非最大损失；小样本下极端分位尤其不稳定。",
        },
        "## 7.5 抽样分布与中心极限定理": {
            "prerequisite": "按顺序复述：概率模型、一个大小为n的样本、样本均值、重复得到的许多均值。",
            "question": "为什么单日收益分布和样本均值的抽样分布不是同一个对象？",
            "prediction": "预测`n=100`时均值分布的中心是否移动，以及宽度约为`n=1`时的多少。",
            "hint": "二维数组形状是`(重复次数, 样本量)`；`axis=1`表示每一行计算一个样本均值。",
            "boundary": "样本均值接近正态不表示单日收益变成正态；依赖、状态变化和极厚尾会削弱近似。",
        },
        "## 7.6 编程练习：离散分布统计": {
            "prerequisite": "闭卷写出概率非负、概率和为1、结果与概率长度一致三条规则。",
            "question": "怎样让函数既计算统计量，又拒绝非法概率模型？",
            "prediction": "先判断负概率、概率和不为1、含`NaN`和长度不一致各应触发什么结果。",
            "hint": "A级验证输入，B级计算期望，C级返回有字段名的结果并添加确定性与对称分布测试。",
            "boundary": "函数正确不等于概率设定符合现实；模型来源和估计误差仍需单独说明。",
        },
        "## 本章总结与小项目": {
            "title": "章末整合任务卡",
            "prerequisite": "用一句话分别定义总体、样本、统计量、抽样分布和模拟输出。",
            "question": "能否提交一份把假设、一次抽样、重复实验与结论边界分开的随机实验报告？",
            "prediction": "先预测薄尾与厚尾模型在1%分位和极端事件比例上的差异，再运行实验。",
            "hint": "固定种子并保存全部参数；表格同时报告理论值、模拟值、样本量和抽样误差。",
            "boundary": "分布描述可能性，但尚未决定投资者最关心哪一种损失；这由第8章继续处理。",
        },
    },
    "08_风险度量与压力测试.ipynb": {
        "## AI学习状态": {
            "title": "章前定位任务卡",
            "prerequisite": "回忆第7章标准差、5%分位和厚尾各自描述了分布的哪一部分。",
            "question": "为什么风险不能由一个万能数字概括？",
            "prediction": "先列出你担心的三类损失，并判断它们分别依赖收益分布、财富路径还是外部情景。",
            "hint": "全章每个指标都记录五项：对象、期限、单位、输入样本和遗漏风险。",
            "boundary": "以下指标是观察窗口，不是安全证明，也不构成投资建议。",
        },
        "## 8.1 波动率：围绕平均值的离散程度": {
            "prerequisite": "回忆第7章方差与标准差，以及第6章年化只是尺度换算。",
            "question": "收益围绕平均值有多分散，上涨和下跌是否被同等对待？",
            "prediction": "比较均值同为0但幅度不同的两组收益，并判断+5%和−5%对标准差贡献是否相同。",
            "hint": "先手算小样本，再解释`.std(ddof=1)`；下行偏差只保留负收益部分后计算。",
            "boundary": "年化平方根规则依赖频率、稳定性和弱相关等条件；波动率也不涵盖流动性或信用风险。",
        },
        "## 8.2 回撤是路径指标": {
            "prerequisite": "回忆第6章累计财富和`cumprod()`，并说明百分比损失恢复为何不对称。",
            "question": "财富相对自己曾经达到的最高点跌了多少？",
            "prediction": "手算`100→120→90→108`的历史峰值和每期回撤，再算从−25%恢复所需涨幅。",
            "hint": "先建`wealth`、`running_peak`、`drawdown`三列，再使用`cummax()`定位峰值与谷底。",
            "boundary": "最大回撤依赖路径和样本区间，是历史描述，不是未来最大损失。",
        },
        "## 8.3 VaR：先把20个损失排队": {
            "prerequisite": "回忆第7.4节分位数只是排序后的阈值，不是样本中的最大值。",
            "question": "最差一部分损失的入口和入口以后的平均严重度分别如何描述？",
            "prediction": "先手排20个损失，圈出最差10%的两个数；判断阈值与这两个数的平均是否相同。",
            "hint": "为减少符号混乱，先令`losses = -returns`，再在损失分布右尾计算分位数和条件平均。",
            "boundary": "“95%一日VaR为2%”不表示最多亏2%；期限、样本、模型和分位数算法都会影响结果。",
        },
        "## 8.4 正态VaR与历史VaR可能给出不同答案": {
            "prerequisite": "回忆第7.4节正态与厚尾模型在极端分位上的差异。",
            "question": "同一风险问题为什么会因分布假设不同得到不同答案？",
            "prediction": "预测厚尾样本下历史法与正态法在更高置信水平时谁可能更大。",
            "hint": "历史法直接排序样本；正态法先压缩成均值与标准差，`norm.ppf`再把概率映射为正态横坐标。",
            "boundary": "历史法看不到样本外事件，正态法可能遗漏厚尾；二者都不是风险真值。",
        },
        "## 8.5 滚动风险揭示非稳定性": {
            "prerequisite": "回忆第5章时间顺序和第7章固定分布假设可能失效。",
            "question": "一个全样本波动率为什么会掩盖市场状态变化？",
            "prediction": "先判断20、60、120日窗口谁反应最快、谁更平滑，并预测切换状态后的滞后。",
            "hint": "使用上下共享横轴子图分别画日收益与滚动指标；解释窗口开始阶段的`NaN`和右对齐。",
            "boundary": "短窗口灵敏但噪声大，长窗口平滑但迟钝；滚动估计只能显示变化，不能消除变化。",
        },
        "## 8.6 压力测试：主动提出历史之外的问题": {
            "prerequisite": "回忆第4章组合权重和第7章“情景不等于发生概率”。",
            "question": "样本未经历某种联合冲击时，怎样检查组合最脆弱的部分？",
            "prediction": "运行前判断“股债同跌”中哪类资产贡献最大损失，并说明由权重还是跌幅主导。",
            "hint": "先计算每个资产的`权重×情景收益`贡献，再按行求和；同时检查权重和是否为1。",
            "boundary": "压力测试检查脆弱性，不给出情景概率；线性加总还忽略流动性、再平衡与被迫卖出。",
        },
        "## 8.7 杠杆放大收益，也放大生存风险": {
            "prerequisite": "回忆资产=负债+权益，以及第6章财富归零后不能靠普通收益率恢复。",
            "question": "为什么资产下跌50%会让2倍杠杆的自有资本归零？",
            "prediction": "用100元权益加100元借款买入200元资产，手算资产下跌10%、30%、50%后的权益。",
            "hint": "先画资产、负债、权益表；图中每条杠杆曲线只画到权益归零，并明确标记耗尽点。",
            "boundary": "简化模型未含融资成本、保证金、跳空和强平；权益归零后不能继续持有同一策略。",
        },
        "## 8.8 编程练习：风险摘要": {
            "prerequisite": "写出波动率、最大回撤、VaR和ES分别依赖分布还是路径。",
            "question": "怎样让风险函数同时可计算、可解释并拒绝非法输入？",
            "prediction": "先决定常数收益、空数组、收益等于−100%、含`NaN`和非法尾部概率的处理方式。",
            "hint": "分级实现标准差、财富、回撤、损失分位与尾部平均；结果字段中写明期限和概率口径。",
            "boundary": "摘要函数不替代模型判断；报告仍需说明数据区间、频率、尾部样本数和遗漏风险。",
        },
        "## 本章总结与小项目": {
            "title": "章末整合任务卡",
            "prerequisite": "闭卷把波动率、回撤、VaR/ES、压力测试和杠杆分别归入分布、路径、情景或资本结构。",
            "question": "能否用多副风险镜头比较两个平均收益相同但失败方式不同的方案？",
            "prediction": "先选出自己最担心的指标，再运行完整体检，检查结果是否改变原判断。",
            "hint": "每项输出附对象、期限、单位、假设和遗漏风险；至少构造一对同均值但不同尾部或路径的数据。",
            "boundary": "单项风险仍未描述资产之间如何共同变化；相关性与分散化留给第9章。",
        },
    },
}


READING_CARDS: dict[str, dict[str, str]] = {
    "06_收益率与财富路径.ipynb": {
        "bad6c271": """
### 读图卡：固定平均下的两期收益差

1. 先检查`d=0`时，两期都为5%，几何平均是否也为5%。
2. 再找到`d=45%`，对应`[-40%, 50%]`，读取终值与几何平均。
3. 曲线描述精确的两期复合关系；它没有给任何路径附加发生概率。
""",
    },
    "07_概率分布与抽样.ipynb": {
        "bbfd3cef": """
### 读图卡：次数不是概率本身

1. 比较三根柱子的样本次数，而不是只看哪根最高。
2. 把次数除以10,000后再与`[0.2, 0.5, 0.3]`比较。
3. 更换随机种子会改变柱高；模型权重未改变。
""",
        "86397dcd": """
### 读图卡：稳定不等于单调

1. 先看前100次，找出累计均值多次穿过理论期望的位置。
2. 再看1,000次以后摆动范围是否缩小。
3. 横轴若使用对数刻度，后期大量样本会被压缩；不要把视觉平滑误认为没有误差。
""",
        "e0b923e9": """
### 读图卡：同中心、同尺度，不同尾部

1. 先核对上方表格中的均值和标准差是否接近。
2. 再沿对数纵轴比较两侧远离中心的位置，观察厚尾模型是否留下更多质量。
3. 图来自两个教学模型；不能仅凭形状宣布真实市场服从其中之一。
""",
        "8ae9b655": """
### 读图卡：变窄的是样本均值分布

1. 三幅图使用同一横轴，比较中心位置是否明显移动。
2. 比较`n=1、10、100`的横向宽度，并核对打印出的标准差。
3. 这里变得集中的是“重复计算的样本均值”，不是单日收益本身。
""",
    },
    "08_风险度量与压力测试.ipynb": {
        "98730965": """
### 读图卡：财富曲线与水下曲线要配对

1. 在上图找到历史峰值和之后的谷底。
2. 在下图同一日期读取回撤，确认最大回撤不是起点到终点收益。
3. 改变观察区间会改变可见峰值和最大回撤，因此它不是未来损失上限。
""",
        "712ab129": """
### 读图卡：VaR是入口，ES看入口以外

1. 横轴已经转换为“损失”，越向右越差。
2. 竖线是95%损失分位，阴影是超过该阈值的样本。
3. 比较阈值与尾部平均，不要把任一数字称为最大可能损失。
""",
        "08c7ae52": """
### 读图卡：窗口长度决定反应速度

1. 上图先定位状态切换及收益摆动扩大的时间。
2. 下图比较20、60、120日曲线何时开始明显上升。
3. 短窗口更快也更抖，长窗口更慢也更平滑；不存在对所有问题都最好的窗口。
""",
        "b0ffbcde": """
### 读图卡：曲线在资本耗尽处终止

1. 从表格验证2倍杠杆在资产下跌50%时权益为0。
2. 在图上找到不同杠杆的资本耗尽点；杠杆越高，耗尽点越靠近0。
3. 终止后的空白是金融约束，不是缺失数据：权益归零后不能继续持有原策略。
""",
    },
}


SOURCE_REVISIONS: dict[str, dict[str, str]] = {
    "06_收益率与财富路径.ipynb": {
        "c8e681c6": r"""
## 6.4 算术平均不等于长期增长率

算术平均描述两期收益数字的中心；几何平均描述从初值到终值的等效复合增长率。为了只研究**确定性的复合关系**，固定两期算术平均为$m$，把两期收益写成$m-d$和$m+d$：

$$
g(d)=\sqrt{(1+m-d)(1+m+d)}-1
=\sqrt{(1+m)^2-d^2}-1,
$$

其中必须满足两期收益都大于$-100\%$。当$d$增大时，算术平均仍为$m$，但两期终值和几何平均会下降。本节不为这些路径指定概率。
""",
        "bad6c271": r"""
average_return = 0.05
return_gap = np.linspace(0, 0.95, 191)

first_return = average_return - return_gap
second_return = average_return + return_gap
geometric_return = np.sqrt((1 + first_return) * (1 + second_return)) - 1
terminal_wealth = 100 * (1 + first_return) * (1 + second_return)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].plot(return_gap, geometric_return, color="tab:blue")
axes[0].axhline(average_return, color="black", ls="--", label="固定算术平均 5%")
axes[0].set(
    xlabel="两期收益差 d",
    ylabel="两期几何平均",
    title="固定算术平均下的精确复合增长",
)
axes[0].legend()

axes[1].plot(return_gap, terminal_wealth, color="tab:green")
axes[1].axhline(100, color="black", lw=1)
axes[1].set(
    xlabel="两期收益差 d",
    ylabel="100元的两期终值（元）",
    title="收益差扩大时终值如何变化",
)
plt.tight_layout()
plt.show()

check_gap = 0.45  # 两期收益恰好为 -40% 与 50%
check_growth = np.sqrt((1 + average_return) ** 2 - check_gap**2) - 1
check_terminal = 100 * ((1 + average_return) ** 2 - check_gap**2)
print({
    "固定算术平均": f"{average_return:.2%}",
    "两期收益": [f"{average_return-check_gap:.2%}", f"{average_return+check_gap:.2%}"],
    "几何平均": f"{check_growth:.2%}",
    "100元终值": round(float(check_terminal), 2),
})
""",
    },
    "07_概率分布与抽样.ipynb": {
        "2d25f442": r"""
## 7.1 随机变量：给结果赋数值

先按顺序认识六个对象，后面的公式才有明确含义：

1. **结果**：一次未来一年实验最终出现的具体状态，例如收益为$-20\%$、$5\%$或$30\%$。
2. **事件**：我们关心的一组结果，例如“发生亏损”在本例中包含$-20\%$这一结果。
3. **随机变量**：把每个结果映射成数值的规则。本章把一年收益记作$R$。
4. **概率**：模型赋给每个结果的权重，必须非负且总和为1。
5. **总体**：这张概率表所描述的全部可能性及其权重，不是一次实际观察表。
6. **样本**：按照模型实际抽到的一组有限结果；不同样本会有不同均值。

设$R$的三个结果为$-20\%$、$5\%$、$30\%$，概率分别为0.2、0.5、0.3。先逐行计算“结果$\times$概率”，再把三项相加得到期望：

$$E[R]=\sum_i p_i r_i.$$

方差再计算各结果与期望之差的加权平方；标准差是方差的平方根：

$$Var(R)=\sum_i p_i(r_i-E[R])^2.$$
""",
        "2d4fc775": r"""
outcomes = np.array([-.20, .05, .30])
probabilities = np.array([.2, .5, .3])

scenario_table = pd.DataFrame({
    "结果（收益）": outcomes,
    "概率（模型权重）": probabilities,
    "结果×概率": outcomes * probabilities,
})
display(scenario_table.style.format({
    "结果（收益）": "{:.1%}",
    "概率（模型权重）": "{:.1%}",
    "结果×概率": "{:.2%}",
}))

expected = np.sum(outcomes * probabilities)
variance = np.sum(probabilities * (outcomes - expected) ** 2)
print({
    "概率和": float(probabilities.sum()),
    "期望收益": f"{expected:.2%}",
    "方差（收益率平方）": round(float(variance), 6),
    "标准差": f"{np.sqrt(variance):.2%}",
})
""",
        "8ae9b655": r"""
population = rng.standard_t(df=4, size=500_000)
fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharex=True)
sampling_rows = []
for ax, n in zip(axes, [1, 10, 100]):
    means = rng.choice(population, size=(5000, n), replace=True).mean(axis=1)
    sampling_rows.append({"样本量": n, "样本均值的平均": means.mean(), "样本均值的标准差": means.std(ddof=1)})
    ax.hist(means, bins=60, density=True)
    ax.axvline(0, color="black", ls="--", lw=1)
    ax.set_title(f"样本量 n={n}")
    ax.set_xlabel("样本均值")
    ax.set_xlim(-4, 4)
axes[0].set_ylabel("密度")
fig.suptitle("样本均值的抽样分布（统一横轴）")
plt.tight_layout()
plt.show()
display(pd.DataFrame(sampling_rows).style.format({"样本均值的平均": "{:.3f}", "样本均值的标准差": "{:.3f}"}))
""",
    },
    "08_风险度量与压力测试.ipynb": {
        "6dd494b0": r"""
## 8.3 VaR：先把20个损失排队

在进入缩写和公式前，先做一个可以手工检查的排序实验。假设小林记录了20次“一日损失金额”；损失越大越糟。先从小到大排序，再圈出最差10%，也就是最大的两个损失。

本节用90%作为手算口径，是为了让20个观察中恰好有2个进入尾部；随后再在较大样本上计算常见的95%一日指标。
""",
        "e46bd320": r"""
tail_probability = .05
losses = -returns  # 损失为正、盈利为负，右侧是更严重的损失
var95 = losses.quantile(1 - tail_probability)
tail = losses[losses >= var95]
es95 = tail.mean()
print({
    "95%一日VaR": f"{var95:.2%}",
    "95%一日Expected Shortfall": f"{es95:.2%}",
    "尾部样本数": len(tail),
    "总样本数": len(losses),
})
""",
        "c0fdf60d": r"""
排序实验之后再给概念命名：

- **VaR（风险价值）**是损失分布的一个分位阈值。95%一日VaR回答：“按当前样本或模型，约有5%的日损失会越过哪一道门槛？”
- **Expected Shortfall（ES，预期损失）**是越过该门槛后，尾部损失的平均严重程度。

两者都依赖样本、模型、期限、置信水平和分位数算法。VaR不是最大损失，ES也不是最坏情形。
""",
        "712ab129": r"""
fig, ax = plt.subplots()
ax.hist(losses, bins=60, density=True, alpha=.7)
ax.axvline(var95, color="red", label=f"95% VaR={var95:.2%}")
ax.axvspan(var95, losses.max(), color="red", alpha=.2, label=f"最差5%尾部，ES={es95:.2%}")
ax.set(title="历史损失分布、VaR阈值与尾部", xlabel="一日损失（正数表示亏损）", ylabel="密度")
ax.legend()
plt.show()
""",
        "08c7ae52": r"""
regime = np.r_[rng.normal(0, .006, 250), rng.normal(0, .025, 250)]
regime = pd.Series(regime, index=dates, name="模拟日收益")

rolling_windows = [20, 60, 120]
rolling_risk = pd.DataFrame({
    f"{window}日": regime.rolling(window).std(ddof=1) * np.sqrt(252)
    for window in rolling_windows
})

fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
regime.plot(ax=axes[0], color="slateblue", lw=.9)
axes[0].axvline(regime.index[250], color="black", ls="--", label="教学状态切换")
axes[0].set(title="模拟日收益：低摆动阶段与高摆动阶段", ylabel="日收益")
axes[0].legend()

rolling_risk.plot(ax=axes[1])
axes[1].axvline(regime.index[250], color="black", ls="--")
axes[1].set(title="不同窗口的滚动年化标准差", xlabel="日期", ylabel="年化标准差")
plt.tight_layout()
plt.show()

print({
    "状态切换日期": str(regime.index[250].date()),
    "20日指标首次有效": str(rolling_risk["20日"].first_valid_index().date()),
    "60日指标首次有效": str(rolling_risk["60日"].first_valid_index().date()),
    "120日指标首次有效": str(rolling_risk["120日"].first_valid_index().date()),
})
""",
        "b0ffbcde": r"""
balance_sheet = pd.DataFrame({
    "资产收益": [-.10, -.30, -.50],
    "期末资产": [180, 140, 100],
    "期末负债": [100, 100, 100],
})
balance_sheet["期末权益"] = balance_sheet["期末资产"] - balance_sheet["期末负债"]
balance_sheet["权益收益"] = balance_sheet["期末权益"] / 100 - 1
display(balance_sheet.style.format({"资产收益": "{:.0%}", "权益收益": "{:.0%}", "期末资产": "{:.0f}", "期末负债": "{:.0f}", "期末权益": "{:.0f}"}))

asset_returns = np.linspace(0, -.60, 121)
fig, ax = plt.subplots()
for leverage in [1, 1.5, 2, 3]:
    equity_returns = leverage * asset_returns
    survives = equity_returns > -1
    ax.plot(asset_returns[survives], equity_returns[survives], label=f"{leverage}倍：仍有权益")
    wipeout_return = -1 / leverage
    if asset_returns.min() <= wipeout_return <= asset_returns.max():
        ax.scatter([wipeout_return], [-1], s=35)

ax.axhline(-1, color="black", ls="--", label="资本耗尽；路径在此终止")
ax.set(
    xlabel="资产收益",
    ylabel="简化权益收益",
    title="杠杆与资本损失（只绘制到权益归零）",
    ylim=(-1.05, .05),
)
ax.legend()
plt.show()
""",
    },
}


EXTRA_AFTER_H2: dict[str, dict[str, list[dict[str, Any]]]] = {
    "08_风险度量与压力测试.ipynb": {
        "## 8.3 VaR：先把20个损失排队": [
            markdown_cell(
                "08-8.3-hand-sort-explanation",
                r"""
### 手排实验：先找尾部，再给它命名

下面20个数的单位都是“元”，正数越大表示当天损失越严重。请先在纸上找出最大的两个数，再运行代码核对。

本手算例约定：最差10%的尾部由最大的两个观察组成；尾部门槛取这两个数中较小者，尾部平均取二者平均。真实软件还可能使用插值，因此报告中要注明分位数算法。
""",
            ),
            code_cell(
                "08-8.3-hand-sort-code",
                r"""
toy_losses_yuan = np.array([
    120, 0, 80, 240, 60, 150, 40, 310, 90, 180,
    20, 270, 110, 50, 200, 70, 360, 140, 900, 1800,
])
sorted_losses = np.sort(toy_losses_yuan)
worst_two = sorted_losses[-2:]
toy_var90 = worst_two.min()
toy_es90 = worst_two.mean()

display(pd.DataFrame({
    "从小到大的序号": np.arange(1, len(sorted_losses) + 1),
    "一日损失（元）": sorted_losses,
    "是否属于最差10%": np.arange(len(sorted_losses)) >= len(sorted_losses) - 2,
}))
print({"90%教学VaR（元）": int(toy_var90), "最差10%平均损失（元）": float(toy_es90)})
""",
            ),
            markdown_cell(
                "08-8.3-after-sort-definition",
                r"""
### 从手排结果到95%一日VaR与ES

手排例子中，900元是进入最差10%的门槛，1,350元是最差两个观察的平均损失。现在把同样思路用于500个模拟日收益：先把收益取负变成“损失”，再读取损失分布的95%分位和超过门槛后的平均值。
""",
            ),
        ],
    },
}


def heading_of(cell: dict[str, Any]) -> str | None:
    if cell.get("cell_type") != "markdown":
        return None
    source = "".join(cell.get("source", []))
    for line in source.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            return line.strip()
    return None


def revise_source(cell: dict[str, Any], source: str) -> None:
    metadata = cell.setdefault("metadata", {})
    if metadata.get("course_org_source_revision") == REVISION:
        return
    cell["source"] = lines(source)
    metadata["course_org_source_revision"] = REVISION


def optimize_notebook(filename: str) -> None:
    path = ROOT / filename
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.setdefault("metadata", {}).get("course_org_revision") == REVISION:
        print(f"skip {filename}: already optimized")
        return

    original_cells = notebook["cells"]
    original_ids = [cell.get("id") for cell in original_cells]
    source_revisions = SOURCE_REVISIONS.get(filename, {})
    for cell in original_cells:
        cell_id = cell.get("id")
        if cell_id in source_revisions:
            revise_source(cell, source_revisions[cell_id])

    new_cells: list[dict[str, Any]] = []
    tasks = TASKS[filename]
    read_cards = READING_CARDS.get(filename, {})
    extra_h2 = EXTRA_AFTER_H2.get(filename, {})

    for index, cell in enumerate(original_cells):
        new_cells.append(cell)

        if index == 0:
            new_cells.append(markdown_cell(f"{filename}-navigation", NAVIGATION[filename]))

        heading = heading_of(cell)
        if heading is not None:
            if heading not in tasks:
                raise KeyError(f"No task card configured for {filename}: {heading}")
            config = tasks[heading]
            new_cells.append(
                task_card(
                    marker=f"{filename}-{cell['id']}-task-card",
                    prerequisite=config["prerequisite"],
                    question=config["question"],
                    prediction=config["prediction"],
                    hint=config["hint"],
                    boundary=config["boundary"],
                    title=config.get("title", "本节任务卡"),
                )
            )
            new_cells.extend(extra_h2.get(heading, []))

        cell_id = cell.get("id")
        if cell_id in read_cards:
            new_cells.append(markdown_cell(f"{filename}-{cell_id}-reading-card", read_cards[cell_id]))

    assert [cell.get("id") for cell in new_cells if cell.get("id") in set(original_ids)] == original_ids
    notebook["cells"] = new_cells
    notebook["metadata"]["course_org_revision"] = REVISION
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"updated {filename}: {len(original_cells)} -> {len(new_cells)} cells")


def main() -> None:
    raise SystemExit(
        "已停用：该脚本会恢复教案式任务卡。当前版本请使用 tools/storyize_course.py。"
    )


if __name__ == "__main__":
    main()
