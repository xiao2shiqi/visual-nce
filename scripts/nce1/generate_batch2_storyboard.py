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

TASKS = [
    {
        "lesson": "l45",
        "chars": "Character Boss: A middle-aged man with grey hair and a dark suit. Character Bob: A young man in a white shirt and tie. Character Pamela: A young woman with blonde hair in a blue dress. ",
        "scene": "Location: A professional 1970s office. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Boss is standing in his office, holding a handwritten letter and calling Bob over. Bob is entering the office.",
            },
            {
                "id": "pamela_office",
                "desc": "Bob is handing the handwritten letter to Pamela in her separate office. Pamela looks puzzled as she looks at the paper.",
            },
            {
                "id": "terrible_handwriting",
                "desc": "Close-up of the letter in Pamela's hands. The handwriting is extremely messy and illegible scribbles. Pamela has a look of frustration.",
            },
        ],
    },
    {
        "lesson": "l47",
        "chars": "Character Christine: A woman with brown hair in a red cardigan. Character Ann: A woman with blonde hair in a yellow blouse. ",
        "scene": "Location: A cozy living room with a coffee table. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Christine is pouring coffee into a white cup for Ann. They are sitting on a sofa.",
            },
            {
                "id": "sugar_no_milk",
                "desc": "Close-up of the coffee table. Ann is adding a spoonful of sugar to her black coffee. There is no milk nearby. A plate of biscuits is on the table.",
            },
            {
                "id": "biscuits",
                "desc": "Ann is taking a round biscuit from the plate, smiling at Christine.",
            },
        ],
    },
    {
        "lesson": "l49",
        "chars": "Character Butcher: A friendly man with a striped apron. Character Mrs. Bird: A middle-aged woman with a floral hat and a coat. ",
        "scene": "Location: A traditional British butcher shop with joints of meat hanging in the window. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mrs. Bird is at the butcher's counter. The Butcher is showing her a large piece of beef. Several chickens are hanging in the background.",
            },
            {
                "id": "steak_mince",
                "desc": "The Butcher is wrapping a thick steak and a package of mince meat for Mrs. Bird. They are talking and smiling.",
            },
        ],
    },
    {
        "lesson": "l51",
        "chars": "Character Man (Dimitri): A young Greek man with dark hair. Character Woman (Traveler): A young woman with a camera. ",
        "scene": "Location: A beautiful Mediterranean setting with white buildings and blue sea (Greece). ",
        "items": [
            {
                "id": "scene1",
                "desc": "Dimitri and the Woman are standing on a terrace overlooking the beautiful blue Aegean Sea and white-domed churches of Greece. The sun is shining brightly.",
            },
            {
                "id": "spring_windy",
                "desc": "A scenic shot of a Greek landscape in spring. Wildflowers are blooming, but the trees are leaning in a strong wind.",
            },
            {
                "id": "winter_snow",
                "desc": "A rare and beautiful shot of a Greek village with a light dusting of white snow on the rooftops and palm trees. Soft winter light.",
            },
        ],
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

    for task in TASKS:
        out_dir = root / "public" / "images" / "nce1" / task["lesson"]
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"🎨 Generating {task['lesson']}...")
        for item in task["items"]:
            out_path = out_dir / f"{item['id']}.png"
            if out_path.exists():
                continue
            print(f"  -> {item['id']}")
            prompt = (
                STYLE
                + task["chars"]
                + task["scene"]
                + item["desc"]
                + " Studio Ghibli style, high consistency."
            )
            img = gemini_generate_image(api_key, model, prompt)
            if img:
                out_path.write_bytes(img)
                time.sleep(2)


if __name__ == "__main__":
    main()
