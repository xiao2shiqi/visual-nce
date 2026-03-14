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


# Master Specs for Lesson 5
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, bright and warm lighting, nostalgic atmosphere. "
SCENE = "Location: A sunny, bright classroom in a language school with wooden desks, a large window showing a green garden outside, and a chalkboard. "
CHAR_MR_BLAKE = "Character Mr. Blake: Middle-aged British man, short brown hair, kind and professional expression, wearing a light grey suit with a white shirt and a blue tie. "
CHAR_ALICE = "Character Alice: Young woman with blonde hair in a ponytail, wearing a white long-sleeved blouse and a green knee-length skirt. "
CHAR_SOPHIE = "Character Sophie Dupont: Elegant young French woman with auburn hair, wearing a light blue dress with a small floral pattern. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the bright classroom. Mr. Blake and Alice are standing at the front, smiling warmly. Several students of different nationalities are sitting at their desks, looking attentive.",
    },
    {
        "id": "mr_blake_enters",
        "desc": "Mr. Blake entering the bright, sunny classroom, waving a hand in a friendly greeting to the students. Warm, welcoming atmosphere.",
    },
    {
        "id": "alice_greets",
        "desc": "Alice, the blonde young woman, smiling and greeting Mr. Blake as he stands at the front of the classroom.",
    },
    {
        "id": "introducing_sophie",
        "desc": "Mr. Blake gesturing towards Sophie Dupont, who is standing next to him. Sophie looks polite and elegant, nodding to the class.",
    },
    {
        "id": "sophie_smile",
        "desc": "Close-up of Sophie Dupont smiling warmly, her auburn hair catching the soft sunlight from the window. High detail, beautiful Ghibli style.",
    },
    {
        "id": "introducing_hans",
        "desc": "Mr. Blake pointing towards Hans, a young man with blond hair sitting at a wooden desk. Hans is looking up and smiling politely.",
    },
    {
        "id": "sophie_hans_greet",
        "desc": "Sophie waving slightly at Hans, who is nodding back. Both characters in the sunny classroom setting.",
    },
    {
        "id": "introducing_naoko",
        "desc": "Mr. Blake introducing Naoko, a young Japanese woman with black bob hair sitting at a desk. She is wearing a yellow cardigan and smiling.",
    },
    {
        "id": "introducing_changwoo",
        "desc": "Mr. Blake introducing Chang-woo, a young Korean man with black hair and glasses sitting at a desk. He looks smart and friendly.",
    },
    {
        "id": "introducing_luming",
        "desc": "Mr. Blake introducing Luming, a young Chinese man wearing a red t-shirt, sitting at a desk and waving his hand.",
    },
    {
        "id": "introducing_xiaohui",
        "desc": "Mr. Blake introducing Xiaohui, a young Chinese woman with long black hair and a friendly smile. She is sitting next to Luming.",
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

    out_dir = root / "public" / "images" / "nce1" / "l5"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L5...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        if out_path.exists():
            print(f"Skipping {item['id']} (already exists)")
            continue

        print(f"Generating {item['id']}...")
        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MR_BLAKE
            + CHAR_ALICE
            + CHAR_SOPHIE
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
