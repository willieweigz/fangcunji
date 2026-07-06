# -*- coding: utf-8 -*-
"""Final fix: replace bare 『...』 in stamps tuples with properly quoted strings"""
import re

filepath = r"G:\微云同步文件夹\邮票网站\gen_md_82_83.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace pattern:  『text』  when it appears as a standalone value between comma/paren
# e.g. , 『惊艳』,  → , "『惊艳』",
# Use a simpler approach: find all 『...』 that are NOT inside a quoted string
# Simpler: just replace all 『 with "『 and all 』 with 』" — but only when NOT already inside quotes

# Actually simplest: find all occurrences of bare 『text』 (not preceded by " or ')
# and wrap them

def fix_bare_angle_quotes(content):
    lines = content.split('\n')
    result = []
    for line in lines:
        # Check if line has bare 『...』 (not inside quotes)
        # Simple heuristic: if the line has 『 that's not preceded by " or '
        new_line = ""
        i = 0
        while i < len(line):
            if line[i] == '\u300e':  # 『
                # Check if preceded by " or '
                if i > 0 and line[i-1] in '"\'':
                    new_line += line[i]
                else:
                    new_line += '"\u300e'
            elif line[i] == '\u300f':  # 』
                # Check if followed by " or '
                if i < len(line) - 1 and line[i+1] in '"\'':
                    new_line += line[i]
                else:
                    new_line += '\u300f"'
            else:
                new_line += line[i]
            i += 1
        result.append(new_line)
    return '\n'.join(result)

content = fix_bare_angle_quotes(content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed bare angle quotes.")
