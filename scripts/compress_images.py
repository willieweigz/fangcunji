# -*- coding: utf-8 -*-
"""
批量压缩网站邮票图片：长边超过 1600px 或体积超过 400KB 的图片
统一缩到长边 ≤1600px、JPEG 质量 85。只处理网站 public 目录，不碰原始图库。

用法（在项目根目录执行）:
    python scripts/compress_images.py
"""
import os
import sys

from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # 允许处理超大图片（邮票原图可能很高分辨率）

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.join("public", "images", "stamps")
MAX_EDGE = 1600
MAX_KB = 400
QUALITY = 85


def compress_file(path: str) -> tuple[int, int] | None:
    """超标则压缩，返回 (原KB, 新KB)；未超标返回 None。"""
    before = os.path.getsize(path)
    with Image.open(path) as im:
        edge = max(im.size)
        if edge <= MAX_EDGE and before / 1024 <= MAX_KB:
            return None
        im = im.convert("RGB")
        if edge > MAX_EDGE:
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        im.save(path, "JPEG", quality=QUALITY, optimize=True)
    return before // 1024, os.path.getsize(path) // 1024


def main():
    done = skipped = saved = 0
    for dirpath, _, files in os.walk(ROOT):
        for name in sorted(files):
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(dirpath, name)
            result = compress_file(path)
            if result is None:
                skipped += 1
            else:
                b, a = result
                saved += b - a
                done += 1
                print(f"  {os.path.relpath(path, ROOT)}: {b}KB -> {a}KB")
    print(f"\n压缩 {done} 张，未超标跳过 {skipped} 张，共节省 {saved / 1024:.1f}MB")


if __name__ == "__main__":
    main()
