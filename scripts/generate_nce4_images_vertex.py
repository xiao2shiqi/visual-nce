#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib import error, request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS_FILE = ROOT / "nce4_missing_images_prompts.md"
DEFAULT_OUTPUT_DIR = ROOT / "public" / "images" / "nce4"


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        raise FileNotFoundError(f".env file not found: {env_path}")

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def parse_prompts(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lessons = []
    parts = re.split(r"## Lesson (\d+):", content)
    for i in range(1, len(parts), 2):
        lesson_num = int(parts[i])
        section = parts[i + 1]
        match = re.search(r"\*\*Prompt:\*\*\s*\n\s*>\s*(.*?)(?:\n\s*\n|$)", section, re.DOTALL)
        if not match:
            continue
        prompt = " ".join(match.group(1).strip().splitlines())
        lessons.append({"lesson": lesson_num, "prompt": prompt})
    return lessons


def image_bytes_from_predict(prediction: dict) -> bytes:
    if isinstance(prediction, dict):
        if "bytesBase64Encoded" in prediction:
            return base64.b64decode(prediction["bytesBase64Encoded"])
        image = prediction.get("image")
        if isinstance(image, dict) and "bytesBase64Encoded" in image:
            return base64.b64decode(image["bytesBase64Encoded"])
    raise ValueError("Vertex response does not include image bytesBase64Encoded")


def vertex_predict(api_key: str, project_id: str, location: str, model: str, prompt: str, aspect_ratio: str) -> bytes:
    endpoint = (
        f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}"
        f"/locations/{location}/publishers/google/models/{model}:predict?key={api_key}"
    )
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": aspect_ratio,
            "personGeneration": "allow_adult",
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(endpoint, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Vertex API HTTP {exc.code}: {detail[:600]}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Vertex API network error: {exc}") from exc

    predictions = body.get("predictions") or []
    if not predictions:
        raise RuntimeError(f"Vertex API returned no predictions: {json.dumps(body)[:600]}")
    return image_bytes_from_predict(predictions[0])


def convert_png_to_jpg(png_path: Path, jpg_path: Path) -> None:
    try:
        from PIL import Image

        with Image.open(png_path) as img:
            rgb = img.convert("RGB")
            rgb.save(jpg_path, format="JPEG", quality=92)
        return
    except Exception:
        pass

    cmd = ["sips", "-s", "format", "jpeg", str(png_path), "--out", str(jpg_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Failed to convert PNG to JPG. Install Pillow (`pip install pillow`) or ensure `sips` is available."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate missing NCE4 images with Vertex Imagen")
    parser.add_argument("--env-file", default="", help="Path to .env file containing GOOGLE_API_KEY and VERTEX_*")
    parser.add_argument("--start", type=int, default=6, help="Start lesson number (inclusive)")
    parser.add_argument("--end", type=int, default=48, help="End lesson number (inclusive)")
    parser.add_argument("--max-images", type=int, default=0, help="Max images to generate in this run (0 = unlimited)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scene1.jpg")
    parser.add_argument("--lesson", type=int, default=0, help="Generate one specific lesson with --prompt-text")
    parser.add_argument("--prompt-text", default="", help="Custom prompt text for single-lesson generation")
    parser.add_argument("--output-name", default="scene1.jpg", help="Output file name inside lesson folder")
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        help="Image aspect ratio for Imagen request (default: 16:9)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print plan only, no API calls")
    parser.add_argument("--sleep", type=float, default=1.5, help="Delay between requests in seconds")
    args = parser.parse_args()

    if args.start > args.end:
        print("Error: --start must be <= --end")
        return 1

    if args.env_file:
        load_env_file(Path(args.env_file).expanduser().resolve())

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    project_id = os.environ.get("VERTEX_PROJECT_ID", "")
    location = os.environ.get("VERTEX_LOCATION", "us-central1")
    model = os.environ.get("VERTEX_IMAGE_MODEL", "imagen-4.0-generate-001")
    aspect_ratio = args.aspect_ratio or os.environ.get("VERTEX_IMAGE_ASPECT_RATIO", "16:9")

    missing = [k for k, v in {
        "GOOGLE_API_KEY": api_key,
        "VERTEX_PROJECT_ID": project_id,
        "VERTEX_LOCATION": location,
    }.items() if not v]
    if missing:
        print(f"Error: missing env vars: {', '.join(missing)}")
        return 1

    if args.lesson and args.prompt_text.strip():
        selected = [{"lesson": args.lesson, "prompt": args.prompt_text.strip()}]
    else:
        lessons = parse_prompts(DEFAULT_PROMPTS_FILE)
        selected = [x for x in lessons if args.start <= x["lesson"] <= args.end]
    if not selected:
        print("No lessons selected from prompts file.")
        return 0

    if args.lesson and args.prompt_text.strip():
        print(f"Loaded 1 custom lesson prompt (L{args.lesson})")
    else:
        print(f"Loaded {len(selected)} lessons from {DEFAULT_PROMPTS_FILE}")
    print(f"Model={model} AspectRatio={aspect_ratio} Location={location}")

    generated = 0
    skipped = 0
    failed = 0

    for item in selected:
        lesson_num = item["lesson"]
        prompt = item["prompt"]
        lesson_dir = DEFAULT_OUTPUT_DIR / f"l{lesson_num}"
        scene_jpg = lesson_dir / args.output_name
        scene_png = lesson_dir / "scene1.png"

        if scene_jpg.exists() and not args.force:
            print(f"[skip] L{lesson_num}: already exists ({scene_jpg})")
            skipped += 1
            continue

        if args.max_images and generated >= args.max_images:
            print("Reached --max-images limit, stopping.")
            break

        print(f"[gen] L{lesson_num}: {prompt[:90]}...")
        if args.dry_run:
            continue

        lesson_dir.mkdir(parents=True, exist_ok=True)
        try:
            img_bytes = vertex_predict(
                api_key=api_key,
                project_id=project_id,
                location=location,
                model=model,
                prompt=prompt,
                aspect_ratio=aspect_ratio,
            )
            scene_png.write_bytes(img_bytes)
            convert_png_to_jpg(scene_png, scene_jpg)
            if scene_png.exists():
                scene_png.unlink()
            generated += 1
            print(f"[ok]   L{lesson_num}: {scene_jpg}")
            time.sleep(max(args.sleep, 0))
        except Exception as exc:
            failed += 1
            print(f"[err]  L{lesson_num}: {exc}")
            time.sleep(2)

    print("\nDone.")
    print(f"Generated: {generated}, Skipped: {skipped}, Failed: {failed}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
