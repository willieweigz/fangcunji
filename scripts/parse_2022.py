"""Parse 2022 stamps - v6 final: handle single-stamp sets properly."""

import os
import re
import json

SRC = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）\50-编年号2022年"
DST_JSON = r"G:\微云同步文件夹\邮票网站\data\stamps\2022.json"

files = sorted(os.listdir(SRC))
image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

type_memorial = {2, 4, 7, 14, 23}

# Step 1: extract set names from overview files
set_names = {}
for f in image_files:
    m = re.match(r'2022-(\d+)-(.+?)\.(jpg|jpeg|png)$', f, re.IGNORECASE)
    if m:
        name_part = m.group(2)
        if not re.search(r'\d+[-—]\d+', name_part):
            if not any(kw in name_part for kw in ['大版张', '小版张', '小型张', '小全张', '赠送版', '全张邮票折']):
                set_names[int(m.group(1))] = name_part.strip()

sets_data = []

for set_num in sorted(set_names.keys()):
    set_name = set_names[set_num]
    entries = [f for f in image_files if re.match(fr'2022-{set_num}-', f)]
    
    stamps = []
    ss_files = []
    mp_files = []
    
    for f in entries:
        rest = re.sub(rf'^2022-{set_num}-', '', f)
        rest_noext = re.sub(r'\.(jpg|jpeg|png)$', '', rest, flags=re.IGNORECASE)
        
        if any(kw in rest for kw in ['大版张', '小版张', '赠送版', '全张邮票折']):
            continue
        
        if '小型张' in rest:
            ss_files.append(f)
            continue
        
        if '小全张' in rest:
            mp_files.append(f)
            continue
        
        mk_patterns = list(re.finditer(r'(\d+)[-—](\d+)', rest_noext))
        if mk_patterns:
            last = mk_patterns[-1]
            total = int(last.group(1))
            seq = int(last.group(2))
            desc = rest_noext[last.end():].strip()
            stamps.append((seq, total, desc, f))
        else:
            # Might be single stamp overview or just overview for a multi-stamp set
            # We'll distinguish below
            stamps.append((1, 1, set_name, f))

    # If there are individual stamp files (M-K pattern), skip the overview file
    has_individual = any(t > 1 for _, t, _, _ in stamps)
    if has_individual:
        stamps = [(s, t, d, f) for s, t, d, f in stamps if t > 1]
    
    # Sort, deduplicate by seq
    seen = {}
    for seq, total, desc, f in stamps:
        if seq not in seen:
            seen[seq] = (seq, total, desc, f)
    stamps = sorted(seen.values(), key=lambda x: x[0])
    
    total_stamps = stamps[0][1] if stamps else 1
    
    # Build stamps array
    stamp_list = []
    for seq, total, desc, f in stamps:
        stamp_list.append({
            "sn": seq,
            "name": desc if desc else set_name,
            "denomination": "",
            "image": f"/images/stamps/2022/2022-{set_num}-{seq}.jpg",
            "format": f"{total}-{seq}"
        })
    
    # Extras
    extras = []
    
    # Small sheet
    if ss_files:
        sn = len(stamp_list) + 1
        ss_name = ""
        for sf in ss_files:
            rest = re.sub(rf'^2022-{set_num}-', '', sf)
            rest = re.sub(r'\.(jpg|jpeg|png)$', '', rest, flags=re.IGNORECASE)
            m = re.search(r'小型张[-—]*(.+)$', rest)
            if m:
                ss_name = m.group(1).strip()
                break
        extras.append("小型张")
        stamp_list.append({
            "sn": sn,
            "name": ss_name or "小型张",
            "denomination": "6元",
            "image": f"/images/stamps/2022/2022-{set_num}-{sn}.jpg",
            "format": "小型张"
        })
    
    if mp_files:
        sn = len(stamp_list) + 1
        extras.append("小全张")
        stamp_list.append({
            "sn": sn,
            "name": set_name,
            "denomination": "",
            "image": f"/images/stamps/2022/2022-{set_num}-{sn}.jpg",
            "format": "小全张"
        })
    
    if any('小版张' in f for f in entries):
        if '小版张' not in extras:
            extras.append('小版张')
    
    stamp_type = "纪念邮票" if set_num in type_memorial else "特种邮票"
    
    sets_data.append({
        "id": f"2022-{set_num}",
        "series": "编年",
        "type": stamp_type,
        "title": set_name,
        "issueDate": f"2022-__-__",
        "year": 2022,
        "themes": [],
        "designer": "",
        "totalStamps": total_stamps,
        "extras": extras,
        "description": "",
        "needsReview": True,
        "stamps": stamp_list
    })

with open(DST_JSON, "w", encoding="utf-8") as f:
    json.dump(sets_data, f, ensure_ascii=False, indent=2)

print(f"Generated: {len(sets_data)} sets, {sum(len(s.get('stamps', [])) for s in sets_data)} stamps\n")

# Check single-stamp sets
singles = [s for s in sets_data if s['totalStamps'] == 1]
print(f"Single-stamp sets ({len(singles)}):")
for s in singles:
    print(f"  {s['id']}: {s['title']} -> {len(s['stamps'])} entries")
print()

# Check 0-entry sets
zero = [s for s in sets_data if len(s['stamps']) == 0]
if zero:
    print(f"WARNING: {len(zero)} sets with 0 entries:")
    for s in zero:
        print(f"  {s['id']}: {s['title']}")
else:
    print("All sets have entries!")

for s in sets_data:
    print(f"{s['id']}: {s['title']} totalStamps={s['totalStamps']} entries={len(s['stamps'])} extras={s['extras']}")
