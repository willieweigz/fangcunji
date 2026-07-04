# -*- coding: utf-8 -*-
"""
生成《录入进度表.md》——每个年份的"能不能开工录入"一览表。

对每个编年年份（1992–2026）检查 5 个维度：
- 标签：tag-plan.json 里该年份套票是否都已定标（manual/confirmed，非 todo）
- 图库整理：图库时期文件夹里是否已按"每套一个子文件夹"整理
- md 文档：每个套票子文件夹是否都有 .md 介绍文档
- 数据录入：data/stamps/<年份>.json 是否已存在
- 图片导入：public/images/stamps/<年份>/ 是否已有图片

前三项是"开工前置条件"，后两项是"完成度"。

此文件为自动生成的只读报表，运行 `python scripts/build_progress.py` 刷新。
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIBRARY = "新中国邮票图片全集（1949年-2026年最新）"
OUT = "录入进度表.md"
YEARS = range(1992, 2027)


def load_plan_by_year():
    path = os.path.join("data", "tag-plan.json")
    if not os.path.exists(path):
        return {}
    by_year = {}
    for e in json.load(open(path, encoding="utf-8")):
        m = re.match(r"(\d{4})-", e["id"])
        if not m:
            continue
        y = int(m.group(1))
        by_year.setdefault(y, []).append(e["status"])
    return by_year


def find_lib_folder(year):
    if not os.path.isdir(LIBRARY):
        return None
    for name in os.listdir(LIBRARY):
        if f"编年号{year}年" in name:
            return os.path.join(LIBRARY, name)
    return None


def check_year(year, plan_by_year):
    # 标签
    statuses = plan_by_year.get(year, [])
    if not statuses:
        tag = "—"
    elif all(s in ("manual", "confirmed") for s in statuses):
        tag = "✅"
    else:
        todo = sum(1 for s in statuses if s not in ("manual", "confirmed"))
        tag = f"⚠️缺{todo}"

    # 图库整理 + md
    folder = find_lib_folder(year)
    if not folder:
        lib, md = "❌无", "—"
    else:
        subs = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
        if not subs:
            lib, md = "❌散图", "—"
        else:
            lib = f"✅{len(subs)}套"
            with_md = sum(
                1
                for d in subs
                if any(f.endswith(".md") for f in os.listdir(os.path.join(folder, d)))
            )
            md = "✅" if with_md == len(subs) else f"⚠️{with_md}/{len(subs)}"

    # 数据录入
    data_path = os.path.join("data", "stamps", f"{year}.json")
    if os.path.exists(data_path):
        n = len(json.load(open(data_path, encoding="utf-8")))
        data = f"✅{n}套"
    else:
        data = "—"

    # 图片导入
    img_dir = os.path.join("public", "images", "stamps", str(year))
    if os.path.isdir(img_dir) and os.listdir(img_dir):
        img = f"✅{len(os.listdir(img_dir))}张"
    else:
        img = "—"

    return tag, lib, md, data, img


def main():
    plan_by_year = load_plan_by_year()
    lines = [
        "# 方寸集 · 录入进度表",
        "",
        "> 由 `python scripts/build_progress.py` 自动生成，**请勿手改**。",
        "",
        "**开工前置条件**（前 3 列）：标签✅ + 图库整理✅ + md✅ 三项齐全，才能开始录入该年份。",
        "**完成度**（后 2 列）：数据已录入、图片已导入。",
        "",
        "| 年份 | ①标签 | ②图库整理 | ③md文档 | 数据录入 | 图片导入 | 可开工? |",
        "|---|---|---|---|---|---|---|",
    ]
    for year in sorted(YEARS, reverse=True):
        tag, lib, md, data, img = check_year(year, plan_by_year)
        ready = "✅ 可" if (tag == "✅" and lib.startswith("✅") and md == "✅") else "—"
        if data.startswith("✅"):
            ready = "已录入"
        lines.append(
            f"| {year} | {tag} | {lib} | {md} | {data} | {img} | {ready} |"
        )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"已生成 {OUT}（{YEARS.start}–{YEARS.stop - 1} 年）")


if __name__ == "__main__":
    main()
