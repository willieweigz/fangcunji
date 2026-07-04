#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成1991年邮票完整数据文件
按发行时间顺序排列，共22套邮票
"""

import json
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_IMAGES = os.path.join(PROJECT_ROOT, "public", "images", "stamps", "1991")
SOURCE_T = "G:/微云同步文件夹/邮票网站/新中国邮票图片全集（1949年-2026年最新）/12-T字头邮票1974年-1991年"
SOURCE_J = "G:/微云同步文件夹/邮票网站/新中国邮票图片全集（1949年-2026年最新）/11-J字头邮票1974年-1991年"

# 1991年邮票完整数据（按发行时间顺序）
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
        "description": "1991年为中国农历辛未羊年，此套邮票是第一轮生肖邮票的最后一套。邮票图案为布玩具羊，造型可爱，色彩鲜艳，体现了民间艺术特色。画面中羔羊侧身伫立，昂首啸天，下垂的长耳与微微前倾的身躯，生动传达了羊的温顺与坚韧。",
        "quantity": "12000万枚",
        "needsReview": False,
        "localImageFolder": "T159 辛未年",
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
        "description": "都江堰位于四川成都平原西部，是战国时期秦国蜀郡太守李冰父子修建的大型水利工程，至今仍在发挥作用。邮票展示了都江堰的三大主体工程：鱼嘴、飞沙堰和宝瓶口。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T156 都江堰水利工程",
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
        "description": "1871年3月18日，法国巴黎爆发了无产阶级革命，建立了世界上第一个无产阶级政权——巴黎公社。邮票展现了巴黎公社的标志性场景。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J175 巴黎公社一百二十周年",
        "stamps": [
            {"sn": 1, "name": "巴黎公社一百二十周年", "denomination": "20分", "image": "/images/stamps/1991/1991-3-1.jpg"}
        ]
    },
    {
        "id": "1991-4",
        "series": "T字头",
        "type": "特种邮票",
        "title": "计划生育",
        "issueDate": "1991-04-20",
        "year": 1991,
        "themes": ["社会", "计划生育"],
        "designer": "王虎鸣",
        "totalStamps": 2,
        "extras": [],
        "description": "计划生育是中国的一项基本国策。邮票通过'控制人口数量'和'提高人口素质'两枚图案，宣传计划生育的重要性。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T160 计划生育",
        "stamps": [
            {"sn": 1, "name": "控制人口数量", "denomination": "20分", "image": "/images/stamps/1991/1991-4-1.jpg"},
            {"sn": 2, "name": "提高人口素质", "denomination": "50分", "image": "/images/stamps/1991/1991-4-2.jpg"}
        ]
    },
    {
        "id": "1991-5",
        "series": "T字头",
        "type": "特种邮票",
        "title": "野羊",
        "issueDate": "1991-05-10",
        "year": 1991,
        "themes": ["动物", "野羊"],
        "designer": "殷会利",
        "totalStamps": 4,
        "extras": [],
        "description": "野羊是指生活在野外的羊类动物。邮票选取了四种珍稀野羊：高鼻羚羊、扭角羚、盘羊和北山羊，均为国家重点保护动物。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T161 野羊",
        "stamps": [
            {"sn": 1, "name": "高鼻羚羊", "denomination": "20分", "image": "/images/stamps/1991/1991-5-1.jpg"},
            {"sn": 2, "name": "扭角羚", "denomination": "20分", "image": "/images/stamps/1991/1991-5-2.jpg"},
            {"sn": 3, "name": "盘羊", "denomination": "50分", "image": "/images/stamps/1991/1991-5-3.jpg"},
            {"sn": 4, "name": "北山羊", "denomination": "50分", "image": "/images/stamps/1991/1991-5-4.jpg"}
        ]
    },
    {
        "id": "1991-6",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "和平解放西藏四十周年",
        "issueDate": "1991-05-23",
        "year": 1991,
        "themes": ["历史事件", "西藏", "和平解放"],
        "designer": "嘎德",
        "totalStamps": 2,
        "extras": ["小型张"],
        "description": "1951年5月23日，中央人民政府与西藏地方政府签订《关于和平解放西藏办法的协议》，西藏实现和平解放。邮票展现了西藏和平解放后的繁荣景象。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J176 和平解放西藏四十周年",
        "stamps": [
            {"sn": 1, "name": "歌舞", "denomination": "20分", "image": "/images/stamps/1991/1991-6-1.jpg"},
            {"sn": 2, "name": "金桥", "denomination": "50分", "image": "/images/stamps/1991/1991-6-2.jpg"}
        ]
    },
    {
        "id": "1991-7",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "南极条约生效三十周年",
        "issueDate": "1991-06-23",
        "year": 1991,
        "themes": ["国际事件", "南极条约"],
        "designer": "王虎鸣",
        "totalStamps": 1,
        "extras": [],
        "description": "《南极条约》于1961年6月23日生效，旨在保证南极洲用于和平目的，促进国际科学合作。1991年是该条约生效三十周年。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J177 南极条约生效三十周年",
        "stamps": [
            {"sn": 1, "name": "南极条约生效三十周年", "denomination": "20分", "image": "/images/stamps/1991/1991-7-1.jpg"}
        ]
    },
    {
        "id": "1991-8",
        "series": "T字头",
        "type": "特种邮票",
        "title": "杜鹃花",
        "issueDate": "1991-06-25",
        "year": 1991,
        "themes": ["植物花卉", "杜鹃花"],
        "designer": "曾孝濂",
        "totalStamps": 8,
        "extras": ["小型张"],
        "description": "杜鹃花是中国十大名花之一，品种繁多，色彩艳丽。邮票展现了八种珍稀杜鹃花：马缨杜鹃、黄杜鹃、映山红、棕背杜鹃、凝毛杜鹃、云锦杜鹃、大树杜鹃和大王杜鹃。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T162 杜鹃花",
        "stamps": [
            {"sn": 1, "name": "马缨杜鹃", "denomination": "20分", "image": "/images/stamps/1991/1991-8-1.jpg"},
            {"sn": 2, "name": "黄杜鹃", "denomination": "20分", "image": "/images/stamps/1991/1991-8-2.jpg"},
            {"sn": 3, "name": "映山红", "denomination": "20分", "image": "/images/stamps/1991/1991-8-3.jpg"},
            {"sn": 4, "name": "棕背杜鹃", "denomination": "20分", "image": "/images/stamps/1991/1991-8-4.jpg"},
            {"sn": 5, "name": "凝毛杜鹃", "denomination": "50分", "image": "/images/stamps/1991/1991-8-5.jpg"},
            {"sn": 6, "name": "云锦杜鹃", "denomination": "50分", "image": "/images/stamps/1991/1991-8-6.jpg"},
            {"sn": 7, "name": "大树杜鹃", "denomination": "1.60元", "image": "/images/stamps/1991/1991-8-7.jpg"},
            {"sn": 8, "name": "大王杜鹃", "denomination": "1.60元", "image": "/images/stamps/1991/1991-8-8.jpg"}
        ]
    },
    {
        "id": "1991-9",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "中国共产党成立七十周年",
        "issueDate": "1991-07-01",
        "year": 1991,
        "themes": ["历史事件", "建党纪念"],
        "designer": "雷汉林",
        "totalStamps": 2,
        "extras": [],
        "description": "1921年7月，中国共产党第一次全国代表大会在上海召开，标志着中国共产党的成立。1991年是建党七十周年。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J178 中国共产党成立七十周年",
        "stamps": [
            {"sn": 1, "name": "中共'一大'南湖会议会址", "denomination": "20分", "image": "/images/stamps/1991/1991-9-1.jpg"},
            {"sn": 2, "name": "光辉的七十年", "denomination": "50分", "image": "/images/stamps/1991/1991-9-2.jpg"}
        ]
    },
    {
        "id": "1991-10",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "陈胜、吴广起义二千二百年",
        "issueDate": "1991-07-07",
        "year": 1991,
        "themes": ["历史事件", "农民起义"],
        "designer": "姜伟杰、李庆发",
        "totalStamps": 1,
        "extras": [],
        "description": "公元前209年，陈胜、吴广领导了中国历史上第一次大规模的农民起义，揭开了秦末农民战争的序幕。1991年是起义二千二百周年。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J179 陈胜、吴广起义二千二百周年",
        "stamps": [
            {"sn": 1, "name": "陈胜、吴广起义二千二百年", "denomination": "20分", "image": "/images/stamps/1991/1991-10-1.jpg"}
        ]
    },
    {
        "id": "1991-11",
        "series": "T字头",
        "type": "特种邮票",
        "title": "恒山",
        "issueDate": "1991-07-20",
        "year": 1991,
        "themes": ["山水风光", "五岳", "恒山"],
        "designer": "杨文清、李德福",
        "totalStamps": 4,
        "extras": [],
        "description": "恒山位于山西省大同市浑源县，是中国五岳中的北岳。邮票展现了恒山的四大景观：悬空古寺、恒山雪霁、北岳恒宗和云中胜迹。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T163 恒山",
        "stamps": [
            {"sn": 1, "name": "悬空古寺", "denomination": "20分", "image": "/images/stamps/1991/1991-11-1.jpg"},
            {"sn": 2, "name": "恒山雪霁", "denomination": "20分", "image": "/images/stamps/1991/1991-11-2.jpg"},
            {"sn": 3, "name": "北岳恒宗", "denomination": "55分", "image": "/images/stamps/1991/1991-11-3.jpg"},
            {"sn": 4, "name": "云中胜迹", "denomination": "80分", "image": "/images/stamps/1991/1991-11-4.jpg"}
        ]
    },
    {
        "id": "1991-12",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "第十三届国际第四纪研究联合会大会",
        "issueDate": "1991-08-02",
        "year": 1991,
        "themes": ["国际事件", "学术会议"],
        "designer": "黄里",
        "totalStamps": 1,
        "extras": [],
        "description": "国际第四纪研究联合会（INQUA）是致力于第四纪研究的国际学术组织。第十三届大会于1991年在中国北京召开。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J180 第十三届国际第四纪研究联合会大会",
        "stamps": [
            {"sn": 1, "name": "第十三届国际第四纪研究联合会大会", "denomination": "20分", "image": "/images/stamps/1991/1991-12-1.jpg"}
        ]
    },
    {
        "id": "1991-13",
        "series": "T字头",
        "type": "特种邮票",
        "title": "承德避暑山庄",
        "issueDate": "1991-08-10",
        "year": 1991,
        "themes": ["建筑", "园林", "承德避暑山庄"],
        "designer": "肖玉田",
        "totalStamps": 3,
        "extras": ["小型张"],
        "description": "承德避暑山庄位于河北省承德市，是清代皇帝避暑和处理政务的场所，也是中国现存最大的古典皇家园林。邮票展现了山庄的三处景观：万壑松风、水榭环碧和青风绿屿。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T164 承德避暑山庄",
        "stamps": [
            {"sn": 1, "name": "万壑松风", "denomination": "20分", "image": "/images/stamps/1991/1991-13-1.jpg"},
            {"sn": 2, "name": "水榭环碧", "denomination": "50分", "image": "/images/stamps/1991/1991-13-2.jpg"},
            {"sn": 3, "name": "青风绿屿", "denomination": "90分", "image": "/images/stamps/1991/1991-13-3.jpg"}
        ]
    },
    {
        "id": "1991-14",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "陈毅同志诞生九十周年",
        "issueDate": "1991-08-26",
        "year": 1991,
        "themes": ["人物", "陈毅"],
        "designer": "李印清",
        "totalStamps": 2,
        "extras": [],
        "description": "陈毅（1901-1972），中国无产阶级革命家、军事家，中华人民共和国元帅。1991年是陈毅同志诞生九十周年。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J181 陈毅同志诞生九十周年",
        "stamps": [
            {"sn": 1, "name": "陈毅同志肖像", "denomination": "20分", "image": "/images/stamps/1991/1991-14-1.jpg"},
            {"sn": 2, "name": "冬夜杂咏之一", "denomination": "50分", "image": "/images/stamps/1991/1991-14-2.jpg"}
        ]
    },
    {
        "id": "1991-15",
        "series": "T字头",
        "type": "特种邮票",
        "title": "赈灾",
        "issueDate": "1991-09-14",
        "year": 1991,
        "themes": ["社会", "赈灾"],
        "designer": "王虎鸣、赵玉华",
        "totalStamps": 1,
        "extras": [],
        "description": "1991年夏季，中国华东地区遭遇特大洪涝灾害。为支援灾区人民，中国邮政特发行此套赈灾邮票，邮票销售收入全部用于赈灾。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T168 赈灾",
        "stamps": [
            {"sn": 1, "name": "赈灾", "denomination": "80分", "image": "/images/stamps/1991/1991-15-1.jpg"}
        ]
    },
    {
        "id": "1991-16",
        "series": "T字头",
        "type": "特种邮票",
        "title": "社会主义建设成就（第四组）",
        "issueDate": "1991-09-20",
        "year": 1991,
        "themes": ["科技", "建设成就"],
        "designer": "陈晓聪",
        "totalStamps": 4,
        "extras": [],
        "description": "邮票展现了改革开放后中国社会主义建设的新成就：洛阳玻璃厂、乌鲁木齐石化总厂大化肥工程、沈大高速公路和西昌卫星发射中心。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T165 社会主义建设成就（第四组）",
        "stamps": [
            {"sn": 1, "name": "洛阳玻璃厂", "denomination": "20分", "image": "/images/stamps/1991/1991-16-1.jpg"},
            {"sn": 2, "name": "乌鲁木齐石化总厂大化肥工程", "denomination": "25分", "image": "/images/stamps/1991/1991-16-2.jpg"},
            {"sn": 3, "name": "沈大高速公路", "denomination": "55分", "image": "/images/stamps/1991/1991-16-3.jpg"},
            {"sn": 4, "name": "西昌卫星发射中心", "denomination": "80分", "image": "/images/stamps/1991/1991-16-4.jpg"}
        ]
    },
    {
        "id": "1991-17",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "辛亥革命时期著名人物",
        "issueDate": "1991-10-10",
        "year": 1991,
        "themes": ["人物", "辛亥革命"],
        "designer": "王书朋",
        "totalStamps": 3,
        "extras": [],
        "description": "1911年爆发的辛亥革命推翻了清朝统治，结束了中国两千多年的封建帝制。邮票纪念了三位辛亥革命时期的著名人物：徐锡麟、秋瑾和宋教仁。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J182 辛亥革命时期著名人物",
        "stamps": [
            {"sn": 1, "name": "徐锡麟", "denomination": "20分", "image": "/images/stamps/1991/1991-17-1.jpg"},
            {"sn": 2, "name": "秋瑾", "denomination": "50分", "image": "/images/stamps/1991/1991-17-2.jpg"},
            {"sn": 3, "name": "宋教仁", "denomination": "80分", "image": "/images/stamps/1991/1991-17-3.jpg"}
        ]
    },
    {
        "id": "1991-18",
        "series": "T字头",
        "type": "特种邮票",
        "title": "景德镇瓷器",
        "issueDate": "1991-10-11",
        "year": 1991,
        "themes": ["文物古迹", "瓷器", "景德镇"],
        "designer": "陈荣明、张磊",
        "totalStamps": 6,
        "extras": [],
        "description": "景德镇位于江西省，是中国著名的瓷都。邮票展现了六件景德镇瓷器精品：宋·青白釉注·注盌、元·青花追韩信图梅瓶、明·五彩云龙纹盖罐、清·五彩花鸟纹尊、现代·青花釉里红鲤鱼盘和现代·描金吊灯图案八角薄胎碗。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T166 景德镇瓷器",
        "stamps": [
            {"sn": 1, "name": "宋·青白釉注·注盌", "denomination": "20分", "image": "/images/stamps/1991/1991-18-1.jpg"},
            {"sn": 2, "name": "元·青花追韩信图梅瓶", "denomination": "25分", "image": "/images/stamps/1991/1991-18-2.jpg"},
            {"sn": 3, "name": "明·五彩云龙纹盖罐", "denomination": "45分", "image": "/images/stamps/1991/1991-18-3.jpg"},
            {"sn": 4, "name": "清·五彩花鸟纹尊", "denomination": "55分", "image": "/images/stamps/1991/1991-18-4.jpg"},
            {"sn": 5, "name": "现代·青花釉里红鲤鱼盘", "denomination": "80分", "image": "/images/stamps/1991/1991-18-5.jpg"},
            {"sn": 6, "name": "现代·描金吊灯图案八角薄胎碗", "denomination": "2元", "image": "/images/stamps/1991/1991-18-6.jpg"}
        ]
    },
    {
        "id": "1991-19",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "陶行知诞生一百周年",
        "issueDate": "1991-10-18",
        "year": 1991,
        "themes": ["人物", "陶行知"],
        "designer": "马刚",
        "totalStamps": 2,
        "extras": [],
        "description": "陶行知（1891-1946），中国教育家，提出'生活即教育'、'社会即学校'、'教学做合一'等教育理念。1991年是陶行知诞生一百周年。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J183 陶行知诞生一百周年",
        "stamps": [
            {"sn": 1, "name": "陶行知肖像", "denomination": "20分", "image": "/images/stamps/1991/1991-19-1.jpg"},
            {"sn": 2, "name": "求真与做人", "denomination": "50分", "image": "/images/stamps/1991/1991-19-2.jpg"}
        ]
    },
    {
        "id": "1991-20",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "徐向前同志诞生九十周年",
        "issueDate": "1991-11-08",
        "year": 1991,
        "themes": ["人物", "徐向前"],
        "designer": "刘向平",
        "totalStamps": 2,
        "extras": [],
        "description": "徐向前（1901-1990），中国无产阶级革命家、军事家，中华人民共和国元帅。1991年是徐向前同志诞生九十周年。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J184 徐向前同志诞生九十周年",
        "stamps": [
            {"sn": 1, "name": "人民公仆", "denomination": "20分", "image": "/images/stamps/1991/1991-20-1.jpg"},
            {"sn": 2, "name": "峥嵘岁月", "denomination": "50分", "image": "/images/stamps/1991/1991-20-2.jpg"}
        ]
    },
    {
        "id": "1991-21",
        "series": "J字头",
        "type": "纪念邮票",
        "title": "第一届世界女子足球锦标赛",
        "issueDate": "1991-11-16",
        "year": 1991,
        "themes": ["体育", "足球"],
        "designer": "王虎鸣",
        "totalStamps": 2,
        "extras": [],
        "description": "第一届世界女子足球锦标赛于1991年在中国广东举行，这是中国首次举办国际性女子足球赛事。邮票展现了锦标赛的会徽和运动员英姿。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "J185 第一届世界女子足球锦标赛",
        "stamps": [
            {"sn": 1, "name": "会徽", "denomination": "20分", "image": "/images/stamps/1991/1991-21-1.jpg"},
            {"sn": 2, "name": "英姿", "denomination": "50分", "image": "/images/stamps/1991/1991-21-2.jpg"}
        ]
    },
    {
        "id": "1991-22",
        "series": "T字头",
        "type": "特种邮票",
        "title": "中国古典文学名著－－《水浒传》（第三组）",
        "issueDate": "1991-11-19",
        "year": 1991,
        "themes": ["文学名著", "水浒传"],
        "designer": "周峰",
        "totalStamps": 4,
        "extras": ["小型张"],
        "description": "《水浒传》是中国四大古典文学名著之一，描写了北宋末年以宋江为首的梁山泊英雄好汉的故事。此套邮票是《水浒传》系列第三组，展现了四个精彩故事场景。",
        "quantity": "未知",
        "needsReview": True,
        "localImageFolder": "T167 中国古典文学名著-《水浒传》（第三组）",
        "stamps": [
            {"sn": 1, "name": "梁山泊戴宗传假信", "denomination": "20分", "image": "/images/stamps/1991/1991-22-1.jpg"},
            {"sn": 2, "name": "一丈青单捉王矮虎", "denomination": "25分", "image": "/images/stamps/1991/1991-22-2.jpg"},
            {"sn": 3, "name": "顾大嫂登州大劫牢", "denomination": "45分", "image": "/images/stamps/1991/1991-22-3.jpg"},
            {"sn": 4, "name": "孙立计破祝家庄", "denomination": "1.60元", "image": "/images/stamps/1991/1991-22-4.jpg"}
        ]
    }
]

def copy_images():
    """复制图片到目标文件夹"""
    if not os.path.exists(TARGET_IMAGES):
        os.makedirs(TARGET_IMAGES)
        print(f"创建目录: {TARGET_IMAGES}")
    
    # 图片映射表：源文件名 -> 目标文件名
    image_mapping = {
        # T159 辛未年
        "T159-辛未年.jpeg": "1991-1-1.jpg",
        
        # T156 都江堰水利工程
        "T156-都江堰水利工程3-1鱼嘴.JPG": "1991-2-1.jpg",
        "T156-都江堰水利工程3-2飞沙堰.JPG": "1991-2-2.jpg",
        "T156-都江堰水利工程3-3宝瓶口.JPG": "1991-2-3.jpg",
        
        # J175 巴黎公社
        "J175-巴黎公社一百二十周年.jpg": "1991-3-1.jpg",
        
        # T160 计划生育
        "T160-计划生育2-1控制人口数量.JPG": "1991-4-1.jpg",
        "T160-计划生育2-2提高人口素质.JPG": "1991-4-2.jpg",
        
        # T161 野羊
        "T161-野羊4-1高鼻羚羊.JPG": "1991-5-1.jpg",
        "T161-野羊4-2扭角羚.JPG": "1991-5-2.jpg",
        "T161-野羊4-3盘羊.JPG": "1991-5-3.jpg",
        "T161-野羊4-4北山羊.JPG": "1991-5-4.jpg",
        
        # J176 和平解放西藏
        "J176-和平解放西藏四十周年2-1歌舞.jpg": "1991-6-1.jpg",
        "J176-和平解放西藏四十周年2-2金桥.jpg": "1991-6-2.jpg",
        "J176-和平解放西藏四十周年-小型张-欢庆.jpg": "1991-6-小型张.jpg",
        
        # J177 南极条约
        "J177-南极条约生效三十周年.jpg": "1991-7-1.jpg",
        
        # T162 杜鹃花
        "T162-杜鹃花8-1马缨杜鹃.JPG": "1991-8-1.jpg",
        "T162-杜鹃花8-2黄杜鹃.JPG": "1991-8-2.jpg",
        "T162-杜鹃花8-3映山红.JPG": "1991-8-3.jpg",
        "T162-杜鹃花8-4棕背杜鹃.JPG": "1991-8-4.jpg",
        "T162-杜鹃花8-5凝毛杜鹃.JPG": "1991-8-5.jpg",
        "T162-杜鹃花8-6云锦杜鹃.JPG": "1991-8-6.jpg",
        "T162-杜鹃花8-7大树杜鹃.JPG": "1991-8-7.jpg",
        "T162-杜鹃花8-8大王杜鹃.JPG": "1991-8-8.jpg",
        "T162-杜鹃花-小型张-黄杯杜鹃.JPG": "1991-8-小型张.jpg",
        
        # J178 建党七十周年
        "J178-中国共产党成立七十周年2-1中共‘一大’南湖会议会址.jpg": "1991-9-1.jpg",
        "J178-中国共产党成立七十周年2-2光辉的七十年.jpg": "1991-9-2.jpg",
        
        # J179 陈胜吴广
        "J179-陈胜、吴广起义二千二百周年.jpg": "1991-10-1.jpg",
        
        # T163 恒山
        "T163-恒山4-1悬空古寺.JPG": "1991-11-1.jpg",
        "T163-恒山4-2恒山雪霁.JPG": "1991-11-2.jpg",
        "T163-恒山4-3北岳恒宗.JPG": "1991-11-3.jpg",
        "T163-恒山4-4云中胜迹.JPG": "1991-11-4.jpg",
        
        # J180 第四纪研究
        "J180-第十三届国际第四纪研究联合会大会.jpg": "1991-12-1.jpg",
        
        # T164 承德避暑山庄
        "T164-承德避暑山庄3-1万壑松风.JPG": "1991-13-1.jpg",
        "T164-承德避暑山庄3-2水榭环碧.JPG": "1991-13-2.jpg",
        "T164-承德避暑山庄3-3青风绿屿.JPG": "1991-13-3.jpg",
        "T164-承德避暑山庄-小型张-澄湖叠翠，无暑清凉.JPG": "1991-13-小型张.jpg",
        
        # J181 陈毅
        "J181-陈毅同志诞生九十周年2-1陈毅同志肖像.jpg": "1991-14-1.jpg",
        "J181-陈毅同志诞生九十周年2-2冬夜杂咏之一.jpg": "1991-14-2.jpg",
        
        # T168 赈灾
        "T168-赈灾.JPG": "1991-15-1.jpg",
        
        # T165 建设成就
        "T165-社会主义建设成就（第四组）4-1洛阳玻璃厂.JPG": "1991-16-1.jpg",
        "T165-社会主义建设成就（第四组）4-2乌鲁木齐石化总厂大化肥工程.JPG": "1991-16-2.jpg",
        "T165-社会主义建设成就（第四组）4-3沈大高速公路.JPG": "1991-16-3.jpg",
        "T165-社会主义建设成就（第四组）4-4西昌卫星发射中心.JPG": "1991-16-4.jpg",
        
        # J182 辛亥革命
        "J182-辛亥革命时期著名人物3-1徐锡麟.jpg": "1991-17-1.jpg",
        "J182-辛亥革命时期著名人物3-2秋瑾.jpg": "1991-17-2.jpg",
        "J182-辛亥革命时期著名人物3-3宋教仁.jpg": "1991-17-3.jpg",
        
        # T166 景德镇瓷器
        "T166-景德镇瓷器6-1宋·青白釉注·注盌.JPG": "1991-18-1.jpg",
        "T166-景德镇瓷器6-2元·青花追韩信图梅瓶.JPG": "1991-18-2.jpg",
        "T166-景德镇瓷器6-3明·五彩云龙纹盖罐.JPG": "1991-18-3.jpg",
        "T166-景德镇瓷器6-4清·五彩花鸟纹尊.JPG": "1991-18-4.jpg",
        "T166-景德镇瓷器6-5现代·青花釉里红鲤鱼盘.JPG": "1991-18-5.jpg",
        "T166-景德镇瓷器6-6现代·描金吊灯图案八角薄胎碗.JPG": "1991-18-6.jpg",
        
        # J183 陶行知
        "J183-陶行知诞生一百周年2-1陶行知肖像.jpg": "1991-19-1.jpg",
        "J183-陶行知诞生一百周年2-2求真与做人.jpg": "1991-19-2.jpg",
        
        # J184 徐向前
        "J184-徐向前同志诞生九十周年2-1人民公仆.jpg": "1991-20-1.jpg",
        "J184-徐向前同志诞生九十周年2-2峥嵘岁月.jpg": "1991-20-2.jpg",
        
        # J185 女足
        "J185-第一届世界女子足球锦标赛2-1会徽.jpg": "1991-21-1.jpg",
        "J185-第一届世界女子足球锦标赛2-2英姿.jpg": "1991-21-2.jpg",
        
        # T167 水浒传
        "T167-中国古典文学名著-《水浒传》（第三组）4-1梁山泊戴宗传假信.JPG": "1991-22-1.jpg",
        "T167-中国古典文学名著-《水浒传》（第三组）4-2一丈青单捉王矮虎.JPG": "1991-22-2.jpg",
        "T167-中国古典文学名著-《水浒传》（第三组）4-3顾大嫂登州大劫牢.JPG": "1991-22-3.jpg",
        "T167-中国古典文学名著-《水浒传》（第三组）4-4孙立计破祝家庄.JPG": "1991-22-4.jpg",
        "T167-中国古典文学名著-《水浒传》（第三组）-小型张-四路劫法场.JPG": "1991-22-小型张.jpg",
    }
    
    print("开始复制图片...")
    for src_file, dst_file in image_mapping.items():
        # 判断源文件在T文件夹还是J文件夹
        if src_file.startswith("T"):
            src_path = os.path.join(SOURCE_T, src_file)
        else:
            src_path = os.path.join(SOURCE_J, src_file)
        
        dst_path = os.path.join(TARGET_IMAGES, dst_file)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"  复制: {src_file} -> {dst_file}")
        else:
            print(f"  文件不存在: {src_path}")

def generate_json():
    """生成1991.json数据文件"""
    output_file = os.path.join(PROJECT_ROOT, "data", "stamps", "1991.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stamps_1991, f, ensure_ascii=False, indent=2)
    
    print(f"\n生成数据文件: {output_file}")
    print(f"共 {len(stamps_1991)} 套邮票")

if __name__ == "__main__":
    print("=" * 60)
    print("生成1991年邮票数据")
    print("=" * 60)
    
    # 复制图片
    copy_images()
    
    # 生成JSON数据
    generate_json()
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
