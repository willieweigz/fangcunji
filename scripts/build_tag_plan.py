# -*- coding: utf-8 -*-
"""
生成/更新全目录预打标签表 data/tag-plan.json。

- 从本地图库提取所有套票（志号+题目）
- 已录入 data/stamps/*.json 的套票：直接采用现有 themes 作为标准答案（status=confirmed）
- 未录入的：按规则自动预打（status=auto，需人工复核）或留空（status=todo，待人工打标）

录入 AI 建 JSON 时必须照抄本表的 themes；表里没有的套票才走《数据录入手册》标签 SOP。
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIBRARY = r"D:\BaiduNetdiskDownload\新中国邮票图片全集（1949年-2025年最新）"
PLAN = os.path.join("data", "tag-plan.json")

GANZHI_ANIMAL = {
    "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔", "辰": "龙", "巳": "蛇",
    "午": "马", "未": "羊", "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪",
}
GANZHI_RE = re.compile(r"^[甲乙丙丁戊己庚辛壬癸]([子丑寅卯辰巳午未申酉戌亥])年")
SERIES_RE = re.compile(r"^(.+?)（[一二三四五六七八九十]+）$")

# (文件夹, 志号前缀正则, series 字段值)
PERIODS = [
    ("01-纪字头邮票1949年-1967年", r"(纪\d+)-(.+)", "纪"),
    ("07-特字头邮票1951年-1966年", r"(特\d+)-(.+)", "特"),
    ("09-文字邮票1967年-1970年", r"(文\d+)-(.+)", "文"),
    ("10-编号邮票1970年-1973年", r"(编号[\d\-]+)-(.+)", "编"),
    ("11-J字头邮票1974年-1991年", r"(J\d+[AM]?)-(.+)", "JT"),
    ("12-T字头邮票1974年-1991年", r"(T\d+[AM]?)-(.+)", "JT"),
    ("33-贺年专用邮票2006年-", r"(贺\d+)-(.+)", "贺"),
]
for _year in range(1992, 2026):
    _folders = {
        y: f for f, y in [
            (name, m.group(1))
            for name in os.listdir(LIBRARY)
            for m in [re.match(r"\d+-编年号(\d{4})年", name)]
            if m
        ]
    }
    if str(_year) in _folders:
        PERIODS.append((_folders[str(_year)], rf"({_year}-\d+)-(.+)", "编年"))


def extract_sets():
    """从图库文件/文件夹名提取 (志号, 题目)，同一志号取最短名（套级条目）。"""
    found = {}
    for folder, pattern, series in PERIODS:
        full = os.path.join(LIBRARY, folder)
        if not os.path.isdir(full):
            continue
        pat = re.compile(pattern)
        # 子文件夹式命名："2024-1 《甲辰年》"
        pat_dir = re.compile(pattern.split("-(")[0].rstrip(")") + r")[ 　]*《(.+)》$")
        for name in os.listdir(full):
            base = re.sub(r"\.(jpg|jpeg|png)$", "", name, flags=re.I)
            m = pat.match(base) or pat_dir.match(base.strip())
            if not m:
                continue
            sid, rest = m.group(1), m.group(2)
            # 去掉版式后缀与"N-M图名"枚级后缀，仅保留题目最短形态
            title = re.split(r"-?(大版张|小版张|小全张|小型张|赠送版|绢质版)", rest)[0]
            title = re.sub(r"\d+-\d+.*$", "", title).strip("-· ")
            if not title:
                continue
            cur = found.get(sid)
            if cur is None or len(title) < len(cur[0]):
                found[sid] = (title, series)
    return found


def auto_tags(title: str, series_val: str, known_series: dict):
    m = GANZHI_RE.match(title)
    if m:
        return ["生肖", "生肖" + GANZHI_ANIMAL[m.group(1)]], "auto"
    if series_val == "贺":
        return ["贺年专用邮票"], "auto"
    if "建交" in title:
        return ["周年纪念", "建交"], "auto"
    if re.search(r"(大学|学院)建校", title):
        return ["周年纪念", "大学建校"], "auto"
    sm = SERIES_RE.match(title)
    if sm and sm.group(1).strip() in known_series:
        s = sm.group(1).strip()
        return list(known_series[s]), "auto"
    return [], "todo"


def main():
    # 现有数据 = 标准答案；同时收集"系列名 -> themes"映射供自动预打
    existing = {}
    existing_titles = {}
    known_series = {}
    for f in sorted(os.listdir(os.path.join("data", "stamps"))):
        if not f.endswith(".json"):
            continue
        for s in json.load(open(os.path.join("data", "stamps", f), encoding="utf-8")):
            existing[s["id"]] = s["themes"]
            existing_titles[s["id"]] = s["title"]
            sm = SERIES_RE.match(s["title"])
            if sm:
                name = sm.group(1).strip()
                if name in s["themes"]:
                    # 只继承 [一级主题, 系列名]，不带兄弟组的专属标签（如人名）
                    known_series[name] = [s["themes"][0], name]

    old_plan = {}
    if os.path.exists(PLAN):
        old_plan = {e["id"]: e for e in json.load(open(PLAN, encoding="utf-8"))}

    all_sets = extract_sets()
    # 已录入但图库缺图的套票也纳入预打表（以数据为准）
    for sid, title in existing_titles.items():
        if sid not in all_sets:
            all_sets[sid] = (title, "")

    plan = []
    stats = {"confirmed": 0, "manual": 0, "auto": 0, "todo": 0}
    for sid, (title, series_val) in sorted(all_sets.items()):
        if sid in existing:
            entry = {"id": sid, "title": title, "themes": existing[sid], "status": "confirmed"}
        elif sid in old_plan and old_plan[sid].get("status") == "manual":
            entry = old_plan[sid]  # 人工定过的不覆盖
        else:
            tags, status = auto_tags(title, series_val, known_series)
            entry = {"id": sid, "title": title, "themes": tags, "status": status}
        stats[entry["status"]] += 1
        plan.append(entry)

    json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"tag-plan.json: 共 {len(plan)} 套")
    print(f"  confirmed(已录入即答案): {stats['confirmed']}")
    print(f"  manual(人工已预打): {stats['manual']}")
    print(f"  auto(规则自动预打,待复核): {stats['auto']}")
    print(f"  todo(待人工打标): {stats['todo']}")


if __name__ == "__main__":
    main()
