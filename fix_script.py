# -*- coding: utf-8 -*-
"""Fix gen_md_82_83.py: convert intro values from double-quoted to single-quoted strings"""
import re

filepath = r"G:\微云同步文件夹\邮票网站\gen_md_82_83.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert any 300e/300f back to double quotes (from previous bad fix)
content = content.replace('\u300e', '\u201c').replace('\u300f', '\u201d')

# Now fix: for each intro line, extract value and wrap in single quotes
lines = content.split('\n')
new_lines = []

for line in lines:
    stripped = line.strip()
    if stripped.startswith('"intro": "') and stripped.endswith('",'):
        indent = line[:len(line) - len(stripped)]
        # Extract the value between the opening " and closing ",
        # The value starts after '"intro": "' and ends before '",'
        # But the value might contain internal " characters
        # We need to find the actual value boundaries
        
        # Simple approach: the line format is exactly: "intro": "VALUE",
        # Where VALUE starts at position len('"intro": "') and ends at position len(stripped) - len('",')
        prefix = '"intro": "'
        suffix = '",'
        value = stripped[len(prefix):-len(suffix)]
        
        # Now wrap in single quotes instead
        new_line = indent + "'intro': '" + value + "',"
        new_lines.append(new_line)
    else:
        new_lines.append(line)

content = '\n'.join(new_lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! All intro values now use single quotes.")
