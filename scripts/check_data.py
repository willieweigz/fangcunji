# -*- coding: utf-8 -*-
"""
方寸集数据体检脚本。录入/修改数据后必须运行并通过（无 ERROR）才算交付。

用法（在项目根目录执行）:
    python scripts/check_data.py            # 校验数据文件
    python scripts/check_data.py --images   # 额外检查图片缺失与超标（需要 Pillow）

检查规则见《数据录入手册.md》。ERROR 必须修复；WARN 供人工判断。
"""
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = os.path.join("data", "stamps")
THEMES_FILE = os.path.join("data", "themes.json")
IMG_ROOT = "public"
MAX_EDGE = 1600  # 图片长边上限(px)
MAX_KB = 400  # 图片体积上限(KB)

GANZHI = re.compile(r"^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]年?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors: list[str] = []
warns: list[str] = []


def check_tag_plan(primary_set):
    """校验预打标签表(data/tag-plan.json)里 status=manual 的条目是否合规。
    confirmed 是真实数据的镜像，已在主流程校验过，这里不重复；auto/todo 是待办，不校验。"""
    plan_path = os.path.join("data", "tag-plan.json")
    if not os.path.exists(plan_path):
        return
    plan = json.load(open(plan_path, encoding="utf-8"))
    for e in plan:
        if e.get("status") != "manual":
            continue
        ctx = f"[预打表] {e['id']}《{e.get('title', '?')}》"
        th = e.get("themes", [])
        prims = [t for t in th if t in primary_set]
        if not th:
            errors.append(f"{ctx}: themes 为空")
        elif th[0] not in primary_set:
            errors.append(f"{ctx}: themes[0]『{th[0]}』不在一级主题列表（data/themes.json）中")
        if len(prims) > 1:
            errors.append(f"{ctx}: 出现多个一级主题 {prims}，有且只能有 1 个")
        if len(th) < 2:
            errors.append(f"{ctx}: 缺少二级标签（每套至少 1 个，最多 3 个）")
        elif len(th) - 1 > 3:
            errors.append(f"{ctx}: 二级标签 {len(th) - 1} 个，超过上限 3 个")
        for t in th:
            if GANZHI.match(t):
                errors.append(f"{ctx}: 不允许干支年名标签『{t}』（生肖票用动物单字）")


def check_images(all_sets):
    missing = 0
    oversized = []
    try:
        from PIL import Image
    except ImportError:
        warns.append("未安装 Pillow，跳过图片尺寸检查（pip install pillow）")
        Image = None
    for s in all_sets:
        for st in s["stamps"]:
            path = os.path.join(IMG_ROOT, st["image"].lstrip("/"))
            if not os.path.exists(path):
                missing += 1
                continue
            kb = os.path.getsize(path) / 1024
            if Image:
                with Image.open(path) as im:
                    edge = max(im.size)
                if edge > MAX_EDGE or kb > MAX_KB:
                    oversized.append(f"{st['image']} ({edge}px, {kb:.0f}KB)")
            elif kb > MAX_KB:
                oversized.append(f"{st['image']} ({kb:.0f}KB)")
    if missing:
        warns.append(f"缺图 {missing} 枚（允许，占位图会显示，但请在交付说明中注明）")
    for o in oversized:
        warns.append(f"图片超标（>{MAX_EDGE}px 或 >{MAX_KB}KB），请运行 scripts/compress_images.py: {o}")


def main():
    primary = json.load(open(THEMES_FILE, encoding="utf-8"))
    primary_set = set(primary)
    if len(primary) != len(primary_set):
        errors.append("themes.json 中有重复的一级主题")

    all_sets = []
    seen_ids: dict[str, str] = {}
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".json"):
            continue
        try:
            sets = json.load(open(os.path.join(DATA_DIR, fname), encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{fname}: JSON 解析失败 — {e}")
            continue
        for s in sets:
            sid = s.get("id", f"{fname}:未知")
            ctx = f"{sid}《{s.get('title', '?')}》"
            all_sets.append(s)

            if sid in seen_ids:
                errors.append(f"{ctx}: 志号与 {seen_ids[sid]} 重复")
            seen_ids[sid] = fname

            for field in ("id", "title", "issueDate", "type", "series", "description"):
                if not s.get(field):
                    errors.append(f"{ctx}: 缺少必填字段 {field}")
            if not DATE_RE.match(s.get("issueDate", "")):
                errors.append(f"{ctx}: issueDate 格式应为 YYYY-MM-DD")
            if not isinstance(s.get("year"), int):
                errors.append(f"{ctx}: year 缺失或不是数字")
            elif s.get("issueDate", "")[:4] != str(s["year"]):
                errors.append(f"{ctx}: year 与 issueDate 年份不一致")

            stamps = s.get("stamps", [])
            regular = [st for st in stamps if not st.get("format")]
            if s.get("totalStamps") != len(regular):
                errors.append(
                    f"{ctx}: totalStamps={s.get('totalStamps')} 但正票条目数={len(regular)}"
                    "（小型张等附加条目须带 format 字段且不计入 totalStamps）"
                )
            for st in stamps:
                if not st.get("image", "").startswith("/images/stamps/"):
                    errors.append(f"{ctx} 第{st.get('sn')}枚: image 路径格式不对")

            th = s.get("themes", [])
            prims = [t for t in th if t in primary_set]
            if not th:
                errors.append(f"{ctx}: themes 为空")
            elif th[0] not in primary_set:
                errors.append(f"{ctx}: themes[0]『{th[0]}』不在一级主题列表（data/themes.json）中")
            if len(prims) > 1:
                errors.append(f"{ctx}: 出现多个一级主题 {prims}，有且只能有 1 个")
            if len(th) < 2:
                errors.append(f"{ctx}: 缺少二级标签（每套至少 1 个，最多 3 个）")
            elif len(th) - 1 > 3:
                errors.append(f"{ctx}: 二级标签 {len(th) - 1} 个，超过上限 3 个")
            for t in th:
                if GANZHI.match(t):
                    errors.append(f"{ctx}: 不允许干支年名标签『{t}』（生肖票用动物单字）")
            if len(th) > 4:
                warns.append(f"{ctx}: 标签 {len(th)} 个，二级标签建议不超过 3 个: {th}")

    pending = sum(
        1 for s in all_sets for st in s["stamps"] if "待核对" in st.get("name", "")
    )
    if pending:
        warns.append(f"全站有 {pending} 枚图名标注'待核对'（允许，逐步补全）")

    no_denom = sum(1 for s in all_sets for st in s["stamps"] if not st.get("denomination"))
    if no_denom:
        warns.append(f"全站有 {no_denom} 枚缺面值（denomination 为空，应逐步补全）")

    check_tag_plan(primary_set)

    if "--images" in sys.argv:
        check_images(all_sets)

    print(f"共检查 {len(all_sets)} 套邮票")
    for e in errors:
        print("  [ERROR]", e)
    for w in warns:
        print("  [WARN]", w)
    if errors:
        print(f"\n结果: 未通过（{len(errors)} 个错误，{len(warns)} 个警告）")
        sys.exit(1)
    print(f"\n结果: 通过（0 错误，{len(warns)} 个警告）")

    # 体检通过后自动刷新标签总表，保证 JSON 和总表始终同步
    export_script = os.path.join("scripts", "export_tags.py")
    if os.path.exists(export_script):
        subprocess.run([sys.executable, export_script], check=False)


if __name__ == "__main__":
    main()
