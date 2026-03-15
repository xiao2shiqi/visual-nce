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
        "lesson": "l53",
        "chars": "Character Dimitri: A young Greek man with dark hair. Character Woman (Traveler): A young woman with a camera. ",
        "scene": "Location: A cozy library or study with a map of Great Britain on the wall. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Dimitri and the Woman are looking at a large map of England. Dimitri is pointing to the North. Outside the window, the sky is overcast.",
            },
            {
                "id": "north_east",
                "desc": "Split screen or montage: On the left, a snowy cold landscape in Northern England. On the right, a windy coastal scene in Eastern England with trees blowing.",
            },
            {
                "id": "west_south",
                "desc": "Split screen or montage: On the left, a rainy wet street in Western England. On the right, a warm sunny garden in Southern England.",
            },
        ],
    },
    {
        "lesson": "l55",
        "chars": "Character Mr. Sawyer: A man in his 30s with a dark suit. Character Mrs. Sawyer: A woman with blonde hair in an apron. Characters Children: A boy and a girl in school uniforms. ",
        "scene": "Location: A tidy British house at 87 King Street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Wide shot of the Sawyer family house on King Street. Mr. Sawyer is getting into his car, and the children are waving goodbye as they leave for school.",
            },
            {
                "id": "housework_friends",
                "desc": "Mrs. Sawyer is happily doing housework in the morning, and later in the afternoon, she is sitting with two female friends, drinking tea and chatting in the living room.",
            },
            {
                "id": "evening_tv",
                "desc": "Evening scene: The children are doing homework at the dining table. Mr. Sawyer and Mrs. Sawyer are sitting together on the sofa, watching a small vintage television.",
            },
        ],
    },
    {
        "lesson": "l57",
        "chars": "Character Mr. Sawyer: A man in his 30s. Character Mrs. Sawyer: A woman with blonde hair. Characters Children: A boy and a girl. ",
        "scene": "Location: The Sawyer house and garden. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The children are walking together along a sidewalk, carrying their schoolbags. They are going to school on foot today instead of by car.",
            },
            {
                "id": "mrs_sawyer_shops",
                "desc": "Mrs. Sawyer is walking down a busy high street, carrying several shopping bags. She is going to the shops this morning.",
            },
            {
                "id": "tea_garden",
                "desc": "Mrs. Sawyer is sitting at a small table in her lush green garden, enjoying a cup of tea under the afternoon sun.",
            },
            {
                "id": "children_playing",
                "desc": "The children are playing tag on the green grass of the garden in the evening light. They are not doing their homework yet.",
            },
            {
                "id": "mr_sawyer_book",
                "desc": "Mr. Sawyer is sitting in a comfortable armchair, deeply engrossed in a thick red book. He is not reading his usual newspaper tonight.",
            },
        ],
    },
    {
        "lesson": "l59",
        "chars": "Character Shopkeeper: A man with a mustache and a brown coat. Character Lady: A woman with a fancy hat and a handbag. ",
        "scene": "Location: A cluttered stationery shop with shelves of paper, glue, and pens. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Lady is at the shop counter, pointing to some large envelopes. The Shopkeeper is reaching for them on a shelf.",
            },
            {
                "id": "buying_glue",
                "desc": "The Lady is looking at a small bottle of glue and a large pad of writing paper on the counter. The Shopkeeper is counting the items.",
            },
            {
                "id": "no_chalk",
                "desc": "The Shopkeeper is showing the Lady a small box of chalk, looking apologetic. The Lady is shaking her head, declining it.",
            },
            {
                "id": "forgetting_change",
                "desc": "The Lady is walking towards the shop door, having forgotten her coins (change) which are still lying on the wooden counter. The Shopkeeper is calling out to her.",
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
