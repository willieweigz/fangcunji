"""Update 2022.json with themes, issue dates, denominations, descriptions."""
import json

DATA_FILE = r"G:\微云同步文件夹\邮票网站\data\stamps\2022.json"

# Complete data for all 27 series of 2022
# Format: {id: {issueDate, themes, designer, description, stamps: {sn: {denomination}}}}
SERIES_DATA = {
    "2022-1": {
        "issueDate": "2022-01-05",
        "themes": ["生肖", "虎"],
        "description": "《壬寅年》特种邮票，全套2枚，图案分别为「国运昌隆」「虎蕴吉祥」。另发行小本票。",
        "stamps": {1: "1.20元", 2: "1.20元"}
    },
    "2022-2": {
        "issueDate": "2022-01-01",
        "themes": ["经济", "国际合作"],
        "description": "《〈区域全面经济伙伴关系协定〉生效》纪念邮票，全套1枚。RCEP现有15个成员国，是世界上最大的自贸区。",
        "stamps": {1: "1.20元"}
    },
    "2022-3": {
        "issueDate": "2022-04-23",
        "themes": ["文学", "红楼梦"],
        "description": "《中国古典文学名著——〈红楼梦〉（五）》特种邮票，全套4枚加小型张1枚。小型张图案为「寒塘鹤影」。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.50元", 5: "6元"}
    },
    "2022-4": {
        "issueDate": "2022-02-04",
        "themes": ["体育", "冬奥会"],
        "description": "《第24届冬季奥林匹克运动会开幕纪念》纪念邮票，全套2枚。北京2022年冬奥会于2月4日开幕。",
        "stamps": {1: "1.20元", 2: "1.20元"}
    },
    "2022-5": {
        "issueDate": "2022-02-14",
        "themes": ["外交", "国际合作"],
        "description": "《中墨建交五十周年》纪念邮票，全套2枚，与墨西哥联合发行。图案分别为观星台和库库尔坎金字塔。",
        "stamps": {1: "1.20元", 2: "1.20元"}
    },
    "2022-6": {
        "issueDate": "2022-04-28",
        "themes": ["自然遗产", "喀斯特"],
        "description": "《世界自然遗产——中国南方喀斯特》特种邮票，全套7枚。展现石林、荔波、武隆、桂林、施秉、金佛山、环江七处喀斯特地貌。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元", 5: "1.20元", 6: "1.20元", 7: "1.20元"}
    },
    "2022-7": {
        "issueDate": "2022-05-05",
        "themes": ["政治", "青年"],
        "description": "《中国共产主义青年团成立一百周年》纪念邮票，全套2枚。图案为「永远跟党走」「请党放心 强国有我」。",
        "stamps": {1: "80分", 2: "1.20元"}
    },
    "2022-8": {
        "issueDate": "2022-05-18",
        "themes": ["名画", "古画"],
        "description": "《姑苏繁华图》特种邮票，全套6枚。原画为清代徐扬所绘，描绘苏州繁华景象，现藏辽宁省博物馆。",
        "stamps": {1: "80分", 2: "1.20元", 3: "1.20元", 4: "1.20元", 5: "1.50元", 6: "1.50元"}
    },
    "2022-9": {
        "issueDate": "2022-05-19",
        "themes": ["建筑", "古镇"],
        "description": "《中国古镇（四）》特种邮票，全套4枚。展现江西浮梁瑶里镇、浙江富阳龙门镇、福建晋江安海镇、山东微山南阳镇。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元"}
    },
    "2022-10": {
        "issueDate": "2022-05-28",
        "themes": ["风光", "湖泊"],
        "description": "《洞庭湖》特种邮票，全套4枚加小型张1枚。小型张图案为「洞庭天下水」。",
        "stamps": {1: "80分", 2: "80分", 3: "1.20元", 4: "1.20元", 5: "6元"}
    },
    "2022-11": {
        "issueDate": "2022-06-01",
        "themes": ["青少年", "教育"],
        "description": "《我和祖国一起成长》特种邮票，全套5枚。展现热爱祖国、刻苦学习、崇尚科学、强健体魄、尊重劳动五个主题。",
        "stamps": {1: "80分", 2: "80分", 3: "1.20元", 4: "1.20元", 5: "1.20元"}
    },
    "2022-12": {
        "issueDate": "2022-06-06",
        "themes": ["教育", "大学"],
        "description": "《东南大学建校一百二十周年》纪念邮票，全套1枚。东南大学始建于1902年。",
        "stamps": {1: "1.20元"}
    },
    "2022-13": {
        "issueDate": "2022-06-28",
        "themes": ["建设", "水利"],
        "description": "《水电建设》特种邮票，全套2枚。展现乌东德水电站和白鹤滩水电站两座世界级水利工程。",
        "stamps": {1: "1.20元", 2: "1.20元"}
    },
    "2022-14": {
        "issueDate": "2022-07-23",
        "themes": ["政治", "党史"],
        "description": "《第一部〈中国共产党章程〉通过一百周年》纪念邮票，全套1枚。1922年7月中共二大通过第一部党章。",
        "stamps": {1: "1.20元"}
    },
    "2022-15": {
        "issueDate": "2022-07-30",
        "themes": ["文化", "建筑"],
        "description": "《中国国家版本馆》特种邮票，全套1枚。国家版本馆是中华版本典藏中心，总馆位于北京。",
        "stamps": {1: "1.20元"}
    },
    "2022-16": {
        "issueDate": "2022-08-05",
        "themes": ["文化", "篆刻"],
        "description": "《中国篆刻》特种邮票，全套4枚。展现战国至唐代四方经典印章。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元"}
    },
    "2022-17": {
        "issueDate": "2022-08-13",
        "themes": ["戏曲", "非物质文化遗产"],
        "description": "《秦腔》特种邮票，全套3枚。秦腔是中国最古老的戏曲剧种之一，国家级非物质文化遗产。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元"}
    },
    "2022-18": {
        "issueDate": "2022-09-03",
        "themes": ["动画", "儿童"],
        "description": "《动画——黑猫警长》特种邮票，全套5枚。黑猫警长是中国经典动画形象，深受几代人喜爱。",
        "stamps": {1: "80分", 2: "80分", 3: "1.20元", 4: "1.20元", 5: "1.20元"}
    },
    "2022-19": {
        "issueDate": "2022-09-05",
        "themes": ["文物", "虎"],
        "description": "《虎（文物）》特种邮票，全套6枚。精选商代至清代六件与虎相关的珍贵文物。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元", 5: "1.20元", 6: "1.20元"}
    },
    "2022-20": {
        "issueDate": "2022-09-07",
        "themes": ["人物", "科学家"],
        "description": "《中国现代科学家（九）》纪念邮票，全套4枚。展现刘东生、程开甲、吴文俊、袁隆平四位科学家。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元"}
    },
    "2022-21": {
        "issueDate": "2022-09-08",
        "themes": ["教育", "大学"],
        "description": "《北京师范大学建校一百二十周年》纪念邮票，全套1枚。北师大始建于1902年。",
        "stamps": {1: "1.20元"}
    },
    "2022-22": {
        "issueDate": "2022-10-03",
        "themes": ["建筑", "园林"],
        "description": "《中国名亭（二）》特种邮票，全套4枚。展现知春亭、水流云在亭、万春亭、双环亭四大名亭。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元"}
    },
    "2022-23": {
        "issueDate": "2022-10-16",
        "themes": ["政治", "党史"],
        "description": "《中国共产党第二十次全国代表大会》纪念邮票，全套2枚加小型张1枚。小型张为「庆祝中国共产党第二十次全国代表大会胜利召开」。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "6元"}
    },
    "2022-24": {
        "issueDate": "2022-10-22",
        "themes": ["人物", "中医药"],
        "description": "《张仲景》特种邮票，全套2枚加小型张1枚。张仲景为东汉医学家，著有《伤寒杂病论》。小型张为「张仲景像」。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "6元"}
    },
    "2022-25": {
        "issueDate": "2022-11-05",
        "themes": ["动物", "鸟类"],
        "description": "《鸽》特种邮票，全套4枚。展现岩鸽、斑尾林鸽、雪鸽、斑林鸽四种鸽类。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元"}
    },
    "2022-26": {
        "issueDate": "2022-11-05",
        "themes": ["自然", "国家公园"],
        "description": "《国家公园》纪念邮票，全套5枚。展现三江源、大熊猫、东北虎豹、海南热带雨林、武夷山五个国家公园。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.20元", 4: "1.20元", 5: "1.20元"}
    },
    "2022-27": {
        "issueDate": "2022-12-25",
        "themes": ["科技", "航天"],
        "description": "《中国空间站》纪念邮票，全套4枚。展现天地往返、空间科学、出舱活动、太空家园。",
        "stamps": {1: "1.20元", 2: "1.20元", 3: "1.50元", 4: "1.50元"}
    }
}

# Special fixes for stamp names
NAME_FIXES = {
    "2022-23": {1: "奋进新征程"},  # Remove spurious "2建功新时代"
}

# Load existing data
data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))

updated_count = 0

for series in data:
    sid = series['id']
    if sid not in SERIES_DATA:
        print(f"WARNING: {sid} not in SERIES_DATA")
        continue
    
    sd = SERIES_DATA[sid]
    
    # Update series-level fields
    series['issueDate'] = sd['issueDate']
    series['themes'] = sd['themes']
    series['description'] = sd['description']
    series['needsReview'] = False
    
    # Update stamp-level fields
    name_fixes = NAME_FIXES.get(sid, {})
    for stamp in series['stamps']:
        sn = stamp['sn']
        if sn in sd['stamps']:
            stamp['denomination'] = sd['stamps'][sn]
        if sn in name_fixes:
            stamp['name'] = name_fixes[sn]
    
    updated_count += 1
    print(f"  Updated {sid}: {series['title']} ({series['issueDate']}) themes={sd['themes']}")

# Save
json.dump(data, open(DATA_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"\nUpdated {updated_count} series. Data saved to {DATA_FILE}")
