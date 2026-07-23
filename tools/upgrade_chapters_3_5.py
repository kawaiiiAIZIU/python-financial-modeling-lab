#!/usr/bin/env python3
"""Idempotently add teaching scaffolds to chapters 3--5.

The script preserves every pre-existing cell, including outputs and student work.
Only cells carrying this script's metadata marker are replaced on a rerun.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = "chapters_3_5_course_upgrade_v1"


def cell_id(key: str) -> str:
    return "u35-" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def markdown_cell(source: str, key: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id(key),
        "metadata": {"course_upgrade": {"owner": OWNER, "key": key}},
        "source": source.strip() + "\n",
    }


def code_cell(source: str, key: str) -> dict:
    return {
        "cell_type": "code",
        "id": cell_id(key),
        "execution_count": None,
        "metadata": {"course_upgrade": {"owner": OWNER, "key": key}},
        "outputs": [],
        "source": source.strip() + "\n",
    }


def task_card(level: str, question: str, connection: str, prediction: str,
              hint: str, interpretation: str) -> str:
    return f"""
> **本节任务卡｜{level}**
>
> - **核心问题**：{question}
> - **前置连接**：{connection}
> - **先预测/再观察**：{prediction}
> - **Python / 数学提示**：{hint}
> - **结果解释重点**：{interpretation}
"""


CHAPTERS = {
    "03_债券与利率风险.ipynb": {
        "navigation": """
<!-- course-upgrade:chapter-03-navigation -->
## 本章导航：你把未来学习资金放进一份付款合同

项目计划三年后支付一笔学习费用，并在教学模拟市场中看到一只固定利率债券：先读懂合同现金流，再研究市场利率变化，最后检查合同之外的风险。

![你理解债券现金流与利率风险](assets/course/03_bond_mechanism.png)

**读图顺序**：先看左侧债券合同，再沿时间轴寻找逐期票息与到期本金，最后观察下方“利率上升—价格下降”的跷跷板。插图只解释机制，不代表真实债券报价或收益保证。

| 学习主线 | 本章路线 |
|---|---|
| 金融 | 借款关系 → 合同现金流 → 市场价格 → 利率风险 → 其他风险 |
| 数学 | 逐笔贴现 → 现值权重 → 一阶近似 → 二阶修正（选学） → 反求利率（选学） |
| Python | 列表/数组 → 定价函数 → 权重表 → 冲击循环 → 数值工具（选学） → 测试 |

**核心路径**：3.1、3.2、3.3的直觉、3.5的金融含义、3.6、3.7静态实验、3.8。  
**数学深化**：3.4凸性；3.5中的SciPy数值求根；3.7滑块。

**术语阶梯**：发行人/投资者 → 面值、票面利率、票息、期限 → 市场收益率 → 价格 → 久期 → 到期收益率 → 信用与流动性风险。术语只在走到对应台阶时使用。

> **单位卡**：`1 bp`（1个基点）=`0.01`个百分点=`0.0001`。例如收益率从5.00%升至5.50%，变化为50 bp，代码中写作`0.005`。

