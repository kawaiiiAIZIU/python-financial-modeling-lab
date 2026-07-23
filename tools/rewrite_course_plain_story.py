#!/usr/bin/env python3
"""压缩第0—8章结构，并把说明文字改成简单、直接的项目故事。

保护范围：代码单元、输出、附件、公式、行内代码、数字、网址和学生作答。
本脚本会合并章首单元，把逐节故事写进知识点正文，并删除文末总结。
"""

from __future__ import annotations

import copy
import importlib.util
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

OPENINGS = {
    "00_从c语言到python.ipynb": """# 第0章 从c语言到python

这门课从已经学过的高等数学和C语言出发，逐步进入金融与量化。

本章先把变量、判断、循环和函数换成Python写法，再用NumPy处理一组数，并用图形检查结果。

![C语言经验迁移到Python量化实验流程](assets/course/00_c_to_python_pipeline.png)

这张图只说明步骤，不提供准确数字。最后，你要做出一台能用手算检查的财富计算器。下一章会用它比较10,000元奖学金的不同安排。""",
    "01_金融与量化.ipynb": """# 第1章 金融与量化

财富计算器已经能运行。现在项目面对一个新的问题：10,000元可以放在现金、债券、股票或基金中，这些选择应当怎样比较？

先看钱从谁流向谁，再把承诺写成现金流，并用Python比较收益和风险。

![从奖学金出发比较金融选择](assets/course/01_financial_choices.png)

这张图只说明金融关系，不代表真实收益。最后，你要完成一页资产比较报告。下一章会把不同日期的钱放到同一个时间点比较。""",
    "02_现金流复利与贴现.ipynb": """# 第2章 现金流、复利与贴现

把今天的10,000元、三年后的12,000元和毕业后的收入写在一起时，新的问题出现了：不同日期的钱不能直接比较。

先用100元、5%和3年做手算，再学习增长、贴现、通胀和多笔现金流。

![增长、贴现与多期现金流的时间价值](assets/course/02_time_value.png)

这张图只说明增长和贴现的方向，不提供准确数字。最后，你要做出一台现金流比较器。第3章会用它给债券定价。""",
    "03_债券与利率风险.ipynb": """# 第3章 债券与利率风险

校园创新社团提出借款10,000元，并承诺按时支付利息。项目需要判断：这份合同今天值多少钱，利率变化又会带来多大影响？

先列出每笔付款，再计算今天的价格，并检查利率变化带来的影响。

![债券现金流、贴现与利率风险关系](assets/course/03_bond_mechanism.png)

这张图只说明合同关系，不提供精确数值。最后，你要交出一份债券报价和压力测试。下一章会比较债权人与股东。""",
    "04_股票基金与市场交易.ipynb": """# 第4章 股票、基金与市场交易

债券分析结束后，项目转向股票。屏幕价格不一定等于最终成交价，因此还需要理解股权、指数、基金和订单簿。

先看股东拥有什么，再建立指数和基金，最后进入一个简单的订单簿。

![企业、股票、指数基金与交易市场关系](assets/course/04_market_mechanism.png)

这张图只说明交易关系，不代表真实报价。最后，你要留下一张能说明价差、滑点和费用的虚拟成交记录。下一章会检查这些数据是否可信。""",
    "05_金融数据与时间边界.ipynb": """# 第5章 金融数据与时间边界

项目下载了一张价格表，却发现其中包含重复日期、空值、拆股和尚未公布的数据。整齐的表格并不一定可信。

先保存原始表，再逐项检查问题，并写下每一次删除、填补和对齐的原因。

![金融数据从来源到可研究数据的审计流程](assets/course/05_data_pipeline.png)

这张图只说明检查顺序。最后，你要保存原始表、隔离表、清洗表和审计记录。下一章只使用通过检查的数据。""",
    "06_收益率与财富路径.ipynb": """# 第6章 收益率与财富路径

数据通过检查后，价格涨跌看似容易计算；但股息、复合和追加资金会得到不同结果。项目需要说明10,000元究竟怎样变化。

先手算100→110→99，再比较价格收益、总回报、平均数、年化和定投。

![价格、收益率、复合与财富路径关系](assets/course/06_returns_wealth.png)

这张图不提供收益数字。最后，你要交出一张收益口径卡和一条财富路径。下一章会把一条历史路径扩展为许多假设情景。""",
    "07_概率分布与抽样.ipynb": """# 第7章 概率、分布与抽样

第6章只记录了一条已经发生的财富路径。为了讨论未来的不确定性，项目需要区分透明假设、随机抽样和事实预测。

先写下亏20%、赚5%和赚30%三种结果，再反复抽样，观察平均数、分位数和尾部怎样变化。

![可能结果、概率模型、抽样与统计量关系](assets/course/07_probability_sampling.png)

这张图只说明模型、抽样和统计量之间的关系。最后，你要交出一份随机实验报告。下一章会用它检查风险。""",
    "08_风险度量与压力测试.ipynb": """# 第8章 风险度量与压力测试

第7章展示了许多可能结果。两项方案的平均收益可能接近，但财富路径和失败方式仍然不同，因此只看平均数还不够。

先看波动和回撤，再检查尾部损失、压力情景和杠杆。

![波动、回撤、尾部、压力与杠杆风险视角](assets/course/08_risk_lenses.png)

这张图只说明五种检查方法。最后，你要交出一份写明期限、单位、样本和遗漏风险的体检报告。第9章会比较单项资产和多资产组合。""",
}

