#!/usr/bin/env python3
"""整理2016-2022年邮票文件夹：将平铺图片按套归入子文件夹，格式对齐2024年标准"""
import os
import re
import shutil

BASE = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）"

YEAR_DIRS = {
    2016: "44-编年号2016年",
    2017: "45-编年号2017年",
    2018: "46-编年号2018年",
    2019: "47-编年号2019年",
    2020: "48-编年号2020年",
    2021: "49-编年号2021年",
    2022: "50-编年号2022年",
}

total_moved = 0
total_folders = 0
total_errors = []

for year, dirname in YEAR_DIRS.items():
    src = os.path.join(BASE, dirname)
    print(f"\n{'='*60}")
    print(f"处理 {year} 年 ({dirname})")
    print(f"{'='*60}")

    files = [f for f in os.listdir(src) if f.lower().endswith(".jpg") and os.path.isfile(os.path.join(src, f))]
    print(f"  散落 jpg 文件数: {len(files)}")

    if not files:
        print("  [跳过] 无文件")
        continue

    # 按 YEAR-N 分组
    groups = {}
    unmatched = []
    for f in files:
        m = re.match(rf"^{year}-(\d+)-(.+)\.jpg$", f)
        if not m:
            unmatched.append(f)
            continue
        num = int(m.group(1))
        groups.setdefault(num, []).append(f)

    if unmatched:
        print(f"  [警告] {len(unmatched)} 个文件无法匹配:")
        for f in unmatched:
            print(f"    {f}")

    print(f"  共 {len(groups)} 套邮票\n")

    for num in sorted(groups.keys()):
        file_list = sorted(groups[num])
        # 封面文件 = 最短的文件名（没有额外后缀的）
        cover = min(file_list, key=len)
        # 提取标题：去掉 "YEAR-N-" 前缀 和 ".jpg" 后缀
        title = re.sub(rf"^{year}-\d+-", "", cover).replace(".jpg", "")
        folder_name = f"{year}-{num} 《{title}》"
        folder_path = os.path.join(src, folder_name)

        os.makedirs(folder_path, exist_ok=True)
        moved = 0
        for f in file_list:
            src_path = os.path.join(src, f)
            dst_path = os.path.join(folder_path, f)
            if os.path.exists(dst_path):
                print(f"    [跳过] 已存在: {dst_path}")
                continue
            shutil.move(src_path, dst_path)
            moved += 1

        print(f"  [OK] {folder_name} <- {moved}/{len(file_list)} 个文件")
        total_moved += moved
        total_folders += 1

    # 验证
    remaining = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    if remaining:
        print(f"\n  [警告] 根目录下仍有 {len(remaining)} 个散落文件:")
        for f in remaining:
            print(f"    {f}")
            total_errors.append(f"{dirname}/{f}")
    else:
        print(f"  [验证] 根目录下无散落文件 ✓")

print(f"\n{'='*60}")
print(f"全部完成！")
print(f"  共创建 {total_folders} 个子文件夹")
print(f"  共移动 {total_moved} 个文件")
if total_errors:
    print(f"  [警告] {len(total_errors)} 个文件未处理")
else:
    print(f"  所有文件均已归入子文件夹 ✓")