**章间产出**：保存一张“你债券风险卡”，包含现金流、当前价格、±50/100/200 bp压力结果和模型未覆盖的风险；第4章用它与股权资产比较。
""",
        "cards": {
            "AI学习状态": task_card(
                "核心｜检索练习", "第2章的贴现如何帮助我们读懂债券？",
                "回忆现值、现金流时点和反求贴现率，不翻答案先说出含义。",
                "若一组固定未来付款不变，而市场比较利率上升，今天的价格方向如何？",
                "先用一句话回答，不写公式；把薄弱点填入学习状态。",
                "这里评估的是前置知识，不追求一次答对；后文会用数值反复检验。",
            ),
            "3.1 债券是一组带条件的未来付款承诺": task_card(
                "核心", "面值1000元、年票息50元、3年到期的合同，今天应值多少钱？",
                "第2章已经学过不同时间的钱不能直接相加。",
                "先写出未来现金流`50、50、1050`，判断能否直接把1150元当成今天的价格。",
                "先用列表表示现金流，再转为NumPy数组；先展开三项贴现，再看求和公式。",
                "示例价格约1027.75元。高于面值源于5%合同票息高于4%市场比较利率，不代表无风险获利。",
            ),
            "3.2 价格—收益率曲线": task_card(
                "核心", "同一份固定付款承诺，为什么会随市场收益率变化而重新定价？",
                "复用3.1的现金流，只有贴现率改变。",
                "预测收益率从3%升至7%时价格方向，再预测长期曲线与短期曲线谁更陡。",
                "列表推导式只是重复调用`bond_price`；横轴收益率在代码中使用小数。",
                "5年债在3%/5%/7%时约为1091.59/1000/918.00元；下降关系来自贴现，期限差异引出久期。",
            ),
            "3.3 久期：现金流时间与价格敏感度": task_card(
                "核心（掌握直觉与一阶近似）", "怎样用一个数概括现金流等待时间和小幅利率敏感度？",
                "3.2已观察到期限越长曲线通常越陡，但到期年数还没有考虑早期票息。",
                "比较零息债与高票息债：谁更早收回更多现值，谁的平均等待时间更短？",
                "先计算每笔现值权重并检查权重和为1；Macaulay久期单位是年，`Δy`必须写成小数。",
                "久期是局部近似，不是保证；现金流越早，久期通常越低，小冲击下近似更可靠。",
            ),
            "3.4 凸性：用二阶项修正曲线弯曲": task_card(
                "数学深化（选学）", "为什么一条切线无法在较大利率冲击下贴合弯曲的价格曲线？",
                "先看3.3中“久期近似－精确价格”的误差，再使用高等数学的二阶导数直觉。",
                "预测冲击从25 bp扩大到200 bp时，一阶近似误差如何变化。",
                "中心差分用`y-step`、`y`、`y+step`估计斜率和弯曲度；`step`不是市场预测。",
                "凸性项能改善本例的大冲击近似，但不能覆盖违约、流动性或模型结构变化。",
            ),
            "3.5 到期收益率：从价格反求利率": task_card(
                "金融含义核心｜SciPy求根为数学深化", "市场只给价格时，怎样反求使现金流现值等于价格的单一利率？",
                "这与第2章反求项目IRR是同一个“让函数等于零”的问题。",
                "票面利率5%的债券价格只有950元时，先判断到期收益率高于还是低于5%。",
                "先理解二分夹逼，再看`brentq`；传入的函数、搜索上下界和利率单位都必须解释。",
                "本例约6.1932%；它是价格与合同现金流的汇总指标，不是实际持有收益保证。",
            ),
            "3.6 不只有利率风险": task_card(
                "核心｜概率章节预告", "合同写着1050元，是否等于一定能收到1050元？",
                "复用第1章“情景及其权重”，本节不建立正式概率模型。",
                "在可靠性不同但票息相同的两位发行人之间，先判断高票息是否足以说明更好。",
                "图中的“期望”只表示按教学假设权重计算的平均付款；第7章再正式学习概率与期望。",
                "直线下降来自固定的两种付款结局和人为权重，不是现实违约率估计；还要分别讨论流动性、通胀和合同条款。",
            ),
            "3.7 交互实验：自行设计一只简化债券": task_card(
                "核心静态实验｜滑块选学", "票息、期限和市场收益率同时变化时，怎样有条理地比较？",
                "综合3.1—3.6，但每次只改变一个参数。",
                "先填三行预测：提高票息、提高市场收益率、延长期限分别会怎样，再运行静态函数；最后再操作滑块。",
                "PyCharm可能只显示widget而不显示嵌套图，先直接调用`bond_lab(...)`作为静态后备。",
                "市场收益率上升通常压低价格；期限对价格水平的影响取决于票息与收益率关系，不能概括成“越长越便宜”。",
            ),
            "3.8 编程练习：补全半年付息债券定价": task_card(
                "核心技能", "如何把所有年口径一致转换为半年一期？",
                "复用3.1的定价函数，并检查每期现金流和每期利率是否同频。",
                "年票息60元、2年、半年付息：先手算每期票息、总期数和每期收益率。",
                "应得到每期30元、4期、每期收益率3%；普通循环解释机制后再用数组。",
                "平价测试只是一个边界；还要检查零息债、不同频率和非法输入。",
            ),
            "本章总结与小项目": task_card(
                "核心｜章间迁移", "能否把合同现金流、利率敏感度和合同外风险放进同一张风险卡？",
                "间隔检索本章所有术语，并为第4章的股权比较准备统一口径。",
                "运行前预测2/5/10年债在±50/100/200 bp下的价格排序和误差大小。",
                "输出表必须同时保留精确重定价、近似值、误差和单位；凸性列可选。",
                "累计收益图不是本章证据；结论必须区分模型内利率风险和模型外信用、流动性风险。",
            ),
        },
    },
    "04_股票基金与市场交易.ipynb": {
        "navigation": """
