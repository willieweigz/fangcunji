"""Copy 2022 stamp images from flat source directory."""

import os
import re
import json

SRC = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\50-编年号2022年"
DST_DIR = r"G:\微云同步文件夹\邮票网站\public\images\stamps\2022"
JSON_FILE = r"G:\微云同步文件夹\邮票网站\data\stamps\2022.json"

# Load JSON to know the mapping
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

src_files = sorted(os.listdir(SRC))
image_files = [f for f in src_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

os.makedirs(DST_DIR, exist_ok=True)

copied = 0
errors = []

for set_data in data:
    set_num = int(set_data["id"].split("-")[1])
    set_name = set_data["title"]
    
    entries = [f for f in image_files if re.match(fr'2022-{set_num}-', f)]
    
    for stamp in set_data["stamps"]:
        sn = stamp["sn"]
        fmt = stamp["format"]
        
        if fmt == "小型张":
            # Find small sheet source file
            src_match = None
            for f in entries:
                if '小型张' in f:
                    src_match = f
                    break
        elif fmt == "小全张":
            src_match = None
            for f in entries:
                if '小全张' in f:
                    src_match = f
                    break
        else:
            # Regular stamp: find file with matching M-K pattern
            src_match = None
            target_mk = f"^{set_num}-"
            
            for f in entries:
                rest = re.sub(rf'^2022-{set_num}-', '', f)
                # Skip sheet/non-stamp
                if any(kw in rest for kw in ['大版张', '小版张', '赠送版', '全张邮票折', '小型张', '小全张']):
                    continue
                
                # Check if this file matches the stamp
                mk_patterns = list(re.finditer(r'(\d+)[-—](\d+)', rest))
                if mk_patterns:
                    last = mk_patterns[-1]
                    f_total = int(last.group(1))
                    f_seq = int(last.group(2))
                    if f_seq == sn and f_total == int(fmt.split("-")[0]):
                        src_match = f
                        break
                else:
                    # Single stamp overview
                    if sn == 1:
                        src_match = f
                        break
        
        # Fallback: also check overview file
        if not src_match and sn == 1:
            for f in entries:
                rest = re.sub(rf'^2022-{set_num}-', '', f)
                rest = re.sub(r'\.(jpg|jpeg|png)$', '', rest, flags=re.IGNORECASE)
                if not re.search(r'\d+[-—]\d+', rest):
                    if not any(kw in rest for kw in ['大版张', '小版张', '赠送版', '全张邮票折', '小型张', '小全张']):
                        src_match = f
                        break
        
        if src_match:
            dst_name = stamp["image"].split("/")[-1]
            dst_path = os.path.join(DST_DIR, dst_name)
            src_path = os.path.join(SRC, src_match)
            
            import shutil
            shutil.copy2(src_path, dst_path)
            copied += 1
        else:
            errors.append(f"  2022-{set_num}-{sn}: NO SOURCE FOUND (fmt={fmt}, name={stamp['name']})")

print(f"Copied: {copied} images")
if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(e)
else:
    print("All images copied successfully!")
