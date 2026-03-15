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


# Master Specs for Lesson 33
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic sunny day, warm outdoor lighting. "
SCENE = "Location: A scenic English countryside with a stone bridge over a sparkling blue river. Lush green trees line the banks. "
CHAR_MR_JONES = "Character Mr. Jones: A man in his 30s with short dark hair, wearing a brown jacket. "
CHAR_MRS_JONES = "Character Mrs. Jones: A woman with blonde hair in a ponytail, wearing a yellow dress. "
CHAR_SALLY = (
    "Character Sally: A young girl with blonde curls, wearing a pink sundress. "
)
CHAR_TIM = "Character Tim: A young boy with dark hair, wearing a striped t-shirt and blue shorts. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the stone bridge on a beautiful sunny day with a few fluffy white clouds in the blue sky. The Jones family is walking together across the bridge.",
    },
    {
        "id": "boats_on_river",
        "desc": "Medium shot of Mr. Jones and Mrs. Jones leaning on the bridge's stone railing, looking down at several small colorful wooden boats floating on the river.",
    },
    {
        "id": "sally_ship",
        "desc": "Sally is pointing excitedly with one hand at a large, majestic white cargo ship that is passing directly underneath the stone bridge.",
    },
    {
        "id": "tim_aeroplane",
        "desc": "Tim is standing on the bridge, looking high up into the blue sky and pointing at a small silver propeller plane flying overhead.",
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

    out_dir = root / "public" / "images" / "nce1" / "l33"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L33...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MR_JONES
            + CHAR_MRS_JONES
            + CHAR_SALLY
            + CHAR_TIM
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
