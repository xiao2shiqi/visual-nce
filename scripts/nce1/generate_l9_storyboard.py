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


# Master Specs for Lesson 9
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, bright and warm lighting, nostalgic atmosphere. "
SCENE = "Location: A pleasant park path with green trees, flower beds, and a park bench in the background. Sunny day. "
CHAR_STEVEN = "Character Steven: Young man with short dark hair, wearing a casual orange sweater and jeans, friendly and energetic. "
CHAR_HELEN = "Character Helen: Young woman with shoulder-length brown hair, wearing a light yellow dress and a white cardigan, looking healthy and cheerful. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of a park path. Steven and Helen have just bumped into each other and are waving. Bright, sunny morning atmosphere.",
    },
    {
        "id": "meeting",
        "desc": "Steven and Helen standing on the path, smiling and greeting each other. Steven has his hands in his pockets, Helen is holding a small book.",
    },
    {
        "id": "helen_healthy",
        "desc": "Close-up of Helen smiling brightly, looking very well. Her eyes are sparkling, and the sunlight filters through the trees behind her.",
    },
    {
        "id": "steven_fine",
        "desc": "Steven nodding and smiling, looking relaxed and healthy. He is enjoying the conversation.",
    },
    {
        "id": "tony_fine",
        "desc": "Helen talking about Tony (a young boy, perhaps her son, visible in a small 'thought bubble' or just mentioned by her gesture). She looks happy.",
    },
    {
        "id": "emma_fine",
        "desc": "Steven talking about Emma (a young woman, perhaps his wife, mentioned by his gesture). He looks very pleased.",
    },
    {
        "id": "goodbye",
        "desc": "Steven and Helen walking away from each other in opposite directions, waving goodbye over their shoulders. The sun is setting slightly, warm colors.",
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

    out_dir = root / "public" / "images" / "nce1" / "l9"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L9...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        if out_path.exists():
            print(f"Skipping {item['id']} (already exists)")
            continue

        print(f"Generating {item['id']}...")
        full_prompt = (
            STYLE
            + SCENE
            + CHAR_STEVEN
            + CHAR_HELEN
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
