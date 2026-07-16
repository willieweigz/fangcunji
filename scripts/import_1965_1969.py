"""Build 1965-1969 stamp data from the organized local stamp library."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

from import_1960_1964 import (
    DATA_DIR,
    IGNORED_IMAGE_WORDS,
    LIBRARY,
    PUBLIC_DIR,
    ROOT,
    bold_places,
    extract_image_names,
    image_files,
    parse_description,
    parse_designer,
    parse_issue_date as parse_base_issue_date,
    parse_quantity,
    parse_rows as parse_base_rows,
    parse_total,
    save_web_image,
    select_normal_images,
)


YEARS = range(1965, 1970)
ISSUE_DATE_OVERRIDES = {
    "特": "1968-11-25",
    "1969-普无号": "1969-10-01",
}
ROW_OVERRIDES = {
    "特": [
        {"name": "小一片红", "denomination": "8分", "quantity": ""},
        {"name": "大一片红", "denomination": "8分", "quantity": ""},
    ],
}
DENOMINATION_OVERRIDES = {
    # The local image order differs from the catalogue order for this no-number set.
    "1969-普无号": [
        "8分", "4分", "10分", "8分", "8分", "50分",
        "20分", "1.5分", "5分", "8分", "1元",
    ],
}
DESCRIPTION_OVERRIDES = {
    "特": (
        "《全国山河一片红》原定于1968年11月25日发行，图案为工农兵群众高举《毛主席语录》，"
        "背景是红旗与中国地图。发行前因地图绘制问题被紧急停止发行并回收。竖版“小一片红”是"
        "拟正式发行的版本，横版“大一片红”是设计过程中的未正式发行样稿；网站将两种版本一并"
        "收录展示，但它们并非两枚正式发行邮票。"
    ),
}
EXTRA_PLACE_NAMES = (
    "印度尼西亚万隆", "南斯拉夫卢布尔雅那", "贵州遵义", "江西井冈山",
    "南京长江大桥", "延安宝塔山", "遵义会议会址", "中共一大会址",
    "人民英雄纪念碑", "天安门", "井冈山", "卢布尔雅那", "万隆",
    "越南", "河内", "日本", "南京", "延安", "安源", "北京", "上海",
)


def selected_years() -> list[int]:
    if len(sys.argv) == 1:
        return list(YEARS)
    year = int(sys.argv[1])
    if year not in YEARS:
        raise ValueError("year must be between 1965 and 1969")
    return [year]


def stamp_id_from_folder(folder: Path) -> str:
    return folder.name.split(" ", 1)[0]


def choose_folders(year: int) -> list[tuple[str, Path]]:
    year_dir = LIBRARY / f"15-{year}年"
    selected: list[tuple[str, Path]] = []
    for folder in year_dir.iterdir():
        if not folder.is_dir():
            continue
        if any(word in folder.name for word in ("包裹", "加字改值", "欠资")):
            continue
        selected.append((stamp_id_from_folder(folder), folder))
    return sorted(selected, key=lambda item: item[0])


def parse_detail_rows(text: str) -> list[dict[str, str]]:
    rows_by_index: dict[int, dict[str, str]] = {}
    pattern = re.compile(
        r"^[（(](?:(?:\d+)-)?(\d+)[）)]"
        r"(?:\s*[—–-]\s*[（(](?:(?:\d+)-)?(\d+)[）)])?\s*(.+)$"
    )
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = pattern.match(line)
        if not match:
            continue
        start = int(match.group(1))
        end = int(match.group(2) or start)
        body = match.group(3).strip()
        denomination_match = re.search(r"(?:各)?(\d+(?:\.\d+)?(?:分|角|元))", body)
        if not denomination_match:
            continue
        denomination = denomination_match.group(1)
        name = body[:denomination_match.start()].strip(" —–-，,")
        quantity_match = re.search(r"(?:各)?(\d+(?:\.\d+)?万枚)", body[denomination_match.end():])
        quantity = quantity_match.group(1) if quantity_match else ""
        for index in range(start, end + 1):
            rows_by_index[index] = {
                "name": name,
                "denomination": denomination,
                "quantity": quantity,
            }
    return [rows_by_index[index] for index in sorted(rows_by_index)]


def rows_for_stamp(stamp_id: str, text: str) -> tuple[list[dict[str, str]], int]:
    if stamp_id in ROW_OVERRIDES:
        rows = [dict(row) for row in ROW_OVERRIDES[stamp_id]]
        return rows, len(rows)

    base_rows, _ = parse_base_rows(text)
    total = parse_total(text, base_rows)
    rows = base_rows if len(base_rows) == total else parse_detail_rows(text)
    if len(rows) != total:
        raise ValueError(f"{stamp_id}: parsed {len(rows)} rows, expected {total}")

    if stamp_id in DENOMINATION_OVERRIDES:
        overrides = DENOMINATION_OVERRIDES[stamp_id]
        if len(overrides) != total:
            raise ValueError(f"{stamp_id}: denomination override count mismatch")
        for row, denomination in zip(rows, overrides):
            row["denomination"] = denomination
    return rows, total


def issue_date_for_stamp(stamp_id: str, text: str) -> str:
    if stamp_id in ISSUE_DATE_OVERRIDES:
        return ISSUE_DATE_OVERRIDES[stamp_id]
    try:
        return parse_base_issue_date(text)
    except ValueError:
        match = re.search(r"邮电部于(\d{4})年(\d{1,2})月(\d{1,2})日起?发行", text)
        if not match:
            raise ValueError(f"{stamp_id}: missing issue date")
        year, month, day = map(int, match.groups())
        return f"{year:04d}-{month:02d}-{day:02d}"


def emphasize_places(text: str) -> str:
    result = bold_places(text)
    protected: dict[str, str] = {}

    def protect(match: re.Match[str]) -> str:
        token = f"@@PLACE{len(protected)}@@"
        protected[token] = match.group(0)
        return token

    result = re.sub(r"\*\*[^*]+\*\*", protect, result)
    for place in sorted(EXTRA_PLACE_NAMES, key=len, reverse=True):
        result = result.replace(place, f"**{place}**")
    for token, value in protected.items():
        result = result.replace(token, value)
    return result


def description_for_stamp(stamp_id: str, text: str) -> str:
    description = DESCRIPTION_OVERRIDES.get(stamp_id, parse_description(text))
    return emphasize_places(description)


def record_type(stamp_id: str) -> tuple[str, str]:
    if stamp_id == "1969-普无号":
        return "普", "普通邮票"
    series_match = re.match(r"[^\d]+", stamp_id)
    if not series_match:
        raise ValueError(f"{stamp_id}: cannot determine series")
    series = series_match.group(0)
    if series == "纪":
        return series, "纪念邮票"
    return series, "特种邮票"


def main() -> None:
    plan = json.loads((ROOT / "data" / "tag-plan.json").read_text(encoding="utf-8"))
    plan_by_id = {entry["id"]: entry for entry in plan}
    report: list[str] = []

    for year in selected_years():
        records: list[dict[str, object]] = []
        destination_dir = PUBLIC_DIR / str(year)
        if destination_dir.exists():
            shutil.rmtree(destination_dir)
        destination_dir.mkdir(parents=True)

        for stamp_id, folder in choose_folders(year):
            if stamp_id not in plan_by_id:
                raise ValueError(f"{year} {stamp_id}: missing tag plan entry")
            md_files = sorted(folder.glob("*.md"))
            if not md_files:
                raise ValueError(f"{year} {stamp_id}: missing Markdown")
            text = md_files[0].read_text(encoding="utf-8-sig")
            rows, total = rows_for_stamp(stamp_id, text)
            files = image_files(folder)
            names_from_images = extract_image_names(files)
            mapped_images = select_normal_images(files, total)

            stamps: list[dict[str, object]] = []
            for index, row in enumerate(rows, start=1):
                stamp = {
                    "sn": index,
                    "name": names_from_images.get(index, row["name"]),
                    "denomination": row["denomination"],
                    "image": f"/images/stamps/{year}/{stamp_id}-{index}.jpg",
                }
                stamps.append(stamp)
                if index in mapped_images:
                    save_web_image(mapped_images[index], destination_dir / f"{stamp_id}-{index}.jpg")

            issue_date = issue_date_for_stamp(stamp_id, text)
            if int(issue_date[:4]) != year:
                raise ValueError(f"{year} {stamp_id}: belongs to {issue_date[:4]}")
            quantity = parse_quantity(text, rows)
            series, stamp_type = record_type(stamp_id)
            record: dict[str, object] = {
                "id": stamp_id,
                "series": series,
                "type": stamp_type,
                "title": plan_by_id[stamp_id]["title"],
                "issueDate": issue_date,
                "year": year,
                "themes": plan_by_id[stamp_id]["themes"],
                "designer": parse_designer(text),
                "totalStamps": total,
                "extras": [],
                "description": description_for_stamp(stamp_id, text),
            }
            if quantity:
                record["quantity"] = quantity
            record.update(
                {
                    "needsReview": True,
                    "localImageFolder": folder.name,
                    "stamps": stamps,
                }
            )
            records.append(record)
            missing = [str(index) for index in range(1, total + 1) if index not in mapped_images]
            report.append(
                f"{year} {stamp_id}: {total}枚; 图片 {len(mapped_images)}/{total}"
                + (f"; 缺 {','.join(missing)}" if missing else "")
            )

        records.sort(key=lambda item: (item["issueDate"], item["id"]))
        (DATA_DIR / f"{year}.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print("\n".join(report))


if __name__ == "__main__":
    main()
