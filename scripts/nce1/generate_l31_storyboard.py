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


# Master Specs for Lesson 31
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic sunny garden, warm outdoor lighting. "
SCENE = "Location: A lush green English garden with a large oak tree and a white wooden fence. "
CHAR_JEAN = "Character Jean: A kind woman in her 30s with blonde hair, wearing a white blouse and a floral skirt. "
CHAR_JACK = (
    "Character Jack: Her husband, a man with short brown hair, wearing a grey sweater. "
)
CHAR_SALLY = "Character Sally: A young girl about 5 years old with blonde curls, wearing a yellow sundress. "
CHAR_TIM = "Character Tim: A young boy about 7 years old with dark hair, wearing a red t-shirt and shorts. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Jean and Jack are standing by a large window looking out at the garden. Jean is asking Jack a question.",
    },
    {
        "id": "sally_under_tree",
        "desc": "Wide shot of the garden. Sally is sitting on the grass in the shade of a large oak tree, happily eating a red apple.",
    },
    {
        "id": "tim_climbing",
        "desc": "Tim is climbing the large oak tree. He is about halfway up, gripping a thick branch and looking down towards the garden.",
    },
    {
        "id": "dog_running",
        "desc": "A small, energetic brown dog is running excitedly across the green grass of the garden.",
    },
    {
        "id": "dog_after_cat",
        "desc": "Action shot: The dog is chasing a black and white cat across the lawn. The cat is sprinting towards the fence.",
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

    out_dir = root / "public" / "images" / "nce1" / "l31"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L31...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_JEAN
            + CHAR_JACK
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
