#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复制1991年T和J邮票图片到14-1991年文件夹
"""

import os
import shutil

# 源文件夹
SOURCE_T = "G:/微云同步文件夹/邮票网站/新中国邮票图片全集（1949年-2026年最新）/12-T字头邮票1974年-1991年"
SOURCE_J = "G:/微云同步文件夹/邮票网站/新中国邮票图片全集（1949年-2026年最新）/11-J字头邮票1974年-1991年"
# 目标文件夹
TARGET = "G:/微云同步文件夹/邮票网站/新中国邮票图片全集（1949年-2026年最新）/14-1991年"

# 1991年T字头邮票（按照发行时间顺序）
t_stamps_1991 = [
    "T156",  # 都江堰水利工程 1991-02-20
    "T159",  # 辛未年 1991-01-05
    "T160",  # 计划生育 1991-04-20
    "T161",  # 野羊 1991-05-10
    "T162",  # 杜鹃花 1991-06-25
    "T163",  # 恒山 1991-07-20
    "T164",  # 承德避暑山庄 1991-08-10
    "T165",  # 社会主义建设成就（第四组） 1991-09-20
    "T166",  # 景德镇瓷器 1991-10-11
    "T167",  # 中国古典文学名著-《水浒传》（第三组） 1991-11-19
    "T168",  # 赈灾 1991-09-14
]

# 1991年J字头邮票（按照发行时间顺序）
j_stamps_1991 = [
    "J175",  # 巴黎公社一百二十周年 1991-03-18
    "J176",  # 和平解放西藏四十周年 1991-05-23
    "J177",  # 南极条约生效三十周年 1991-06-23
    "J178",  # 中国共产党成立七十周年 1991-07-01
    "J179",  # 陈胜、吴广农民起义二千二百年 1991-07-07
    "J180",  # 第十三届国际第四纪研究联合会大会 1991-08-02
    "J181",  # 陈毅同志诞生九十周年 1991-08-26
    "J182",  # 辛亥革命时期著名人物 1991-10-10
    "J183",  # 陶行知诞生一百周年 1991-10-18
    "J184",  # 徐向前同志诞生九十周年 1991-11-08
    "J185",  # 第一届世界女子足球锦标赛 1991-11-16
]

def copy_files():
    """复制文件到目标文件夹"""
    if not os.path.exists(TARGET):
        os.makedirs(TARGET)
        print(f"创建目录: {TARGET}")
    
    # 复制T字头邮票
    print("\n复制T字头邮票...")
    for prefix in t_stamps_1991:
        # 查找所有以prefix开头的文件
        files = [f for f in os.listdir(SOURCE_T) if f.startswith(prefix)]
        for file in files:
            src_path = os.path.join(SOURCE_T, file)
            dst_path = os.path.join(TARGET, file)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"  复制: {file}")
            else:
                print(f"  文件不存在: {src_path}")
    
    # 复制J字头邮票
    print("\n复制J字头邮票...")
    for prefix in j_stamps_1991:
        # 查找所有以prefix开头的文件
        files = [f for f in os.listdir(SOURCE_J) if f.startswith(prefix)]
        for file in files:
            src_path = os.path.join(SOURCE_J, file)
            dst_path = os.path.join(TARGET, file)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"  复制: {file}")
            else:
                print(f"  文件不存在: {src_path}")

if __name__ == "__main__":
    print("=" * 60)
    print("复制1991年T和J邮票图片")
    print("=" * 60)
    
    copy_files()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
