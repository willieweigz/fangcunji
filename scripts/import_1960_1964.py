"""Build the 1960-1964 stamp data and import their local images.

This importer is intentionally limited to the already-organized early-year folders.
It follows the data-entry manual's precedence rule: individual image filenames supply
stamp names, while each folder's Markdown supplies dates, denominations, quantities,
designers, and background text.
"""

from __future__ import annotations

import io
import json
import re
import shutil
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "新中国邮票图片全集（1949年-2026年最新）"
DATA_DIR = ROOT / "data" / "stamps"
PUBLIC_DIR = ROOT / "public" / "images" / "stamps"
YEARS = range(1960, 1965)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
IGNORED_IMAGE_WORDS = ("大版张", "整版", "全套", "无齿", "小本票")

# The local Markdown was machine-prepared and a subset of its early face values
# is wrong. These corrections were checked against the stamp face plus the
# China Post/China Philately and 一本邮册 catalogues.
DENOMINATION_OVERRIDES = {
    "纪78": ["8分", "8分"],
    "纪77": ["4分", "8分", "20分"],
    "特39": ["8分", "10分"],
    "纪79": ["8分", "8分"],
    "特38": ["4分", "4分", "4分", "4分", "8分", "8分", "8分", "8分", "8分", "8分", "8分", "8分"],
    "特40": ["8分", "8分", "8分", "8分", "8分"],
    "纪82": ["8分", "8分"],
    "特42": ["8分", "10分"],
    "纪83": ["8分", "8分"],
    "特43": ["8分", "8分", "8分", "8分", "8分"],
    "特41": ["8分", "10分"],
    "纪84": ["8分", "8分"],
    "纪80": ["8分", "10分"],
    "特44": ["4分", "4分", "8分", "8分", "8分", "8分", "8分", "8分", "10分", "10分", "20分", "20分", "22分", "22分", "30分", "30分", "35分", "52分"],
    "纪85": ["8分", "8分"],
    "纪86": ["8分", "10分", "20分", "22分"],
    "纪87": ["8分", "10分"],
    "纪95": ["8分", "20分"],
    "特56": ["4分", "4分", "4分", "4分", "4分", "8分", "8分", "8分", "8分", "8分", "10分", "10分", "10分", "10分", "10分", "20分", "20分", "22分", "30分", "50分"],
    "特58": ["4分", "8分", "10分", "4分", "8分", "10分", "4分", "8分", "10分"],
    "特61": ["4分", "4分", "8分", "8分", "8分", "8分", "8分", "10分", "10分", "10分", "10分", "10分", "20分", "43分", "52分"],
}

QUANTITY_OVERRIDES = {
    "纪78": "800万套", "纪77": "200万套", "特39": "300万套", "纪79": "800万套",
    "特38": "400万套", "特40": "480万套", "纪82": "540万套", "纪83": "540万套",
    "特43": "440万套", "特41": "240万套", "纪84": "540万套", "纪80": "250万套",
    "特44": "100万套", "纪86": "150万套", "特47": "150万套", "纪95": "300万套",
    "特54": "125万套", "特53": "100万套", "特58": "150万套", "纪101": "450万套",
    "纪102": "450万套", "特61": "100万套",
}

DESIGNER_OVERRIDES = {"纪84": "卢天骄", "纪86": "吴建坤"}

EXTRA_OVERRIDES = {
    "纪86": [{"name": "第26届世界乒乓球锦标赛", "denomination": "60分", "format": "小全张"}],
    "纪94": [{"name": "《贵妃醉酒》", "denomination": "3元", "format": "小型张"}],
    "特61": [{"name": "状元红·大金粉", "denomination": "2元", "format": "小型张"}],
    "纪106": [{"name": "中华人民共和国成立十五周年", "denomination": "24分", "format": "小全张"}],
}

