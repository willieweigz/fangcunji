"""Batch add 'format' field to all stamp entries in JSON data files.

Rule:
- Regular stamps: format = "{totalStamps}-{sn}"  (e.g. "4-1", "4-2")
- Small sheet/small pane: format = "小型张" or "小全张"

Detection logic:
- Entry already has a "format" field → skip
- Entry's parent set has extras containing "小型张" or "小全张"
  AND this stamp's sn is NOT in range 1..totalStamps → assign small sheet format
- Otherwise → regular stamp: "{totalStamps}-{sn}"
"""

import json
import os

DATA_DIR = r"G:\微云同步文件夹\邮票网站\data\stamps"

for filename in sorted(os.listdir(DATA_DIR)):
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified = False
    for set_data in data:
        total = set_data.get("totalStamps", 0)
        extras = set_data.get("extras", [])

        has_small_sheet = "小型张" in extras
        has_mini_pane = "小全张" in extras

        for stamp in set_data.get("stamps", []):
            if "format" in stamp:
                continue  # already has

            sn = stamp.get("sn", 0)

            if has_small_sheet and sn > total:
                stamp["format"] = "小型张"
            elif has_mini_pane and sn > total:
                stamp["format"] = "小全张"
            else:
                stamp["format"] = f"{total}-{sn}"

            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated: {filename} ({len(data)} sets)")
    else:
        print(f"Skipped: {filename} (no changes)")

print("\nDone!")
