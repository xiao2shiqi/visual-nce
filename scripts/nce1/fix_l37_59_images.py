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


STYLE = "Studio Ghibli-inspired illustration style, vibrant watercolor textures, soft hand-drawn lines, nostalgic 1970s atmosphere, warm lighting. "

TASKS = [
    {
        "lesson": "l37",
        "chars": "George: A man in his 30s, dark hair, work apron over white shirt. Dan: His friend, blonde hair, blue sweater. ",
        "scene": "Workshop with tools and wood. ",
        "items": [
            {
                "id": "scene1",
                "desc": "George is at a workbench sawing a wooden plank. Dan stands nearby, watching. No trains, strictly a home workshop.",
            },
            {
                "id": "hammer",
                "desc": "Dan is handing a heavy metal hammer to George. A bookcase frame is visible.",
            },
            {
                "id": "painting_pink",
                "desc": "George is using a brush to paint a wooden bookcase bright pink. He looks happy.",
            },
        ],
    },
    {
        "lesson": "l39",
        "chars": "Penny: Young woman, auburn hair, green dress. Sam: Man, brown hair, beige cardigan. ",
        "scene": "A sunny living room with a shelf. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Penny is holding a delicate blue ceramic vase. Sam is reaching out to help her. No trains, just a room.",
            },
            {
                "id": "vase_shelf",
                "desc": "Sam is carefully placing the blue vase on a high wooden shelf. Penny looks worried.",
            },
        ],
    },
    {
        "lesson": "l41",
        "chars": "Penny: Auburn hair, green dress. Sam: Brown hair, beige cardigan. ",
        "scene": "A dining room with a chair. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Penny enters with a heavy brown paper shopping bag. Sam is helping her put it on a chair.",
            },
            {
                "id": "bag_contents",
                "desc": "Items on the table: a piece of cheese, a loaf of bread, a bar of soap, a bottle of milk, and a tin of tobacco labeled 'Tobacco'.",
            },
        ],
    },
    {
        "lesson": "l43",
        "chars": "Penny: Auburn hair, green dress. Sam: Brown hair, beige cardigan. ",
        "scene": "A cozy 1970s kitchen. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Sam is in the kitchen looking confused. Penny is at the door. No trains! Only kitchen cabinets and a stove.",
            },
            {
                "id": "kitchen_search",
                "desc": "Sam is looking behind a large porcelain teapot on the counter, searching for tea. A silver kettle is on the stove.",
            },
            {
                "id": "kettle_boiling",
                "desc": "The silver kettle on the stove is whistling with steam. Sam holds two white tea cups.",
            },
        ],
    },
    {
        "lesson": "l45",
        "chars": "The Boss: Middle-aged man, grey hair, dark suit, glasses. Bob: Young man, white shirt and tie. Pamela: Young woman, blonde hair, blue dress. ",
        "scene": "A professional office. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Boss is in his office, holding a handwritten letter, calling Bob. Bob is entering the room.",
            },
            {
                "id": "pamela_office",
                "desc": "Bob hands the letter to Pamela in her office. She is looking at it with a confused expression.",
            },
            {
                "id": "terrible_handwriting",
                "desc": "Close-up of the letter. The handwriting is messy scribbles. Pamela looks frustrated.",
            },
        ],
    },
    {
        "lesson": "l47",
        "chars": "Christine: Woman, brown hair, red cardigan. Ann: Woman, blonde hair, yellow blouse. ",
        "scene": "Cozy living room with coffee table. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Christine is pouring coffee from a pot into a cup for Ann. They are on a sofa.",
            },
            {
                "id": "sugar_no_milk",
                "desc": "Close-up of coffee. Ann adds sugar but there is no milk. A plate of biscuits is there.",
            },
            {
                "id": "biscuits",
                "desc": "Ann is happily eating a biscuit and talking to Christine.",
            },
        ],
    },
    {
        "lesson": "l49",
        "chars": "Butcher: Man, striped apron, friendly. Mrs. Bird: Woman, floral hat, brown coat. ",
        "scene": "A classic British butcher shop. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mrs. Bird is at the counter. The Butcher shows her a large slab of red beef. Meat hooks in background.",
            },
            {
                "id": "steak_mince",
                "desc": "The Butcher is weighing a piece of steak and some mince meat. Mrs. Bird is nodding.",
            },
        ],
    },
    {
        "lesson": "l51",
        "chars": "Dimitri: Young Greek man, dark hair. Woman Traveler: Young woman, camera, sun hat. ",
        "scene": "A terrace in Greece overlooking the sea. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Dimitri and the Woman look at the Aegean sea with white buildings. Bright sunlight.",
            },
            {
                "id": "spring_windy",
                "desc": "Greek landscape in spring. Trees are blowing hard in the wind. Wildflowers are visible.",
            },
            {
                "id": "winter_snow",
                "desc": "Rare snow in Greece. A village with white roofs and palm trees covered in light snow.",
            },
        ],
    },
    {
        "lesson": "l53",
        "chars": "Hans: Young man, blonde hair. Jim: Young man, dark hair. ",
        "scene": "A library with a map of England. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Hans and Jim are studying a map of Great Britain. They are pointing to different regions.",
            },
            {
                "id": "north_east",
                "desc": "Montage: On left, a rainy street in the West. On right, a sunny garden in the South of England.",
            },
            {
                "id": "west_south",
                "desc": "Montage: On left, cold snow in the North. On right, windy coast in the East of England.",
            },
        ],
    },
    {
        "lesson": "l55",
        "chars": "Mr. Sawyer: Man, dark suit. Mrs. Sawyer: Woman, blonde hair, apron. Children: Boy and girl in uniforms. ",
        "scene": "A house at 87 King Street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mr. Sawyer is getting into his car. The children are walking to school. Mrs. Sawyer waves from the door.",
            },
            {
                "id": "housework_friends",
                "desc": "Mrs. Sawyer is having tea with two friends in her living room. They are laughing.",
            },
            {
                "id": "evening_tv",
                "desc": "Evening: Children doing homework. Mr. and Mrs. Sawyer are watching a small vintage TV.",
            },
        ],
    },
    {
        "lesson": "l57",
        "chars": "The Sawyer Family (Mr. Sawyer, Mrs. Sawyer, two children). ",
        "scene": "House and garden. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The children are walking to school on a sidewalk. It is an unusual day because they are walking.",
            },
            {
                "id": "mrs_sawyer_shops",
                "desc": "Mrs. Sawyer is in a busy street with many shops, carrying bags.",
            },
            {
                "id": "tea_garden",
                "desc": "Mrs. Sawyer is relaxing in a sunny garden with a cup of tea. Very peaceful.",
            },
            {
                "id": "children_playing",
                "desc": "The children are playing outside in the garden near a large tree. No homework.",
            },
            {
                "id": "mr_sawyer_book",
                "desc": "Mr. Sawyer is reading an interesting red book in his armchair. No newspaper tonight.",
            },
        ],
    },
    {
        "lesson": "l59",
        "chars": "Shopkeeper: Man with mustache. Lady: Woman with elegant hat and pearls. ",
        "scene": "Stationery shop. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Lady asks for large envelopes. The Shopkeeper points to a shelf of paper and glue.",
            },
            {
                "id": "buying_glue",
                "desc": "The Shopkeeper places a bottle of glue and a pad of paper on the counter for the Lady.",
            },
            {
                "id": "no_chalk",
                "desc": "The Shopkeeper shows a small box of chalk. The Lady shakes her head 'no'.",
            },
            {
                "id": "forgetting_change",
                "desc": "The Lady is leaving the shop. Her coins (change) are left on the counter. The Shopkeeper calls out.",
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
        print(f"🎨 Processing {task['lesson']}...")
        for item in task["items"]:
            out_path = out_dir / f"{item['id']}.png"

            # Check if updated today (15 Mar 2026)
            if out_path.exists():
                mtime = time.localtime(out_path.stat().st_mtime)
                if mtime.tm_year == 2026 and mtime.tm_mon == 3 and mtime.tm_mday == 15:
                    print(f"  -> {item['id']} (Already updated today, skipping)")
                    continue

            print(f"  -> {item['id']} (Generating...)")
            prompt = (
                STYLE
                + task["chars"]
                + task["scene"]
                + item["desc"]
                + " Maintain high character and background consistency. Studio Ghibli watercolor style."
            )
            img = gemini_generate_image(api_key, model, prompt)
            if img:
                out_path.write_bytes(img)
                time.sleep(3)
            else:
                print(f"  !! Failed to generate {item['id']}")


if __name__ == "__main__":
    main()