PLACE_NAMES = (
    "北京市复兴路9号", "丹麦哥本哈根", "阿尔及利亚", "捷克斯洛伐克",
    "晋察冀边区", "贵州遵义", "河北赵县", "浙江绍兴", "印度尼西亚万隆",
    "北京天安门", "北京卢沟桥", "成都杜甫草堂", "巴黎万神庙", "伦敦圣马丁堂",
    "济州岛", "莫斯科", "布拉格", "斯摩尔尼宫", "阿尔巴尼亚", "匈牙利",
    "蒙古", "朝鲜", "越南", "古巴", "美国", "法国", "苏联", "非洲",
    "西藏", "河内", "北京", "上海", "南昌", "瑞金", "延安", "武昌",
    "成都", "绍兴", "巴黎", "伦敦", "新安江", "黄山", "贡嘎山",
    "慕士塔格山", "珠穆朗玛峰", "公格尔九别峰", "希夏帮马峰",
)


def natural_key(value: str) -> list[object]:
    return [int(piece) if piece.isdigit() else piece for piece in re.split(r"(\d+)", value)]


def first_match(patterns: tuple[str, ...], text: str) -> re.Match[str] | None:
    for pattern in patterns:
        match = re.search(pattern, text, re.M)
        if match:
            return match
    return None


def parse_issue_date(text: str) -> str:
    match = first_match(
        (
            r"发行日期\*\*?[：:]\s*(\d{4})年(\d{1,2})月(\d{1,2})日",
            r"(?:邮电部于|中国邮政定于)(\d{4})年(\d{1,2})月(\d{1,2})日发行",
        ),
        text,
    )
    if not match:
        raise ValueError("missing issue date")
    year, month, day = map(int, match.groups())
    return f"{year:04d}-{month:02d}-{day:02d}"


def parse_designer(text: str) -> str:
    match = re.search(r"(?:\*\*)?设计者(?:\*\*)?[：:]\s*([^\r\n]+)", text)
    if not match:
        return ""
    value = re.sub(r"\s*（小型张[^）]*）\s*", "", match.group(1)).strip()
    return value.strip("* ")


