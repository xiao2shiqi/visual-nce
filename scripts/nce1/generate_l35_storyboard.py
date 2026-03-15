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


# Master Specs for Lesson 35
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic English village, warm sunny lighting. "
SCENE_VILLAGE = "Location: A charming English village in a green valley, surrounded by two rolling hills. A clear river flows through the village. "
CHAR_NARRATOR = "Character Narrator: A man in his 30s with short dark hair, wearing a casual brown jacket. "
CHAR_WIFE = (
    "Character Wife: A woman with blonde hair in a ponytail, wearing a floral dress. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide panoramic shot of the beautiful village in a valley between two green hills. The village is on the bank of a sparkling river. High character/background consistency.",
    },
    {
        "id": "walking_bank",
        "desc": "The Narrator and his Wife are walking happily along the grassy bank of the clear blue river. They are on the left side of the frame.",
    },
    {
        "id": "boy_swimming",
        "desc": "Focus on the river. A young boy is swimming vigorously across the water. The river bank is visible in the background.",
    },
    {
        "id": "school_park",
        "desc": "Wide shot of a brick school building next to a lush green park. The park is on the right side of the building.",
    },
    {
        "id": "children_action",
        "desc": "Some children are coming out of the school building doors, and some other children are entering the green park nearby. Energetic atmosphere.",
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

    out_dir = root / "public" / "images" / "nce1" / "l35"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L35...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE_VILLAGE
            + CHAR_NARRATOR
            + CHAR_WIFE
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
