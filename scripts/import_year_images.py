# -*- coding: utf-8 -*-
"""
按年份把本地邮票图库的单枚图导入网站目录。

用法（在项目根目录执行）:
    python scripts/import_year_images.py 2024

规则:
- 读取 data/stamps/<年份>.json 获取每套的志号和枚数 N
- 在图库中找到该年份的时期文件夹，再按志号匹配套票子文件夹
- 智能排序：优先取单枚邮票图（"第X枚"/"邮票X"/(X-Y)模式），
  过滤小型张/小全张/小本票/全套/封底封面等非单枚图
- 复制到 public/images/stamps/<年份>/<志号>-<枚序>.jpg（已存在则跳过，不覆盖）
- 打印每套的映射清单，供人工/AI 抽查
"""
import json
import os
import re
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIBRARY = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）"
MAX_EDGE = 1600  # 长边超过则压缩
MAX_KB = 400  # 体积超过则压缩
QUALITY = 85


def copy_compressed(src: str, dst: str):
    """复制图片，超标（>1600px 或 >400KB）时自动压缩后落盘。"""
    try:
        from PIL import Image
    except ImportError:
        shutil.copy2(src, dst)
        return
    with Image.open(src) as im:
        if max(im.size) <= MAX_EDGE and os.path.getsize(src) / 1024 <= MAX_KB:
            shutil.copy2(src, dst)
            return
        im = im.convert("RGB")
        im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        im.save(dst, "JPEG", quality=QUALITY, optimize=True)

# ---- 图片优先级判断 ----

# 这些关键词表示非单枚图，优先级最低
NON_STAMP_KEYWORDS = [
    "小型张", "小全张", "小本票", "全套", "套票",
    "封底", "封面", "小型张", "小版张", "小版",
    "整版票", "版式一", "版式二", "小版票",
]


def _natural_key(s: str) -> tuple:
    """自然排序：把字符串中的数字转为整数，使 "10" 排在 "2" 之后"""
    parts = re.split(r"(\d+)", s)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # 数字部分
            result.append(int(part))
        else:
            result.append(part)
    return tuple(result)


def _is_stamp_image(name: str) -> bool:
    """判断文件名是否看起来像单枚邮票（非小型张等）"""
    for kw in NON_STAMP_KEYWORDS:
        if kw in name:
            return False
    return True


def _sort_key(name: str) -> tuple:
    """
    排序键：单枚邮票优先，然后按自然顺序排列。
    返回 (优先级, 自然排序key)
    优先级：0=单枚邮票, 1=其他
    """
    priority = 0 if _is_stamp_image(name) else 1
    return (priority, _natural_key(name))


# ---- 文件夹查找 ----

def find_year_dir(year: str) -> str | None:
    matches = [
        name
        for name in os.listdir(LIBRARY)
        if os.path.isdir(os.path.join(LIBRARY, name)) and f"{year}年" in name
    ]
    if not matches:
        return None
    # 图库中同一年份可能有多个文件夹（如"贺卡专用邮票2013年-"），优先取"编年号"正票文件夹
    matches.sort(key=lambda n: (0 if "编年号" in n else 1, n))
    return os.path.join(LIBRARY, matches[0])


def find_set_folder(year_dir: str, set_id: str) -> str | None:
    for name in os.listdir(year_dir):
        full = os.path.join(year_dir, name)
        if not os.path.isdir(full):
            continue
        head = name.replace("《", " ").replace("　", " ").split(" ")[0].strip()
        # 去掉 T/J 后缀再比较（如 "2026-6T" 匹配 "2026-6"）
        if head.rstrip("TJ") == set_id:
            return full
    return None


# ---- 主流程 ----

def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/import_year_images.py <年份>")
        sys.exit(1)
    year = sys.argv[1]

    data_path = os.path.join("data", "stamps", f"{year}.json")
    if not os.path.exists(data_path):
        print(f"[错误] 找不到数据文件 {data_path}，请先完成数据录入")
        sys.exit(1)
    with open(data_path, encoding="utf-8") as f:
        sets = json.load(f)

    year_dir = find_year_dir(year)
    if not year_dir:
        print(f"[错误] 图库中找不到 {year} 年的文件夹: {LIBRARY}")
        sys.exit(1)
    print(f"图库目录: {year_dir}")

    dst_dir = os.path.join("public", "images", "stamps", year)
    os.makedirs(dst_dir, exist_ok=True)

    copied = skipped = 0
    problems = []
    warnings = []

    for s in sets:
        sid, n = s["id"], s["totalStamps"]
        folder = find_set_folder(year_dir, sid)
        if not folder:
            problems.append(f"{sid} {s['title']}: 图库中没有对应文件夹")
            continue

        all_files = [
            f
            for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png")) and "(1)" not in f
        ]

        if len(all_files) < n:
            problems.append(
                f"{sid} {s['title']}: 文件数 {len(all_files)} < 枚数 {n}，跳过"
            )
            continue

        # 智能排序：单枚邮票优先，自然数字排序
        files = sorted(all_files, key=_sort_key)

        # 检测是否有非单枚图被排除
        if len(files) > n and not _is_stamp_image(files[0]):
            # 第一张就是非单枚图，但可能有足够的候补
            pass

        pairs = []
        for i in range(n):
            dst = os.path.join(dst_dir, f"{sid}-{i + 1}.jpg")
            if os.path.exists(dst):
                skipped += 1
            else:
                copy_compressed(os.path.join(folder, files[i]), dst)
                copied += 1
            pairs.append(f"    {files[i]} -> {sid}-{i + 1}.jpg")

        print(f"[{sid}] {s['title']}（{n}枚）")
        for p in pairs:
            print(p)

        # 如果排在前面的有非单枚图，发出警告
        stamp_count = sum(1 for f in files[:n] if _is_stamp_image(f))
        if stamp_count < n:
            non_stamp = [f for f in files[:n] if not _is_stamp_image(f)]
            warnings.append(
                f"{sid} {s['title']}: {n}枚中有{n - stamp_count}张非单枚图"
                f"（{', '.join(non_stamp)}），请人工抽查"
            )

    print(f"\n完成: 新复制 {copied} 张，已存在跳过 {skipped} 张")
    if warnings:
        print("\n[有非单枚图入选，建议抽查]")
        for w in warnings:
            print(" ⚠", w)
    if problems:
        print("\n[需要人工处理]")
        for p in problems:
            print(" -", p)


if __name__ == "__main__":
    main()
