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


# Master Specs for Lesson 27
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s living room interior, warm sunny lighting. "
SCENE = "Location: A large, comfortable British living room with large windows, floral curtains, and a wooden floor. "
CHAR_MRS_SMITH = "Character Mrs. Smith: A middle-aged woman with her hair in a tidy perm, wearing a blue floral dress and a pearl necklace. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the large living room. Mrs. Smith is standing gracefully in the center, gesturing to her beautiful home. Sunlight streams through the large window.",
    },
    {
        "id": "tv_magazines",
        "desc": "Medium shot of a vintage television set placed near the window. A few colorful magazines are neatly stacked on top of the television.",
    },
    {
        "id": "table_newspapers",
        "desc": "Focus on a low wooden coffee table in the room. A few folded newspapers are lying on the table surface.",
    },
    {
        "id": "armchairs",
        "desc": "Medium shot of two comfortable pink armchairs arranged near the wooden coffee table.",
    },
    {
        "id": "stereo_books",
        "desc": "Focus on a stereo system positioned near the room's wooden door. Several hardcover books are stacked on top of the stereo.",
    },
    {
        "id": "pictures_wall",
        "desc": "Focus on the living room wall where several framed landscape paintings are hanging. The wall has a subtle patterned wallpaper.",
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

    out_dir = root / "public" / "images" / "nce1" / "l27"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L27...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MRS_SMITH
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
