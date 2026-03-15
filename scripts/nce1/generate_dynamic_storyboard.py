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
        "lesson": "l37",
        "chars": "George: A man in his 30s, dark hair, work apron over white shirt. Dan: His friend, blonde hair, blue sweater. ",
        "scene": "Workshop with tools and wood. Strictly NO trains. ",
        "items": [
            {
                "id": "scene1",
                "desc": "George is at a workbench sawing a wooden plank. Dan stands nearby, watching.",
            },
            {
                "id": "pointing_wood",
                "desc": "George is pointing at a stack of wood planks, talking to Dan about his project.",
            },
            {
                "id": "hammer",
                "desc": "Dan is handing a heavy metal hammer to George. A bookcase frame is visible.",
            },
            {
                "id": "painting_start",
                "desc": "George is opening a can of bright pink paint. Dan looks surprised.",
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
        "scene": "A sunny living room with a shelf. NO trains. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Penny is holding a delicate blue ceramic vase. Sam is reaching out to help her.",
            },
            {
                "id": "handing_vase",
                "desc": "Penny carefully hands the blue vase to Sam. She looks worried and is giving him a warning.",
            },
            {
                "id": "vase_shelf",
                "desc": "Sam is carefully placing the blue vase on a high wooden shelf. Penny watches with concern.",
            },
            {
                "id": "successful_placement",
                "desc": "Sam has placed the vase on the shelf and is stepping back. Penny looks relieved.",
            },
        ],
    },
    {
        "lesson": "l41",
        "chars": "Penny: Auburn hair, green dress. Sam: Brown hair, beige cardigan. ",
        "scene": "A dining room with a chair and table. NO trains. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Penny enters with a heavy brown paper shopping bag. Sam is helping her put it on a chair.",
            },
            {
                "id": "bag_on_chair",
                "desc": "Penny is sitting on the chair next to the heavy bag. Sam is looking into the bag.",
            },
            {
                "id": "cheese_bread",
                "desc": "Penny is taking out a piece of cheese and a loaf of bread, placing them on the table.",
            },
            {
                "id": "soap_milk",
                "desc": "Penny is taking out a bar of soap and a bottle of milk from the bag.",
            },
            {
                "id": "bag_contents",
                "desc": "The table is full of groceries. Sam is holding a tin of tobacco labeled 'Tobacco' and looking pleased.",
            },
        ],
    },
    {
        "lesson": "l43",
        "chars": "Penny: Auburn hair, green dress. Sam: Brown hair, beige cardigan. ",
        "scene": "A cozy 1970s kitchen. NO trains. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Sam is in the kitchen looking confused. Penny is at the door, asking him to make tea.",
            },
            {
                "id": "checking_kettle",
                "desc": "Sam is looking into a silver kettle on the stove to see if there is any water.",
            },
            {
                "id": "kitchen_search",
                "desc": "Sam is looking behind a large porcelain teapot on the counter, searching for tea.",
            },
            {
                "id": "finding_cups",
                "desc": "Sam is opening a kitchen cupboard and finding two white tea cups.",
            },
            {
                "id": "kettle_boiling",
                "desc": "The silver kettle on the stove is whistling with steam. Penny is urging Sam to hurry up.",
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
                "id": "handing_letter",
                "desc": "The Boss hands the handwritten letter to Bob. Bob is looking at it curiously.",
            },
            {
                "id": "pamela_office",
                "desc": "Bob hands the letter to Pamela in her office. She is looking at it with a confused expression.",
            },
            {
                "id": "terrible_handwriting",
                "desc": "Close-up of the letter in Pamela's hands. The handwriting is messy scribbles. Pamela looks frustrated.",
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
                "id": "ann_coffee",
                "desc": "Ann is holding her cup of coffee, smiling at Christine. A plate of biscuits is on the table.",
            },
            {
                "id": "sugar_no_milk",
                "desc": "Close-up of coffee. Ann adds sugar with a spoon. No milk jug is present.",
            },
            {
                "id": "biscuits",
                "desc": "Ann is taking a round biscuit from the plate, happily talking to Christine.",
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
                "desc": "Mrs. Bird is at the counter. The Butcher shows her a large slab of red beef.",
            },
            {
                "id": "showing_lamb",
                "desc": "The Butcher is showing a leg of lamb to Mrs. Bird. She is shaking her head, preferring beef.",
            },
            {
                "id": "steak_mince",
                "desc": "The Butcher is weighing a piece of steak and some mince meat. Mrs. Bird is nodding.",
            },
            {
                "id": "showing_chicken",
                "desc": "The Butcher points to some chickens hanging in the window. Mrs. Bird declines with a smile.",
            },
        ],
    },
    {
        "lesson": "l51",
        "chars": "Dimitri: Young Greek man, dark hair. Man Traveler: Young man with a camera and a backpack. ",
        "scene": "A terrace in Greece overlooking the sea. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Dimitri and the Man Traveler look at the Aegean sea with white buildings. Bright sunlight.",
            },
            {
                "id": "spring_windy",
                "desc": "Greek landscape in spring. Trees are blowing hard in the wind. Two men are standing outside.",
            },
            {
                "id": "summer_hot",
                "desc": "A very hot summer day in Greece. Dimitri and the traveler are wiping sweat from their brows.",
            },
            {
                "id": "autumn_warm",
                "desc": "A beautiful autumn day in Greece. The two men are walking through an olive grove.",
            },
            {
                "id": "winter_snow",
                "desc": "Rare snow in Greece. Dimitri and the traveler looking at a village with white roofs and palm trees covered in light snow.",
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
                "desc": "Hans and Jim are studying a large map of Great Britain on the wall. They are pointing to the North.",
            },
            {
                "id": "north_cold",
                "desc": "Image of Northern England: A cold, snowy landscape with grey skies.",
            },
            {
                "id": "east_windy",
                "desc": "Image of Eastern England: A windy coast with waves crashing and trees leaning.",
            },
            {
                "id": "west_wet",
                "desc": "Image of Western England: A rainy city street with people carrying umbrellas.",
            },
            {
                "id": "south_warm",
                "desc": "Image of Southern England: A warm, sunny garden with blooming flowers.",
            },
        ],
    },
    {
        "lesson": "l55",
        "chars": "Mrs. Sawyer: A young woman in her early 30s, blonde hair in a neat bun, wearing a white blouse and a green apron. Mr. Sawyer: A man in his 30s, dark hair, grey suit. Children: A young boy and a young girl in school uniforms. ",
        "scene": "A house at 87 King Street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Morning: Mr. Sawyer getting into his car. The young children are walking to school. Mrs. Sawyer (young, early 30s) waves from the door.",
            },
            {
                "id": "housework",
                "desc": "Mrs. Sawyer (young, early 30s) is inside the house, busily vacuuming the living room.",
            },
            {
                "id": "lunch_noon",
                "desc": "Mrs. Sawyer (young, early 30s) is sitting at the kitchen table, eating her lunch alone at noon.",
            },
            {
                "id": "housework_friends",
                "desc": "Afternoon: Mrs. Sawyer (young, early 30s) is having tea with two other young female friends in her living room. They are laughing.",
            },
            {
                "id": "evening_tv",
                "desc": "Evening: The young children doing homework. Mr. and Mrs. Sawyer (young, early 30s) are on the sofa watching a small vintage TV.",
            },
        ],
    },
    {
        "lesson": "l57",
        "chars": "Mrs. Sawyer: A young woman in her early 30s, blonde hair in a neat bun, wearing a white blouse and a yellow floral dress. Mr. Sawyer: A man in his 30s, dark hair, casual shirt. Children: A young boy and a young girl. ",
        "scene": "House and garden. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Morning: The two young children are walking to school on a sidewalk. It is an unusual day because they are walking instead of going by car. They look energetic.",
            },
            {
                "id": "mrs_sawyer_shops",
                "desc": "Morning: Mrs. Sawyer (young, early 30s) is walking down a busy high street with many shops, carrying several shopping bags. She looks cheerful.",
            },
            {
                "id": "tea_garden",
                "desc": "Afternoon: Mrs. Sawyer (young, early 30s) is relaxing at a wooden table in her sunny green garden, enjoying a cup of tea. Very peaceful atmosphere.",
            },
            {
                "id": "children_playing",
                "desc": "Evening: The two young children are playing together happily on the green grass of the garden near a large tree.",
            },
            {
                "id": "mr_sawyer_book",
                "desc": "Night: Mr. Sawyer (man in his 30s) is sitting in a comfortable armchair indoors, deeply engrossed in a thick red book. He looks very focused.",
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
                "desc": "The Lady is at the shop counter, pointing to some large envelopes. The Shopkeeper is reaching for them.",
            },
            {
                "id": "writing_paper",
                "desc": "The Shopkeeper shows the Lady a large pad of writing paper. She looks at it.",
            },
            {
                "id": "buying_glue",
                "desc": "The Shopkeeper is placing a bottle of glue on the counter for the Lady.",
            },
            {
                "id": "no_chalk",
                "desc": "The Shopkeeper shows a small box of chalk. The Lady shakes her head 'no', declining it.",
            },
            {
                "id": "forgetting_change",
                "desc": "The Lady is leaving the shop. Her coins (change) are left on the wooden counter. The Shopkeeper calls out to her.",
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

            # Check if updated very recently (within 1 hour)
            if out_path.exists():
                mtime = out_path.stat().st_mtime
                if time.time() - mtime < 3600:
                    # Specific exception for L51 to force regenerate
                    if task["lesson"] not in ["l51"]:
                        print(f"  -> {item['id']} (Recently updated, skipping)")
                        continue

            print(f"  -> {item['id']} (Generating...)")
            prompt = (
                STYLE
                + task["chars"]
                + task["scene"]
                + item["desc"]
                + " Maintain high character and background consistency. Studio Ghibli watercolor style."
            )

            # Retry mechanism
            img = None
            for attempt in range(3):
                img = gemini_generate_image(api_key, model, prompt)
                if img:
                    break
                print(f"    !! Attempt {attempt + 1} failed, retrying...")
                time.sleep(5)

            if img:
                out_path.write_bytes(img)
                time.sleep(3)
            else:
                print(f"    !! PERMANENT FAILURE for {item['id']}")


if __name__ == "__main__":
    main()
