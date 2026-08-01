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
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIBRARY = "新中国邮票图片全集（1949年-2026年最新）"
OUT = "录入进度表.md"
YEARS = range(1949, 2027)


def load_plan_by_id():
    path = os.path.join("data", "tag-plan.json")
    if not os.path.exists(path):
        return {}
    return {e["id"]: e["status"] for e in json.load(open(path, encoding="utf-8"))}


def find_lib_folder(year):
    if not os.path.isdir(LIBRARY):
        return None
    matches = []
    for name in os.listdir(LIBRARY):
        # 1992年及以后叫"编年号XXXX年"；1989/1990/1991（从JT合集里提取出来的）叫"XXXX年"或"15-XXXX年"
        if f"编年号{year}年" in name or name == f"15-{year}年" or name == f"{year}年":
            matches.append(name)
    if matches:
        matches.sort(key=lambda n: (0 if "编年号" in n else 1, n))
        return os.path.join(LIBRARY, matches[0])
    return None


def folder_ids(folder, subs):
    """从子文件夹名提取志号（空格前的第一段），用于历史 T/J 志号年份的标签核对。"""
    ids = []
    for d in subs:
        head = d.replace("《", " ").split(" ")[0].strip()
        if head:
            ids.append(head)
    return ids


def check_year(year, plan_by_id):
    # 图库整理 + md（先算，历史志号年份要靠子文件夹名反查标签状态）
    folder = find_lib_folder(year)
    if not folder:
        lib, md, subs = "❌无", "—", []
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

    # 标签：该年份数据已录入即视为标签✅（已通过体检的真实数据必然标签合规）
    data_path_check = os.path.join("data", "stamps", f"{year}.json")
    if os.path.exists(data_path_check):
        tag = "✅"
    else:
        ids = folder_ids(folder, subs) if folder else []
        if not ids:
            tag = "—"
        else:
            statuses = [plan_by_id.get(i, "todo") for i in ids]
            if all(s in ("manual", "confirmed") for s in statuses):
                tag = "✅"
            else:
                todo = sum(1 for s in statuses if s not in ("manual", "confirmed"))
                tag = f"⚠️缺{todo}"

    # 数据录入
    data_path = os.path.join("data", "stamps", f"{year}.json")
    if os.path.exists(data_path):
        n = len(json.load(open(data_path, encoding="utf-8")))
        data = f"✅{n}套"
    else:
        data = "—"

    # 图片导入
    img_dir = os.path.join("image-store", "images", "stamps", str(year))
    if os.path.isdir(img_dir) and os.listdir(img_dir):
        img = f"✅{len(os.listdir(img_dir))}张"
    else:
        img = "—"

    return tag, lib, md, data, img


def main():
    plan_by_id = load_plan_by_id()
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
    # 累计汇总
    total_years = 0
    total_lib = 0
    md_done = 0
    md_partial = 0
    total_data = 0
    total_img = 0
    total_entered = 0

    for year in sorted(YEARS, reverse=True):
        tag, lib, md, data, img = check_year(year, plan_by_id)
        ready = "✅ 可" if (tag == "✅" and lib.startswith("✅") and md == "✅") else "—"
        if data.startswith("✅"):
            ready = "已录入"
        lines.append(
            f"| {year} | {tag} | {lib} | {md} | {data} | {img} | {ready} |"
        )
        # 汇总统计
        total_years += 1
        if lib.startswith("✅"):
            total_lib += int(lib[1:].rstrip("套"))
        if md == "✅":
            md_done += 1
        elif md.startswith("⚠️"):
            md_partial += 1
        if data.startswith("✅"):
            total_data += int(data[1:].rstrip("套"))
            total_entered += 1
        if img.startswith("✅"):
            total_img += int(img[1:].rstrip("张"))

    # 汇总行
    md_summary = f"✅{md_done} ⚠️{md_partial}" if md_partial else f"✅{md_done}"
    lines.append(
        f"| **合计** | **{total_years}年** | ✅**{total_lib}套** | {md_summary} | ✅**{total_data}套** | ✅**{total_img}张** | **{total_entered}年已录入** |"
    )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"已生成 {OUT}（{YEARS.start}–{YEARS.stop - 1} 年）")


if __name__ == "__main__":
    main()
