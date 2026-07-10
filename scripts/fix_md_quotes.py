#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复已生成的md文件中的引号配对问题：将连续两个左引号中的第二个改为右引号。"""

import os
import glob

BASE = r"G:\微云同步文件夹\邮票网站\新中国邮票图片全集（1949年-2026年最新）\42-编年号2014年"

LEFT_Q = '\u201c'  # "
RIGHT_Q = '\u201d'  # "

for md_path in glob.glob(os.path.join(BASE, "*", "*.md")):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix pattern: LEFT_Q ... LEFT_Q -> should be LEFT_Q ... RIGHT_Q
    # Strategy: iterate through, toggle between expecting left and right quote
    fixed = []
    expect_left = True  # Start expecting left quote
    for ch in content:
        if ch == LEFT_Q:
            if expect_left:
                fixed.append(LEFT_Q)
                expect_left = False
            else:
                fixed.append(RIGHT_Q)
                expect_left = True
        else:
            fixed.append(ch)
    
    result = ''.join(fixed)
    
    if result != content:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Fixed: {os.path.basename(md_path)}")
    else:
        print(f"OK: {os.path.basename(md_path)}")
