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


# Master Specs for Lesson 23
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic interior, warm indoor lighting. "
SCENE = "Location: A cozy room with a wooden sideboard or shelf. Several pairs of glasses and cups are arranged on the shelf. "
CHAR_MAN = "Character Man: A man in his 40s with short brown hair, wearing a light grey sweater over a collared shirt. "
CHAR_WOMAN = (
    "Character Woman: A woman in her 30s with blonde hair, wearing a floral dress. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the room. The Man is talking to the Woman, gesturing towards a shelf where several items are kept.",
    },
    {
        "id": "pointing_shelf",
        "desc": "The Woman pointing to a high shelf where two pairs of glasses are visible next to some cups. One pair is large and one is small.",
    },
    {
        "id": "which_glasses",
        "desc": "Close-up of the shelf. There are two pairs of glasses: one large pair with thick black frames and one small pair with thin gold frames. The Man is pointing towards them.",
    },
    {
        "id": "handing_glasses",
        "desc": "The Woman taking the small gold-framed glasses from the shelf and handing them to the Man.",
    },
    {
        "id": "checking_glasses",
        "desc": "The Man holding the small glasses, looking at them closely. The Woman is smiling at him.",
    },
    {
        "id": "thanking",
        "desc": "The Man putting the glasses into his pocket and nodding his head in thanks to the Woman. Friendly and warm atmosphere.",
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

    out_dir = root / "public" / "images" / "nce1" / "l23"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L23...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MAN
            + CHAR_WOMAN
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
