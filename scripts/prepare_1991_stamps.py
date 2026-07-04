#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准备1991年邮票数据
- 从源文件夹复制图片到public/images/stamps/1991/
- 生成data/stamps/1991.json数据文件
"""

import os
import shutil
import json
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 源图片目录
SOURCE_T = os.path.join("G:", os.sep, "微云同步文件夹", "邮票网站", "新中国邮票图片全集（1949年-2026年最新）", "12-T字头邮票1974年-1991年")
SOURCE_J = os.path.join("G:", os.sep, "微云同步文件夹", "邮票网站", "新中国邮票图片全集（1949年-2026年最新）", "11-J字头邮票1974年-1991年")
# 目标图片目录
TARGET_IMAGES = os.path.join(PROJECT_ROOT, "public", "images", "stamps", "1991")

# 1991年邮票数据（按发行时间顺序）
stamps_1991 = [
    {
        "id": "1991-1",
        "series": "T字头",
        "type": "特种邮票",
        "title": "辛未年",
        "issueDate": "1991-01-05",
        "year": 1991,
        "themes": ["生肖", "生肖羊"],
        "designer": "雷汉林",
        "totalStamps": 1,
        "extras": [],
        "description": "1991年为中国农历辛未羊年，此套邮票是第一轮生肖邮票的最后一套。邮票图案为布玩具羊，造型可爱，色彩鲜艳，体现了民间艺术特色。",
        "quantity": "12000万枚",
        "needsReview": True,
        "localImageFolder": "T159 辛未年",
        "source_folder": SOURCE_T,
        "source_files": ["T159-辛未年.jpeg"],
        "stamps": [
            {"sn": 1, "name": "辛未年", "denomination": "20分", "image": "/images/stamps/1991/1991-1-1.jpg"}
        ]
    },
    {
        "id": "1991-2",
        "series": "T字头",
        "type": "特种邮票",
        "title": "都江堰水利工程",
        "issueDate": "1991-02-20",
        "year": 1991,
        "themes": ["建筑", "水利工程", "都江堰"],
        "designer": "吴建坤",
        "totalStamps": 3,
        "extras": [],
        "description": "都江堰位于四川成都平原西部，是战国时期秦国蜀郡太守李冰父子修建的大型水利工程，至今仍在发挥作用。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T156 都江堰水利工程",
        "source_folder": SOURCE_T,
        "source_files": ["T156-都江堰水利工程.JPG", "T156-都江堰水利工程3-1鱼嘴.JPG", "T156-都江堰水利工程3-2飞沙堰.JPG", "T156-都江堰水利工程3-3宝瓶口.JPG"],
        "stamps": [
            {"sn": 1, "name": "鱼嘴", "denomination": "20分", "image": "/images/stamps/1991/1991-2-1.jpg"},
            {"sn": 2, "name": "飞沙堰", "denomination": "50分", "image": "/images/stamps/1991/1991-2-2.jpg"},
            {"sn": 3, "name": "宝瓶口", "denomination": "80分", "image": "/images/stamps/1991/1991-2-3.jpg"}
        ]
    },
    {
        "id": "1991-3",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "巴黎公社一百二十周年",
        "issueDate": "1991-03-18",
        "year": 1991,
        "themes": ["历史事件", "巴黎公社"],
        "designer": "卢天骄",
        "totalStamps": 1,
        "extras": [],
        "description": "1871年3月18日，法国巴黎爆发了无产阶级革命，建立了世界上第一个无产阶级政权——巴黎公社。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J175 巴黎公社一百二十周年",
        "source_folder": SOURCE_J,
        "source_files": ["J175-巴黎公社一百二十周年.jpg"],
        "stamps": [
            {"sn": 1, "name": "巴黎公社一百二十周年", "denomination": "20分", "image": "/images/stamps/1991/1991-3-1.jpg"}
        ]
    },
]

def copy_images():
    """复制图片到目标文件夹"""
    if not os.path.exists(TARGET_IMAGES):
        os.makedirs(TARGET_IMAGES)
        print(f"创建目录: {TARGET_IMAGES}")
    
    for stamp in stamps_1991:
        print(f"\n处理: {stamp['title']} ({stamp['id']})")
        source_folder = stamp['source_folder']
        
        for idx, source_file in enumerate(stamp['source_files']):
            source_path = os.path.join(source_folder, source_file)
            
            # 确定目标文件名
            if idx == 0 and len(stamp['source_files']) == 1:
                # 只有一枚邮票
                target_file = f"{stamp['id']}-1.jpg"
            elif idx == 0:
                # 第一张可能是整版图片，跳过或者重命名
                print(f"  跳过整版图片: {source_file}")
                continue
            else:
                # 具体邮票图片
                target_file = f"{stamp['id']}-{idx}.jpg"
            
            target_path = os.path.join(TARGET_IMAGES, target_file)
            
            # 复制文件
            if os.path.exists(source_path):
                shutil.copy2(source_path, target_path)
                print(f"  复制: {source_file} -> {target_file}")
            else:
                print(f"  文件不存在: {source_path}")

def generate_json():
    """生成1991.json数据文件"""
    output_file = os.path.join(PROJECT_ROOT, "data", "stamps", "1991.json")
    
    # 这里只输出前3套邮票作为示例
    output_data = stamps_1991
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n生成数据文件: {output_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("准备1991年邮票数据")
    print("=" * 60)
    
    # 复制图片
    copy_images()
    
    # 生成JSON数据
    generate_json()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
