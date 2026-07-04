"""Verify 2022 stamp images — cross-reference each stamp MD5 against source."""
import json
import os
import hashlib
import re

SOURCE = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\50-编年号2022年"
TARGET = r"G:\微云同步文件夹\邮票网站\public\images\stamps\2022"
DATA_FILE = r"G:\微云同步文件夹\邮票网站\data\stamps\2022.json"

def md5(fpath):
    h = hashlib.md5()
    with open(fpath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def find_source_file(series_id, title, stamp_name, sn, total, fmt, source_files):
    """Given stamp info, find the matching source file."""
    
    if fmt in ("小型张", "小全张"):
        for sf in source_files:
            if f"{series_id}-" in sf and title in sf and stamp_name in sf:
                if "小型张" in sf or "小全张" in sf:
                    return sf
        return None
    
    if total == 1:
        prefix = f"{series_id}-{title}"
        for sf in source_files:
            if sf.startswith(prefix):
                basename = sf[len(prefix):]
                if any(kw in basename for kw in ['大版张', '小版张', '赠送版', '全张', '小型张', '小全张']):
                    continue
                if re.search(r'\d+-\d+', basename):
                    continue
                return sf
        return None
    
    # Regular multi-stamp
    expected = f"{series_id}-{title}{total}-{sn}{stamp_name}.jpg"
    if expected in source_files:
        return expected
    return None

# Load data
data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
source_files = set(os.listdir(SOURCE))
source_files = {f for f in source_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))}

issues = []
verified = 0
total = 0

for series in data:
    sid = series['id']
    title = series['title']
    n_total = series['totalStamps']
    
    for stamp in series['stamps']:
        total += 1
        sn = stamp['sn']
        name = stamp['name']
        fmt = stamp['format']
        
        # Build target path
        tgt_file = f"{sid}-{sn}.jpg"
        tgt_path = os.path.join(TARGET, tgt_file)
        
        # Find source file
        src_file = find_source_file(sid, title, name, sn, n_total, fmt, source_files)
        
        tgt_exists = os.path.exists(tgt_path)
        
        if not tgt_exists:
            issues.append(f"[MISSING] {sid} ({fmt}) {name} -> target {tgt_file} not found")
            continue
        
        if src_file is None:
            issues.append(f"[NO_SRC] {sid} ({fmt}) {name} -> no source match")
            continue
        
        src_path = os.path.join(SOURCE, src_file)
        
        try:
            if md5(src_path) == md5(tgt_path):
                verified += 1
            else:
                issues.append(f"[MISMATCH] {sid} ({fmt}) {name} -> MD5 differs: src={src_file}")
        except Exception as e:
            issues.append(f"[ERROR] {sid} ({fmt}) {name} -> {e}")

print(f"=== 2022 邮票图片校验结果 ===")
print(f"总计: {total} 张")
print(f"通过: {verified} 张")
print(f"问题: {len(issues)} 张")
print()

if issues:
    for i in issues:
        print(i)
else:
    print("全部通过！")
