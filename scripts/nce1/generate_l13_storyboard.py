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


# Master Specs for Lesson 13
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s interior, warm and cozy lighting. "
SCENE_LIVING_ROOM = "Location: A cozy 1970s living room with a patterned rug, a wooden coffee table, and a staircase visible in the background. "
SCENE_BEDROOM = "Location: A sunny upstairs bedroom with a floral wallpaper, a large wooden wardrobe, and a mirror. "
CHAR_ANNA = "Character Anna: A young woman with auburn hair tied in a loose bun, wearing a simple white blouse and a beige skirt. "
CHAR_LOUISE = "Character Louise: Anna's friend, a young woman with short blonde hair, wearing a light yellow cardigan over a floral dress. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the living room. Louise and Anna are sitting on a sofa, talking. Louise is asking Anna a question. Warm afternoon light through the window.",
    },
    {
        "id": "scene2",
        "desc": "Anna standing up with a smile, gesturing towards the stairs. Louise is also standing, looking curious and ready to follow.",
    },
    {
        "id": "scene3",
        "desc": "Wide shot of the upstairs bedroom. Anna is opening her wardrobe, revealing a vibrant emerald green dress hanging inside. The dress has a small white tag on the collar.",
    },
    {
        "id": "scene4",
        "desc": "Close-up of the emerald green dress. Anna is holding the fabric, showing the fine texture to Louise who is looking on with admiration.",
    },
    {
        "id": "scene5",
        "desc": "Anna reaching into the wardrobe again and pulling out a stylish green hat that matches the dress exactly. She looks proud of it.",
    },
    {
        "id": "scene6",
        "desc": "Louise looking at the green hat with a delighted expression, gesturing towards it with both hands. A lovely, friendly atmosphere.",
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

    out_dir = root / "public" / "images" / "nce1" / "l13"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L13...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        # Determine which scene spec to use
        scene_spec = (
            SCENE_LIVING_ROOM if item["id"] in ["scene1", "scene2"] else SCENE_BEDROOM
        )

        full_prompt = (
            STYLE
            + scene_spec
            + CHAR_ANNA
            + CHAR_LOUISE
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