def parse_rows(text: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    normal: list[dict[str, str]] = []
    extras: list[dict[str, str]] = []
    table_lines = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    header: list[str] | None = None
    for line in table_lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(re.fullmatch(r"[-: ]+", cell or "-") for cell in cells):
            continue
        if any(cell in {"图名", "面值", "编号", "枚序"} for cell in cells):
            header = cells
            continue
        denom_index = next(
            (index for index, cell in enumerate(cells) if re.fullmatch(r"\d+(?:\.\d+)?(?:分|角|元)", cell)),
            None,
        )
        if denom_index is None:
            continue
        denomination = cells[denom_index]
        if header and "图名" in header:
            name_index = header.index("图名")
            name = cells[name_index] if name_index < len(cells) else ""
        elif denom_index + 1 < len(cells):
            name = cells[denom_index + 1]
        else:
            name = cells[denom_index - 1]
        quantity_cell = next((cell for cell in cells if re.fullmatch(r"\d+(?:\.\d+)?万枚", cell)), "")
        row = {"name": name.strip(), "denomination": denomination, "quantity": quantity_cell}
        if any("小型张" in cell or "小全张" in cell for cell in cells):
            row["format"] = "小全张" if any("小全张" in cell for cell in cells) else "小型张"
            extras.append(row)
        else:
            normal.append(row)

    if normal:
        return normal, extras

    detail_pattern = re.compile(
        r"^（\d+-(\d+)）\s*(?:J|T)?\s*(.+?)\s+(\d+(?:\.\d+)?(?:分|角|元))(?:\s+(\d+(?:\.\d+)?万枚))?\s*$",
        re.M,
    )
    for match in detail_pattern.finditer(text):
        normal.append(
            {
                "name": match.group(2).strip(),
                "denomination": match.group(3),
                "quantity": match.group(4) or "",
            }
        )
    return normal, extras


def parse_total(text: str, rows: list[dict[str, str]]) -> int:
    match = first_match(
        (
            r"全套枚数\*\*?[：:]\s*(\d+)枚",
            r"1套(\d+)枚",
        ),
        text,
    )
    return int(match.group(1)) if match else len(rows)


def parse_quantity(text: str, rows: list[dict[str, str]]) -> str:
    explicit = re.search(r"^发行量[：:]\s*(\d+(?:\.\d+)?)万套", text, re.M)
    if explicit:
        return f"{explicit.group(1)}万套"
    values = [float(row["quantity"][:-2]) for row in rows if row.get("quantity", "").endswith("万枚")]
    if not values:
        return ""
    minimum = min(values)
    rendered = str(int(minimum)) if minimum.is_integer() else str(minimum).rstrip("0").rstrip(".")
    return f"{rendered}万套"


def parse_description(text: str) -> str:
    candidates: list[str] = []
    for paragraph in re.split(r"\r?\n\s*\r?\n", text):
        value = " ".join(line.strip() for line in paragraph.splitlines()).strip()
        if not value or value.startswith("#") or value.startswith("|"):
            continue
        if re.match(r"^(?:\*\*)?(?:发行日期|志号|全套|邮票规格|齿孔度数|整张枚数|版别|设计者|雕刻者|印制厂|原作品作者|原画作者|摄影者|原作者)(?:\*\*)?[：:]", value):
            continue
        if re.match(r"^(?:邮电部于|中国邮政定于)", value):
            continue
        if re.match(r"^（\d+-\d+）", value):
            continue
        candidates.append(value)
    if not candidates:
        raise ValueError("missing description")
    description = candidates[-1]
    description = re.sub(r"，市价高达[^。]+。", "。", description)
    return bold_places(description)


def bold_places(text: str) -> str:
    protected: dict[str, str] = {}

    def protect(match: re.Match[str]) -> str:
        token = f"@@BOLD{len(protected)}@@"
        protected[token] = match.group(0)
        return token

    result = re.sub(r"\*\*[^*]+\*\*", protect, text)
    for place in sorted(PLACE_NAMES, key=len, reverse=True):
        result = result.replace(place, f"**{place}**")
    for token, original in protected.items():
        result = result.replace(token, original)
    return result


def image_files(folder: Path) -> list[Path]:
    return sorted(
        (path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS),
        key=lambda path: natural_key(path.name),
    )


def choose_folders(year: int) -> list[tuple[str, Path]]:
    year_dir = LIBRARY / f"15-{year}年"
    groups: dict[str, list[Path]] = {}
    for folder in year_dir.iterdir():
        if not folder.is_dir():
            continue
        match = re.match(r"([^ ]+)\s", folder.name)
        if not match or any(word in folder.name for word in ("包裹", "加字改值", "欠资")):
            continue
        groups.setdefault(match.group(1), []).append(folder)
    selected = []
    for stamp_id, folders in groups.items():
        folder = max(folders, key=lambda item: len(image_files(item)))
        selected.append((stamp_id, folder))
    return selected


def extract_image_names(files: list[Path]) -> dict[int, str]:
    names: dict[int, str] = {}
    for path in files:
        if any(word in path.stem for word in (*IGNORED_IMAGE_WORDS, "小型张", "小全张")):
            continue
        match = re.search(r"(?<!\d)(\d+)-(\d+)(?!\d)", path.stem)
        if not match:
            continue
        index = int(match.group(2))
        suffix = path.stem[match.end():].lstrip("-—_ ")
        suffix = re.sub(r"\s*\(\d+\)$", "", suffix)
        if suffix and index not in names:
            names[index] = suffix
    return names


def select_normal_images(files: list[Path], total: int) -> dict[int, Path]:
    mapped: dict[int, Path] = {}
    for path in files:
        if any(word in path.stem for word in (*IGNORED_IMAGE_WORDS, "小型张", "小全张")):
            continue
        match = re.search(r"(?<!\d)(\d+)-(\d+)(?!\d)", path.stem)
        if match:
            index = int(match.group(2))
            if 1 <= index <= total and index not in mapped:
                mapped[index] = path
    if total == 1 and not mapped:
        candidates = [
            path for path in files
            if not any(word in path.stem for word in (*IGNORED_IMAGE_WORDS, "小型张", "小全张"))
        ]
        if candidates:
            mapped[1] = candidates[0]
    return mapped


def save_web_image(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        quality = 72
        while True:
            buffer = io.BytesIO()
            image.save(buffer, "JPEG", quality=quality, optimize=True, progressive=True)
            payload = buffer.getvalue()
            if len(payload) <= 400 * 1024 or quality <= 42:
                destination.write_bytes(payload)
                return
            quality -= 5


def main() -> None:
    plan = json.loads((ROOT / "data" / "tag-plan.json").read_text(encoding="utf-8"))
    plan_by_id = {entry["id"]: entry for entry in plan}
    report: list[str] = []

    for year in YEARS:
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
            rows, extra_rows = parse_rows(text)
            total = parse_total(text, rows)
            if len(rows) != total:
                raise ValueError(f"{year} {stamp_id}: parsed {len(rows)} rows, expected {total}")
            if stamp_id in DENOMINATION_OVERRIDES:
                overrides = DENOMINATION_OVERRIDES[stamp_id]
                if len(overrides) != total:
                    raise ValueError(f"{year} {stamp_id}: denomination override count mismatch")
                for row, denomination in zip(rows, overrides):
                    row["denomination"] = denomination

            files = image_files(folder)
            names_from_images = extract_image_names(files)
            mapped_images = select_normal_images(files, total)
            stamps: list[dict[str, object]] = []
            for index, row in enumerate(rows, start=1):
                name = names_from_images.get(index, row["name"])
                stamp = {
                    "sn": index,
                    "name": name,
                    "denomination": row["denomination"],
                    "image": f"/images/stamps/{year}/{stamp_id}-{index}.jpg",
                }
                stamps.append(stamp)
                if index in mapped_images:
                    save_web_image(mapped_images[index], destination_dir / f"{stamp_id}-{index}.jpg")

            extra_formats: list[str] = []
            extra_files = [path for path in files if "小型张" in path.stem or "小全张" in path.stem]
            for offset, source in enumerate(extra_files, start=1):
                format_name = "小全张" if "小全张" in source.stem else "小型张"
                if format_name not in extra_formats:
                    extra_formats.append(format_name)
                configured_extras = EXTRA_OVERRIDES.get(stamp_id, [])
                extra_row = (
                    configured_extras[offset - 1]
                    if offset - 1 < len(configured_extras)
                    else next((row for row in extra_rows if row.get("format") == format_name), {})
                )
                sn = total + offset
                stamps.append(
                    {
                        "sn": sn,
                        "name": extra_row.get("name") or format_name,
                        "denomination": extra_row.get("denomination") or "",
                        "format": format_name,
                        "image": f"/images/stamps/{year}/{stamp_id}-{sn}.jpg",
                    }
                )
                save_web_image(source, destination_dir / f"{stamp_id}-{sn}.jpg")

            issue_date = parse_issue_date(text)
            if int(issue_date[:4]) != year:
                raise ValueError(f"{year} {stamp_id}: belongs to {issue_date[:4]}")
            quantity = QUANTITY_OVERRIDES.get(stamp_id, parse_quantity(text, rows))
            record: dict[str, object] = {
                "id": stamp_id,
                "series": re.match(r"[^\d]+", stamp_id).group(0),
                "type": "普通邮票" if stamp_id.startswith("普") else ("纪念邮票" if stamp_id.startswith("纪") else "特种邮票"),
                "title": plan_by_id[stamp_id]["title"],
                "issueDate": issue_date,
                "year": year,
                "themes": plan_by_id[stamp_id]["themes"],
                "designer": DESIGNER_OVERRIDES.get(stamp_id, parse_designer(text)),
                "totalStamps": total,
                "extras": extra_formats,
                "description": parse_description(text),
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
                f"{year} {stamp_id}: {total}枚 + {len(extra_files)}附属图; "
                f"图片 {len(mapped_images)}/{total}" + (f"; 缺 {','.join(missing)}" if missing else "")
            )

        records.sort(key=lambda item: (item["issueDate"], item["id"]))
        (DATA_DIR / f"{year}.json").write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print("\n".join(report))


if __name__ == "__main__":
    main()
