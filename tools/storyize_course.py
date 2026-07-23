#!/usr/bin/env python3
"""把第0—8章的教案式提示改写为连续项目故事。

脚本只会修改章首介绍、章首项目页、旧任务卡和明确登记的章末项目标题；
学生回答、代码、输出、附件及其余教学正文必须保持不变。
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "00_从c语言到python.ipynb",
    "01_金融与量化.ipynb",
    "02_现金流复利与贴现.ipynb",
    "03_债券与利率风险.ipynb",
    "04_股票基金与市场交易.ipynb",
    "05_金融数据与时间边界.ipynb",
    "06_收益率与财富路径.ipynb",
    "07_概率分布与抽样.ipynb",
    "08_风险度量与压力测试.ipynb",
]

TITLE_INTROS = {
    "00_从c语言到python.ipynb": """# 第0章 从c语言到python

你刚拿到一笔奖学金，想请你帮他比较几种安排。你已经学过C语言，不必从“什么是程序”重新开始；这一章只做一件事：把熟悉的变量、判断、循环和函数换成Python写法，并做出第一台财富计算器。""",
    "01_金融与量化.ipynb": """# 第1章 金融与量化

财富计算器已经能运行，但你发现自己还没回答最重要的问题：10,000元奖学金究竟可以放到哪里？你将和他一起追踪资金流向，把口头承诺画成现金流，再用Python比较不同选择。""",
    "02_现金流复利与贴现.ipynb": """# 第2章 现金流、复利与贴现

你的第一份比较报告遇到了麻烦：今天的10,000元、三年后的12,000元和毕业后的收入不能直接放在一起比较。于是他要为所有现金流装上一把共同的“时间尺”。""",
    "03_债券与利率风险.ipynb": """# 第3章 债券与利率风险

校园创新社团想借10,000元，承诺每年付一笔利息，到期归还本金。你没有立刻答应：这份未来付款合同今天值多少钱？市场利率改变后，旧合同为什么也会变价？""",
    "04_股票基金与市场交易.ipynb": """# 第4章 股票、基金与市场交易

研究完“把钱借给企业”，项目又转向另一种关系：成为企业很小的一部分所有者。即使决定买股票，仍要弄清指数、基金、买价、卖价和交易费用怎样改变真正成交的结果。""",
    "05_金融数据与时间边界.ipynb": """# 第5章 金融数据与时间边界

你下载了一张看起来整整齐齐的价格表，准备计算收益。你却发现里面混着重复日期、缺失值、拆股和尚未公布的数据。现在你们要像数据侦探一样，先保护现场，再决定哪些记录可以进入研究。""",
    "06_收益率与财富路径.ipynb": """# 第6章 收益率与财富路径

清洗后的价格终于可以使用，但“价格涨了多少”仍不等于“你赚了多少”。股息、复合、年化和追加资金会把同一列价格变成不同的财富故事。""",
    "07_概率分布与抽样.ipynb": """# 第7章 概率、分布与抽样

历史数据只记录了一条已经发生的路。你想讨论未来，却不愿把猜测伪装成预测。于是你们先写出一个透明的三情景模型，再用反复抽样观察模型可能产生什么。""",
    "08_风险度量与压力测试.ipynb": """# 第8章 风险度量与压力测试

你拿到两项平均收益相近的方案，却发现“风险”没有一个万能答案。你们将用波动、回撤、尾部、压力情景和资本存续五副镜头检查同一项投资。""",
}

OPENINGS = {
    "00_从c语言到python.ipynb": """### 量化研究项目：先造一台财富计算器

![C语言经验迁移到Python量化实验流程](assets/course/00_c_to_python_pipeline.png)

你先给出一个最小委托：输入本金、收益率和年份，程序要返回每年的财富，还要能检查明显不合理的输入。你会先用熟悉的C语言思路拆解，再逐步换成Python、NumPy和图形。

这张概念图只说明工作关系，不承载精确数值。**本章交付物是一台可手算核对的财富计算器**；下一章，你会真的拿它比较自己的10,000元奖学金。""",
    "01_金融与量化.ipynb": """### 量化研究项目：10,000元该去哪里

![从奖学金出发比较金融选择](assets/course/01_financial_choices.png)

课程不会在开头堆叠一串资产定义，而是先追问钱从谁流向谁，再依次进入现金、借款、债券、股票和基金；每遇到一种选择，就把权利、现金流和风险记进同一份报告。

