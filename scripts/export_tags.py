# -*- coding: utf-8 -*-
"""
生成《标签总表.md》——全站标签的人工审查报表。

用法（在项目根目录执行）:
    python scripts/export_tags.py

注意: 标签总表.md 是自动生成的报表，唯一数据源是 data/stamps/*.json。
     要改标签请改 JSON 数据文件，然后重新运行本脚本，不要手改 md。
"""
import json
import os
import sys
from collections import Counter
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = os.path.join("data", "stamps")
OUT = "标签总表.md"


def sort_key(sid: str):
    parts = sid.split("-")
    try:
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return (0, 0)


def main():
    primary_list = json.load(open("data/themes.json", encoding="utf-8"))
    sets = []
    for f in sorted(os.listdir(DATA_DIR)):
        if f.endswith(".json"):
            sets += json.load(open(os.path.join(DATA_DIR, f), encoding="utf-8"))
    sets.sort(key=lambda s: sort_key(s["id"]))

    p_count = Counter(s["themes"][0] for s in sets if s["themes"])
    s_count = Counter(t for s in sets for t in s["themes"][1:])

    lines = [
        "# 方寸集 · 标签总表",
        "",
        f"> ⚠️ 本文件由 `python scripts/export_tags.py` 自动生成（{date.today()}），"
        "**请勿手改**。要调整标签请修改 `data/stamps/*.json`，然后重新生成。",
        "",
        f"共 {len(sets)} 套邮票。",
        "",
        "## 一级主题统计",
        "",
        "| 一级主题 | 套数 |",
        "|---|---|",
    ]
    for t in primary_list:
        lines.append(f"| {t} | {p_count.get(t, 0)} |")
    unknown = [t for t in p_count if t not in primary_list]
    for t in unknown:
        lines.append(f"| ⚠️ {t}（不在 themes.json！） | {p_count[t]} |")

    lines += [
        "",
        "## 二级标签统计（按使用次数，用于发现同义异名）",
        "",
        "| 二级标签 | 次数 |",
        "|---|---|",
    ]
    for t, n in s_count.most_common():
        lines.append(f"| {t} | {n} |")

    lines += [
        "",
        "## 全量标签表（已录入）",
        "",
        "| 志号 | 名称 | 一级主题 | 二级标签 |",
        "|---|---|---|---|",
    ]
    for s in sets:
        th = s["themes"]
        lines.append(
            f"| {s['id']} | {s['title']} | {th[0] if th else '⚠️无'} | "
            f"{'、'.join(th[1:]) if len(th) > 1 else ''} |"
        )

    # 预打标签（tag-plan 中尚未录入的 manual/auto 条目）
    plan_path = os.path.join("data", "tag-plan.json")
    if os.path.exists(plan_path):
        entered = {s["id"] for s in sets}
        plan = [
            e
            for e in json.load(open(plan_path, encoding="utf-8"))
            if e["id"] not in entered and e["status"] in ("manual", "auto")
        ]
        plan.sort(key=lambda e: sort_key(e["id"]))
        lines += [
            "",
            f"## 预打标签表（尚未录入，共 {len(plan)} 套）",
            "",
            "站长/主力 AI 预先规划的标签，录入时照抄。状态 auto 为规则自动预打，录入时需复核。",
            "",
            "| 志号 | 名称 | 一级主题 | 二级标签 | 状态 |",
            "|---|---|---|---|---|",
        ]
        for e in plan:
            th = e["themes"]
            lines.append(
                f"| {e['id']} | {e['title']} | {th[0] if th else ''} | "
                f"{'、'.join(th[1:]) if len(th) > 1 else ''} | {e['status']} |"
            )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"已生成 {OUT}: {len(sets)} 套，一级主题 {len(p_count)} 个，二级标签 {len(s_count)} 个")


if __name__ == "__main__":
    main()
