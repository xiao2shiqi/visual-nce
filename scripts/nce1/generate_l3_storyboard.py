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


# Master Specs for Lesson 3
STYLE = "Studio Ghibli illustration style, vibrant watercolor textures, painterly, detailed background, warm interior lighting, nostalgic atmosphere. "
SCENE = "Location: A classic elegant cloakroom counter with wooden panels, rows of coats hanging in the background, brass coat check tags visible. "
CHAR_YOUNG_MAN = "Character Young Man (Customer): Young man in his 20s, with short black hair, wearing a brown corduroy jacket over a white collared shirt, polite and neat appearance. "
CHAR_OLD_MAN = "Character Older Man (Attendant): Kind older man in his 60s, balding with white hair on the sides, wearing a gray knitted vest over a light blue shirt and a dark tie, wearing round spectacles. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the cloakroom. The older attendant is behind the counter, and the young man is standing in front of it. Both characters fully visible, talking politely.",
    },
    {
        "id": "handing_ticket",
        "desc": "Close-up of the young man's hand handing a small paper ticket to the older attendant across the wooden counter.",
    },
    {
        "id": "searching",
        "desc": "The older attendant is searching through a row of hanging wool coats and umbrellas, looking closely at the numbered tags.",
    },
    {
        "id": "wrong_umbrella",
        "desc": "The older attendant hands a bright red umbrella and a black coat to the young man; the young man looks confused and is politely gesturing 'no' with one hand.",
    },
    {
        "id": "showing_correct",
        "desc": "The older attendant is now showing a dark green umbrella to the young man. The young man looks at it with interest and recognition.",
    },
    {
        "id": "receiving_correct",
        "desc": "The young man is smiling happily and receiving the dark green umbrella from the older attendant. Both are smiling, warm atmosphere.",
    },
]


def main():
    root = Path(__file__).resolve().parents[1]
    load_env_file(root / ".env")
    api_key = os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("VERTEX_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found")
        return

    out_dir = root / "public" / "images" / "nce1" / "l3"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L3...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        if out_path.exists():
            print(f"Skipping {item['id']} (already exists)")
            continue

        print(f"Generating {item['id']}...")
        full_prompt = (
            STYLE
            + SCENE
            + CHAR_YOUNG_MAN
            + CHAR_OLD_MAN
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