<!-- course-upgrade:chapter-04-navigation -->
## 本章导航：你从“借钱给企业”走向“持有企业的一部分”

第3章的你是债权人；本章他比较成为股东、通过基金持有一篮子资产，以及一笔订单如何在市场中真正成交。

![你理解股票、基金与市场成交机制](assets/course/04_market_mechanism.png)

**读图顺序**：先区分企业与企业发行的份额，再观察多个资产如何进入基金篮子，最后沿买卖双方的方向理解价格形成。插图展示关系，不代表真实交易场所或产品结构。

| 学习主线 | 本章路线 |
|---|---|
| 金融 | 债权/股权 → 股息与总回报 → 指数规则 → 基金/ETF → 报价与成交 → 成本 |
| 数学 | 比例 → 收益分解 → 加权平均/点积 → 加权成交价 → 盈亏分解 |
| Python | 字典 → 标量计算 → DataFrame派生列 → 筛选/排序 → 循环成交 → 校验 |

**核心路径**：4.1—4.4；4.5的成交机制；4.6；4.7。  
**选学深化**：4.4申购赎回机制；4.5通用撮合函数与动态订单到达。

**术语阶梯**：企业融资 → 债权/股权 → 股息与总回报 → 指数/成分/权重 → 基金份额/NAV → ETF交易价格 → 买价/卖价/价差 → 市价单/限价单 → 滑点与成本。

