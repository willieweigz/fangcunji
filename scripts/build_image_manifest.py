# -*- coding: utf-8 -*-
"""
生成图片清单 data/image-manifest.json：记录 image-store 里每张图片的尺寸 [宽, 高]。

为什么需要它：2026-08 起图片迁到独立仓库 fangcunji-images（经 jsDelivr 读取），
Vercel 构建的主仓库里不再有图片文件。而网站构建时需要知道
(1) 每套票的每一枚是否有图（决定显示图片还是"图片待录入"占位）、
(2) 小全张的长宽比（决定能否当列表封面）——这两件事以前靠读图片文件本体做，
现在改为读这份清单。清单很小（几百 KB），随主仓库提交，Vercel 能直接用。

用法（在项目根目录执行）:
    python scripts/build_image_manifest.py

**什么时候要重跑**：只要往 image-store 里加了/删了/换了图片，就重跑一次，
再连同 data/image-manifest.json 一起提交。import_year_images.py 导入完会自动调用它。
"""
import json
import os
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

IMG_ROOT = os.path.join("image-store", "images", "stamps")
OUT_FILE = os.path.join("data", "image-manifest.json")


def main() -> None:
    manifest: dict[str, list[int]] = {}
    bad = 0
    for dirpath, _, files in os.walk(IMG_ROOT):
        for name in files:
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(dirpath, name)
            # 网站里 image 字段形如 /images/stamps/2026/2026-11-1.jpg
            rel = os.path.relpath(path, "image-store").replace(os.sep, "/")
            key = "/" + rel
            try:
                with Image.open(path) as im:
                    w, h = im.size
                manifest[key] = [w, h]
            except Exception as exc:  # 损坏/无法读取的图不进清单（等同缺图占位）
                bad += 1
                print(f"  [跳过] {key}: 无法读取尺寸（{exc}）")

    # 按键排序，保证多次生成的 diff 稳定、可读
    ordered = {k: manifest[k] for k in sorted(manifest)}
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")

    print(f"\n已写入 {OUT_FILE}：{len(ordered)} 张图片" + (f"，跳过 {bad} 张损坏" if bad else ""))


if __name__ == "__main__":
    main()
