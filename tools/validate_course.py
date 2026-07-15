#!/usr/bin/env python3
"""对第0—8章执行不改写源文件的课程质量检查。"""

from __future__ import annotations

import argparse
import ast
import copy
import contextlib
import io
import os
import re
import sys
import time
from pathlib import Path

import nbformat
from IPython.display import HTML, display
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    ROOT / "00_从c语言到python.ipynb",
    ROOT / "01_金融与量化.ipynb",
    ROOT / "02_现金流复利与贴现.ipynb",
    ROOT / "03_债券与利率风险.ipynb",
    ROOT / "04_股票基金与市场交易.ipynb",
    ROOT / "05_金融数据与时间边界.ipynb",
    ROOT / "06_收益率与财富路径.ipynb",
    ROOT / "07_概率分布与抽样.ipynb",
    ROOT / "08_风险度量与压力测试.ipynb",
]

LOCKED_H2 = {
    "01_金融与量化.ipynb": [
        "1.1 小林的第一个问题：钱为什么会流动？",
        "1.2 小林把口头承诺画成现金流",
        "1.3 小林需要一个可以比较的比例",
        "1.4 小林扩大候选清单：现金、债券、股票、基金",
        "1.5 小林决定用量化分析约束自己的判断",
        "1.6 小林第一次面对不确定性：情景不是预测",
        "1.7 小林把两个情景扩展成许多可能路径",
        "1.8 小林观看不确定性如何逐年展开",
        "1.9 小林检查结论是否依赖参数",
        "1.10 Python练习：帮小林比较自定义情景",
        "1.11 研究任务：完成小林的第一份比较报告",
    ],
    "02_现金流复利与贴现.ipynb": [
        "2.1 不同时间的钱不能直接相加",
        "2.2 不同的复利频率",
        "2.3 一个小尝试",
        "2.4 小林寻找项目的盈亏平衡贴现率",
        "2.5 金额增长不等于购买力增长",
        "2.6 小林测试未来学习支出的现值",
        "2.7 编程练习：为小林实现通用NPV工具",
        "作业",
    ],
}

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def source_text(cell: nbformat.NotebookNode) -> str:
    return str(cell.get("source", ""))


def h2_headings(nb: nbformat.NotebookNode) -> list[str]:
    headings: list[str] = []
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            headings.extend(match.group(1) for match in H2_RE.finditer(source_text(cell)))
    return headings


def validate_notebook(path: Path) -> tuple[nbformat.NotebookNode, dict[str, int]]:
    nb = nbformat.read(path, as_version=4)
    nbformat.validate(nb)

    ids = [cell.get("id") for cell in nb.cells]
    if any(not cell_id for cell_id in ids):
        raise AssertionError("存在缺失的cell id")
    if len(ids) != len(set(ids)):
        raise AssertionError("cell id不唯一")

    code_count = 0
    answer_count = 0
    story_count = 0
    image_count = 0

    for index, cell in enumerate(nb.cells):
        text = source_text(cell)
        if cell.cell_type == "code":
            code_count += 1
            try:
                ast.parse(text)
            except SyntaxError as exc:
                raise AssertionError(f"代码单元{index}语法错误：{exc}") from exc
        elif cell.cell_type == "markdown":
            answer_count += int("我的回答" in text)
            story_count += int(cell.get("metadata", {}).get("course_role") == "story_section")
            for target in IMAGE_RE.findall(text):
                if target.startswith("attachment:"):
                    attachment_name = target.removeprefix("attachment:")
                    if attachment_name not in cell.get("attachments", {}):
                        raise AssertionError(f"附件不存在：{target}")
                    continue
                if target.startswith(("http://", "https://", "data:")):
                    continue
                image_count += 1
                image_path = (path.parent / target).resolve()
                if not image_path.is_file():
                    raise AssertionError(f"图片链接不存在：{target}")

    forbidden_scaffolds = (
        "AI学习状态",
        "本节任务卡",
        "章前定位任务卡",
        "章末整合任务卡",
        "学习目标",
        "**总结**",
        "总结：小林完成了什么？",
    )
    markdown_text = "\n".join(source_text(cell) for cell in nb.cells if cell.cell_type == "markdown")
    found_forbidden = [term for term in forbidden_scaffolds if term in markdown_text]
    if found_forbidden:
        raise AssertionError(f"学生页仍含教案式脚手架：{found_forbidden}")

    # 每个知识性H2本身包含短故事，不再另插一个重复单元。
    for index, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown" or not H2_RE.search(source_text(cell)):
            continue
        heading = H2_RE.search(source_text(cell)).group(1)
        if cell.get("metadata", {}).get("course_role") != "story_section":
            raise AssertionError(f"二级标题缺少内嵌故事：{heading}")
        if "小林" not in source_text(cell):
            raise AssertionError(f"二级标题没有接入小林的事件：{heading}")

    navigation_cell = nb.cells[0] if nb.cells else {}
    navigation = source_text(navigation_cell)
    if navigation_cell.get("metadata", {}).get("course_role") != "chapter_story":
        raise AssertionError("章首缺少项目故事")
    if "最后" not in navigation:
        raise AssertionError("章首项目故事缺少最后要完成的作品")
    chapter_number = int(path.name[:2])
    if "下一章" not in navigation and f"第{chapter_number + 1}章" not in navigation:
        raise AssertionError("章首项目故事缺少后续去向")
    if image_count < 1:
        raise AssertionError("章首概念图链接缺失")

    expected = LOCKED_H2.get(path.name)
    if expected is not None and h2_headings(nb) != expected:
        raise AssertionError("第1—2章H2锁定检查失败")

    return nb, {
        "cells": len(nb.cells),
        "code": code_count,
        "stories": story_count,
        "answers": answer_count,
        "images": image_count,
    }


