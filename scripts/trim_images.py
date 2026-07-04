# -*- coding: utf-8 -*-
# 批量裁掉邮票图片四周的白色扫描边距（保留齿孔，留 4px 余量）
# 用法: python scripts/trim_images.py public/images/stamps/2024
import os
import sys

from PIL import Image, ImageChops

THRESHOLD = 18  # 与纯白的差异阈值，越小裁得越紧
PAD = 4  # 裁剪后保留的白边像素


def trim(path: str) -> bool:
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg).convert("L")
    mask = diff.point(lambda x: 255 if x > THRESHOLD else 0)
    bbox = mask.getbbox()
    if not bbox:
        return False
    l, t, r, b = bbox
    l = max(0, l - PAD)
    t = max(0, t - PAD)
    r = min(im.width, r + PAD)
    b = min(im.height, b + PAD)
    if (r - l) >= im.width and (b - t) >= im.height:
        return False
    im.crop((l, t, r, b)).save(path, quality=92)
    return True


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    trimmed = skipped = 0
    for name in sorted(os.listdir(target)):
        if not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        if trim(os.path.join(target, name)):
            trimmed += 1
        else:
            skipped += 1
    print(f"trimmed: {trimmed}, unchanged: {skipped}")


if __name__ == "__main__":
    main()
