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


# Master Specs for Lesson 15
STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s airport atmosphere. "
SCENE = "Location: A busy airport customs area with a wooden counter, 'CUSTOMS' sign visible, other travelers with luggage in the background. "
CHAR_OFFICER = "Character Customs Officer: A professional man in a dark blue uniform with a peaked cap, serious but polite expression. "
CHAR_WOMAN_1 = "Character Danish Woman 1: A young woman with long blonde hair, wearing a blue coat and a white scarf. "
CHAR_WOMAN_2 = "Character Danish Woman 2: Her friend, a young woman with short auburn hair, wearing a green jacket over a beige sweater. "

STORYBOARD = [
    {
        "id": "scene1",
        "desc": "Wide shot of the customs counter. The Officer is standing behind the counter, looking at the two Danish Women who are standing in front. They look slightly nervous but polite. They are both young tourists.",
    },
    {
        "id": "passports",
        "desc": "Close-up of Danish Woman 1's hand handing two dark red passports to the Customs Officer across the wooden counter.",
    },
    {
        "id": "suitcases",
        "desc": "The Customs Officer pointing towards two large brown leather suitcases on the floor belonging to the two women. The suitcases have several colorful travel stickers and a visible white customs label hanging from the handle.",
    },
    {
        "id": "officer_checks",
        "desc": "The Customs Officer leaning over the counter to inspect the brown suitcases closely. The two Danish women are watching him attentively.",
    },
    {
        "id": "friends",
        "desc": "The Customs Officer looking towards a group of their friends nearby (Norwegian friends) who are also mostly young women carrying luggage. The friends are waving slightly.",
    },
    {
        "id": "fine",
        "desc": "The Customs Officer smiling slightly and nodding, handing the passports back to the two women. The atmosphere is relieved and friendly.",
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

    out_dir = root / "public" / "images" / "nce1" / "l15"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Starting Storyboard Generation for NCE1 L15...")

    for item in STORYBOARD:
        out_path = out_dir / f"{item['id']}.png"
        print(f"Generating {item['id']}...")

        full_prompt = (
            STYLE
            + SCENE
            + CHAR_OFFICER
            + CHAR_WOMAN_1
            + CHAR_WOMAN_2
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
