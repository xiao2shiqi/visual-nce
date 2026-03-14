#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS_FILE = ROOT / "nce4_missing_images_prompts.md"
DEFAULT_OUTPUT_DIR = ROOT / "public" / "images"


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def parse_prompts(file_path: Path):
    if not file_path.exists():
        return []
    content = file_path.read_text(encoding="utf-8")
    lessons = []
    parts = re.split(r"## Lesson (\d+):", content)
    for i in range(1, len(parts), 2):
        lesson_num = int(parts[i])
        section = parts[i + 1]
        match = re.search(
            r"\*\*Prompt:\*\*\s*\n\s*>\s*(.*?)(?:\n\s*\n|$)", section, re.DOTALL
        )
        if not match:
            continue
        prompt = " ".join(match.group(1).strip().splitlines())
        lessons.append({"lesson": lesson_num, "prompt": prompt})
    return lessons


def gemini_generate_image(api_key, model, prompt):
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        endpoint, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )

    with request.urlopen(req, timeout=120) as resp:
        full_resp = json.loads(resp.read().decode("utf-8"))
        parts = full_resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"])
    return None


def main():
    parser = argparse.ArgumentParser(description="Visual NCE Image Generator")
    parser.add_argument(
        "--book", default="nce4", help="Book ID (nce1, nce2, nce3, nce4)"
    )
    parser.add_argument("--start", type=int, default=1, help="Start lesson")
    parser.add_argument("--end", type=int, default=48, help="End lesson")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")
    parser.add_argument("--prompts", help="Path to prompts file")
    args = parser.parse_args()

    load_env_file(ROOT / ".env")
    api_key = os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("VERTEX_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env")
        return

    prompts_file = (
        Path(args.prompts)
        if args.prompts
        else ROOT / f"{args.book}_missing_images_prompts.md"
    )
    lessons = parse_prompts(prompts_file)
    selected = [x for x in lessons if args.start <= x["lesson"] <= args.end]

    if not selected:
        print(f"No prompts found for {args.book} lessons {args.start}-{args.end}")
        return

    print(f"Using model: {model}")
    for item in selected:
        num = item["lesson"]
        prompt = item["prompt"]
        out_dir = DEFAULT_OUTPUT_DIR / args.book / f"l{num}"
        out_path = out_dir / "scene1.png"  # Standard naming convention

        if out_path.exists() and not args.force:
            print(f"Skipping L{num} (exists)")
            continue

        print(f"Generating {args.book} L{num}...")
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            img_bytes = gemini_generate_image(api_key, model, prompt)
            if img_bytes:
                out_path.write_bytes(img_bytes)
                print(f"Success: {out_path}")
            else:
                print(f"Failed to generate L{num}")
            time.sleep(2)
        except Exception as e:
            print(f"Error L{num}: {e}")


if __name__ == "__main__":
    main()
