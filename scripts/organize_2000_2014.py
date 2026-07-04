#!/usr/bin/env python3
"""整理2000-2014年邮票文件夹：将平铺图片按套归入子文件夹，格式对齐2024年标准"""
import os
import re
import shutil

BASE = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）"

# 文件夹映射: year -> dirname
YEAR_DIRS = {
    2000: "25-编年号2000年",
    2001: "26-编年号2001年",
    2002: "27-编年号2002年",
    2003: "29-编年号2003年",
    2004: "30-编年号2004年",
    2005: "31-编年号2005年",
    2006: "32-编年号2006年",
    2007: "34-编年号2007年",
    2008: "35-编年号2008年",
    2009: "36-编年号2009年",
    2010: "37-编年号2010年",
    2011: "38-编年号2011年",
    2012: "39-编年号2012年",
    2013: "40-编年号2013年",
    2014: "42-编年号2014年",
}

total_moved = 0
total_folders = 0
total_leftover = 0

for year, dirname in YEAR_DIRS.items():
    src = os.path.join(BASE, dirname)
    print(f"\n{'='*60}")
    print(f"处理 {year} 年 ({dirname})")
    print(f"{'='*60}")

    # 收集所有文件（jpg/jpeg/png），不限于jpg
    files = [f for f in os.listdir(src)
             if os.path.isfile(os.path.join(src, f))
             and re.match(rf"^{year}-\d+", f)
             and f.lower().endswith((".jpg", ".jpeg", ".png"))]

    # 也收集不匹配的文件
    all_files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    unmatched = [f for f in all_files if f not in files]

    print(f"  总文件数: {len(all_files)}, 可匹配: {len(files)}")

    if not files:
        print("  [跳过] 无匹配文件")
        continue

    # 按 YEAR-N 分组
    groups = {}
    for f in files:
        m = re.match(rf"^({year})-(\d+)-(.+)\.(jpg|jpeg|png)$", f, re.IGNORECASE)
        if not m:
            unmatched.append(f)
            continue
        num = int(m.group(2))
        groups.setdefault(num, []).append(f)

    print(f"  共 {len(groups)} 套邮票")

    for num in sorted(groups.keys()):
        file_list = sorted(groups[num])
        # 封面文件 = 最短的文件名（没有额外后缀的）
        cover = min(file_list, key=len)
        # 提取标题：去掉 "YEAR-N-" 前缀 和 扩展名
        title = re.sub(rf"^{year}-\d+-", "", cover)
        title = re.sub(r"\.(jpg|jpeg|png)$", "", title, flags=re.IGNORECASE)
        folder_name = f"{year}-{num} 《{title}》"
        folder_path = os.path.join(src, folder_name)

        os.makedirs(folder_path, exist_ok=True)
        moved = 0
        for f in file_list:
            src_path = os.path.join(src, f)
            dst_path = os.path.join(folder_path, f)
            if os.path.exists(dst_path):
                continue
            shutil.move(src_path, dst_path)
            moved += 1

        print(f"  [OK] {folder_name} <- {moved}/{len(file_list)} 个文件")
        total_moved += moved
        total_folders += 1

    # 处理不匹配的文件
    if unmatched:
        print(f"\n  [警告] {len(unmatched)} 个文件无法按 {year}-N 模式匹配:")
        for f in unmatched:
            print(f"    {f}")
        total_leftover += len(unmatched)

    # 验证
    remaining = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    if remaining:
        print(f"  根目录剩余 {len(remaining)} 个散落文件")
    else:
        print(f"  [验证] 根目录下无散落文件 ✓")

print(f"\n{'='*60}")
print(f"全部完成！")
print(f"  共创建 {total_folders} 个子文件夹")
print(f"  共移动 {total_moved} 个文件")
if total_leftover:
    print(f"  [警告] {total_leftover} 个文件未处理（非标准命名）")
else:
    print(f"  所有文件均已归入子文件夹 ✓")