def execute_notebook(nb: nbformat.NotebookNode, path: Path, timeout: int) -> float:
    # 只执行内存副本；不把执行计数和输出写回学生Notebook。
    execution_copy = copy.deepcopy(nb)
    started = time.monotonic()
    client = NotebookClient(
        execution_copy,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
        allow_errors=False,
        record_timing=False,
    )
    client.execute()
    return time.monotonic() - started


def execute_notebook_in_process(nb: nbformat.NotebookNode, path: Path) -> float:
    """在禁止本地端口的沙箱中，用独立命名空间顺序执行代码单元。

    该模式不模拟Jupyter消息协议，但每章使用全新命名空间、按原顺序执行，
    足以检查变量依赖、导入、运行时异常和绘图代码。
    """
    namespace: dict[str, object] = {
        "__name__": "__main__",
        "display": display,
        "HTML": HTML,
    }
    previous_cwd = Path.cwd()
    started = time.monotonic()
    try:
        os.chdir(path.parent)
        for index, cell in enumerate(nb.cells):
            if cell.cell_type != "code" or not source_text(cell).strip():
                continue
            code = compile(source_text(cell), f"{path.name}:cell-{index}", "exec")
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                exec(code, namespace)  # noqa: S102 - 只执行仓库内受版本控制的课程代码
    finally:
        os.chdir(previous_cwd)
        try:
            import matplotlib.pyplot as plt

            plt.close("all")
        except ImportError:
            pass
    return time.monotonic() - started


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="从新内核顺序执行全部Notebook的内存副本")
    parser.add_argument(
        "--execute-in-process",
        action="store_true",
        help="在禁止Jupyter本地端口的沙箱中，用每章独立命名空间顺序执行",
    )
    parser.add_argument("--timeout", type=int, default=240, help="单个代码单元超时秒数")
    args = parser.parse_args()

    os.environ.setdefault("MPLBACKEND", "Agg")
    failures: list[str] = []
    rows: list[tuple[str, dict[str, int], float | None]] = []

    for path in NOTEBOOKS:
        try:
            nb, stats = validate_notebook(path)
            if args.execute_in_process:
                elapsed = execute_notebook_in_process(nb, path)
            elif args.execute:
                elapsed = execute_notebook(nb, path, args.timeout)
            else:
                elapsed = None
            rows.append((path.name, stats, elapsed))
        except Exception as exc:  # noqa: BLE001 - 汇总全部章节，而不是首错即停
            failures.append(f"{path.name}: {type(exc).__name__}: {exc}")

    print("章节\t单元\t代码\t故事节\t回答区\t本地图\t执行秒")
    for name, stats, elapsed in rows:
        elapsed_text = f"{elapsed:.1f}" if elapsed is not None else "-"
        print(
            f"{name}\t{stats['cells']}\t{stats['code']}\t{stats['stories']}\t"
            f"{stats['answers']}\t{stats['images']}\t{elapsed_text}"
        )

    if failures:
        print("\n失败：", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    executed = args.execute or args.execute_in_process
    mode = "结构、语法、链接、标题锁与从头执行" if executed else "结构、语法、链接与标题锁"
    print(f"\n通过：第0—8章{mode}检查。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
