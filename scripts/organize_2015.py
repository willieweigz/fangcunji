#!/usr/bin/env python3
"""整理2015年邮票文件夹：将平铺图片按套归入子文件夹，格式对齐2024年标准"""
import os
import re
import shutil

SRC = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\43-编年号2015年"

# 1. 收集所有jpg文件
files = [f for f in os.listdir(SRC) if f.lower().endswith(".jpg")]
print(f"总文件数: {len(files)}")

# 2. 按 2015-N 分组
# 正则: 2015-(数字)-(剩余标题部分).jpg
groups = {}  # {num: [filenames]}
for f in files:
    m = re.match(r"^2015-(\d+)-(.+)\.jpg$", f)
    if not m:
        print(f"[警告] 无法匹配: {f}")
        continue
    num = int(m.group(1))
    groups.setdefault(num, []).append(f)

print(f"共 {len(groups)} 套邮票\n")

# 3. 对每套提取标题（取最短文件名作为封面，去掉 2015-N- 前缀和 .jpg 后缀）
plan = []  # [(num, title, folder_name, [files])]
for num in sorted(groups.keys()):
    file_list = sorted(groups[num])
    # 封面文件 = 最短的文件名（没有额外后缀的）
    cover = min(file_list, key=len)
    # 提取标题：去掉 "2015-N-" 前缀 和 ".jpg" 后缀
    title = re.sub(r"^2015-\d+-", "", cover).replace(".jpg", "")
    folder_name = f"2015-{num} 《{title}》"
    plan.append((num, title, folder_name, file_list))

# 4. 打印计划
for num, title, folder_name, file_list in plan:
    print(f"  {folder_name}  ({len(file_list)} 个文件)")
    for f in file_list:
        print(f"    <- {f}")
    print()

# 5. 执行：创建子文件夹并移动
print("=" * 60)
print("开始执行移动...")
moved = 0
for num, title, folder_name, file_list in plan:
    folder_path = os.path.join(SRC, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    for f in file_list:
        src_path = os.path.join(SRC, f)
        dst_path = os.path.join(folder_path, f)
        if os.path.exists(dst_path):
            print(f"[跳过] 已存在: {dst_path}")
            continue
        shutil.move(src_path, dst_path)
        moved += 1
    print(f"[OK] {folder_name} <- {len(file_list)} 个文件")

print(f"\n完成！共移动 {moved} 个文件，创建 {len(plan)} 个子文件夹")

# 6. 验证：根目录下应只剩子文件夹
remaining_files = [f for f in os.listdir(SRC) if os.path.isfile(os.path.join(SRC, f))]
if remaining_files:
    print(f"\n[警告] 根目录下仍有 {len(remaining_files)} 个散落文件:")
    for f in remaining_files:
        print(f"  {f}")
else:
    print("\n[验证] 根目录下无散落文件，全部归入子文件夹 ✓")
