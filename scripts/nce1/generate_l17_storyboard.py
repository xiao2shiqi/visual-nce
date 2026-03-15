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


# Master Specs for Lesson 17
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s office interior, warm indoor lighting. "
SCENE = "Location: A large open-plan office with wooden desks, typewriters, large windows showing a city view, filing cabinets in the background. "
CHAR_JACKSON = "Character Mr. Jackson: A senior manager in his 50s, graying hair, wearing a dark navy suit and a red tie. "
CHAR_RICHARDS = "Character Mr. Richards: A visitor in his 40s, wearing a brown suit and glasses, looking curious. "
CHAR_WOMEN = "Characters Nicola Grey and Claire Taylor: Two young women in professional dresses, one with dark hair and one with blonde hair. "
CHAR_SALES = "Characters Michael Baker and Jeremy Short: Two men in shirts and ties, looking relaxed and not very busy. "
CHAR_JIM = "Character Jim: A young office assistant with messy hair, wearing a white shirt and a gray vest. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the office entrance. Mr. Jackson is welcoming Mr. Richards, gesturing towards the busy office area. Both men are smiling and professional.",
    },
    {
        "id": "keyboard_operators",
        "desc": "Nicola and Claire sitting at their desks, typing busily on large mechanical keyboards. They both have small white name badges that say 'Keyboard Operator' on their lapels.",
    },
    {
        "id": "sales_reps",
        "desc": "Michael and Jeremy leaning against a desk, chatting and laughing, with coffee mugs in their hands. They look very relaxed and idle. A 'Sales Dept' sign is visible nearby.",
    },
    {
        "id": "introductions",
        "desc": "Mr. Jackson introducing Michael and Jeremy to Mr. Richards. Michael and Jeremy are standing up politely but still look very casual compared to the others.",
    },
    {
        "id": "jim",
        "desc": "Jim, the young office assistant, carrying a large stack of papers and files through the office. He looks energetic and busy.",
    },
    {
        "id": "office_wide",
        "desc": "Wide shot of the whole office scene showing the contrast between the hard-working women and the lazy sales reps. Mr. Jackson and Mr. Richards are observing the scene.",
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

    out_dir = root / "public" / "images" / "nce1" / "l17"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L17...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_JACKSON
            + CHAR_RICHARDS
            + CHAR_WOMEN
            + CHAR_SALES
            + CHAR_JIM
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
