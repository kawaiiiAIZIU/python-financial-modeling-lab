# Notebook维护工具

Notebook 是学生课程内容和学习记录的主版本。本目录只保存可复查的维护工具，不把任何脚本视为可以随时覆盖 Notebook 的另一份“真源”。

## 日常安全入口

```bash
.venv/bin/python tools/validate_course.py
.venv/bin/python tools/validate_course.py --execute
.venv/bin/python tools/validate_course.py --execute-in-process
```

第一条检查 Notebook 结构、代码语法、章首图片、每节内嵌故事和第1—2章知识性标题锁。第二条还会在新内核中按顺序执行第0—8章的副本，不会写回学生输出。如果运行环境不允许 Jupyter 创建本地端口，就用第三条。它会为每章建立独立环境并执行代码。

## 当前改写脚本

- `rewrite_course_plain_story.py`：把章首和各节改成短而连续的故事。它只改普通文字，不改代码、输出、附件和学生作答。

## 已停用的旧脚本

- `storyize_course.py`
- `organize_chapters_00_02.py`
- `upgrade_chapters_3_5.py`
- `optimize_chapters_06_08.py`

这些脚本只记录旧版改写过程。它们不能再运行，以免把已经删除的任务卡或独立故事格写回 Notebook。

## 旧版基线构建器

- `build_notebooks.py`
- `build_chapters_02_05.py`
- `build_chapters_06_08.py`

这些文件保留早期课程基线，只用于历史重建。它们生成的内容早于当前章首导航、任务卡、概念图和课程衔接，**默认拒绝覆盖当前 Notebook**。只有明确需要恢复旧版且已经备份时，才可显式传入：

```bash
--overwrite-current-notebooks
```

正常备课、批改和学生学习均不应使用这个参数。
