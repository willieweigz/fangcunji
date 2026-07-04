#!/usr/bin/env python3
"""Import 2017 stamp images: explicit mapping for individual images,
group image fallback for stamps without individual images.
Also converts PNG to JPG."""
import shutil, os, sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\45-编年号2017年"
DST = r"G:\微云同步文件夹\邮票网站\public\images\stamps\2017"

os.makedirs(DST, exist_ok=True)

# (source filename, target filename) — for stamps WITH individual images
INDIVIDUAL = [
    # 2017-1 丁酉年 (sn=1 has individual)
    ("2017-1-丁酉年2-1意气风发.jpg", "2017-1-1.jpg"),
    # 2017-6 春夏秋冬 (sn=1,3,4 have individual)
    ("2017-6-春夏秋冬4-1春燕剪柳.jpg", "2017-6-1.jpg"),
    ("2017-6-春夏秋冬4-3秋鸡鸣穗.jpg", "2017-6-3.jpg"),
    ("2017-6-春夏秋冬4-4冬雪映梅.jpg", "2017-6-4.jpg"),
    # 2017-7 西游记二 (4 PNG files -> convert to JPG)
    ("2017-7-中国古典文学名著—《西游记》（二）4-1 智收白龙马.png", "2017-7-1.jpg"),
    ("2017-7-中国古典文学名著—《西游记》（二）4-2 猪八戒拜师.png", "2017-7-2.jpg"),
    ("2017-7-中国古典文学名著—《西游记》（二）4-3 沙河收沙僧.png", "2017-7-3.jpg"),
    ("2017-7-中国古典文学名著—《西游记》（二）4-4 偷吃人参果.png", "2017-7-4.jpg"),
    # 2017-9 内蒙古七十周年 (sn=2 has individual)
    ("2017-9-内蒙古自治区成立七十周年3-2亮丽北疆.jpg", "2017-9-2.jpg"),
    # 2017-11 中国恐龙 (6 individual + 小型张)
    ("2017-11-中国恐龙6-1青岛龙.jpg", "2017-11-1.jpg"),
    ("2017-11-中国恐龙6-2永川龙.jpg", "2017-11-2.jpg"),
    ("2017-11-中国恐龙6-3华阳龙.jpg", "2017-11-3.jpg"),
    ("2017-11-中国恐龙6-4中华龙鸟.jpg", "2017-11-4.jpg"),
    ("2017-11-中国恐龙6-5巨盗龙.jpg", "2017-11-5.jpg"),
    ("2017-11-中国恐龙6-6小盗龙.jpg", "2017-11-6.jpg"),
    ("2017-11-中国恐龙-小型张.jpg", "2017-11-7.jpg"),
    # 2017-14 锦鲤 (8 individual)
    ("2017-14-锦鲤8-1红白.jpg", "2017-14-1.jpg"),
    ("2017-14-锦鲤8-2大正三色.jpg", "2017-14-2.jpg"),
    ("2017-14-锦鲤8-3昭和三色.jpg", "2017-14-3.jpg"),
    ("2017-14-锦鲤8-4秋翠.jpg", "2017-14-4.jpg"),
    ("2017-14-锦鲤8-5黄金.jpg", "2017-14-5.jpg"),
    ("2017-14-锦鲤8-6白别甲.jpg", "2017-14-6.jpg"),
    ("2017-14-锦鲤8-7绯写.jpg", "2017-14-7.jpg"),
    ("2017-14-锦鲤8-8红白丹顶.jpg", "2017-14-8.jpg"),
    # 2017-16 小全张
    ("2017-16-香港回归祖国二十周年-小全张两地联合.jpg", "2017-16-4.jpg"),
    # 2017-18 小型张
    ("2017-18-中国人民解放军建军九十周年-小型张-听党指挥.jpg", "2017-18-7.jpg"),
    # 2017-20 小全张
    ("2017-20-中华人民共和国第十三届运动会-小全张.jpg", "2017-20-3.jpg"),
    # 2017-24 小型张
    ("2017-24-张骞-小型张-张骞像.jpg", "2017-24-3.jpg"),
    # 2017-26 小型张
    ("2017-26-中国共产党第十九次全国代表大会-小型张-筑梦.jpg", "2017-26-3.jpg"),
    # 2017-28 大版张 individual images
    ("2017-28-沧州铁狮子与巴肯寺狮子-大版张2-1沧州铁狮子.jpg", "2017-28-1.jpg"),
    ("2017-28-沧州铁狮子与巴肯寺狮子-大版张2-2巴肯寺狮子.jpg", "2017-28-2.jpg"),
    # 2017-29 小型张
    ("2017-29-中国高速铁路发展成就-小型张-“复兴号”动车组.jpg", "2017-29-5.jpg"),
    # 2017-31 大版张 individual images
    ("2017-31-北京2022年冬奥会会徽和冬残奥会会徽-大版张2-1冬奥会会徽.jpg", "2017-31-1.jpg"),
    ("2017-31-北京2022年冬奥会会徽和冬残奥会会徽-大版张2-2冬残奥会会徽.jpg", "2017-31-2.jpg"),
]