**章间产出**：保存“你市场记录”，包含两个指数、基金NAV、800股逐档成交明细和成本分解；第5章将把这些记录当作待审计数据。
""",
        "cards": {
            "AI学习状态": task_card(
                "核心｜检索练习", "债权人与股东分别拥有什么权利、承担什么风险？",
                "回忆第3章固定合同现金流和发行人风险。",
                "买入股票后，企业是否欠你一笔固定本金？先用一句话说明。",
                "先比较关系，不急着写代码；把无法解释的术语记录为薄弱点。",
                "债券与股票都能融资，但现金流权利不同；这一区分支撑整章。",
            ),
            "4.1 股票代表剩余所有权": task_card(
                "核心", "持有企业很小的一部分，究竟意味着什么？",
                "与第3章债权合同对照，再进入股权。",
                "若企业经营恶化，债权人和普通股股东谁通常先承担剩余损失？",
                "字典类似带名字字段的记录；示例中的`company_value`应理解为简化股权市值，不是真实企业价值证明。",
                "本例每股5元、持仓1000元、持股0.002%；不表示可以拿走企业0.002%的设备或现金。",
            ),
            "4.2 股票总回报不只来自价格": task_card(
                "核心", "价格上涨和收到股息怎样共同形成持有回报？",
                "连接第1章收益率与第3章现金流。",
                "20元买入、21元卖出、期间收到0.6元股息：先判断只看价格漏掉多少。",
                "先用标量手算`(21-20+0.6)/20`，再封装；分子和分母单位都为元。",
                "价格收益率5%，含股息总回报8%；仍未计税费、再投资和公司行动。",
            ),
            "4.3 指数：把一篮子证券压缩为一个数": task_card(
                "核心", "同样三只股票，为什么不同指数规则会得到不同结果？",
                "复用加权平均；指数是规则和尺度，不是可直接持有的资产。",
                "先找出期初市值最大的乙，预测其-10%对等权还是市值加权影响更大。",
                "权重必须使用决策时已知的期初数据；逐列计算后再用乘积求和或点积。",
                "权重约7.41%/74.07%/18.52%；等权收益1.33%，市值加权-5.93%，差异来自规则而非代码冲突。",
            ),
            "4.4 基金与ETF": task_card(
                "核心｜申购赎回机制选学", "指数、基金和ETF为什么不是三个同义词？",
                "4.3的指数只是规则；本节加入真正持有资产的组合和可交易份额。",
                "先判断NAV与ETF市场价格是否必须每一刻完全相同。",
                "按“资产合计－负债→基金净资产→除以份额”三步打印中间值。",
                "本例NAV 4.95元、价格5.02元、溢价约1.41%；一天的偏离不能证明无风险套利。",
            ),
            "4.5 订单簿：价格来自愿意交易的买卖双方": task_card(
                "核心机制｜通用撮合函数选学", "一笔800股市价买单为什么不一定全部按最低卖价成交？",
                "先区分买方最高愿付与卖方最低愿收，再研究数量约束。",
                "不运行函数，先在卖盘表中逐档圈出300股和随后500股。",
                "先手算加权均价；代码循环每一档只做三件事：取可成交量、记录、更新剩余量。",
                "平均价10.0325元，相对最佳卖价滑点约12.48 bp；阶梯来自每档可成交数量有限。",
            ),
            "4.6 交易成本会改变收益": task_card(
                "核心", "从信号价看到的利润，经过成交与费用后还剩多少？",
                "承接4.5的真实买入均价，不再假设无限量按信号价成交。",
                "先预测本例中滑点损失和佣金谁更大。",
                "分开计算基准毛利润、执行损失、显式费用和净利润，避免把成本重复扣除。",
                "当前模型只包含买入滑点和佣金；没有卖出滑点、税费、冲击、延迟和成交失败，不能称为现实净利润。",
            ),
            "4.7 编程练习：实现市值加权组合收益": task_card(
                "核心技能", "怎样把线性代数点积变成有边界检查的金融函数？",
                "4.3已经手算权重与收益的乘积和。",
                "先手算`0.2×10%-0.6×10%+0.2×4%`，再预测函数结果。",
                "转换为一维数组后检查长度、权重和；本练习若限定多头，还应检查非负。",
                "正常结果为-3.2%；一个测试通过不代表边界正确，还需测试长度和权重错误。",
            ),
            "本章总结与小项目": task_card(
                "核心｜章间迁移", "能否从企业权利一路解释到最终成交成本？",
                "间隔检索债权/股权、指数/基金/ETF和报价/成交三组边界。",
                "先预测等权与市值加权方向，再预测800股订单会吃掉哪些价位。",
                "项目分成指数表和成交表两个小产物，失败交易也必须留日志。",
                "指数上涨不证明所有成分上涨；回测毛收益也不等于可实现净收益。",
            ),
        },
    },
    "05_金融数据与时间边界.ipynb": {
        "navigation": """
<!-- course-upgrade:chapter-05-navigation -->
## 本章导航：你下载了一张“看起来很整齐”的价格表

你准备比较第4章的资产与交易记录，却发现一条数值的对象、单位、观测时间、发布时间和清洗历史，往往比数值本身更重要。

![你审计金融数据与时间边界](assets/course/05_data_pipeline.png)

**读图顺序**：从左侧原始记录开始，寻找重复、空白和时间冲突；再看中间的审计与隔离环节；最后确认右侧数据只有越过发布时间闸门后才能用于决策。插图解释流程，不代替真实审计报告。

| 学习主线 | 本章路线 |
|---|---|
| 金融 | 行情含义 → 交易日/停牌 → 公司行动 → 频率 → 可知时间 → 数据血缘 |
| 数学 | 单位与主键 → 缺失状态 → 收益率桥梁 → 采样聚合 → 信息集合 |
| Python | DataFrame → 日期解析/布尔检查 → 隔离表 → 时间索引 → `pct_change` → `resample` → `merge_asof` → 测试 |

**核心路径**：5.1—5.8全部核心；5.1另类数据、5.7文件哈希和真实交易所日历接口可选学。  
**术语阶梯**：行情字段 → 数据护照 → 主键/重复/缺失 → 交易日历 → 公司行动/复权 → 重采样 → 观测时间/发布时间/可知时间 → 数据血缘。

