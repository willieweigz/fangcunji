#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彻底修复 gen_2014_md.py 中的中文引号配对问题。
策略：将所有 U+201C 和 U+201D 统一替换为 ASCII 双引号，
然后在 Python 字符串字面量内部重新配对为 U+201C(左)...U+201D(右)。
"""

import re

LEFT = '\u201c'
RIGHT = '\u201d'

with open('scripts/gen_2014_md.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Replace all Chinese curly quotes back to ASCII double quotes
content = content.replace(LEFT, '"').replace(RIGHT, '"')

# Step 2: Now we need to find ASCII double quotes that are INSIDE string literals
# and are surrounded by Chinese characters. These should be Chinese curly quotes.
# The string literals are delimited by either ' or " (the outer quotes).

# We'll process line by line. For each line, we identify string values
# and fix inner quotes.

lines = content.split('\n')
fixed_lines = []

for line in lines:
    # For lines like: "key": "value with inner quotes",
    # The value starts after the colon+space+" and ends at the last " before , or }
    # We need to find the value portion and fix inner quotes.

    # Pattern: "key": "....."  (value may contain inner double quotes)
    # We'll match: ("[^"]*":\s*)"(.*)"(\s*[,\n])
    # And in the value (group 2), toggle inner quotes

    m = re.match(r'^(\s*"[^"]*":\s*)"(.*)"(\s*,?\s*)$', line)
    if m:
        prefix = m.group(1)
        value = m.group(2)
        suffix = m.group(3)

        # Toggle inner double quotes in the value
        fixed_value = []
        is_left = True
        for ch in value:
            if ch == '"':
                if is_left:
                    fixed_value.append(LEFT)
                else:
                    fixed_value.append(RIGHT)
                is_left = not is_left
            else:
                fixed_value.append(ch)

        line = prefix + '"' + ''.join(fixed_value) + '"' + suffix

    # Also handle single-quoted strings like ENDING = '...'
    m2 = re.match(r"^(\w+\s*=\s*')(.*)(')\s*$", line)
    if m2:
        prefix = m2.group(1)
        value = m2.group(2)
        suffix = m2.group(3)

        fixed_value = []
        is_left = True
        for ch in value:
            if ch == '"':
                if is_left:
                    fixed_value.append(LEFT)
                else:
                    fixed_value.append(RIGHT)
                is_left = not is_left
            else:
                fixed_value.append(ch)

        line = prefix + ''.join(fixed_value) + suffix

    fixed_lines.append(line)

fixed = '\n'.join(fixed_lines)

with open('scripts/gen_2014_md.py', 'w', encoding='utf-8') as f:
    f.write(fixed)

# Verify
with open('scripts/gen_2014_md.py', 'r', encoding='utf-8') as f:
    content = f.read()
left = content.count(LEFT)
right = content.count(RIGHT)
print(f"After fix: Left={left}, Right={right}, Diff={left-right}")
