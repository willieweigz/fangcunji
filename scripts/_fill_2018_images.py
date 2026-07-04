#!/usr/bin/env python3
"""Fill empty image fields in 2018.json by copying the set's group image (套图)
for each missing stamp. Updates JSON and copies images."""
import json, shutil, os

SRC = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\46-编年号2018年"
DST = r"G:\微云同步文件夹\邮票网站\public\images\stamps\2018"
JSON_PATH = r"G:\微云同步文件夹\邮票网站\data\stamps\2018.json"

# Set number -> source group image filename
GROUP_IMAGES = {
    "2018-4":  "2018-4-元宵节.jpg",
    "2018-6":  "2018-6-海棠花.jpg",
    "2018-9":  "2018-9-马克思诞辰200周年.jpg",
    "2018-13": "2018-13-中国古代科学家及著作（一）.jpg",
    "2018-14": "2018-14-喀什风光.jpg",
    "2018-15": "2018-15-屈原.jpg",
    "2018-17": "2018-17-清正廉洁（一）.jpg",
    "2018-18": "2018-18-水果（三）.jpg",
    "2018-19": "2018-19-近代民族英雄.jpg",
    "2018-20": "2018-20-四景山水图.jpg",
    "2018-21": "2018-21-二十四节气（三）.jpg",
    "2018-23": "2018-23-长江经济带.jpg",
    "2018-24": "2018-24-诗经.jpg",
    "2018-26": "2018-26-宁夏回族自治区成立六十周年.jpg",
    "2018-29": "2018-29-广西壮族自治区成立六十周年.jpg",
    "2018-30": "2018-30-中国国际进口博览会.jpg",
    "2018-31": "2018-31-港珠澳大桥.jpg",
    "2018-32": "2018-32-北京2022年冬奥会—雪上运动.jpg",
    "2018-34": "2018-34-改革开放四十周年.jpg",
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

filled = 0
copied = 0
for s in data:
    sid = s["id"]
    if sid not in GROUP_IMAGES:
        continue
    group_src = os.path.join(SRC, GROUP_IMAGES[sid])
    for st in s["stamps"]:
        if st.get("image"):  # already has an image
            continue
        sn = st["sn"]
        target_name = f"{sid}-{sn}.jpg"
        target_path = os.path.join(DST, target_name)
        image_url = f"/images/stamps/2018/{target_name}"
        # Copy group image
        shutil.copy2(group_src, target_path)
        copied += 1
        # Update JSON
        st["image"] = image_url
        filled += 1
        print(f"  [FILL] {target_name}  <-  {GROUP_IMAGES[sid]}")

# Save updated JSON
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"\nFilled {filled} image fields, copied {copied} images, JSON updated.")