**章间产出**：保存原始表、隔离表、清洗表、审计摘要和数据护照；第6章只能使用通过时间边界检查的清洗表计算收益率。
""",
        "cards": {
            "AI学习状态": task_card(
                "核心｜检索练习", "第4章的一笔价格记录，至少还需要哪些上下文才能用于研究？",
                "回忆价格、成交量、总回报和成交时间并不是同一个字段。",
                "先列出对象、单位和时间三类信息，再查看本章导航。",
                "不写清含义前不调用清洗函数；把无法判断的字段记为薄弱点。",
                "数据质量不是表格是否整齐，而是能否回答来源、含义和当时是否可知。",
            ),
            "5.1 常见金融数据不只有收盘价": task_card(
                "核心｜另类数据选学", "一行OHLCV究竟描述谁、哪段时间和什么单位？",
                "第4章已经出现价格、数量、股息和交易成本，本节为它们建立字段身份。",
                "看到`close=10.20`时，先写出至少三个仍无法回答的问题。",
                "为每个数据集建立数据护照：对象、字段、单位、频率/时区、观测时间、可知时间、来源/许可、修订与复权。",
                "字段名相同不保证定义相同；没有护照的数值不能直接进入模型。",
            ),
            "5.2 金融数据侦探：先检查一份故意损坏的数据": task_card(
                "核心", "如何在不丢失证据的前提下发现并分类数据问题？",
                "使用5.1的数据护照判断哪些规则可自动执行、哪些必须回源核实。",
                "先肉眼数坏日期、重复键、缺失价格和负成交量，再运行审计函数。",
                "先逐项调用`to_datetime/isna/duplicated`，最后才封装函数；完全重复行与日期键重复必须分开。",
                "本表6行、1个坏日期、0个完全重复行、2条重复日期记录、1个缺失价格、1个负成交量且未排序。",
            ),
            "5.3 交易日缺失与数据缺失不是一回事": task_card(
                "核心", "表里没有一行，究竟是休市、停牌、零成交还是接口漏数？",
                "5.2只发现空缺，尚未给空缺解释。",
                "在没有交易所日历和来源日志时，先判断能否给缺失日定性。",
                "`freq='B'`只排除周末，不是任何交易所的正式交易日历；`reindex`创建网格，不创造观察。",
                "前向填充可作为明确的估值假设，但不是新成交，不能据此伪造日收益。",
            ),
            "5.4 公司行动与复权：价格跳变不一定是亏损": task_card(
                "核心", "拆股后每股价格减半时，持仓财富是否也减半？",
                "连接第4章股数、每股价格和总回报。",
                "先手算100元到50元的价格收益，再把股数10变20检查持仓价值。",
                "先用`after / before - 1`，确认等于`Series.pct_change()`的第二项，再进入完整表格。",
                "原始每股价格显示-50%，拆股前后持仓价值均为1000元；复权口径仍要按研究目的选择。",
            ),
            "5.5 频率转换：日数据到月数据": task_card(
                "核心", "价格、成交量和收益率转换到月频时为什么不能使用同一聚合规则？",
                "复用5.1的字段单位和5.4的收益率含义。",
                "先判断月末价格应取最后值还是求和，月成交量又应如何处理。",
                "价格是时点量常取末值，成交量是期间流量常求和，收益率按定义复合；`resample`不会替你决定。",
                "月表是新的统计口径，不是更“真实”的数据；首尾不完整月、复权和时区仍需记录。",
            ),
            "5.6 最危险的错误：把发布日期之前的数据用于决策": task_card(
                "核心", "数据属于某个统计期，是否意味着当时已经可以知道？",
                "从5.1的数据护照取出观测时间与可知时间两列。",
                "在11:30与15:30发布前，先手工填写9:00—16:00每个市场时点能看到哪个值。",
                "先人工向后寻找最近已发布记录，再使用排序后的`merge_asof(direction='backward')`。",
                "9:00—11:00为空，12:00—15:00只能看到4.8，16:00才看到5.1；`forward`会泄漏未来。",
            ),
            "5.7 数据血缘：让未来的自己知道数据从哪里来": task_card(
                "核心｜文件哈希选学", "半年后怎样证明这张表来自哪里、经历了哪些变换？",
                "5.2—5.6的每个清洗与对齐决定都需要留痕。",
                "若只保存最终CSV，预测哪些信息将无法恢复。",
                "metadata至少记录来源、固定获取时间、原始文件校验、字段字典、时区、复权、转换和版本；下载时间应在获取时固定，而非每次重跑都覆盖。",
                "血缘是审计证据，不会自动证明数据正确；原始文件应保持不可变。",
            ),
            "5.8 编程练习：编写安全的价格表清洗函数": task_card(
                "核心技能", "怎样把清洗决定写成可检查、不会悄悄改原表的函数合同？",
                "综合日期、主键、非正价格、排序、隔离与审计。",
                "先写出哪些情况自动处理，哪些情况必须报错，不要先写函数体。",
                "输入/输出、列名、时区和错误策略必须明确；测试原表不变、坏日期、重复键、非正价格和审计计数。",
                "当前3行基础测试只证明一个例子；安全性需要边界测试和被排除记录。",
            ),
            "本章总结与小项目": task_card(
                "核心｜章间迁移", "能否让另一位研究者复现从原始表到可用表的每个决定？",
                "间隔检索数据护照、隔离表、复权、频率和可知时间。",
                "先预测`forward`匹配会在哪些时点偷看未来，再运行对照。",
                "固定交付原始表、隔离表、清洗表、审计JSON和数据字典五件套。",
                "第6章收益率只能基于通过时间边界检查的数据；清洗后的漂亮曲线不是质量证明。",
            ),
        },
    },
}


READING_CARDS = {
    "03_price_yield": """
