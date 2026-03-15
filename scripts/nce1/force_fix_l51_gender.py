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

    try:
        with request.urlopen(req, timeout=120) as resp:
            full_resp = json.loads(resp.read().decode("utf-8"))
            parts = (
                full_resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            )
            for part in parts:
                if "inlineData" in part:
                    return base64.b64decode(part["inlineData"]["data"])
    except Exception as e:
        print(f"API Error: {e}")
    return None


STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s atmosphere, warm indoor lighting. "

# Focus ONLY on fixing Lesson 51 with extremely explicit gender instructions
L51_FIX = {
    "lesson": "l51",
    "chars": "TWO MEN: Dimitri (a young Greek man with dark curly hair) and a Traveler (a young man with short brown hair, wearing a sun hat and carrying a camera). NO WOMEN AT ALL. ",
    "scene": "A terrace in Greece overlooking the blue Aegean sea and white buildings. ",
    "items": [
        {
            "id": "scene1",
            "desc": "Wide shot of Dimitri and the Traveler (two men) standing on a terrace. They are both looking at the sea. Strictly two adult males, absolutely no female characters.",
        },
        {
            "id": "spring_windy",
            "desc": "The two men (Dimitri and the traveler) standing in a windy Greek landscape in spring. Trees blowing. Both characters are male.",
        },
        {
            "id": "summer_hot",
            "desc": "The two men (Dimitri and the traveler) under a hot summer sun in Greece. Both are male.",
        },
        {
            "id": "autumn_warm",
            "desc": "The two men (Dimitri and the traveler) walking in a warm autumn olive grove. Both are male.",
        },
        {
            "id": "winter_snow",
            "desc": "The two men (Dimitri and the traveler) looking at snow-covered palm trees in Greece. Both are male.",
        },
    ],
}


def main():
    root = Path(__file__).resolve().parents[2]
    load_env_file(root / ".env")
    api_key = os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("VERTEX_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found")
        return

    out_dir = root / "public" / "images" / "nce1" / L51_FIX["lesson"]
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"🔥 FORCE FIXING GENDER FOR {L51_FIX['lesson']}...")
    for item in L51_FIX["items"]:
        out_path = out_dir / f"{item['id']}.png"
        print(f"  -> {item['id']} (FORCE OVERWRITE)")
        prompt = (
            STYLE
            + L51_FIX["chars"]
            + L51_FIX["scene"]
            + item["desc"]
            + " High character consistency. TWO MEN ONLY. NO WOMEN."
        )

        img = gemini_generate_image(api_key, model, prompt)
        if img:
            out_path.write_bytes(img)
            print(f"  ✅ Saved {item['id']}")
            time.sleep(5)
        else:
            print(f"  ❌ Failed {item['id']}")


if __name__ == "__main__":
    main()
