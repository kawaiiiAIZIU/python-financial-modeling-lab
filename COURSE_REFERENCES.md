# 课程官方来源地图

本文件把会影响课程定义、软件行为和研究边界的内容连接到官方文档、监管机构或原始标准。它不是学生必须逐页阅读的参考书，而是教师与 AI 备课时的**核验入口**。

最后联网核验：**2026-07-14**。

## 第0—2章：Python、数组与时间价值

- [Python 官方教程](https://docs.python.org/3/tutorial/)：语法恢复、控制流、函数和异常。
- [NumPy Random Generator](https://numpy.org/doc/stable/reference/random/generator.html)：`Generator`、`default_rng`与可复现实验。固定随机种子只保证重复得到同一伪随机序列，不证明模型更真实。
- [SciPy `brentq`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html)：第2章IRR与第3章到期收益率的选学求根工具。使用前需有连续函数与端点异号的夹逼区间，求得根后仍要代回验证。

## 第3—4章：债券、股票与基金

- [Investor.gov：Bonds](https://www.investor.gov/introduction-investing/investing-basics/investment-products/bonds-or-fixed-income-products/bonds)：债权关系、利息、本金、到期与利率风险的入门核验。
- [Investor.gov：Stocks](https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks)：股票的所有权、股息、风险和交易费用。
- [Investor.gov：Exchange-Traded Funds](https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-2)：基金资产组合、份额、NAV与市场价格的区别。

这些页面采用美国监管语境，只用于核验通用机制；涉及中国市场的发行、交易、税费、停牌和信息披露规则时，应改查中国证监会、交易所、人民银行或其他主管机构的最新原文。

## 第5—6章：时间数据与收益口径

- [pandas 时间序列指南](https://pandas.pydata.org/docs/user_guide/timeseries.html)：日期索引、频率转换、重采样和自定义工作日。`B`表示工作日/星期日历，并不自动等于任何证券交易所的正式交易日历。
- [pandas `merge_asof`](https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html)：时间键必须先排序；`backward`寻找当时或之前最近记录，`forward`会寻找当时或之后记录。课程用二者对照未来信息泄漏。
- [pandas `Series.pct_change`](https://pandas.pydata.org/docs/reference/api/pandas.Series.pct_change.html)：计算相邻观察的比例变化。它不会替研究者判断价格是否复权、股息是否计入或缺失值是否应该填补。

## 第7—8章：概率、抽样与风险

- [NIST：Normal Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3661.htm)：正态分布、分位函数与中心极限定理的官方统计参考。课程强调，样本均值的分布趋近正态不等于单期金融收益本身正态。
- [Basel Framework MAR33](https://www.bis.org/basel_framework/chapter/MAR/33.htm)：Expected Shortfall 在银行市场风险资本框架中的正式使用背景。课程中的历史ES是入门估计，不等同于监管资本模型。

## 按章使用

| 章 | 首选核验入口 | 核验重点 |
|---:|---|---|
| 0 | Python、NumPy | 语法、数组语义、随机生成器 |
| 1 | Investor.gov、NumPy | 资产关系与“模拟不是事实” |
| 2 | SciPy | 根求解的输入条件与验证 |
| 3 | Investor.gov Bonds、SciPy | 债券合同、利率风险、求根边界 |
| 4 | Investor.gov Stocks/ETFs | 所有权、基金组合、NAV与市场交易 |
| 5 | pandas time series/merge_asof | 交易日、重采样、当时可知信息 |
| 6 | pandas pct_change、NumPy | 收益口径、缺失与复权边界 |
| 7 | NIST、NumPy | 总体、样本、抽样分布与随机种子 |
| 8 | NIST、Basel Framework | 分位数、尾部风险与ES适用范围 |

## 更新规则

1. 软件API、市场规则、法规和数据接口在使用前重新联网核实，不仅依赖本文件的日期。
2. 优先链接原始监管文本、交易所/央行页面、官方软件文档和原始论文。
3. 把“官方定义”“课程简化模型”“代码实现”分开写；三者相似不代表完全等价。
4. 若来源只适用于特定司法辖区或市场，必须在正文写明，不能自动推广到中国市场。