概念图只帮助辨认关系，不代表真实收益。**本章交付物是一页资产比较报告**；下一章将解决报告中“不同时点金额不能直接比较”的问题。""",
    "02_现金流复利与贴现.ipynb": """### 量化研究项目：给现金流装上时间尺

![增长、贴现与多期现金流的时间价值](assets/course/02_time_value.png)

你从100元、5%和3年这个可以手算的例子出发，先在今天与未来之间来回换算，再处理多笔现金流、通胀和一项校园实践计划。

概念图只解释增长与贴现的方向，不提供精确数值。**本章交付物是一台现金流比较器**；下一章会用它给一份债券合同定价。""",
    "03_债券与利率风险.ipynb": """### 量化研究项目：要不要接受这份借款合同

![债券现金流、贴现与利率风险关系](assets/course/03_bond_mechanism.png)

社团给出的合同写着面值、票息和到期日。你要先列出每一笔未来付款，再判断今天的合理价格；随后他会让市场利率上下变化，看看合同价格承受多大冲击。

概念图只说明合同关系。**本章交付物是一份债券报价与压力测试**；下一章将把债权人与股东的权利放在一起比较。""",
    "04_股票基金与市场交易.ipynb": """### 量化研究项目：完成第一笔虚拟交易

![企业、股票、指数基金与交易市场关系](assets/course/04_market_mechanism.png)

你先辨认股东拥有什么，再把多只股票合成指数，最后走进一个简化订单簿。屏幕上的价格不是自动成交价：订单大小、买卖价差和费用都会留下痕迹。

概念图不代表真实市场报价。**本章交付物是一张可解释的虚拟成交记录**；下一章将审查这些行情和成交数据是否可信。""",
    "05_金融数据与时间边界.ipynb": """### 量化研究项目：抢救一张有问题的价格表

![金融数据从来源到可研究数据的审计流程](assets/course/05_data_pipeline.png)

你先保存原始表，再逐项寻找乱序、重复、缺失、复权和发布时间问题。每一次删除、填补或对齐都必须留下理由，不能让一行清洗代码悄悄改写历史。

概念图只说明审计流程。**本章交付物是原始表、隔离表、清洗表和审计记录**；下一章只使用通过检查的数据计算收益。""",
    "06_收益率与财富路径.ipynb": """### 量化研究项目：10,000元到底变成了多少

![价格、收益率、复合与财富路径关系](assets/course/06_returns_wealth.png)

项目从100→110→99这个小例子开始，分清价格收益、总回报、算术平均、几何增长和年化。加入股息或定投以后，还要说明现金流发生在什么时候。

概念图不提供任何收益数字。**本章交付物是一张收益口径审计卡和财富路径**；下一章会把一条历史路径扩展为许多假设情景。""",
    "07_概率分布与抽样.ipynb": """### 量化研究项目：把不确定性写成透明模型

![可能结果、概率模型、抽样与统计量关系](assets/course/07_probability_sampling.png)

你先写下亏20%、赚5%和赚30%三张情景卡，并明确每个概率只是教学假设。之后你们反复抽样，观察样本均值、分位数和尾部为什么会随样本改变。

概念图只说明“模型—抽样—统计量”的关系。**本章交付物是一份随机实验报告**；下一章将从这些样本中提取不同风险视角。""",
    "08_风险度量与压力测试.ipynb": """### 量化研究项目：给资产做一次风险体检

![波动、回撤、尾部、压力与杠杆风险视角](assets/course/08_risk_lenses.png)

同一项资产会依次接受五项检查：平时有多颠簸、从高点跌了多少、最差一小部分有多严重、假设危机发生会怎样，以及使用杠杆后还能否继续留在场内。

