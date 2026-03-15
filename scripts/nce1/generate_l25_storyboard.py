#!/usr/bin/env python3
import os
import base64
import json
import time
from pathlib import Path
from urllib import request


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


# Master Specs for Lesson 25
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s kitchen interior, warm indoor lighting. "
SCENE = (
    "Location: A small, cozy British kitchen with tiled walls and a checkered floor. "
)
CHAR_MRS_SMITH = "Character Mrs. Smith: A middle-aged woman with her hair in a tidy perm, wearing a green apron over a simple dress. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the small kitchen. Mrs. Smith is standing near the entrance, smiling. The kitchen is tidy and brightly lit.",
    },
    {
        "id": "refrigerator",
        "desc": "Focus on the right side of the kitchen. A tall, vintage white refrigerator is standing against the wall. Mrs. Smith is gesturing towards it.",
    },
    {
        "id": "cooker",
        "desc": "Focus on the left side of the kitchen. A vibrant blue electric cooker is positioned against the wall. It looks clean and well-maintained.",
    },
    {
        "id": "table",
        "desc": "Medium shot of a wooden table located exactly in the middle of the kitchen. The morning sunlight hits the table surface.",
    },
    {
        "id": "bottle_cup",
        "desc": "Close-up of the wooden table. An empty glass bottle and a clean, white ceramic cup are sitting on the table. The background shows the cozy kitchen.",
    },
]


def main():
    root = Path(__file__).resolve().parents[2]
    load_env_file(root / ".env")
    api_key = os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("VERTEX_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found")
        return

    out_dir = root / "public" / "images" / "nce1" / "l25"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L25...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MRS_SMITH
            + item["desc"]
            + " Maintain high character and background consistency. Studio Ghibli watercolor style."
        )

        try:
            img_bytes = gemini_generate_image(api_key, model, full_prompt)
            if img_bytes:
                out_path.write_bytes(img_bytes)
                print(f"✅ Saved: {out_path}")
            else:
                print(f"❌ Failed to generate {item['id']}")
            time.sleep(3)
        except Exception as e:
            print(f"🔥 Error generating {item['id']}: {e}")


if __name__ == "__main__":
    main()
