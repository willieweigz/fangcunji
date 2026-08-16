import argparse
from pathlib import Path
from PIL import Image

SOURCE = Path(r"G:\微云同步文件夹\纸上山河资料\画册 - 原稿\三十三剑客")
OUTPUT = Path(__file__).resolve().parents[1] / "image-store" / "images" / "albums" / "sanshisan-jianke-tu"
SPECIAL_PAGES = {
    "000": SOURCE / "000-三十三劍客圖-封面長卷-v1-原題字引首-21：9.png",
    "034": SOURCE / "034-三十三劍客-全體群像-v1-山巔會聚-21：9.png",
}


def save_webp(source: Path, target: Path, max_width: int, quality: int) -> None:
    with Image.open(source) as image:
        image = image.convert("RGB")
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.Resampling.LANCZOS)
        image.save(target, "WEBP", quality=quality, method=6)


def prepare_standard_pages() -> None:
    complete_pages = sorted(SOURCE.glob("???-*完整頁*.png"))
    if len(complete_pages) != 33:
        raise RuntimeError(f"Expected 33 complete pages, found {len(complete_pages)}")

    for source in complete_pages:
        number = source.name[:3]
        save_webp(source, OUTPUT / f"{number}.webp", max_width=3600, quality=84)

    cover_candidates = sorted(SOURCE.glob("001-*主画*.png"))
    if len(cover_candidates) != 1:
        raise RuntimeError(f"Expected one final cover scene, found {len(cover_candidates)}")
    save_webp(cover_candidates[0], OUTPUT / "cover.webp", max_width=1800, quality=86)


def prepare_special_pages() -> None:
    for number, source in SPECIAL_PAGES.items():
        if not source.is_file():
            raise FileNotFoundError(f"Missing special page: {source}")
        save_webp(source, OUTPUT / f"{number}.webp", max_width=3600, quality=84)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare WebP assets for 三十三剑客图")
    parser.add_argument("--special-only", action="store_true", help="Only prepare cover and ending pages")
    args = parser.parse_args()

    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not args.special_only:
        prepare_standard_pages()
    prepare_special_pages()

    files = sorted(OUTPUT.glob("*.webp"))
    total_mb = sum(file.stat().st_size for file in files) / 1024 / 1024
    print(f"Prepared {len(files)} WebP files, {total_mb:.1f} MB total")


if __name__ == "__main__":
    main()