# Set number -> group image filename (for stamps WITHOUT individual images)
GROUP_IMAGES = {
    "2017-1":  "2017-1-丁酉年.jpg",
    "2017-2":  "2017-2-拜年.jpg",
    "2017-3":  "2017-3-千里江山图.jpg",
    "2017-4":  "2017-4-商务印书馆.jpg",
    "2017-5":  "2017-5-京津冀协同发展.jpg",
    "2017-6":  "2017-6-春夏秋冬.jpg",
    "2017-8":  "2017-8-红山文化玉器.jpg",
    "2017-9":  "2017-9-内蒙古自治区成立七十周年.jpg",
    "2017-10": "2017-10-“一带一路”国际合作高峰论坛.jpg",
    "2017-12": "2017-12-浙江大学建校一百二十周年.jpg",
    "2017-13": "2017-13-儿童游戏（一）.jpg",
    "2017-15": "2017-15-国际禁毒日.jpg",
    "2017-16": "2017-16-香港回归祖国二十周年.jpg",
    "2017-17": "2017-17-凤（文物）.jpg",
    "2017-18": "2017-18-中国人民解放军建军九十周年.jpg",
    "2017-19": "2017-19-金砖国家领导人厦门会晤.jpg",
    "2017-20": "2017-20-中华人民共和国第十三届运动会.jpg",
    "2017-21": "2017-21-喜鹊.jpg",
    "2017-22": "2017-22-外国音乐家（二）.jpg",
    "2017-23": "2017-23-科技创新.jpg",
    "2017-24": "2017-24-张骞.jpg",
    "2017-25": "2017-25-粤剧.jpg",
    "2017-26": "2017-26-中国共产党第十九次全国代表大会.jpg",
    "2017-27": "2017-27-记者节.jpg",
    "2017-29": "2017-29-中国高速铁路发展成就.jpg",
    "2017-30": "2017-30-河北雄安新区设立纪念.jpg",
}

# Import JSON to know which stamps need group images
import json
with open(r"G:\微云同步文件夹\邮票网站\data\stamps\2017.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ok = 0
fail = 0

# Step 1: Copy individual images (convert PNG to JPG)
for src_name, dst_name in INDIVIDUAL:
    src_path = os.path.join(SRC, src_name)
    dst_path = os.path.join(DST, dst_name)
    if not os.path.exists(src_path):
        print(f"  [MISSING] {src_name}")
        fail += 1
        continue
    if src_name.lower().endswith(".png"):
        # Convert PNG to JPG
        with Image.open(src_path) as im:
            im.convert("RGB").save(dst_path, "JPEG", quality=90)
        print(f"  [PNG->JPG] {dst_name}  <-  {src_name[:40]}...  ({os.path.getsize(dst_path)//1024}KB)")
    else:
        shutil.copy2(src_path, dst_path)
        print(f"  [OK] {dst_name}  <-  {src_name[:40]}...  ({os.path.getsize(dst_path)//1024}KB)")
    ok += 1

# Step 2: Fill group images for stamps with empty image field
filled = 0
for s in data:
    sid = s["id"]
    if sid not in GROUP_IMAGES:
        continue
    group_src = os.path.join(SRC, GROUP_IMAGES[sid])
    for st in s["stamps"]:
        if st.get("image"):  # already has individual image
            continue
        sn = st["sn"]
        target_name = f"{sid}-{sn}.jpg"
        target_path = os.path.join(DST, target_name)
        st["image"] = f"/images/stamps/2017/{target_name}"
        shutil.copy2(group_src, target_path)
        filled += 1
        print(f"  [GROUP] {target_name}  <-  {GROUP_IMAGES[sid][:30]}...")

# Save updated JSON
with open(r"G:\微云同步文件夹\邮票网站\data\stamps\2017.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nDone: {ok} individual copied, {filled} group filled, {fail} missing")
