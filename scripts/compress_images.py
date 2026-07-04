#!/usr/bin/env python3
"""One-off: convert public/images PNG/JPG to WebP, generate homepage
thumbnails, and rewrite JSON references.

- Full images: same dimensions, WebP q82 (visually lossless for this art style)
- Covers referenced by curriculum.json: extra thumb.webp at 480px wide
- Skips files referenced directly in .vue code (sponsor.jpg)
"""
import json
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "public" / "images"
SKIP = {IMAGES / "sponsor.jpg"}
QUALITY = 82
THUMB_WIDTH = 480


def convert_one(path_str: str) -> tuple[str, int, int]:
    path = Path(path_str)
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    out = path.with_suffix(".webp")
    im.save(out, "WEBP", quality=QUALITY, method=6)
    old_size = path.stat().st_size
    new_size = out.stat().st_size
    if out != path:
        path.unlink()
    return (str(path.relative_to(ROOT)), old_size, new_size)


def make_thumb(src: Path) -> Path:
    """Generate thumb.webp next to a cover image. src may already be .webp."""
    im = Image.open(src)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    w, h = im.size
    if w > THUMB_WIDTH:
        im = im.resize((THUMB_WIDTH, round(h * THUMB_WIDTH / w)), Image.LANCZOS)
    out = src.parent / "thumb.webp"
    im.save(out, "WEBP", quality=75, method=6)
    return out


IMG_REF = re.compile(r'(/images/[^"]+?)\.(png|jpe?g)')


def rewrite_json_refs(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, n = IMG_REF.subn(r"\1.webp", text)
    if n:
        path.write_text(new_text, encoding="utf-8")
    return n


def main() -> None:
    targets = [
        str(p)
        for p in IMAGES.rglob("*")
        if p.suffix.lower() in (".png", ".jpg", ".jpeg") and p not in SKIP
    ]
    print(f"converting {len(targets)} images ...", flush=True)
    old_total = new_total = done = 0
    with ProcessPoolExecutor(max_workers=8) as pool:
        for rel, old, new in pool.map(convert_one, targets, chunksize=8):
            old_total += old
            new_total += new
            done += 1
            if done % 100 == 0:
                print(f"  {done}/{len(targets)}  {old_total/1e9:.2f}GB -> {new_total/1e6:.0f}MB", flush=True)
    print(f"converted {done}: {old_total/1e9:.2f}GB -> {new_total/1e6:.0f}MB", flush=True)

    # rewrite JSON refs (.png/.jpg -> .webp)
    total_refs = 0
    for jf in [ROOT / "src/data/curriculum.json", *(ROOT / "src/data/lessons").glob("*.json")]:
        total_refs += rewrite_json_refs(jf)
    print(f"rewrote {total_refs} JSON refs", flush=True)

    # thumbnails for curriculum covers, then point curriculum at them
    curriculum_path = ROOT / "src/data/curriculum.json"
    data = json.loads(curriculum_path.read_text(encoding="utf-8"))
    made = 0
    for book in data["books"]:
        for lesson in book["lessons"]:
            img = lesson.get("image")
            if not img:
                continue
            src = ROOT / "public" / img.lstrip("/")
            if not src.exists():
                print(f"  MISSING cover: {img}", flush=True)
                continue
            make_thumb(src)
            lesson["image"] = str(Path(img).parent / "thumb.webp")
            made += 1
    curriculum_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"generated {made} thumbnails and updated curriculum.json", flush=True)


if __name__ == "__main__":
    sys.exit(main())