> **实验图读图卡｜价格—收益率曲线**
>
> - 横轴是市场收益率，纵轴是同一合同现金流的今天价格；颜色只区分到期期限。
> - 先找5%附近与1000元水平线的交点，再比较各曲线斜率。
> - 能观察到收益率上升时价格下降、长期曲线通常更陡；图没有加入违约、税费与流动性。
""",
    "03_approximation": """
> **实验图读图卡｜精确重定价与近似**
>
> - 横轴是收益率变化（代码中为小数），纵轴是价格；三条线分别代表精确值、一阶久期和久期+凸性。
> - 先比较±25 bp，再比较±200 bp：冲击越大，一阶近似偏离越明显，二阶项在本例中更贴近精确值。
> - 这只检验数学近似误差，不能据此声称覆盖信用或流动性风险。
""",
    "03_credit": """
> **实验图读图卡｜情景权重预告**
>
> - 横轴是人为设定的违约情景权重，纵轴是两种付款结局的加权平均。
> - 直线下降是因为付款额和回收额都被固定；它不是用历史数据估计出的违约概率。
> - 第7章将正式学习随机变量、概率与期望；本节只复习第1章情景加权。
""",
    "03_lab": """
> **实验图读图卡｜局部压力实验**
>
> - 红色竖线是当前市场收益率，曲线显示其附近收益率变化对应的价格。
> - 每次只改一个参数并保存关键数值；若PyCharm只显示滑块，请直接调用`bond_lab(...)`获得静态图。
> - 参数敏感性不是预测，图外仍有信用、流动性与合同条款风险。
""",
    "04_order_size": """
> **实验图读图卡｜订单规模与成交均价**
>
> - 横轴是市价买入数量，纵轴是逐档成交后的加权平均价；虚线是最佳卖价。
> - 阶梯向上说明订单吃掉低价卖盘后必须前往更高价位，不是资产基本价值突然跳升。
> - 本图使用静态三档卖盘，未模拟撤单、排队、延迟和订单到达。
""",
    "05_fill": """
> **实验图读图卡｜观察值与填充值**
>
> - 实线圆点是表中真实可用记录，虚线叉号是演示性的前向填充。
> - 两条线重合不等于新增了成交；填充值只携带上一次观察。
> - `B`频率只排除周末，不是交易所日历，因此本图不能判定空缺原因。
""",
    "05_split": """
