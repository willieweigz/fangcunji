#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 gen_2014_md.py 中的引号问题：字符串内的 ASCII 双引号替换为中文弯引号。"""

import re

with open('scripts/gen_2014_md.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy: find all Python string literals and replace inner ASCII double quotes
# with Chinese curly quotes (U+201C left, U+201D right)
# A string literal starts with " after a colon or opening bracket,
# and the closing " is at end of line (before comma or closing bracket)

lines = content.split('\n')
fixed_lines = []

for line in lines:
    # Match lines like:  "key": "value with "inner" quotes",
    # We need to find the value part and fix inner quotes
    
    # Pattern: after "key": "  ... the value ... "  ,
    # Find the value string and fix inner quotes
    
    # Simple approach: for lines that have a string value containing Chinese text,
    # count the double quotes. If there are more than 2 (or 4 for key+value),
    # the extra ones need to be converted to curly quotes.
    
    # Even simpler: replace patterns like 中文字"中文 with 中文字\u201c中文
    # and 中文"中文标点 with 中文\u201d中文标点
    
    # Use regex: find " that is preceded by a CJK character and followed by a CJK character
    # -> replace with left curly quote \u201c
    line = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f])"(?=[\u4e00-\u9fff])', '\u201c', line)
    
    # Find " that is preceded by a CJK character and followed by CJK punctuation
    # -> replace with right curly quote \u201d
    line = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f])"(?=[\u3000-\u303f\uff00-\uffef])', '\u201d', line)
    
    # Find " that is preceded by CJK punctuation and followed by CJK char (for left quote after punctuation)
    line = re.sub(r'(?<=[\u3000-\u303f\uff00-\uffef])"(?=[\u4e00-\u9fff])', '\u201c', line)
    
    fixed_lines.append(line)

fixed = '\n'.join(fixed_lines)

with open('scripts/gen_2014_md.py', 'w', encoding='utf-8') as f:
    f.write(fixed)

print("Done. Fixed quotes in gen_2014_md.py")
