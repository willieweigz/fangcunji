#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 2012 stamp md files in 2024 standard format."""

import os, json

BASE = r"G:\微云同步文件夹\邮票网站\新中国邮票图片全集（1949年-2026年最新）\39-编年号2012年"

LQ = "\u201c"
RQ = "\u201d"

SELL_TEXT = (
    "\u81ea\u53d1\u884c\u4e4b\u65e5\u8d77\uff0c\u5728\u5168\u56fd\u6307\u5b9a\u90ae\u653f\u7f51\u70b9\u3001"
    "\u96c6\u90ae\u7f51\u5385\uff08https://jiyou.11185.cn\uff09\u3001"
    "\u4e2d\u56fd\u90ae\u653f\u624b\u673a\u5ba2\u6237\u7aef\u3001"
    "\u4e2d\u56fd\u90ae\u653f\u5fae\u90ae\u5c40\u96c6\u90ae\u5fae\u4fe1\u5546\u57ce\u548c"
    "\u4e2d\u56fd\u90ae\u653f\u5546\u57ce\u5fae\u4fe1\u5c0f\u7a0b\u5e8f\u51fa\u552e\uff0c"
    "\u51fa\u552e\u671f\u96506\u4e2a\u6708\u3002"
)

ENDING = (
    "\u8be5\u5957\u90ae\u7968\u5728\u5168\u56fd\u6307\u5b9a\u90ae\u653f\u7f51\u70b9\u3001"
    "\u96c6\u90ae\u7f51\u5385\u3001\u4e2d\u56fd\u90ae\u653f\u624b\u673a\u5ba2\u6237\u7aef\u3001"
    "\u4e2d\u56fd\u90ae\u653f\u5fae\u90ae\u5c40\u96c6\u90ae\u5fae\u4fe1\u5546\u57ce\u548c"
    "\u4e2d\u56fd\u90ae\u653f\u5546\u57ce\u5fae\u4fe1\u5c0f\u7a0b\u5e8f\u51fa\u552e\uff0c"
    "\u51fa\u552e\u671f\u96506\u4e2a\u6708\u3002\u4e3a\u66f4\u52a0\u4e30\u5bcc\u5730\u5c55\u73b0"
    "\u90ae\u7968\u5185\u5bb9\uff0c\u4e2d\u56fd\u90ae\u653f\u5c06\u901a\u8fc7" + LQ +
    "\u4e2d\u56fd\u96c6\u90ae\u90ae\u7968\u767e\u79d1" + RQ +
    "\u5fae\u4fe1\u5c0f\u7a0b\u5e8f\u53d1\u5e03\u6570\u5b57\u5316\u5185\u5bb9\uff0c"
    "\u53ef\u4f7f\u7528AR\u529f\u80fd\u89c2\u770b\u3002"
    "\uff08\u4e2d\u56fd\u90ae\u653f\u96c6\u56e2\u6709\u9650\u516c\u53f8\u90ae\u653f\u4e1a\u52a1\u90e8\uff09"
)


def make_md(s):
    lines = []
    title_in_book = s.get("title_in_book", s["title"])
    lines.append("# {} \u300a{}\u300b".format(s["id"], title_in_book))
    lines.append("")
    header = "\u4e2d\u56fd\u90ae\u653f\u5b9a\u4e8e{}\u53d1\u884c\u300a{}\u300b{}1\u5957{}\u679a".format(
        s["date"], s["title"], s["type"], s["count"])
    if s.get("header_extra"):
        header += s["header_extra"]
    header += "\u3002\u8be6\u60c5\u5982\u4e0b\uff1a"
    lines.append(header)
    lines.append("")
    for fmt, name, denom in s["stamps_list"]:
        lines.append("{} {} {}".format(fmt, name, denom))
    if s["stamps_list"]:
        lines.append("")
    if s.get("mini_stamps"):
        for fmt, name, denom in s["mini_stamps"]:
            lines.append("{} {} {}".format(fmt, name, denom))
        lines.append("")
    for spec in s["specs"]:
        lines.append(spec)
    lines.append("")
    lines.append("\u7248\u522b\uff1a{}".format(s["version"]))
    lines.append("")
    lines.append("\u9632\u4f2a\u65b9\u5f0f\uff1a{}".format(
        s.get("anti_fake", "\u9632\u4f2a\u7eb8\u5f20\u3001\u9632\u4f2a\u6cb9\u58a8\u3001\u5f02\u5f62\u9f7f\u5b54\u3001\u8367\u5149\u55b7\u7801")))
    lines.append("")
    lines.append("\u8bbe\u8ba1\u8005\uff1a{}".format(s["designer"]))
    if s.get("extra_design"):
        lines.append(s["extra_design"])
    if s.get("data_provider"):
        lines.append("\u8d44\u6599\u63d0\u4f9b\uff1a{}".format(s["data_provider"]))
    if s.get("photographer"):
        lines.append("\u6444\u5f71\u8005\uff1a{}".format(s["photographer"]))
    if s.get("engraver"):
        lines.append("\u96d5\u523b\u8005\uff1a{}".format(s["engraver"]))
    lines.append("")
    lines.append("\u5370\u5236\u5382\uff1a{}".format(s["printer"]))
    lines.append("")
    lines.append("\u8ba1\u5212\u53d1\u884c\u6570\u91cf\uff1a{}".format(s["quantity"]))
    lines.append("")
    lines.append(SELL_TEXT)
    lines.append("")
    if s.get("note"):
        lines.append("\u6ce8\uff1a{}".format(s["note"]))
        lines.append("")
    lines.append(s["overview"])
    lines.append("")
    lines.append(s["background"])
    lines.append("")
    prod = "\u8be5\u5957\u90ae\u7968\u7531{}\u8bbe\u8ba1".format(
        s["designer"].split("\u3001")[0] if "\u3001" in s["designer"] else s["designer"])
    prod += "\uff0c{}\u5de5\u827a\u5370\u5236\u3002".format(s["version"])
    lines.append(prod)
    lines.append("")
    lines.append(ENDING)
    lines.append("")
    return "\n".join(lines)


# Load stamp data from JSON file
data_file = os.path.join(os.path.dirname(__file__), "gen_2012_data.json")
with open(data_file, "r", encoding="utf-8") as f:
    stamps = json.load(f)

count = 0
for s in stamps:
    md_content = make_md(s)
    folder = s["folder"]
    # The md filename should match the folder name
    md_filename = folder + ".md"
    md_path = os.path.join(BASE, folder, md_filename)
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    count += 1
    print("Generated: {}".format(md_filename))

print("\nTotal: {} files generated.".format(count))