> **实验图读图卡｜每股价格与持仓价值**
>
> - 左图观察每股价格，右图同时纳入持股数；两图纵轴单位不同。
> - 拆股时左图约减半，右图没有同步减半，说明“价格收益”不能脱离公司行动解释。
> - 这是无费用的教学例子，真实总回报还需核对分红、税费和数据商复权定义。
""",
    "05_availability": """
> **实验图读图卡｜当时可知与未来泄漏**
>
> - 蓝色阶梯只向后匹配已经发布的数据；红色虚线故意向前匹配尚未发布的数据。
> - 发布竖线之前，蓝线保持缺失或旧值；红线提前出现新值就是未来信息。
> - 正确方向仍不够：真实项目还要核对时区、发布延迟、修订版本和可交易时刻。
""",
}


EXTRAS = {
    "04_manual_fill": markdown_cell(
        """
### 先手算800股市价买单

最低卖价一档只有300股，因此剩余500股必须进入下一档：

$$
\\text{平均成交价}=\\frac{300\\times10.02+500\\times10.04}{800}=10.0325
$$

相对最佳卖价10.02元的滑点约为`12.48 bp`。先确认这两步，再阅读循环函数；函数只是把同样的逐档过程推广到任意数量。
""",
        "04_manual_fill",
    ),
    "04_cost_boundary": markdown_cell(
        """
> **成本边界卡**
>
> 按信号价10.00元计算的理论毛利润是320元；实际买入滑点消耗26元，佣金约4.90元，当前净利润约289.10元。代码尚未模拟卖出滑点、税费、延迟、订单冲击、部分成交或无法成交，因此这个结果只是简化成本下的净利润，不是现实可实现性证明。
""",
        "04_cost_boundary",
    ),
    "05_quarantine_code": code_cell(
        """
# 审计证据表：保留原始行号和问题标记，不把异常记录悄悄丢掉。
evidence_table = raw.copy()
evidence_table.insert(0, "source_row", raw.index)
evidence_table["parsed_date"] = pd.to_datetime(evidence_table["date"], errors="coerce")
evidence_table["bad_date"] = evidence_table["parsed_date"].isna()
evidence_table["duplicate_date"] = (
    evidence_table["parsed_date"].notna()
    & evidence_table["parsed_date"].duplicated(keep=False)
)
evidence_table["missing_close"] = evidence_table["close"].isna()
evidence_table["invalid_volume"] = evidence_table["volume"] < 0

issue_columns = ["bad_date", "duplicate_date", "missing_close", "invalid_volume"]
quarantine = evidence_table.loc[evidence_table[issue_columns].any(axis=1)].copy()

print("原始行数：", len(raw), "隔离待复核行数：", len(quarantine))
display(quarantine)
""",
        "05_quarantine_code",
    ),
    "05_quarantine_note": markdown_cell(
        """
> **证据保留卡**
>
> `cleaned`是按演示规则得到的工作视图，`quarantine`才保存了被排除或有冲突的原始记录。真实项目应把隔离表与原因一起落盘；否则无法回查为什么删除，也无法在数据源更正后重新处理。
""",
        "05_quarantine_note",
    ),
    "05_pct_bridge_code": code_cell(
        """
# 最小桥梁：先手算一段收益率，再确认pct_change做的是同一件事。
before_price, after_price = 100.0, 50.0
manual_return = after_price / before_price - 1
two_prices = pd.Series([before_price, after_price], index=["拆股前", "拆股后"])
pandas_return = two_prices.pct_change().iloc[1]

print({"手算收益率": manual_return, "pct_change结果": pandas_return,
       "两者一致": bool(np.isclose(manual_return, pandas_return))})
""",
        "05_pct_bridge_code",
    ),
    "05_pct_bridge_note": markdown_cell(
        """
> **Python提示：`pct_change()`并不理解拆股**
>
> 它只逐项计算`本期 / 上期 - 1`。得到-50%说明原始每股价格变了，不会自动判断这是市场亏损还是公司行动；金融解释仍由数据字段和复权信息决定。
""",
        "05_pct_bridge_note",
    ),
    "05_availability_code": code_cell(
        """
