"""Build the first two course notebooks from readable source blocks."""

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]


def md(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text: str, tags=None):
    cell = nbf.v4.new_code_cell(dedent(text).strip())
    if tags:
        cell.metadata["tags"] = tags
    return cell


def notebook(cells, title):
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata.update(
        {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3"},
            "course": {
                "title": title,
                "audience": "本科二年级；已学C语言、线性代数和高等数学；金融零基础",
                "disclaimer": "教学用途，不构成投资建议",
            },
        }
    )
    return nb


chapter0 = notebook(
    [
        md(
            r"""
            # 第0章 Python量化实验室快速恢复

            > **定位**：这不是完整语法课。我们用一个真实可计算的问题——“钱经过多年会变成多少”——恢复 Python 手感，并建立以后每章都会使用的实验习惯。

            本章不会先扔出一串库名。我们从你已经会写的 C 程序出发，每次只比较一个区别：输出、变量、判断、循环和函数。能够读懂基础 Python 后，再进入数组和绘图。

            **完成标准**

            1. 能读懂并修改本章代码；
            2. 能把一段简单 C 程序改写成 Python；
            3. 能指出两种语言在类型、括号、缩进和循环写法上的区别；
            4. 能用手算和边界条件检查结果；
            5. 在理解基础写法后，再使用数组和绘图完成复利实验。

            > 本课程中的收益率均为教学假设，不构成投资建议或收益承诺。
            """
        ),
        md(
            """
            ## AI学习状态

            当前进度：第0章开始

            已掌握：待填写

            仍然薄弱：待填写

            常见错误：待填写

            下一步：从上到下运行；每次实验先预测，再观察。
            """
        ),
        md(
            """
            ## 0.1 第一行Python：先让程序说一句话

            在 C 语言中，打印一句话需要包含头文件、`main`函数、分号和返回值：

            ```c
            #include <stdio.h>

            int main(void) {
                printf("开始学习Python金融建模！\\n");
                return 0;
            }
            ```

            Python把这些固定结构省略了。同样的任务只写一行：
            """
        ),
        code(
            """
            print("开始学习Python金融建模！")
            """
        ),
        md(
            """
            ### 这里先记住三个区别

            | C语言 | Python |
            |---|---|
            | 程序通常从`main`开始 | Notebook代码可以直接执行 |
            | 语句末尾通常写`;` | 通常不写分号 |
            | `printf`需要格式说明 | `print`可以直接打印文字或数值 |

            先运行上一格。看到文字就说明环境能工作。现在不导入任何数据分析库。
            """
        ),
        md(
            """
            ## 0.2 变量：C先声明类型，Python直接赋值

            假设本金是1000元、年收益率是3%。C语言写法：

            ```c
            int principal = 1000;
            double annual_rate = 0.03;
            double one_year = principal * (1 + annual_rate);

            printf("%.2f\\n", one_year);
            ```

            Python写法如下。请先找出哪几处符号被省略了。
            """
        ),
        code(
            """
            principal = 1000
            annual_rate = 0.03
            one_year = principal * (1 + annual_rate)

            print(one_year)
            print(type(principal), type(annual_rate))
            """
        ),
        md(
            """
            ### 区别是什么？

            - C语言在变量名前写`int`、`double`；Python赋值时不写类型。
            - Python仍然有类型。`type(...)`显示`principal`是整数，`annual_rate`是浮点数。
            - C的每行以分号结束；Python依靠换行分隔语句。
            - 两种语言的`+`、`-`、`*`、`/`和圆括号含义基本一致。

            **不要误解**：Python“不写类型”不等于“没有类型”。字符串和数值不能随意相加，错误类型仍会报错。
            """
        ),
        md(
            """
            ## 0.3 判断：大括号变成冒号和缩进

            C语言：

            ```c
            if (annual_rate > 0) {
                printf("财富会增长\\n");
            } else {
                printf("财富不会增长\\n");
            }
            ```

            Python：
            """
        ),
        code(
            """
            if annual_rate > 0:
                print("财富会增长")
            else:
                print("财富不会增长")
            """
        ),
        md(
            """
            Python的条件外面通常不用圆括号，条件后写冒号`:`。属于`if`或`else`的代码必须向右缩进。C语言用大括号划分代码块，Python用缩进划分。

            ### 小修改

            把`annual_rate`暂时改为`0`和`-0.03`，预测并观察输出，然后改回`0.03`。
            """
        ),
        md(
            """
            ## 0.4 循环：C自己控制计数，Python遍历一个范围

            C语言：

            ```c
            for (int year = 1; year <= 3; year++) {
                printf("第%d年\\n", year);
            }
            ```

            Python：
            """
        ),
        code(
            """
            for year in range(1, 4):
                print("第", year, "年")
            """
        ),
        md(
            """
            `range(1, 4)`产生1、2、3，**不包含右端点4**。Python没有在这一行写`year++`；每轮循环自动取出下一个数。

            | C的循环组成 | Python中的对应含义 |
            |---|---|
            | `int year = 1` | 从`range`的1开始 |
            | `year <= 3` | 在4之前停止 |
            | `year++` | 自动取下一个数 |
            """
        ),
        md(
            """
            ## 0.5 函数：先给一段计算起名字

            C语言需要声明参数和返回值类型：

            ```c
            double grow_one_year(double money, double rate) {
                return money * (1 + rate);
            }
            ```

            Python使用`def`定义函数：
            """
        ),
        code(
            """
            def grow_one_year(money, rate):
                return money * (1 + rate)


            print(grow_one_year(1000, 0.03))
            """
        ),
        md(
            """
            - `def`表示开始定义函数；
            - 参数放在圆括号中，末尾写冒号；
            - 函数体缩进；
            - `return`把结果交还给调用者；
            - 本例没有写参数类型，但变量仍必须支持乘法和加法。

            到这里为止，只出现了Python自身的基础写法。下面才开始把这些写法组合成一个完整的复利问题。
            """
        ),
        md(
            """
            ## 0.6 第一个完整问题：1000元会怎样增长？

            假设今天有本金 $P=1000$ 元，每年按固定收益率 $r=3\\%$ 增长，持有 $n=10$ 年，并把每年收益继续投入。

            第一年后：

            $$W_1=P(1+r)$$

            第二年后：

            $$W_2=P(1+r)^2$$

            第 $n$ 年后：

            $$W_n=P(1+r)^n$$

            **运行前预测**：最终财富高于、等于还是低于1300元？先用心算给出范围，不要追求精确值。

            ### 我的预测

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        code(
            """
            principal = 1_000       # 本金，单位：元
            annual_rate = 0.03      # 年收益率，3%写成小数0.03
            years = 10              # 投资年数

            final_wealth = principal * (1 + annual_rate) ** years
            print(f"{years}年后的财富：{final_wealth:.2f}元")
            """
        ),
        md(
            """
            **Python提示：数字与格式**

            - `1_000`与`1000`完全相同，下划线只是帮助阅读。
            - `**`表示乘方。
            - `f"...{value:.2f}"`把数值嵌入字符串，并保留两位小数。

            **单位检查**：`annual_rate`是比例，没有“元”这个单位；`principal`和`final_wealth`的单位都是元。
            """
        ),
        md(
            """
            ## 0.7 用循环观察逐年增长

            现在把前面学过的变量、循环和输出组合起来。这里的`range(years)`产生从0到`years-1`的整数，因此显示年份时使用`year + 1`。
            """
        ),
        code(
            """
            wealth = principal
            wealth_history = [wealth]

            for year in range(years):
                wealth = wealth * (1 + annual_rate)
                wealth_history.append(wealth)
                print(f"第{year + 1:2d}年：{wealth:8.2f}元")
            """
        ),
        md(
            """
            **从前面的简单循环多走一步**

            - `wealth_history = [wealth]`创建一个Python列表，先放入初始财富。
            - `append`把每一年算出的财富追加到列表末尾。
            - 循环内部仍然用缩进划分，不使用大括号。
            - `wealth_history[0]`是初始财富，`wealth_history[10]`是第10年末财富。

            ### 观察问题

            1. 每年增加的“元数”是否相同？
            2. 如果收益率固定，为什么增加额仍然会变化？
            3. 列表为什么需要先放入初始财富？

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 0.8 从Python列表进入NumPy数组

            前面用列表保存逐年财富。进行大量数学计算时，我们还会使用NumPy数组。先不用记住这个库的全部功能，只观察一个关键区别。
            """
        ),
        code(
            """
            import numpy as np

            python_list = [10, 11, 12]
            numpy_array = np.array([10, 11, 12])

            print("列表 * 2：", python_list * 2)
            print("数组 * 2：", numpy_array * 2)
            """
        ),
        md(
            """
            **Python提示：运算由对象类型决定**

            - 列表乘整数表示重复列表；
            - NumPy数组乘数值表示逐元素运算；
            - 量化计算中常用NumPy数组，因为数学公式可以直接作用于整组数据。

            请运行：`type(python_list)`、`type(numpy_array)`和`numpy_array.dtype`，然后解释三个输出。
            """
        ),
        code(
            """
            print(type(python_list))
            print(type(numpy_array))
            print(numpy_array.dtype)
            """
        ),
        md(
            """
            ## 0.9 用NumPy把公式作用于整条时间轴

            令年份数组为

            $$t=[0,1,2,\\ldots,n]$$

            NumPy可以一次计算

            $$W_t=P(1+r)^t$$

            这叫**向量化**：用数组运算表达数学关系，而不是在Python层逐项循环。
            """
        ),
        code(
            """
            time = np.arange(years + 1)
            wealth_vector = principal * (1 + annual_rate) ** time

            print("年份：", time)
            print("财富：", np.round(wealth_vector, 2))
            print("循环与向量结果一致：", np.allclose(wealth_history, wealth_vector))
            """
        ),
        md(
            """
            **量化编程警告：向量化不会自动修正金融逻辑**

            代码更短不代表模型正确。这里的固定3%收益率只是教学假设；真实风险资产收益并不固定。`np.allclose`只说明两段代码算出了相近数值，不说明金融假设合理。
            """
        ),
        md(
            """
            ## 0.10 把完整计算封装成函数

            函数把“输入 → 规则 → 输出”明确写出。金融函数尤其应说明单位、参数范围和假设。
            """
        ),
        code(
            """
            def future_value(principal, annual_rate, years):
                # 计算固定年收益率、按年复利时的终值。
                if principal < 0:
                    raise ValueError("principal不能为负数")
                if years < 0:
                    raise ValueError("years不能为负数")
                return principal * (1 + annual_rate) ** years


            examples = [
                (1_000, 0.03, 0),
                (1_000, 0.00, 10),
                (1_000, 0.03, 10),
            ]

            for p, r, n in examples:
                print(p, r, n, "->", round(future_value(p, r, n), 2))
            """
        ),
        md(
            """
            ### 边界条件检查

            - `years=0`时终值应等于本金；
            - `annual_rate=0`时财富不增长；
            - 本金或年份为负时，本函数主动拒绝输入。

            **Python提示：`raise`**

            `raise ValueError(...)`用于明确告诉调用者：输入不符合本函数的约定。报错不是失败，而是阻止错误数据悄悄产生错误结论。
            """
        ),
        md(
            """
            ## 0.11 可视化：数字如何变成形状

            一张图至少要回答：横轴是什么、纵轴是什么、单位是什么、不同曲线代表什么。
            """
        ),
        code(
            """
            import matplotlib.pyplot as plt

            plt.rcParams["figure.figsize"] = (8, 4.5)
            plt.rcParams["axes.grid"] = True
            plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC", "SimHei", "DejaVu Sans"]
            plt.rcParams["axes.unicode_minus"] = False

            rates = [0.00, 0.03, 0.08]
            time = np.arange(0, 31)

            fig, ax = plt.subplots()
            for rate in rates:
                path = principal * (1 + rate) ** time
                ax.plot(time, path, label=f"年收益率 {rate:.0%}")

            ax.set(title="固定收益率假设下的财富路径", xlabel="年份", ylabel="财富（元）")
            ax.legend()
            plt.show()
            """
        ),
        md(
            """
            ### 观察问题

            1. 3%和8%的曲线为什么不是直线？
            2. 时间越长，两条曲线之间的差距如何变化？
            3. 图中哪一个假设最不符合股票等风险资产的真实情况？

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 0.12 参数滑块：自己控制模型

            安装`ipywidgets`后可以拖动收益率和期限。若当前环境没有该库，代码会显示安装提示和一张静态后备图。
            """
        ),
        code(
            """
            def plot_compound(rate=0.03, horizon=20):
                t = np.arange(horizon + 1)
                w = principal * (1 + rate) ** t
                fig, ax = plt.subplots()
                ax.plot(t, w, color="#2563eb", linewidth=2)
                ax.set(title=f"年收益率={rate:.1%}，期限={horizon}年",
                       xlabel="年份", ylabel="财富（元）")
                plt.show()
                print({"rate": rate, "horizon": horizon, "final_wealth": round(float(w[-1]), 2)})


            try:
                from ipywidgets import interact, FloatSlider, IntSlider
                interact(
                    plot_compound,
                    rate=FloatSlider(value=0.03, min=-0.10, max=0.15, step=0.01, description="年收益率"),
                    horizon=IntSlider(value=20, min=1, max=50, step=1, description="年数"),
                )
            except ImportError:
                print("未安装ipywidgets：请执行 python -m pip install ipywidgets")
                plot_compound()
            """
        ),
        md(
            """
            ## 0.13 调试：先读错误，再改代码

            下面故意调用一个不存在的变量。`try/except`让Notebook继续运行，并把异常类型保存为普通文本。
            """
        ),
        code(
            """
            try:
                wrong_result = initial_money * (1 + annual_rate) ** years
            except Exception as error:
                print("异常类型：", type(error).__name__)
                print("异常信息：", error)
                print("诊断：代码使用了尚未定义的变量initial_money。")
            """
        ),
        md(
            """
            **AI辅助调试的提问模板**

            > 请解释异常类型、指出最小修改，并说明如何用一个边界条件验证修复。不要重写整段代码。

            这种问法要求AI解释原因，而不是直接替你重写答案。
            """
        ),
        md(
            """
            ## 0.14 练习：定期追加储蓄

            每年末追加相同金额时，财富递推为：

            $$W_{t+1}=W_t(1+r)+C$$

            其中 $C$ 是每年末追加金额。请补全函数。先用两年、0%收益率手算，再运行测试。
            """
        ),
        code(
            """
            def saving_path(initial, annual_contribution, annual_rate, years):
                # 返回从第0年到第years年的财富数组。
                # TODO：创建初始财富，并逐年完成“先增长、后追加”的递推
                # 提示：结果长度应为 years + 1
                return None
            """,
            tags=["exercise"],
        ),
        code(
            """
            # 完成函数后运行本格。未完成时只提示，不中断整章。
            student_result = saving_path(1_000, 100, 0.00, 2)
            if student_result is None:
                print("练习尚未完成。")
            else:
                expected = np.array([1_000, 1_100, 1_200], dtype=float)
                print("你的结果：", student_result)
                print("基础测试通过：", np.allclose(student_result, expected))
            """,
            tags=["exercise-test"],
        ),
        md(
            """
            ### 我的解释

            请说明：为什么本题的“追加发生在年末”必须写进模型假设？如果改成每年年初追加，结果会发生什么变化？

            <!-- 在这里填写；完成前AI不要代答 -->

            ### AI批改区

            <!-- 保存后让Codex检查：递推顺序、结果长度、边界条件和文字解释。 -->
            """
        ),
        md(
            """
            ## 本章压缩总结

            - 变量必须带有清晰的金融含义和单位；
            - 列表适合保存通用对象，NumPy数组适合数值向量化；
            - 循环适合解释过程，向量化适合表达整组数学关系；
            - 函数应明确输入、输出、假设和异常；
            - 图形用于比较模型行为，不替代数值检查；
            - 可复现Notebook必须能够从零按顺序运行。

            **参考**

            - Python官方教程：https://docs.python.org/3/tutorial/
            - NumPy Quickstart：https://numpy.org/doc/stable/user/quickstart.html
            - Matplotlib教程：https://matplotlib.org/stable/tutorials/index.html
            - Jupyter Widgets：https://ipywidgets.readthedocs.io/
            """
        ),
    ],
    "第0章 Python量化实验室快速恢复",
)


chapter1 = notebook(
    [
        md(
            r"""
            # 第1章 金融、量化与Python初体验

            > **故事起点**：大学生小林有10,000元暂时不用。他可以放在现金账户、借给某个可靠发行者、购买企业的一小部分，或者通过基金持有一篮子资产。不同选择到底改变了什么？

            **三条学习线**

            - 金融：储蓄者、融资者、现金、债券、股票、基金、收益和风险。
            - 数学：现金流、简单收益率、情景和期望的直觉。
            - Python：字典、DataFrame、函数、条件、随机数组、图表和动画。

            **完成标准**

            1. 能用自己的话区分股票和债券；
            2. 能画出简单现金流时间轴；
            3. 能计算持有期收益率；
            4. 能解释“期望终值相近”为什么不等于“风险相同”；
            5. 能修改模拟假设并记录结论。

            > 所有模拟参数均为教学假设，不代表任何资产的未来表现。
            """
        ),
        md(
            """
            ## AI学习状态

            当前进度：第1章开始

            已掌握：第0章的变量、循环、函数和NumPy基础（需根据实际情况修改）

            仍然薄弱：待填写

            常见错误：待填写

            下一步：先回答情境问题，再运行模型。
            """
        ),
        code(
            """
            import numpy as np
            import pandas as pd
            import matplotlib.pyplot as plt
            from matplotlib.animation import FuncAnimation
            from IPython.display import HTML, display

            plt.rcParams["figure.figsize"] = (8, 4.5)
            plt.rcParams["axes.grid"] = True
            plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "PingFang SC", "SimHei", "DejaVu Sans"]
            plt.rcParams["axes.unicode_minus"] = False

            rng = np.random.default_rng(20260711)
            print("实验随机种子：20260711")
            """
        ),
        md(
            """
            ## 1.1 金融首先是“跨时间交换资源”

            有些人今天有暂时不用的钱，有些人今天需要钱来读书、买房、建设工厂或修建公共设施。金融系统帮助资金从**盈余方**流向**资金需求方**，同时约定未来的权利、义务和风险。

            一个最小金融系统包含：

            | 角色 | 今天 | 未来 | 主要问题 |
            |---|---|---|---|
            | 储蓄者/投资者 | 提供资金 | 希望收回本金并获得回报 | 会不会亏？何时能取回？ |
            | 企业/政府/个人融资者 | 获得资金 | 偿还债务或分享企业成果 | 资金成本是多少？ |
            | 银行、交易所、基金等中介 | 连接双方、提供交易与管理 | 收取费用并承担相应责任 | 如何控制信用、流动性和操作风险？ |

            ### 先想后算

            如果小林把10,000元借给同学一年，约定一年后收回10,500元：

            1. 今天谁是资金提供者？
            2. 未来的10,500元中，哪部分是本金，哪部分是回报？
            3. 如果同学无法偿还，这属于什么直观风险？

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            r"""
            ## 1.2 用现金流时间轴描述承诺

            站在小林的角度，今天付出10,000元记为负现金流，一年后收到10,500元记为正现金流：

            $$CF_0=-10{,}000,\qquad CF_1=+10{,}500$$

            正负号取决于**观察者视角**。站在借款人角度，符号正好相反。
            """
        ),
        code(
            """
            cash_flows = {0: -10_000, 1: 10_500}

            fig, ax = plt.subplots(figsize=(8, 3))
            ax.axhline(0, color="black", linewidth=1)
            for time, amount in cash_flows.items():
                color = "#16a34a" if amount > 0 else "#dc2626"
                ax.vlines(time, 0, amount, color=color, linewidth=4)
                ax.scatter(time, amount, color=color, s=80)
                ax.text(time, amount, f" {amount:+,.0f}元", va="bottom" if amount > 0 else "top")

            ax.set(title="站在资金提供者角度的现金流时间轴", xlabel="年份", ylabel="现金流（元）")
            ax.set_xticks([0, 1])
            plt.show()
            print(cash_flows)
            """
        ),
        md(
            """
            **Python提示：字典**

            `{0: -10000, 1: 10500}`用“键:值”保存数据。这里键是时间，值是该时点现金流。字典适合表达少量有明确标签的项目；以后大量时间序列会使用pandas。

            **量化编程警告：先确定视角和符号**

            同一笔交易在双方账上符号相反。如果不写清视角，净现值、盈亏和风险计算都会混乱。
            """
        ),
        md(
            r"""
            ## 1.3 第一个收益率

            买入价格为 $P_0$，卖出价值为 $P_1$，期间暂不考虑其他现金流，则持有期简单收益率为：

            $$R=\frac{P_1-P_0}{P_0}=\frac{P_1}{P_0}-1$$

            它回答的是：**相对于最初投入，财富变化了多大比例？**
            """
        ),
        code(
            """
            initial_value = 10_000
            final_value = 10_500
            holding_return = final_value / initial_value - 1

            print(f"绝对增加：{final_value - initial_value:.2f}元")
            print(f"持有期收益率：{holding_return:.2%}")
            """
        ),
        md(
            """
            ### 手算检查

            如果初始投入改为20,000元、最终价值为21,000元：绝对增加变成多少？收益率是否改变？

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 1.4 四类常见选择：现金、债券、股票、基金

            ### 现金或存款类工具

            主要作用是支付、保存流动性和满足近期支出。它并非“完全没有风险”：购买力可能被通胀侵蚀，不同账户也有不同信用、期限和规则。

            ### 债券

            债券本质上是债务证券。投资者把钱借给政府、企业等发行者，发行者约定支付利息并在到期时偿还本金。主要风险包括利率、信用和流动性风险。

            ### 股票

            股票代表企业所有权的一部分。回报可能来自股息和价格上涨，但没有固定偿还承诺；企业经营和市场估值都会影响结果。

            ### 基金

            基金把许多投资者的资金汇集起来，持有股票、债券或其他资产。基金是一种组织与持有方式，不自动等于低风险；风险取决于底层资产、策略、费用和约束。

            **来源提示**：以上入门定义可对照 Investor.gov 的 Stocks、Bonds 和 Mutual Funds 页面。中国市场的具体规则将在后续章节改用中国证监会、交易所和基金业协会资料核实。
            """
        ),
        code(
            """
            products = pd.DataFrame(
                {
                    "核心关系": ["持有可支付资产", "把钱借给发行者", "拥有企业的一部分", "共同持有一篮子资产"],
                    "典型现金流": ["取用本金/利息", "利息与本金偿还", "股息与出售价值", "分配收益与份额赎回/交易价值"],
                    "主要不确定性": ["通胀、规则、信用", "利率、信用、流动性", "经营、估值、市场", "取决于底层资产、费用和策略"],
                },
                index=["现金/存款类", "债券", "股票", "基金"],
            )
            products
            """
        ),
        md(
            """
            ### 判断练习

            下面说法是否正确？请先写理由，再让AI检查。

            1. 买入企业债券后，投资者成为企业所有者。
            2. 股票价格上涨是股票投资者唯一可能的回报来源。
            3. 基金一定比单只股票安全。
            4. 现金没有任何风险。

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 1.5 什么是量化分析？

            “量化”不是“用复杂模型猜涨跌”。一个完整的量化问题至少包含：

            1. **问题**：要比较、解释、预测还是决策？
            2. **变量**：价格、现金流、收益率、期限、风险分别如何定义？
            3. **假设**：哪些条件被简化或固定？
            4. **数据**：数据何时可知、来源和单位是什么？
            5. **模型**：变量如何联系？
            6. **验证**：手算、边界条件、样本外结果是否支持结论？
            7. **决策边界**：交易成本、约束和模型失效如何处理？

            本章的模型很简单，但已经必须遵守这七步。
            """
        ),
        md(
            """
            ## 1.6 情景不是预测：先建立一个两状态模型

            假设某项投资一年后只有两个教学情景：

            - 较好情景：10,000元变成12,000元；
            - 较差情景：10,000元变成8,000元。

            假设两个情景各占50%。这不是对真实股票的预测，只是用最小模型理解“平均结果”和“结果分散”。
            """
        ),
        code(
            """
            scenario_values = np.array([12_000, 8_000])
            probabilities = np.array([0.5, 0.5])

            expected_value = np.sum(scenario_values * probabilities)
            scenario_returns = scenario_values / 10_000 - 1

            print("情景终值：", scenario_values)
            print("情景收益率：", scenario_returns)
            print("期望终值：", expected_value)
            print("期望不等于必然发生：", expected_value not in scenario_values)
            """
        ),
        md(
            r"""
            期望终值为

            $$E[W_1]=\sum_i p_iW_i$$

            这里期望恰好等于10,000元，但实际情景中没有一个结果等于10,000元。

            ### 观察问题

            1. “期望没有亏损”能否推出“这一年不会亏损”？
            2. 如果较差情景改为2,000元，期望和风险分别如何变化？
            3. 这个模型遗漏了真实市场中的哪些可能性？

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 1.7 从两个情景扩展到许多随机路径

            我们构造三种纯教学资产：

            - “现金类”：年收益波动很小；
            - “债券类”：平均收益和波动居中；
            - “股票类”：平均收益假设较高，但波动明显更大。

            为保持初学者可读性，本章暂用正态分布生成年收益。真实金融收益可能厚尾、偏斜并随时间变化，第7章会专门修正这一简化。
            """
        ),
        code(
            """
            assumptions = pd.DataFrame(
                {
                    "mean_return": [0.02, 0.04, 0.07],
                    "volatility": [0.005, 0.06, 0.18],
                },
                index=["现金类", "债券类", "股票类"],
            )
            assumptions.style.format("{:.1%}")
            """
        ),
        md(
            """
            **量化编程警告：参数是模型输入，不是事实**

            上表数值是为了观察差异而设置的教学假设。严谨研究必须说明估计区间、数据来源、样本时期和不确定性，不能把历史均值直接当成未来承诺。
            """
        ),
        code(
            """
            def simulate_wealth(initial, mean_return, volatility, years, paths, rng):
                # 用独立正态年收益生成教学性财富路径。
                returns = rng.normal(mean_return, volatility, size=(years, paths))
                wealth = np.empty((years + 1, paths))
                wealth[0] = initial
                wealth[1:] = initial * np.cumprod(1 + returns, axis=0)
                return wealth, returns


            simulation_rng = np.random.default_rng(42)
            simulated = {}
            for asset, row in assumptions.iterrows():
                wealth, returns = simulate_wealth(
                    initial=10_000,
                    mean_return=row["mean_return"],
                    volatility=row["volatility"],
                    years=10,
                    paths=2_000,
                    rng=simulation_rng,
                )
                simulated[asset] = {"wealth": wealth, "returns": returns}

            print({name: value["wealth"].shape for name, value in simulated.items()})
            """
        ),
        md(
            """
            **Python提示：二维数组与`axis`**

            `returns`形状是`(年份, 路径)`。`np.cumprod(..., axis=0)`沿年份方向累计，使每一列成为一条财富路径。量化代码中必须先写清每个轴代表什么。
            """
        ),
        code(
            """
            fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

            for ax, (asset, result) in zip(axes, simulated.items()):
                wealth = result["wealth"]
                ax.plot(wealth[:, :40], alpha=0.25, linewidth=1)
                ax.plot(np.median(wealth, axis=1), color="black", linewidth=2, label="中位数")
                ax.axhline(10_000, color="gray", linestyle="--", linewidth=1)
                ax.set(title=asset, xlabel="年份")
                ax.legend()

            axes[0].set_ylabel("财富（元）")
            fig.suptitle("相同初始资金、不同假设下的部分模拟路径")
            plt.tight_layout()
            plt.show()
            """
        ),
        md(
            """
            ### 观察问题

            1. 哪类资产的路径最集中？哪类最分散？
            2. 股票类的平均收益假设较高，是否意味着每条股票路径都优于现金？
            3. 为什么图中只画40条路径，而统计时保留2000条？

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        code(
            """
            summary_rows = []
            for asset, result in simulated.items():
                terminal = result["wealth"][-1]
                summary_rows.append(
                    {
                        "资产": asset,
                        "平均终值": terminal.mean(),
                        "中位终值": np.median(terminal),
                        "10%分位": np.quantile(terminal, 0.10),
                        "90%分位": np.quantile(terminal, 0.90),
                        "低于本金的比例": np.mean(terminal < 10_000),
                    }
                )

            summary = pd.DataFrame(summary_rows).set_index("资产")
            display(summary.style.format({
                "平均终值": "{:,.0f}",
                "中位终值": "{:,.0f}",
                "10%分位": "{:,.0f}",
                "90%分位": "{:,.0f}",
                "低于本金的比例": "{:.1%}",
            }))
            """
        ),
        md(
            """
            ### 从图到证据

            路径图帮助建立直觉，汇总表帮助精确比较。请用表中至少两个指标说明“高平均终值”和“高不确定性”可以同时存在。

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 1.8 动画：不确定性如何逐年展开

            动画只展示股票类的20条路径。播放时观察：早期接近的路径如何随时间逐渐分散。动画下方另有普通文本摘要，便于AI检查。
            """
        ),
        code(
            """
            stock_paths = simulated["股票类"]["wealth"][:, :20]
            years_axis = np.arange(stock_paths.shape[0])

            fig, ax = plt.subplots(figsize=(8, 4.5))
            ax.set(xlim=(0, years_axis[-1]),
                   ylim=(0, stock_paths.max() * 1.05),
                   xlabel="年份", ylabel="财富（元）",
                   title="股票类教学模型：财富路径逐年展开")
            lines = [ax.plot([], [], alpha=0.55)[0] for _ in range(stock_paths.shape[1])]

            def update(frame):
                for index, line in enumerate(lines):
                    line.set_data(years_axis[: frame + 1], stock_paths[: frame + 1, index])
                return lines

            animation = FuncAnimation(fig, update, frames=len(years_axis), interval=350, blit=True)
            plt.close(fig)
            display(HTML(animation.to_jshtml()))
            print({
                "displayed_paths": int(stock_paths.shape[1]),
                "years": int(years_axis[-1]),
                "min_terminal": round(float(stock_paths[-1].min()), 2),
                "max_terminal": round(float(stock_paths[-1].max()), 2),
            })
            """
        ),
        md(
            """
            ## 1.9 交互实验：修改股票类假设

            拖动“平均年收益”和“年波动率”。每次更新都使用同一个随机种子，使差异主要来自参数，而不是重新抽到另一批随机数。
            """
        ),
        code(
            """
            def terminal_distribution(mean_return=0.07, volatility=0.18):
                local_rng = np.random.default_rng(7)
                wealth, _ = simulate_wealth(10_000, mean_return, volatility, 10, 5_000, local_rng)
                terminal = wealth[-1]

                fig, ax = plt.subplots()
                ax.hist(terminal, bins=50, color="#2563eb", alpha=0.75)
                ax.axvline(np.median(terminal), color="black", linewidth=2, label="中位数")
                ax.axvline(10_000, color="#dc2626", linestyle="--", label="初始本金")
                ax.set(title="10年终值分布（教学模型）", xlabel="终值（元）", ylabel="模拟次数")
                ax.legend()
                plt.show()

                print({
                    "mean_return": mean_return,
                    "volatility": volatility,
                    "median_terminal": round(float(np.median(terminal)), 2),
                    "loss_probability": round(float(np.mean(terminal < 10_000)), 4),
                })


            try:
                from ipywidgets import interact, FloatSlider
                interact(
                    terminal_distribution,
                    mean_return=FloatSlider(value=0.07, min=-0.05, max=0.15, step=0.01, description="平均收益"),
                    volatility=FloatSlider(value=0.18, min=0.01, max=0.50, step=0.01, description="波动率"),
                )
            except ImportError:
                print("未安装ipywidgets：请执行 python -m pip install ipywidgets")
                terminal_distribution()
            """
        ),
        md(
            """
            ### 参数实验记录

            至少尝试三组参数，并记录“中位终值”和“低于本金的比例”。不要把模拟概率解释成真实世界概率。

            | 平均收益假设 | 波动率假设 | 中位终值 | 低于本金的比例 | 我的解释 |
            |---:|---:|---:|---:|---|
            | | | | | |
            | | | | | |
            | | | | | |

            ### 我的回答

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 1.10 Python练习：比较一个自定义情景

            请完成函数，使它接收初始金额和一组可能终值，返回每个情景的收益率。先手算`[9000, 10000, 11000]`相对于10000元的结果。
            """
        ),
        code(
            """
            def scenario_returns(initial, final_values):
                # 返回每个终值相对于initial的简单收益率数组。
                # TODO：把final_values转换为NumPy数组并计算收益率
                return None
            """,
            tags=["exercise"],
        ),
        code(
            """
            result = scenario_returns(10_000, [9_000, 10_000, 11_000])
            if result is None:
                print("练习尚未完成。")
            else:
                expected = np.array([-0.10, 0.00, 0.10])
                print("你的结果：", result)
                print("基础测试通过：", np.allclose(result, expected))
            """,
            tags=["exercise-test"],
        ),
        md(
            """
            ### AI批改请求

            保存Notebook后，可以让Codex检查：

            > 请只检查第1.10节。我是否正确处理了列表输入、除法顺序和返回类型？再给我一个`initial=0`的边界问题，但先不要直接提供最终实现。

            ### 我的修正记录

            <!-- 保留第一次错误和修正原因 -->
            """
        ),
        md(
            """
            ## 1.11 小型研究任务：给小林一份“不做推荐”的比较报告

            从本章的现金、债券、股票和基金概念中任选三类，完成一页观察报告：

            1. 每类资产代表什么权利或关系？
            2. 可能产生哪些现金流？
            3. 至少列出两类风险；
            4. 本章模拟使用了哪些明显简化？
            5. 为了做真实比较，还需要哪些数据？

            不要写“应该买某资产”，也不要把教学参数当成预期收益。

            ### 我的报告

            <!-- 在这里填写；完成前AI不要代答 -->
            """
        ),
        md(
            """
            ## 本章压缩总结

            - 金融系统连接今天的资金与未来的权利、义务和风险；
            - 债券通常代表债权，股票代表所有权，基金代表共同持有的一篮子资产；
            - 收益率必须相对于初始投入定义；
            - 期望是按概率加权的平均，不是必然发生的结果；
            - 模拟用于研究“如果假设成立会怎样”，不是预测或承诺；
            - 量化研究必须写清问题、变量、假设、数据、模型、验证和边界；
            - Python代码必须同时接受金融逻辑和数值测试。

            **参考入口**

            - Investor.gov 投资入门：https://www.investor.gov/introduction-investing
            - Stocks：https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks
            - Bonds：https://www.investor.gov/introduction-investing/investing-basics/investment-products/bonds-or-fixed-income-products/bonds
            - Mutual Funds：https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-funds-etfs/mutual-funds
            - NumPy随机抽样：https://numpy.org/doc/stable/reference/random/index.html
            """
        ),
    ],
    "第1章 金融、量化与Python初体验",
)


for filename, nb in [
    ("00_Python量化实验室.ipynb", chapter0),
    ("01_金融量化与Python初体验.ipynb", chapter1),
]:
    nbf.write(nb, ROOT / filename)
    print(f"wrote {filename}: {len(nb.cells)} cells")