概念图只是检查清单。**本章交付物是一份写明期限、单位、样本和遗漏风险的体检报告**；第9章将用它比较单项资产与多资产组合。""",
}

PROJECT_HEADING_RENAMES = {
    "03_债券与利率风险.ipynb": ("本章总结与小项目", "项目交付：债券压力测试"),
    "04_股票基金与市场交易.ipynb": ("本章总结与小项目", "项目交付：第一笔虚拟交易"),
    "05_金融数据与时间边界.ipynb": ("本章总结与小项目", "项目交付：把脏数据变成可审计数据"),
    "06_收益率与财富路径.ipynb": ("本章总结与小项目", "项目交付：说明10,000元究竟怎样变化"),
    "07_概率分布与抽样.ipynb": ("本章总结与小项目", "项目交付：随机实验报告"),
    "08_风险度量与压力测试.ipynb": ("本章总结与小项目", "项目交付：五镜头风险体检"),
}

SPECIAL_SOURCE_REPLACEMENTS = {
    "### AI批改请求": "### 让AI扮演一位挑错的同学",
    "### 本章导航与学习路线": "### 量化研究项目",
    "### 运行前后的解释": "### 把数字讲明白",
    "### 观察问题": "### 停下来核对",
    "### 思考": "### 继续追问",
    "### 读图卡：": "### 怎样读这张图：",
}

H2_RE = re.compile(r"^##\s+(?!#)(.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"\*\*([^*]+)\*\*：\s*(.+)")


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def set_source(cell: dict, source: str) -> None:
    cell["source"] = source.rstrip() + "\n"


def signature(cell: dict) -> str:
    return json.dumps(cell, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def h2_heading(cell: dict) -> str | None:
    if cell.get("cell_type") != "markdown":
        return None
    match = H2_RE.search(source_text(cell))
    return match.group(1) if match else None


def clean_phrase(text: str) -> str:
    replacements = {
        "学习状态": "研究日志",
        "分别标记金融、数学、Python三条线的当前状态": "在金融、数学、Python三栏各写一句目前能解释的事",
        "状态用于安排练习": "这份记录只用于安排下一步练习",
        "这不是能力评分": "这不是考试评分",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip().rstrip("。")


def parse_card(source: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in source.splitlines():
        line = raw_line.lstrip("> ").strip()
        match = FIELD_RE.search(line)
        if match:
            fields[match.group(1).replace(" ", "")] = clean_phrase(match.group(2))
    return fields


def first_value(fields: dict[str, str], *keys: str) -> str:
    for key in keys:
        compact = key.replace(" ", "")
        if compact in fields:
            return fields[compact]
    return ""


def without_first(text: str) -> str:
    for prefix in ("先", "请先"):
        if text.startswith(prefix):
            return text[len(prefix) :]
    return text


def story_title(anchor: str | None) -> str:
    if anchor == "AI学习状态" or anchor is None:
        return "故事开场：你带着上一份档案回来"
    if any(word in anchor for word in ("练习", "研究任务")):
        return "轮到你接手代码"
    if any(word in anchor for word in ("总结", "作业", "项目交付")):
        return "把成果放进你的研究档案"
    return "你的下一步"


def story_from_card(source: str, anchor: str | None) -> str:
    fields = parse_card(source)
    prior = first_value(fields, "前置连接", "前置检索")
    question = first_value(fields, "核心问题")
    prediction = first_value(fields, "运行前预测", "先预测/再观察", "先预测，后运行")
    hint = first_value(fields, "Python/数学提示", "Python / 数学提示", "手算 / Python提示")
    boundary = first_value(fields, "解释边界", "结果解释重点")

    paragraphs: list[str] = [f"### {story_title(anchor)}"]
    if prior and question:
        paragraphs.append(f"你把前面的线索带了过来：{prior}。接着他追问：**{question}**")
    elif question:
        paragraphs.append(f"你接着追问：**{question}**")
    elif prior:
        paragraphs.append(f"你把前面的线索带了过来：{prior}。")

    actions: list[str] = []
    if prediction:
        actions.append(f"动手前：{without_first(prediction)}。")
    if hint:
        actions.append(f"核对时：{without_first(hint)}。")
    if actions:
        paragraphs.append("".join(actions))
    if boundary:
        paragraphs.append(f"你还在报告旁边注明：{boundary}。")
    return "\n\n".join(paragraphs)


def polish_existing_bridge(source: str) -> str:
    """把第一版自动改写中仍显生硬的动作句改成自然短句。"""
    source = re.sub(
        r"运行代码前，你先([^\n]+?)；随后([^\n]+?)。(?=\n|$)",
        r"运行代码前，你先做一个判断：\1。核对时再使用这条线索：\2。",
        source,
    )
    source = source.replace("运行代码前，你先做一个判断：", "动手前：")
    source = source.replace("核对时再使用这条线索：", "核对时：")
    source = source.replace("最后把这条边界写进研究日志：", "你还在报告旁边注明：")
    source = source.replace("把薄弱点填入研究日志", "把暂时说不清的地方记进研究日志")
    source = source.replace("记录为薄弱点", "记进研究日志")
    source = source.replace("把无法判断的字段记为薄弱点", "把暂时无法判断的字段记进研究日志")
    source = source.replace("查看本章导航", "查看章首的项目档案")
    source = source.replace("标记“能读懂、能修改、需要复习”三类状态", "把内容分成“能读懂、能修改、需要复习”三类")
    source = source.replace("状态要用实际运行、手算和边界测试作为证据", "这些判断要用实际运行、手算和边界测试作为证据")
    source = source.replace("？。", "？").replace("！。", "！")
    return source


def transform(path: Path) -> tuple[int, int, int]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    before_cells = copy.deepcopy(notebook["cells"])

    targets: set[str] = set()
    for index, cell in enumerate(before_cells):
        text = source_text(cell)
        heading = h2_heading(cell)
        if (
            index in (0, 1)
            or "任务卡" in text
            or heading == "AI学习状态"
            or cell.get("metadata", {}).get("course_role") == "story_bridge"
        ):
            targets.add(cell.get("id", f"index-{index}"))
        if path.name in PROJECT_HEADING_RENAMES:
            old, _ = PROJECT_HEADING_RENAMES[path.name]
            if heading == old:
                targets.add(cell.get("id", f"index-{index}"))
        if any(old in text for old in SPECIAL_SOURCE_REPLACEMENTS):
            targets.add(cell.get("id", f"index-{index}"))

    protected_before = {
        cell.get("id", f"index-{index}"): signature(cell)
        for index, cell in enumerate(before_cells)
        if cell.get("id", f"index-{index}") not in targets
    }

    new_cells: list[dict] = []
    current_h2: str | None = None
    removed = 0
    bridges = 0
    for index, original in enumerate(before_cells):
        cell = copy.deepcopy(original)
        heading = h2_heading(cell)
        if heading is not None:
            current_h2 = heading

        if heading == "AI学习状态":
            removed += 1
            continue

        text = source_text(cell)
        if index == 0:
            set_source(cell, TITLE_INTROS[path.name])
            cell.setdefault("metadata", {})["course_role"] = "chapter_story_intro"
        elif index == 1:
            set_source(cell, OPENINGS[path.name])
            cell.setdefault("metadata", {})["course_role"] = "chapter_project"
        elif "任务卡" in text and current_h2 == "AI学习状态":
            # 这张卡原本只服务于“AI学习状态”，没有项目内容，直接删除。
            removed += 1
            continue
        elif "任务卡" in text:
            set_source(cell, story_from_card(text, current_h2))
            metadata = cell.setdefault("metadata", {})
            for old_key in ("course_org_v2", "course_upgrade", "course_org_revision", "course_org_marker"):
                metadata.pop(old_key, None)
            metadata["course_role"] = "story_bridge"
            metadata["story_anchor"] = "chapter_start" if current_h2 == "AI学习状态" else current_h2
            bridges += 1
        elif (
            cell.get("metadata", {}).get("course_role") == "story_bridge"
            and cell.get("metadata", {}).get("story_anchor") == "chapter_start"
        ):
            removed += 1
            continue
        elif cell.get("metadata", {}).get("course_role") == "story_bridge":
            set_source(cell, polish_existing_bridge(text))
            metadata = cell.setdefault("metadata", {})
            for old_key in ("course_org_v2", "course_upgrade", "course_org_revision", "course_org_marker"):
                metadata.pop(old_key, None)
            metadata["story_anchor"] = current_h2 or "chapter_start"
            bridges += 1
        else:
            if path.name in PROJECT_HEADING_RENAMES:
                old, new = PROJECT_HEADING_RENAMES[path.name]
                if heading == old:
                    set_source(cell, text.replace(f"## {old}", f"## {new}", 1))
                    current_h2 = new
            for old, new in SPECIAL_SOURCE_REPLACEMENTS.items():
                if old in source_text(cell):
                    set_source(cell, source_text(cell).replace(old, new))

        new_cells.append(cell)

    protected_after = {
        cell.get("id", f"index-{index}"): signature(cell)
        for index, cell in enumerate(new_cells)
        if cell.get("id", f"index-{index}") in protected_before
    }
    if protected_after != protected_before:
        changed = sorted(
            key for key, value in protected_before.items() if protected_after.get(key) != value
        )
        raise AssertionError(f"{path.name}: 未授权单元被修改：{changed}")

    notebook["cells"] = new_cells
    notebook.setdefault("metadata", {})["course_story_revision"] = "pbl-story-v1"
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(before_cells), len(new_cells), bridges


def main() -> None:
    raise SystemExit(
        "此脚本属于旧版迁移流程，不能覆盖当前Notebook。"
        "如需调整课程文字，请使用 rewrite_course_plain_story.py。"
    )


if __name__ == "__main__":
    main()
