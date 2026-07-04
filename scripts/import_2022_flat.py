#!/usr/bin/env python3
"""
2022年邮票图片导入 v5 - 完整版（含单枚回退）
"""
import json, os, shutil, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\50-编年号2022年"
DST_DIR = os.path.join(BASE, "public", "images", "stamps", "2022")
DATA_FILE = os.path.join(BASE, "data", "stamps", "2022.json")

SKIP_KW = ["大版张", "小版张", "赠送版", "全张"]

def find_regular_stamp(sid, sn, sname, total_stamps, src_files):
    """Find source file for a regular (non-small-sheet) stamp."""
    candidates = []
    for f in src_files:
        if not (sid + '-' in f or f.startswith(sid.replace('-','') + '-')):
            continue
        # For single-stamp series, the name must match
        if sname not in f:
            continue
        
        base = os.path.splitext(f)[0]
        
        # Look for N-{sn} pattern
        patterns = re.findall(r'(\d+)-(\d+)', base)
        
        if total_stamps == 1:
            # Single stamp: accept the overview image (no N-M pattern needed)
            # But make sure it's not a different type of image
            if not any(kw in f for kw in SKIP_KW):
                candidates.append(f)
        else:
            # Multi-stamp: require sequence number match
            if patterns and any(int(p[1]) == sn for p in patterns):
                candidates.append(f)
    
    return candidates[0] if candidates else None

def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    src_files = [f for f in os.listdir(SRC_DIR) 
                 if f.lower().endswith(('.jpg','.jpeg','.png'))
                 and not any(kw in f for kw in SKIP_KW)]
    
    # Clear dst
    if os.path.exists(DST_DIR):
        for f in os.listdir(DST_DIR):
            os.remove(os.path.join(DST_DIR, f))
    
    copied = 0
    missing = []
    used_src = set()
    
    for series in data:
        sid = series['id']
        total = series['totalStamps']
        
        for stamp in series.get('stamps', []):
            sn = stamp['sn']
            sname = stamp['name']
            fmt = stamp.get('format', '')
            dst_name = f"{sid}-{sn}.jpg"
            
            found = None
            
            if fmt in ('小型张', '小全张'):
                candidates = [f for f in src_files 
                             if sid + '-' in f and fmt in f]
                found = candidates[0] if candidates else None
            else:
                found = find_regular_stamp(sid, sn, sname, total, src_files)
            
            if found:
                shutil.copy2(os.path.join(SRC_DIR, found), 
                            os.path.join(DST_DIR, dst_name))
                used_src.add(found)
                copied += 1
                print(f"  OK {dst_name} <- {found}")
            else:
                missing.append((sid, sn, sname))
                print(f"  !! 缺失 {dst_name} ({sname})")
    
    print(f"\n{'='*50}")
    print(f"复制: {coped}/{copied+len(missing)}")
    if missing:
        print(f"\n缺失 ({len(missing)}):")
        for s, n, name in missing:
            print(f"  {s}-{n}: {name}")

if __name__ == '__main__':
    main()