# 对照正确的向后匹配与故意错误的向前匹配。
leaked_forward = pd.merge_asof(
    market.sort_values("time"), releases.sort_values("release_time"),
    left_on="time", right_on="release_time", direction="forward"
)

availability_compare = aligned[["time", "indicator"]].rename(
    columns={"indicator": "当时已知_backward"}
)
availability_compare["错误示范_forward"] = leaked_forward["indicator"]
display(availability_compare)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.step(availability_compare["time"], availability_compare["当时已知_backward"],
        where="post", marker="o", label="当时已知：backward")
ax.step(availability_compare["time"], availability_compare["错误示范_forward"],
        where="post", linestyle="--", marker="x", label="未来泄漏：forward")
for release_time in releases["release_time"]:
    ax.axvline(release_time, color="gray", linestyle=":", alpha=0.8)
ax.set(title="发布时间决定数据何时可用于决策", xlabel="市场时点", ylabel="当时匹配到的指标")
ax.legend()
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
""",
        "05_availability_code",
    ),
}


def heading_of(cell: dict) -> str | None:
    if cell.get("cell_type") != "markdown":
        return None
    for line in "".join(cell.get("source", [])).splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            return line[3:].strip()
    return None


def upgrade_notebook(filename: str, config: dict) -> None:
    path = ROOT / filename
    notebook = json.loads(path.read_text(encoding="utf-8"))

    original_cells = [
        cell for cell in notebook["cells"]
        if cell.get("metadata", {}).get("course_upgrade", {}).get("owner") != OWNER
    ]
    upgraded: list[dict] = []

    for index, cell in enumerate(original_cells):
        upgraded.append(cell)
        source = "".join(cell.get("source", []))

        if index == 0:
            upgraded.append(markdown_cell(config["navigation"], f"{filename}:navigation"))

        heading = heading_of(cell)
        if heading in config["cards"]:
            upgraded.append(markdown_cell(config["cards"][heading], f"{filename}:card:{heading}"))

            if filename.startswith("05_") and heading.startswith("5.4 "):
                upgraded.extend([EXTRAS["05_pct_bridge_code"], EXTRAS["05_pct_bridge_note"]])

        if filename.startswith("03_"):
            if "固定票息债券的价格—收益率关系" in source:
                upgraded.append(markdown_cell(READING_CARDS["03_price_yield"], "03_price_yield_reading"))
            if "duration_convexity =" in source:
                upgraded.append(markdown_cell(READING_CARDS["03_approximation"], "03_approximation_reading"))
            if "expected_payments =" in source:
                upgraded.append(markdown_cell(READING_CARDS["03_credit"], "03_credit_reading"))
            if "def bond_lab" in source:
                upgraded.append(markdown_cell(READING_CARDS["03_lab"], "03_lab_reading"))

        if filename.startswith("04_"):
            if "orders = pd.DataFrame" in source:
                upgraded.append(EXTRAS["04_manual_fill"])
            if "订单规模与平均成交价" in source:
                upgraded.append(markdown_cell(READING_CARDS["04_order_size"], "04_order_size_reading"))
            if "net_pnl =" in source:
                upgraded.append(EXTRAS["04_cost_boundary"])

        if filename.startswith("05_"):
            if "cleaned = raw.copy()" in source:
                upgraded.extend([EXTRAS["05_quarantine_code"], EXTRAS["05_quarantine_note"]])
            if "填充值不是新观察" in source:
                upgraded.append(markdown_cell(READING_CARDS["05_fill"], "05_fill_reading"))
            if "持仓价值（股数已调整）" in source:
                upgraded.append(markdown_cell(READING_CARDS["05_split"], "05_split_reading"))
            if "aligned = pd.merge_asof" in source:
                upgraded.extend([
                    EXTRAS["05_availability_code"],
                    markdown_cell(READING_CARDS["05_availability"], "05_availability_reading"),
                ])

    notebook["cells"] = upgraded
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{filename}: {len(original_cells)} original cells -> {len(upgraded)} total cells")


def main() -> None:
    raise SystemExit(
        "已停用：该脚本会恢复教案式任务卡。当前版本请使用 tools/storyize_course.py。"
    )


if __name__ == "__main__":
    main()
