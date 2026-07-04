"""Compress 2022 stamp images — resize to 1080px, save to temp dir, step 1 of 2."""
from PIL import Image
import os, sys, shutil

Image.MAX_IMAGE_PIXELS = None

SRC = r"G:\微云同步文件夹\邮票网站\public\images\stamps\2022"
TMP = r"C:\temp\stamps_2022_compressed"
MAX_DIM = 1080
JPEG_QUALITY = 85

os.makedirs(TMP, exist_ok=True)

files = sorted([f for f in os.listdir(SRC) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

total_before = 0
total_after = 0
n = len(files)

for i, f in enumerate(files):
    path = os.path.join(SRC, f)
    size_before = os.path.getsize(path)
    total_before += size_before
    
    try:
        img = Image.open(path)
        img.verify()
        img = Image.open(path)
        w, h = img.size
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        ratio = min(MAX_DIM / w, MAX_DIM / h)
        if ratio < 1.0:
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        
        out_path = os.path.join(TMP, f)
        img.save(out_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        
        size_after = os.path.getsize(out_path)
        total_after += size_after
        
        reduction = (1 - size_after / size_before) * 100
        print(f"[{i+1}/{n}] {f}: {w}x{h} -> {img.size[0]}x{img.size[1]}  |  {size_before//1024}KB -> {size_after//1024}KB  ({reduction:.0f}%)")
        sys.stdout.flush()
    except Exception as e:
        print(f"[{i+1}/{n}] {f}: ERROR - {e}")
        sys.stdout.flush()
        # Copy as-is on error
        shutil.copy2(path, os.path.join(TMP, f))
        total_after += size_before

print()
print(f"Total before: {total_before // (1024*1024)} MB")
print(f"Total after:  {total_after // (1024*1024)} MB")
print(f"Saved:        {(total_before - total_after) // (1024*1024)} MB ({(1 - total_after/total_before)*100:.0f}%)")
print()
print(f"Compressed images saved to: {TMP}")
print("Run step 2: PowerShell to copy back to target directory.")
