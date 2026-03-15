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


# Master Specs for Lesson 29
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s bedroom interior, warm lighting. "
SCENE = "Location: A messy bedroom with a wooden bed, a large wardrobe, and a dressing table. "
CHAR_MRS_JONES = "Character Mrs. Jones: A middle-aged woman with tidy hair, wearing a floral apron over a simple dress. "
CHAR_AMY = "Character Amy: A young girl with her hair in a ponytail, wearing a light blue dress and a white apron. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the messy bedroom. Amy is standing at the door looking in. Mrs. Jones is standing inside, gesturing to the clothes on the floor and the unmade bed.",
    },
    {
        "id": "shut_door",
        "desc": "Amy turning back to shut the wooden bedroom door politely. Mrs. Jones is looking at her.",
    },
    {
        "id": "air_room",
        "desc": "Amy opening a large window to let the fresh air in. Mrs. Jones is standing nearby, giving instructions.",
    },
    {
        "id": "wardrobe",
        "desc": "Amy picking up clothes from a chair and putting them neatly into a large wooden wardrobe.",
    },
    {
        "id": "make_bed",
        "desc": "Amy smoothing out the blankets and pillows on the wooden bed, making it look tidy.",
    },
    {
        "id": "sweep_floor",
        "desc": "Amy using a wooden broom to sweep the wooden floor. The bedroom now looks much tidier.",
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

    out_dir = root / "public" / "images" / "nce1" / "l29"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L29...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MRS_JONES
            + CHAR_AMY
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
