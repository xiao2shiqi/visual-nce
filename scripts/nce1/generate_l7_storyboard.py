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


# Master Specs for Lesson 7
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, bright and warm lighting, nostalgic atmosphere. "
SCENE = "Location: A sunny study area in a language school with wooden tables, some books and coffee cups, large windows showing a green garden. "
CHAR_ROBERT = "Character Robert: Young man in his early 20s, friendly smile, wearing a green knitted sweater over a white shirt. "
CHAR_SOPHIE = "Character Sophie Dupont: Elegant young French woman with auburn hair, wearing a light blue dress with a small floral pattern (same as Lesson 5). "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of Robert and Sophie sitting at a wooden table in the study area. Robert is gesturing as he introduces himself, and Sophie is listening with a friendly smile.",
    },
    {
        "id": "robert_intro",
        "desc": "Robert pointing to himself with a friendly smile, introducing himself. He looks enthusiastic and approachable.",
    },
    {
        "id": "sophie_intro",
        "desc": "Sophie smiling and nodding, introducing herself to Robert. She looks elegant and polite.",
    },
    {
        "id": "talking_nationality",
        "desc": "Robert and Sophie in conversation. Robert is asking a question, and Sophie is answering with a bright smile.",
    },
    {
        "id": "talking_nationality_2",
        "desc": "Sophie leaning forward slightly, asking Robert a question in return. Both are engaged in a pleasant conversation.",
    },
    {
        "id": "robert_italian",
        "desc": "Robert smiling proudly, perhaps with a slight Italian gesture, explaining his nationality. Warm, sunlit scene.",
    },
    {
        "id": "asking_job",
        "desc": "Close-up of Robert and Sophie. Robert is looking curious as he asks about Sophie's profession.",
    },
    {
        "id": "keyboard_operator",
        "desc": "Sophie explaining her job, perhaps gesturing towards an imaginary keyboard. She looks focused and professional.",
    },
    {
        "id": "engineer",
        "desc": "Robert explaining his job as an engineer, looking happy and confident. Both are smiling at the end of their conversation.",
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

    out_dir = root / "public" / "images" / "nce1" / "l7"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L7...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        if out_path.exists():
            print(f"Skipping {item['id']} (already exists)")
            continue

        print(f"Generating {item['id']}...")
        full_prompt = (
            STYLE
            + SCENE
            + CHAR_ROBERT
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