TRANSITION_REPLACEMENTS = {
    "逐档圈出300股和随后500股": "逐档圈出300股，再圈出后面的500股",
    "与此同时": "同时",
    "在此基础上": "然后",
    "首先": "先",
    "随后": "然后",
    "最终": "最后",
    "因此": "所以",
    "然而": "但是",
    "此外": "还有",
    "由此": "所以",
    "进而": "再",
    "从而": "所以",
    "换言之": "也就是说",
    "并非": "不是",
    "无需": "不用",
    "仅仅": "只",
    "仍然": "还是",
    "仍未": "还没有",
    "尚未": "还没有",
    "不得": "不能",
    "核验": "检查",
    "可核验": "可以检查",
    "间隔检索": "先回想",
    "假设透明": "把假设写清楚",
    "分栏": "分开写",
    "不能脱离": "要结合",
    "复现从原始表到可用表的每个决定": "按相同步骤得到同一张可用表",
    "复现": "重复得到",
    "显式": "写清楚",
    "隐式": "没有写出",
    "承载精确数值": "提供准确数字",
    "不承载精确数据": "不提供准确数字",
    "不承载精确数值": "不提供准确数字",
    "解释边界": "不能说明什么",
    "结果解释重点": "结果要说明",
    "统一时间标尺": "放到同一个时间点比较",
    "脆弱性": "容易出问题的地方",
    "非稳定性": "会随时间变化",
    "复用": "再用",
    "映射成": "对应成",
    "取决于": "取决于",
}

ANSWER_MARKERS = ("### 我的回答", "### 我的解释", "### 我的报告")
H2_RE = re.compile(r"^##\s+(?!#)(.+?)\s*$", re.MULTILINE)
PROTECTED_RE = re.compile(
    r"```.*?```|`[^`\n]+`|\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)",
    re.DOTALL,
)
URL_RE = re.compile(r"https?://[^\s)>]+")
NUMBER_RE = re.compile(r"(?<![A-Za-z_])[-+]?\d[\d,]*(?:\.\d+)?%?")

PROJECT_SOURCE_HEADINGS = {
    "项目交付：债券压力测试": "本章总结与小项目",
    "项目交付：第一笔虚拟交易": "本章总结与小项目",
    "项目交付：把脏数据变成可审计数据": "本章总结与小项目",
    "项目交付：说明10,000元究竟怎样变化": "本章总结与小项目",
    "项目交付：随机实验报告": "本章总结与小项目",
    "项目交付：五镜头风险体检": "本章总结与小项目",
}

DISPLAY_HEADING_RENAMES = {
    "0.5 函数：无需声明参数和返回值类型": "0.5 函数：不用先写参数和返回值类型",
    "5.6 最危险的错误：把发布日期之前的数据用于决策": "5.6 最危险的错误：提前使用还没公布的数据",
    "5.7 数据血缘：让未来的自己知道数据从哪里来": "5.7 数据血缘：记清数据从哪里来",
    "8.5 滚动风险揭示非稳定性": "8.5 滚动风险会随时间变化",
}

SPEC_SOURCE_HEADINGS = {
    **PROJECT_SOURCE_HEADINGS,
    **{current: old for old, current in DISPLAY_HEADING_RENAMES.items()},
}


