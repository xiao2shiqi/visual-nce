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


# Master Specs for Lesson 19
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic sunny afternoon, warm outdoor lighting. "
SCENE = "Location: A pleasant park with green trees, a paved path, and a wooden park bench. "
CHAR_MUM = "Character Mother (Mum): A kind woman in her 30s with light brown hair, wearing a simple yellow dress and carrying a small floral handbag. "
CHAR_ANDY = "Character Andy: A young boy about 8 years old with messy dark hair, wearing a striped t-shirt and blue shorts. "
CHAR_LUCY = "Character Lucy: A young girl about 6 years old with blonde pigtails, wearing a pink sundress. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the park. The Mother is walking with Andy and Lucy. The children look very exhausted, wiping sweat from their foreheads, looking tired and thirsty.",
    },
    {
        "id": "bench",
        "desc": "The Mother pointing towards a wooden park bench under a large shady tree. Andy and Lucy are looking at the bench with relief.",
    },
    {
        "id": "sitting",
        "desc": "Andy and Lucy sitting on the park bench, slumped over slightly, looking very thirsty. The Mother is standing in front of them, looking concerned.",
    },
    {
        "id": "ice_cream_man",
        "desc": "The Mother looking towards a colorful ice cream van parked nearby. A cheerful Ice Cream Man is visible through the window. The children are looking up with bright eyes.",
    },
    {
        "id": "buying",
        "desc": "The Mother standing at the ice cream van, buying two large ice cream cones. One is strawberry and one is chocolate.",
    },
    {
        "id": "eating",
        "desc": "Andy and Lucy sitting on the bench, each happily eating an ice cream cone. They are smiling and look much better. The Mother is watching them with a happy smile.",
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

    out_dir = root / "public" / "images" / "nce1" / "l19"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L19...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_MUM
            + CHAR_ANDY
            + CHAR_LUCY
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
