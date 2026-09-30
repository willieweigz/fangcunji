"""Build small list-cover previews without changing the original stamp images.

Uses the same cover choice as lib/stamps.ts + StampCard. Existing small images,
unusual color modes and files with less than 10% savings keep their original URL.
Requires Pillow, just like build_image_manifest.py. Generated files belong to the
separate image-store repository; only the JSON manifest belongs to the website.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import io
import json

from PIL import Image, ImageOps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default='.')
    parser.add_argument('--image-store')
    parser.add_argument('--output-store')
    args = parser.parse_args()
    project = Path(args.project)
    store = Path(args.image_store) if args.image_store else project / 'image-store'
    destination = Path(args.output_store) if args.output_store else store
    sizes = json.loads((project / 'data/image-manifest.json').read_text(encoding='utf-8'))
    output = project / 'data/stamp-preview-manifest.json'
    previous = json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
    selected = set()

    for file in (project / 'data/stamps').glob('*.json'):
        for stamp_set in json.loads(file.read_text(encoding='utf-8-sig')):
            available = [stamp for stamp in stamp_set['stamps'] if stamp['image'] in sizes]
            preferred = next((stamp for form in ['小全张', '全套', '整版']
                              for stamp in available if stamp.get('format') == form), None)
            if preferred:
                width, height = sizes[preferred['image']]
                if not height or not 1 / 3 <= width / height <= 3:
                    preferred = None
            cover = preferred or next(iter(available), None)
            if cover:
                selected.add(cover['image'])

    def convert(key):
        if not key.startswith('/images/stamps/') or '..' in Path(key).parts:
            raise ValueError(f'Unexpected source path: {key}')
        source = store / key.lstrip('/')
        raw = source.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        with Image.open(io.BytesIO(raw)) as metadata:
            # Keep CMYK and transparent images on the original-image path.
            if metadata.mode != 'RGB':
                return key, None
            has_profile = bool(metadata.info.get('icc_profile'))
        recipe = b'list-640-lanczos-q90-v2' + (b'-keep-icc' if has_profile else b'')
        fingerprint = hashlib.sha256(raw + recipe).hexdigest()[:16]
        relative = (Path('images/stamp-previews') / Path(key).parent.name /
                    (Path(key).stem + '.' + fingerprint + '.webp'))
        target = destination / relative
        old = previous.get(key)
        if (old and old.get('sourceSha256') == digest and
                old.get('preview') == '/' + relative.as_posix() and target.exists()):
            return key, old

        with Image.open(io.BytesIO(raw)) as image:
            profile = image.info.get('icc_profile')
            image = ImageOps.exif_transpose(image).convert('RGB')
            original_size = image.size
            if max(image.size) <= 640:
                return key, None
            image.thumbnail((640, 640), Image.Resampling.LANCZOS)
            # Encode in memory first so a rejected preview never creates a file.
            buffer = io.BytesIO()
            image.save(buffer, 'WEBP', quality=90, method=4,
                       **({'icc_profile': profile} if profile else {}))
            encoded = buffer.getvalue()
            if len(encoded) >= len(raw) * 0.9:
                return key, None
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(encoded)
            return key, {
                'preview': '/' + relative.as_posix(), 'sourceSha256': digest,
                'width': image.width, 'height': image.height, 'bytes': len(encoded),
                'sourceBytes': len(raw), 'sourceWidth': original_size[0],
                'sourceHeight': original_size[1],
            }

    results = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for index, (key, value) in enumerate(pool.map(convert, sorted(selected)), 1):
            if value:
                results[key] = value
            if index % 200 == 0:
                print(f'processed {index} of {len(selected)}', flush=True)
    output.write_text(json.dumps(results, ensure_ascii=False, separators=(',', ':')) + '\n',
                      encoding='utf-8')
    print(json.dumps({'covers': len(selected), 'previews': len(results),
                      'originalBytes': sum(row['sourceBytes'] for row in results.values()),
                      'previewBytes': sum(row['bytes'] for row in results.values())}), flush=True)


if __name__ == '__main__':
    main()
