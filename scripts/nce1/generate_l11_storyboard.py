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


# Master Specs for Lesson 11
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s atmosphere, warm indoor lighting. "
SCENE = "Location: A classic British classroom with wooden desks, large windows, and a chalkboard in the background. The atmosphere is orderly and school-like. "
CHAR_TEACHER = "Character Teacher (Sir): A middle-aged man with kind eyes, graying hair, wearing a brown tweed blazer over a white shirt and a dark green tie. "
CHAR_DAVE = "Character Dave: A young schoolboy with messy dark hair, wearing a light blue school shirt and a gray school sweater. "
CHAR_TIM = "Character Tim: Another schoolboy with blond hair, also in a similar school uniform. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the classroom. The Teacher is standing at the front, holding up a white shirt and looking closely at the label on the collar. Dave is sitting at a desk nearby, looking up at the teacher.",
    },
    {
        "id": "scene3",
        "desc": "Medium shot of the Teacher. He is holding the white shirt, pointing to the brand label on the neck, looking thoughtfully, then turns his gaze towards Tim.",
    },
    {
        "id": "scene2",
        "desc": "Close-up of Dave at his desk. He is shaking his head 'no' with a polite expression, pointing to his own shirt, which is a distinct light blue color.",
    },
    {
        "id": "scene3",
        "desc": "Medium shot of the Teacher. He is looking thoughtfully at the white shirt in his hands, then turns his gaze towards the back of the classroom where Tim is sitting.",
    },
    {
        "id": "scene4",
        "desc": "The Teacher cupping his hand slightly to call out 'Tim!', gesturing with his other hand towards Tim who is further away in the classroom.",
    },
    {
        "id": "scene5",
        "desc": "Action shot: The Teacher is throwing the folded white shirt through the air. The shirt is captured in mid-motion, flying towards Tim.",
    },
    {
        "id": "scene6",
        "desc": "Tim standing by his desk, catching the white shirt with both hands, a bright smile on his face. Warm, happy ending scene.",
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

    out_dir = root / "public" / "images" / "nce1" / "l11"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L11...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"

        print(f"Generating {item['id']}...")
        full_prompt = (
            STYLE
            + SCENE
            + CHAR_TEACHER
            + CHAR_DAVE
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
