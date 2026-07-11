"""Build chapters 6-8."""
from pathlib import Path
from textwrap import dedent
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
def md(s): return nbf.v4.new_markdown_cell(dedent(s).strip())
def code(s, tags=None):
    c = nbf.v4.new_code_cell(dedent(s).strip())
    if tags: c.metadata["tags"] = tags
    return c
def make(title, cells):
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata={"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                 "language_info":{"name":"python","version":"3"},
                 "course":{"title":title,"disclaimer":"教学用途，不构成投资建议"}}
    return nb

setup="""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]=(8,4.5); plt.rcParams["axes.grid"]=True
plt.rcParams["font.sans-serif"]=["Arial Unicode MS","PingFang SC","SimHei","DejaVu Sans"]
plt.rcParams["axes.unicode_minus"]=False
rng=np.random.default_rng(20260711)
"""

chapter6=make("第6章 收益率与财富路径",[
md(r"""
# 第6章 收益率与财富路径

> **核心问题**：价格变化怎样转化为可比较的回报？为什么平均收益不错，最终财富仍可能令人失望？

- 金融线：价格收益、总回报、累计收益、年化、定投和路径依赖。
- 数学线：比率、连乘、对数求和、算术平均与几何平均。
- Python线：`shift`、`pct_change`、`cumprod`、向量化、时间索引和函数测试。
"""),
md("""## AI学习状态

当前进度：第6章开始  
已掌握：价格、股息、时间索引和数据审计  
仍然薄弱：待填写  
下一步：每个收益率都写清起止时点和现金流。"""),
code(setup),
md(r"""
## 6.1 简单收益率

$$R_t=\frac{P_t-P_{t-1}}{P_{t-1}}=\frac{P_t}{P_{t-1}}-1$$

它是相对于期初价格的比例。上涨10%后再下跌10%不会回到原点，因为第二个10%的基数不同。
"""),
code("""
prices=pd.Series([100,110,99],index=pd.date_range("2026-01-01",periods=3,freq="D"),name="price")
returns=prices.pct_change()
display(pd.concat([prices,returns.rename("return")],axis=1).style.format({"price":"{:.2f}","return":"{:.2%}"}))
print("最终累计收益：",f"{prices.iloc[-1]/prices.iloc[0]-1:.2%}")
"""),
md("""
**Python提示：`pct_change()`**计算当前值相对前一期的比例变化，第一行因没有前一期而是`NaN`。它不会判断价格是否已复权，也不会自动加入股息。

### 我的解释

为什么+10%和-10%的算术和为0，但财富变化为-1%？

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md(r"""
## 6.2 总回报与累计财富

有股息 $D_t$ 时，一期总回报为

$$R_t^{total}=\frac{P_t-P_{t-1}+D_t}{P_{t-1}}$$

多期财富通过连乘累积：

$$W_T=W_0\prod_{t=1}^T(1+R_t)$$
"""),
code("""
data=pd.DataFrame({"price":[100,103,101,106],"dividend":[0,0,2,0]},
                  index=pd.date_range("2026-03-01",periods=4,freq="ME"))
data["price_return"]=data["price"].pct_change()
data["total_return"]=(data["price"]+data["dividend"])/data["price"].shift(1)-1
data["wealth_price_only"]=10_000*(1+data["price_return"].fillna(0)).cumprod()
data["wealth_total"]=10_000*(1+data["total_return"].fillna(0)).cumprod()
data
"""),
md("""**量化编程警告**：股息的除息时点、再投资价格和税费会影响真实总回报。把股息简单加到收盘价只适合本章的期末教学例子。"""),
md(r"""
## 6.3 对数收益率

$$r_t=\ln\left(\frac{P_t}{P_{t-1}}\right)=\ln(1+R_t)$$

对数收益可跨期相加，但把相加结果转回简单累计收益时要用 $e^{\sum r_t}-1$。当简单收益接近-100%时，对数收益会非常负；价格不能为非正数。
"""),
code("""
simple=prices.pct_change().dropna()
log_return=np.log(prices/prices.shift(1)).dropna()
print({"简单收益连乘":float((1+simple).prod()-1),
       "对数收益求和后转换":float(np.exp(log_return.sum())-1),
       "对数收益之和":float(log_return.sum())})
"""),
md("""
## 6.4 算术平均不等于长期增长率

算术平均描述单期收益的平均；几何平均描述从初值到终值的等效复合增长率。波动越大，两者差距通常越明显。
"""),
code("""
samples={"稳定":[0.05,0.05],"波动":[0.50,-0.40],"先跌后涨":[-0.40,0.50]}
rows=[]
for name,rs in samples.items():
    rs=np.array(rs,dtype=float)
    rows.append({"路径":name,"算术平均":rs.mean(),"几何平均":(np.prod(1+rs))**(1/len(rs))-1,"终值":100*np.prod(1+rs)})
display(pd.DataFrame(rows).set_index("路径").style.format({"算术平均":"{:.2%}","几何平均":"{:.2%}","终值":"{:.2f}"}))
"""),
code("""
vols=np.linspace(0,0.50,100)
mean=0.08
approx_growth=mean-0.5*vols**2
plt.plot(vols,approx_growth); plt.axhline(0,color="black",lw=1)
plt.xlabel("波动率"); plt.ylabel("近似对数增长率"); plt.title("固定算术均值下的波动拖累（近似）"); plt.show()
"""),
md("""
### 观察问题

为什么“先跌后涨”和“先涨后跌”的无追加终值相同？如果中间有定投或提款，顺序还会无关吗？

### 我的回答

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md("""
## 6.5 年化必须说明频率和样本长度

日均收益简单乘252是一种近似；复合年化常写为`(终值/初值) ** (每年期数/样本期数) - 1`。252只是常用交易日近似，不适合所有市场、资产或缺失数据。
"""),
code("""
monthly_returns=np.array([.02,-.01,.03,.00,.015,-.02,.01,.025,-.005,.02,.01,.015])
annual_compound=np.prod(1+monthly_returns)-1
annual_arithmetic=monthly_returns.mean()*12
print({"复合年度收益":f"{annual_compound:.2%}","月均收益×12":f"{annual_arithmetic:.2%}"})
"""),
md("""
## 6.6 定投引入现金流，不能只看资产收益率

资金加权收益会受现金流时点影响；时间加权收益用于隔离外部现金流影响。本节先模拟财富，不急于引入完整绩效归因。
"""),
code("""
def wealth_with_contributions(returns,initial=0,contribution=1000):
    wealth=initial; path=[wealth]
    for r in returns:
        wealth=wealth*(1+r)+contribution  # 期末追加
        path.append(wealth)
    return np.array(path)

path_a=wealth_with_contributions([-.30,.40,.10])
path_b=wealth_with_contributions([.10,.40,-.30])
pd.DataFrame({"先跌路径":path_a,"后跌路径":path_b},index=range(4))
"""),
md("""
### 我的解释

两组收益包含相同三个数字，为什么定投终值不同？“下跌对长期投资者一定有利”这句话遗漏了哪些风险？

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md("""
## 6.7 编程练习：累计财富

函数接收收益率和初始财富；拒绝任何`return <= -1`；返回包含初始值的数组。
"""),
code("""
def cumulative_wealth(returns,initial=1.0):
    # TODO
    return None
""",tags=["exercise"]),
code("""
ans=cumulative_wealth([.10,-.10],100)
if ans is None: print("练习尚未完成。")
else: print("测试通过：",np.allclose(ans,[100,110,99]))
""",tags=["exercise-test"]),
md("""
## 本章总结与小项目

为一组含价格和股息的月度数据计算价格收益、总回报、累计财富、算术/几何平均和复合年化；再加入三种现金流时点，解释路径差异。

**底线**：收益率定义、现金流、复权、频率和年化口径必须同时报告。
""")])

chapter7=make("第7章 概率、分布与抽样",[
md(r"""
# 第7章 概率、分布与抽样

> **核心问题**：不确定结果如何用模型表达？样本平均为什么会变化？正态分布为什么有用又危险？

- 金融线：情景、损失概率、尾部事件和模型风险。
- 数学线：随机变量、期望、方差、分位数、大数定律和中心极限定理。
- Python线：随机生成器、布尔统计、直方图、经验分布、重复抽样和动画。
"""),
md("""## AI学习状态

当前进度：第7章开始  
已掌握：收益率和财富路径  
仍然薄弱：待填写  
下一步：区分总体假设、一次样本和估计结果。"""),
code(setup),
md(r"""
## 7.1 随机变量：给结果赋数值

设一年后收益 $R$有三个情景：-20%、5%、30%，概率分别为0.2、0.5、0.3。概率必须非负且总和为1。

$$E[R]=\sum_i p_ir_i,\qquad Var(R)=\sum_i p_i(r_i-E[R])^2$$
"""),
code("""
outcomes=np.array([-.20,.05,.30]); probabilities=np.array([.2,.5,.3])
expected=np.sum(outcomes*probabilities)
variance=np.sum(probabilities*(outcomes-expected)**2)
print({"概率和":probabilities.sum(),"期望收益":f"{expected:.2%}","标准差":f"{np.sqrt(variance):.2%}"})
"""),
md("""
### 我的解释

期望收益是否一定是三个情景之一？标准差为什么与收益率使用相同单位，而方差不是？

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md("""
## 7.2 模拟不是“制造事实”

随机模拟从我们指定的概率模型中抽样。它能回答“如果模型成立会怎样”，不能证明模型符合市场。
"""),
code("""
draws=rng.choice(outcomes,size=10_000,p=probabilities)
print({"模拟均值":draws.mean(),"理论期望":expected,"模拟亏损比例":np.mean(draws<0)})
plt.hist(draws,bins=[-.25,-.075,.175,.35],rwidth=.8); plt.xlabel("收益情景"); plt.ylabel("次数"); plt.title("离散情景的10000次抽样"); plt.show()
"""),
md("""
## 7.3 大数定律：样本平均逐渐稳定

大数定律不保证短期接近期望，也不说明期望本身安全；它说明在适当条件下，独立同分布样本平均随样本量增加趋近总体期望。
"""),
code("""
draws=rng.choice(outcomes,size=5000,p=probabilities)
running_mean=np.cumsum(draws)/np.arange(1,len(draws)+1)
plt.plot(running_mean,label="累计样本均值"); plt.axhline(expected,color="red",ls="--",label="理论期望")
plt.xscale("log"); plt.xlabel("样本量（对数轴）"); plt.ylabel("平均收益"); plt.title("大数定律的数值观察"); plt.legend(); plt.show()
"""),
md("""
### 观察问题

为什么前几十次波动剧烈？把横轴改为线性后，视觉感受有何变化？金融市场收益为何可能不满足独立同分布？

### 我的回答

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md("""
## 7.4 分位数与尾部

5%分位数表示约5%的观察不高于该数，并不等于“最大损失”。经验分位数依赖样本和方法，在小样本下尤其不稳定。
"""),
code("""
normal=rng.normal(.0003,.01,100_000)
heavy=rng.standard_t(df=4,size=100_000)*.01/np.sqrt(4/(4-2))+.0003
rows=[]
for name,x in [("正态",normal),("t(4)厚尾",heavy)]:
    rows.append({"模型":name,"均值":x.mean(),"标准差":x.std(ddof=1),"1%分位":np.quantile(x,.01),"绝对收益>4%":np.mean(np.abs(x)>.04)})
display(pd.DataFrame(rows).set_index("模型").style.format("{:.3%}"))
"""),
code("""
fig,ax=plt.subplots(); bins=np.linspace(-.06,.06,120)
ax.hist(normal,bins=bins,density=True,alpha=.5,label="正态"); ax.hist(heavy,bins=bins,density=True,alpha=.5,label="t(4)厚尾")
ax.set_yscale("log"); ax.set(title="相同均值和方差附近、不同尾部（纵轴对数）",xlabel="收益",ylabel="密度"); ax.legend(); plt.show()
"""),
md("""
**量化编程警告**：样本均值和标准差相近，不代表极端风险相近。正态模型不是默认真理；模型选择应结合机制、诊断和压力测试。
"""),
md("""
## 7.5 抽样分布与中心极限定理

重复抽取大小为$n$的样本，每次计算均值；这些均值本身构成抽样分布。许多条件下，样本均值标准误约为`总体标准差/sqrt(n)`。
"""),
code("""
population=rng.standard_t(df=4,size=500_000)
fig,axes=plt.subplots(1,3,figsize=(13,3.8))
for ax,n in zip(axes,[1,10,100]):
    means=rng.choice(population,size=(5000,n),replace=True).mean(axis=1)
    ax.hist(means,bins=50,density=True); ax.set_title(f"样本量 n={n}"); ax.set_xlabel("样本均值")
axes[0].set_ylabel("密度"); fig.suptitle("样本均值的抽样分布"); plt.tight_layout(); plt.show()
"""),
md("""
### 我的解释

随着$n$增加，样本均值分布的中心和宽度如何变化？这是否说明单日收益本身变成正态？

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md("""
## 7.6 编程练习：离散分布统计

检查概率合法性，返回期望、方差和标准差。
"""),
code("""
def discrete_stats(outcomes,probabilities):
    # TODO
    return None
""",tags=["exercise"]),
code("""
ans=discrete_stats([-1,1],[.5,.5])
if ans is None: print("练习尚未完成。")
else: print("基础测试：",np.allclose(ans,[0,1,1]))
""",tags=["exercise-test"]),
md("""
## 本章总结与小项目

自行设计一个三情景投资模型，计算理论统计量；模拟不同样本量；比较正态与厚尾模型的1%分位和极端事件比例；解释模拟结论依赖哪些假设。

**关键区分**：总体、样本、估计量和模拟输出不是同一个对象。
""")])

chapter8=make("第8章 风险度量与压力测试",[
md(r"""
# 第8章 风险度量与压力测试

> **核心问题**：风险能否被一个数字概括？波动率、回撤、VaR和Expected Shortfall分别看见什么，又遗漏什么？

- 金融线：波动、下行、回撤、尾部损失、压力情景和杠杆。
- 数学线：标准差、半方差、路径极值、分位数和条件均值。
- Python线：滚动窗口、自定义风险函数、历史模拟、图层与边界测试。
"""),
md("""## AI学习状态

当前进度：第8章开始  
已掌握：收益分布、分位数和抽样  
仍然薄弱：待填写  
下一步：每个风险指标都写出对象、期限和置信水平。"""),
code(setup),
md("""
## 8.1 波动率：围绕平均值的离散程度

样本标准差衡量收益围绕样本均值的变化。年化日波动率常用`日标准差×sqrt(252)`，但它依赖独立、稳定和交易日数等假设，不能机械套用。
"""),
code("""
dates=pd.date_range("2024-01-01",periods=500,freq="B")
returns=pd.Series(rng.standard_t(5,500)*.012,index=dates,name="return")
daily_vol=returns.std(ddof=1); annual_vol=daily_vol*np.sqrt(252)
downside=np.sqrt(np.mean(np.minimum(returns,0)**2))*np.sqrt(252)
print({"日波动率":f"{daily_vol:.2%}","年化波动率":f"{annual_vol:.2%}","年化下行偏差":f"{downside:.2%}"})
"""),
md("""
### 思考

同样大小的上涨和下跌都会提高波动率，但投资者感受是否相同？下行偏差为什么仍不能涵盖流动性或信用风险？

### 我的回答

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md(r"""
## 8.2 回撤是路径指标

财富 $W_t$ 相对历史峰值 $M_t=\max_{s\le t}W_s$ 的回撤：

$$DD_t=\frac{W_t}{M_t}-1$$

最大回撤是样本期内最小的$DD_t$。它依赖观察区间和路径，不能告诉我们未来最大损失。
"""),
code("""
wealth=10_000*(1+returns).cumprod()
running_peak=wealth.cummax()
drawdown=wealth/running_peak-1
max_dd=drawdown.min(); trough=drawdown.idxmin(); peak=wealth.loc[:trough].idxmax()
print({"最大回撤":f"{max_dd:.2%}","峰值日期":str(peak.date()),"谷底日期":str(trough.date())})

fig,axes=plt.subplots(2,1,figsize=(9,7),sharex=True)
wealth.plot(ax=axes[0],title="财富与历史峰值"); running_peak.plot(ax=axes[0],ls="--",label="历史峰值"); axes[0].legend()
drawdown.plot(ax=axes[1],color="crimson",title="回撤"); axes[1].fill_between(drawdown.index,drawdown,0,alpha=.25,color="crimson")
plt.tight_layout(); plt.show()
"""),
md("""
## 8.3 VaR：一个损失分位点

对收益分布，95%的一日VaR可写为`-收益的5%分位数`。它表示在模型/样本下，有约5%的日收益比该阈值更差；它不描述超过阈值后会多糟。
"""),
code("""
alpha=.05
var95=-returns.quantile(alpha)
tail=returns[returns<=returns.quantile(alpha)]
es95=-tail.mean()
print({"95%一日VaR":f"{var95:.2%}","95%一日Expected Shortfall":f"{es95:.2%}","尾部样本数":len(tail)})
"""),
md(r"""
Expected Shortfall（ES）是落入最差$\alpha$尾部时损失的平均，能反映阈值以外的严重程度，但同样依赖样本、模型、期限和估计方法。
"""),
code("""
q=returns.quantile(.05)
fig,ax=plt.subplots(); ax.hist(returns,bins=60,density=True,alpha=.7)
ax.axvline(q,color="red",label=f"5%分位={q:.2%}"); ax.axvspan(returns.min(),q,color="red",alpha=.2,label="ES对应尾部")
ax.set(title="历史收益分布、VaR阈值与尾部",xlabel="日收益",ylabel="密度"); ax.legend(); plt.show()
"""),
md("""
### 我的解释

“95% VaR为2%”为什么不能说“最大只会亏2%”？如果样本从未经历危机，历史VaR会有什么问题？

<!-- 在这里填写；完成前AI不要代答 -->
"""),
md("""
## 8.4 正态VaR与历史VaR可能给出不同答案

正态法用均值和标准差概括分布，历史法直接使用经验分位。厚尾、偏度和状态变化会让结果明显不同。
"""),
code("""
from scipy.stats import norm
mu,sigma=returns.mean(),returns.std(ddof=1)
normal_var=-(mu+sigma*norm.ppf(.05))
historical_var=-returns.quantile(.05)
print({"正态VaR":f"{normal_var:.2%}","历史VaR":f"{historical_var:.2%}"})
"""),
md("""
## 8.5 滚动风险揭示非稳定性

整段样本的一个波动率会掩盖不同市场状态。滚动估计更接近“当时可知”，但窗口选择也会影响灵敏度和噪声。
"""),
code("""
regime=np.r_[rng.normal(0,.006,250),rng.normal(0,.025,250)]
regime=pd.Series(regime,index=dates)
rolling_vol=regime.rolling(60).std()*np.sqrt(252)
regime.cumsum().plot(label="累计简单和（仅观察）"); plt.twinx(); rolling_vol.plot(color="red",label="60日年化波动")
plt.title("市场状态变化与滚动波动率"); plt.show()
"""),
md("""
## 8.6 压力测试：主动提出历史之外的问题

压力测试直接施加情景，如股票-30%、债券-8%、现金0%，研究组合结果。情景不是概率预测，而是脆弱性检查。
"""),
code("""
weights=pd.Series({"股票":.6,"债券":.3,"现金":.1})
scenarios=pd.DataFrame({
    "温和下跌":{"股票":-.10,"债券":.02,"现金":.00},
    "股债同跌":{"股票":-.30,"债券":-.08,"现金":.00},
    "快速反弹":{"股票":.20,"债券":-.03,"现金":.00},
}).T
scenarios["组合收益"]=scenarios.mul(weights,axis=1).sum(axis=1)
display(scenarios.style.format("{:.1%}"))
"""),
md("""
## 8.7 杠杆放大收益，也放大生存风险

简单教学模型中，杠杆$L$把风险资产收益放大，并扣融资成本。一次-50%收益在2倍杠杆下可能耗尽资本，之后无法靠普通百分比反弹恢复。
"""),
code("""
losses=np.linspace(0,-.60,121)
for leverage in [1,1.5,2,3]:
    equity_return=leverage*losses
    plt.plot(losses,equity_return,label=f"{leverage}倍")
plt.axhline(-1,color="black",ls="--",label="资本耗尽")
plt.xlabel("资产收益"); plt.ylabel("简化权益收益"); plt.title("杠杆与资本损失（未计融资和强平细节）"); plt.legend(); plt.show()
"""),
md("""
**量化编程警告**：现实中保证金、逐日盯市、融资成本、跳空和强平规则会使杠杆路径更复杂，不能用简单乘法替代真实风险管理。
"""),
md("""
## 8.8 编程练习：风险摘要

返回波动率、最大回撤、历史VaR和ES；检查置信水平在0与1之间且收益大于-100%。
"""),
code("""
def risk_summary(returns,alpha=.05):
    # TODO
    return None
""",tags=["exercise"]),
code("""
ans=risk_summary([.10,-.10,.05,-.20],.25)
if ans is None: print("练习尚未完成。")
else: print(ans)
""",tags=["exercise-test"]),
md("""
## 本章总结与小项目

比较两个“平均收益相同”的策略：报告年化波动、下行偏差、最大回撤、历史/正态VaR、ES和三个压力情景；解释每个指标遗漏的风险。

**底线**：风险是多维的；指标是观察窗口，不是安全证明。
""")])

for filename,nb in [("06_收益率与财富路径.ipynb",chapter6),("07_概率分布与抽样.ipynb",chapter7),("08_风险度量与压力测试.ipynb",chapter8)]:
    nbf.write(nb,ROOT/filename); print(f"wrote {filename}: {len(nb.cells)} cells")