def load_local_module(filename: str, module_name: str):
    path = ROOT / "tools" / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法读取维护脚本：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_old_card(source: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in source.splitlines():
        line = raw_line.lstrip("> ").strip()
        match = re.search(r"\*\*([^*]+)\*\*：\s*(.+)", line)
        if match:
            fields[match.group(1).replace(" ", "")] = match.group(2).strip()
    return {
        "prior": fields["前置连接"],
        "question": fields["核心问题"],
        "prediction": fields["先预测/再观察"],
        "hint": fields["Python/数学提示"],
        "boundary": fields["结果解释重点"],
    }


def load_task_specs() -> dict[str, dict[str, dict[str, str]]]:
    result: dict[str, dict[str, dict[str, str]]] = {}

    early = load_local_module("organize_chapters_00_02.py", "course_cards_00_02")
    for filename, cards in early.TASKS.items():
        result[filename] = {}
        for heading, values in cards.items():
            prior, question, prediction, hint, boundary = values
            result[filename][heading] = {
                "prior": prior,
                "question": question,
                "prediction": prediction,
                "hint": hint,
                "boundary": boundary,
            }

    middle = load_local_module("upgrade_chapters_3_5.py", "course_cards_03_05")
    for filename, config in middle.CHAPTERS.items():
        result[filename] = {
            heading: parse_old_card(card) for heading, card in config["cards"].items()
        }

    late = load_local_module("optimize_chapters_06_08.py", "course_cards_06_08")
    for filename, cards in late.TASKS.items():
        result[filename] = {}
        for raw_heading, values in cards.items():
            heading = raw_heading.removeprefix("## ")
            result[filename][heading] = {
                "prior": values["prerequisite"],
                "question": values["question"],
                "prediction": values["prediction"],
                "hint": values["hint"],
                "boundary": values["boundary"],
            }

    for filename, specs in result.items():
        for current, old in PROJECT_SOURCE_HEADINGS.items():
            if old in specs and current not in specs:
                specs[current] = specs[old]
    return result


TASK_SPECS = load_task_specs()


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def set_source(cell: dict, source: str) -> None:
    cell["source"] = source.strip() + "\n"


def h2_heading(cell: dict) -> str | None:
    if cell.get("cell_type") != "markdown":
        return None
    match = H2_RE.search(source_text(cell))
    return match.group(1) if match else None


def split_answer(source: str) -> tuple[str, str]:
    positions = [source.find(marker) for marker in ANSWER_MARKERS if marker in source]
    if not positions:
        return source, ""
    index = min(position for position in positions if position >= 0)
    return source[:index], source[index:]


def replace_plain_segment(text: str) -> str:
    for old, new in TRANSITION_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = re.sub(r"若(?!干)", "如果", text)
    text = text.replace("，但是不是", "，但它不是")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def plain_language(source: str) -> str:
    """只改普通文字，不碰代码块、行内代码和公式。"""
    protected: list[str] = []

    def keep(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"\x00PROTECTED_{len(protected) - 1}\x00"

    masked = PROTECTED_RE.sub(keep, source)
    masked = replace_plain_segment(masked)
    for index, value in enumerate(protected):
        masked = masked.replace(f"\x00PROTECTED_{index}\x00", value)
    return masked


def strip_first(text: str) -> str:
    text = text.strip().rstrip("。")
    for prefix in ("请先", "先"):
        if text.startswith(prefix):
            return text[len(prefix) :]
    return text


def normalize_action(text: str) -> str:
    text = strip_first(text)
    if text.startswith("若"):
        return "判断：如果" + text[1:]
    if text.startswith("如果"):
        return "判断：" + text
    if text.startswith("看到"):
        return "查看" + text[2:]
    for prefix in ("运行", "编码", "写报告", "逐笔计算", "拖动", "每次拖动", "操作滑块", "调用函数"):
        marker = prefix + "前"
        if text.startswith(marker):
            rest = strip_first(text[len(marker) :])
            return "在" + marker + rest
    return text


def end_sentence(text: str) -> str:
    text = text.strip()
    return text if text.endswith(("。", "？", "！")) else text + "。"


def format_action_sentence(action: str) -> str:
    action = re.sub(r"([，：])先", r"\1", action)
    return end_sentence(f"动手前先做：{action}")


def parse_story(source: str) -> tuple[str, str, str, str, str]:
    prior_match = re.search(r"前面的线索带了过来：(.+?)。接着他追问", source)
    question_match = re.search(r"追问：\*\*(.+?)\*\*", source)
    action_match = re.search(r"动手前：(.+?)(?:。)?核对时：", source)
    hint_match = re.search(r"核对时：(.+?)。", source)
    boundary_match = re.search(r"你还在报告旁边注明：(.+?)\s*$", source, re.DOTALL)
    if not all((prior_match, question_match, action_match, hint_match, boundary_match)):
        raise AssertionError(f"无法读取故事桥：{source[:160]}")
    return (
        prior_match.group(1).strip(),
        question_match.group(1).strip(),
        strip_first(action_match.group(1)),
        strip_first(hint_match.group(1)),
        boundary_match.group(1).strip(),
    )


def scene_for(chapter: int, heading: str, question: str) -> str:
    del chapter, heading, question
    return ""


def make_story_parts_from_spec(chapter: int, heading: str, spec: dict[str, str]) -> tuple[str, str]:
    prior = spec["prior"].strip().rstrip("。")
    question = spec["question"].strip().rstrip("。")
    action = normalize_action(spec["prediction"])
    hint = strip_first(spec["hint"])
    boundary = spec["boundary"].strip().rstrip("。")
    lead = f"已有线索：{prior}。本节要解决：**{question}**"
    action_text = format_action_sentence(action) + end_sentence(f"核对提示：{hint}")
    negative_words = ("不", "只", "取决于", "假设", "不能", "未", "没有", "并不")
    if "，但" in boundary:
        ending = boundary.replace("，但", "，但是", 1) + "。"
    elif "。" in boundary:
        ending = f"结果与限制：{boundary}。"
    elif any(word in boundary for word in negative_words):
        ending = f"但是，{boundary}。"
    else:
        ending = f"结果记录：{boundary}。"
    return lead, action_text + "\n\n" + ending


def make_story_parts(chapter: int, heading: str, bridge_source: str) -> tuple[str, str]:
    prior, question, action, hint, boundary = parse_story(bridge_source)
    return make_story_parts_from_spec(
        chapter,
        heading,
        {
            "prior": prior,
            "question": question,
            "prediction": action,
            "hint": hint,
            "boundary": boundary,
        },
    )


def simplify_regular_markdown(source: str) -> str:
    prefix, answer = split_answer(source)
    prefix = plain_language(prefix)
    # 文末不再放总结句。参考资料和项目要求保留。
    prefix = re.sub(r"\n*\*\*总结\*\*：[^\n]*\n?", "\n", prefix)
    return prefix.rstrip() + ("\n\n" + answer.lstrip() if answer else "")


def remove_end_recap(path: Path, heading: str, body: str) -> str:
    if path.name == "01_金融与量化.ipynb" and heading == "1.11 研究任务：完成第一份比较报告":
        body = re.sub(
            r"回到本章开头：你还是拥有10,000元，但现在已经学会描述现金流、计算收益率、区分资产关系并检查不确定性。从现金、债券、股票和基金中任选三类，完成一页观察报告：",
            "你还没有决定10,000元该怎么安排。请从现金、债券、股票和基金中任选三类，完成一页观察报告：",
            body,
        )
    if path.name == "02_现金流复利与贴现.ipynb" and heading == "作业":
        body = re.sub(
            r"你从“今天和未来的钱能否直接比较”出发，先学习终值与现值，再检查复利频率，用NPV和IRR分析校园项目，最后区分名义金额与实际购买力。现在请",
            "你要把这章的工具放进同一个程序。请",
            body,
        )
    return body


def protected_ledger(cells: list[dict], excluded_ids: set[str]) -> dict[str, set[str]]:
    text_parts: list[str] = []
    for cell in cells:
        if cell.get("id") in excluded_ids or cell.get("cell_type") != "markdown":
            continue
        text_parts.append(source_text(cell))
    text = "\n".join(text_parts)
    return {
        "protected": set(PROTECTED_RE.findall(text)),
        "urls": set(URL_RE.findall(text)),
        "numbers": set(NUMBER_RE.findall(text)),
    }


def polish_v1(path: Path, notebook: dict, *, write: bool) -> tuple[int, int]:
    """修正第一版合并文本，并从原任务资料恢复完整限制条件。"""
    before_cells = copy.deepcopy(notebook["cells"])
    before_ledger = protected_ledger(before_cells, set())
    code_before = {
        cell.get("id"): json.dumps(cell, ensure_ascii=False, sort_keys=True)
        for cell in before_cells
        if cell.get("cell_type") == "code"
    }
    attachments_before = {
        cell.get("id"): copy.deepcopy(cell.get("attachments", {}))
        for cell in before_cells
        if cell.get("cell_type") == "markdown" and cell.get("attachments")
    }
    answer_before: dict[str, str] = {}
    for cell in before_cells:
        if cell.get("cell_type") != "markdown":
            continue
        _, answer = split_answer(source_text(cell))
        if answer:
            answer_before[cell.get("id")] = answer

    new_cells: list[dict] = []
    for original in before_cells:
        cell = copy.deepcopy(original)
        if cell.get("cell_type") != "markdown":
            new_cells.append(cell)
            continue

        heading = h2_heading(cell)
        if heading is not None and cell.get("metadata", {}).get("course_role") == "story_section":
            source = source_text(cell)
            prefix, answer = split_answer(source)
            parts = prefix.strip().split("\n\n")
            if len(parts) < 4:
                raise AssertionError(f"{path.name}: 无法识别合并段落：{heading}")
            first_line = parts[0]
            body = "\n\n".join(parts[2:-2])
            body = plain_language(body)
            body = re.sub(r"\n*\*\*总结\*\*：[^\n]*\n?", "\n", body).strip()
            body = remove_end_recap(path, heading, body)

            source_heading = SPEC_SOURCE_HEADINGS.get(heading, heading)
            spec = TASK_SPECS[path.name].get(source_heading)
            if spec is None:
                raise AssertionError(f"{path.name}: 缺少原始任务资料：{heading}")
            lead, ending = make_story_parts_from_spec(int(path.name[:2]), heading, spec)
            lead = plain_language(lead).strip()
            ending = plain_language(ending).strip()

            display_heading = DISPLAY_HEADING_RENAMES.get(heading, heading)
            first_line = "## " + display_heading
            merged = [first_line, lead]
            if body:
                merged.append(body)
            merged.append(ending)
            prefix_after = "\n\n".join(merged).rstrip()
            cell["source"] = prefix_after + ("\n\n" + answer if answer else "\n")
        else:
            original_source = source_text(cell)
            simplified = simplify_regular_markdown(original_source)
            _, answer = split_answer(original_source)
            cell["source"] = simplified if answer else simplified.strip() + "\n"
        new_cells.append(cell)

    notebook["cells"] = new_cells
    notebook.setdefault("metadata", {})["plain_story_revision"] = "plain-story-v5"

    code_after = {
        cell.get("id"): json.dumps(cell, ensure_ascii=False, sort_keys=True)
        for cell in new_cells
        if cell.get("cell_type") == "code"
    }
    if code_after != code_before:
        raise AssertionError(f"{path.name}: v2润色改动了代码或输出")
    attachments_after = {
        cell.get("id"): copy.deepcopy(cell.get("attachments", {}))
        for cell in new_cells
        if cell.get("cell_type") == "markdown" and cell.get("attachments")
    }
    if attachments_after != attachments_before:
        raise AssertionError(f"{path.name}: v2润色改动了附件")
    for cell in new_cells:
        cell_id = cell.get("id")
        if cell_id not in answer_before:
            continue
        _, answer = split_answer(source_text(cell))
        if answer != answer_before[cell_id]:
            raise AssertionError(f"{path.name}: v2润色改动了学生作答：{cell_id}")

    after_ledger = protected_ledger(new_cells, set())
    for key, values in before_ledger.items():
        missing = values - after_ledger[key]
        if missing:
            raise AssertionError(f"{path.name}: v2润色丢失{key}：{sorted(missing)[:8]}")

    if write:
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(before_cells), len(new_cells)


def transform(path: Path, *, write: bool) -> tuple[int, int]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    before_cells = copy.deepcopy(notebook["cells"])
    revision = notebook.get("metadata", {}).get("plain_story_revision")
    if revision == "plain-story-v5":
        return len(before_cells), len(before_cells)
    if revision in {"plain-story-v1", "plain-story-v2", "plain-story-v3", "plain-story-v4"}:
        return polish_v1(path, notebook, write=write)

    removed_ids: set[str] = set()
    for index, cell in enumerate(before_cells):
        if h2_heading(cell) == "总结：你完成了什么？":
            removed_ids.add(cell.get("id"))
            if index + 1 < len(before_cells):
                next_cell = before_cells[index + 1]
                if next_cell.get("metadata", {}).get("course_role") == "story_bridge":
                    removed_ids.add(next_cell.get("id"))

    before_ledger = protected_ledger(before_cells, removed_ids)
    code_before = {
        cell.get("id"): json.dumps(cell, ensure_ascii=False, sort_keys=True)
        for cell in before_cells
        if cell.get("cell_type") == "code"
    }
    attachments_before = {
        cell.get("id"): copy.deepcopy(cell.get("attachments", {}))
        for cell in before_cells
        if cell.get("cell_type") == "markdown" and cell.get("attachments")
    }
    answer_before = {}
    for cell in before_cells:
        if cell.get("cell_type") != "markdown":
            continue
        _, answer = split_answer(source_text(cell))
        if answer:
            answer_before[cell.get("id")] = answer

    new_cells: list[dict] = []
    index = 0
    while index < len(before_cells):
        cell = copy.deepcopy(before_cells[index])

        if index == 0:
            set_source(cell, OPENINGS[path.name])
            metadata = cell.setdefault("metadata", {})
            metadata.clear()
            metadata["course_role"] = "chapter_story"
            new_cells.append(cell)
            index = 2  # 章首介绍和项目页已经合并
            continue

        heading = h2_heading(cell)
        if heading == "总结：你完成了什么？":
            index += 1
            if index < len(before_cells) and before_cells[index].get("metadata", {}).get("course_role") == "story_bridge":
                index += 1
            continue

        if heading is not None:
            if index + 1 >= len(before_cells):
                raise AssertionError(f"{path.name}: {heading} 后缺少故事桥")
            bridge = before_cells[index + 1]
            if bridge.get("metadata", {}).get("course_role") != "story_bridge":
                raise AssertionError(f"{path.name}: {heading} 后不是故事桥")

            source = source_text(cell)
            first_line, _, body = source.partition("\n")
            body_prefix, answer = split_answer(body.lstrip())
            source_heading = SPEC_SOURCE_HEADINGS.get(heading, heading)
            spec = TASK_SPECS[path.name].get(source_heading)
            if spec is None:
                raise AssertionError(f"{path.name}: 缺少故事资料：{heading}")
            lead, ending = make_story_parts_from_spec(int(path.name[:2]), heading, spec)
            first_line = "## " + DISPLAY_HEADING_RENAMES.get(heading, heading)
            body_prefix = plain_language(body_prefix).strip()
            body_prefix = remove_end_recap(path, heading, body_prefix)
            ending = plain_language(ending).strip()
            merged_parts = [first_line, lead]
            if body_prefix:
                merged_parts.append(body_prefix)
            merged_parts.append(ending)
            if answer:
                cell["source"] = "\n\n".join(merged_parts).rstrip() + "\n\n" + answer
            else:
                set_source(cell, "\n\n".join(merged_parts))
            metadata = cell.setdefault("metadata", {})
            metadata["course_role"] = "story_section"
            metadata.pop("story_anchor", None)
            new_cells.append(cell)
            index += 2
            continue

        if cell.get("cell_type") == "markdown":
            original_source = source_text(cell)
            simplified = simplify_regular_markdown(original_source)
            _, answer = split_answer(original_source)
            if answer:
                cell["source"] = simplified
            else:
                set_source(cell, simplified)
        new_cells.append(cell)
        index += 1

    notebook["cells"] = new_cells
    notebook.setdefault("metadata", {})["plain_story_revision"] = "plain-story-v5"

    code_after = {
        cell.get("id"): json.dumps(cell, ensure_ascii=False, sort_keys=True)
        for cell in new_cells
        if cell.get("cell_type") == "code"
    }
    if code_after != code_before:
        raise AssertionError(f"{path.name}: 代码或输出被修改")

    attachments_after = {
        cell.get("id"): copy.deepcopy(cell.get("attachments", {}))
        for cell in new_cells
        if cell.get("cell_type") == "markdown" and cell.get("attachments")
    }
    if attachments_after != attachments_before:
        raise AssertionError(f"{path.name}: Notebook附件被修改")

    for cell in new_cells:
        cell_id = cell.get("id")
        if cell_id not in answer_before:
            continue
        _, answer = split_answer(source_text(cell))
        if answer != answer_before[cell_id]:
            raise AssertionError(f"{path.name}: 学生作答区被修改：{cell_id}")

    after_ledger = protected_ledger(new_cells, set())
    for key, values in before_ledger.items():
        missing = values - after_ledger[key]
        if missing:
            raise AssertionError(f"{path.name}: 丢失{key}：{sorted(missing)[:8]}")

    if write:
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(before_cells), len(new_cells)


def main() -> None:
    results: dict[str, tuple[int, int]] = {}
    for filename in NOTEBOOKS:
        results[filename] = transform(ROOT / filename, write=False)
    for filename in NOTEBOOKS:
        before, after = transform(ROOT / filename, write=True)
        print(f"{filename}: {before} -> {after} cells")


if __name__ == "__main__":
    main()
