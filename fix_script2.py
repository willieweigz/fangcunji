# -*- coding: utf-8 -*-
"""Fix: replace all Chinese curly quotes with ASCII quotes inside stamps tuples and other places"""
filepath = r"G:\微云同步文件夹\邮票网站\gen_md_82_83.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all Chinese left/right double quotes with simple angle brackets for display
# This avoids any Python string delimiter issues
content = content.replace('\u201c', '\u300e')  # left " → 『
content = content.replace('\u201d', '\u300f')  # right " → 』

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced all Chinese curly quotes with angle quotes.")
