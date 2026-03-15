#!/usr/bin/env python3
import os, base64, json, time
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
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
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

BATCH_6 = [
    {
        "lesson": "l93",
        "chars": "Nigel: Young man. Ian: His friend. New Neighbour: Young woman with blonde hair. ",
        "scene": "Garden of their new house. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Nigel and Ian are working in their garden. Nigel is mowing the lawn. A new neighbor is waving from the fence.",
            },
            {
                "id": "neighbour_talk",
                "desc": "Ian is talking to the new neighbor over the garden fence. She is holding a watering can.",
            },
            {
                "id": "tea_invite",
                "desc": "Nigel and Ian having tea in the garden with the new neighbor. They are all laughing.",
            },
        ],
    },
    {
        "lesson": "l95",
        "chars": "George: Young man. Ken: His friend. Station Master: Man in uniform with a cap. ",
        "scene": "A train station platform. ",
        "items": [
            {
                "id": "scene1",
                "desc": "George and Ken are standing on a train station platform, looking at their tickets. The train is arriving.",
            },
            {
                "id": "station_master",
                "desc": "The Station Master is checking George's ticket. He looks professional.",
            },
            {
                "id": "boarding",
                "desc": "George and Ken boarding the vintage green train. They are waving to the station master.",
            },
        ],
    },
    {
        "lesson": "l97",
        "chars": "Mr. Hall: Man in 40s. Customs Officer: Man in uniform. ",
        "scene": "Airport customs area. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mr. Hall is at the customs counter with a small blue suitcase. The Customs Officer is looking at it.",
            },
            {
                "id": "opening_case",
                "desc": "Mr. Hall is opening the small blue case. Inside are some clothes and a small gift box.",
            },
            {
                "id": "cleared",
                "desc": "The Customs Officer is marking the case with chalk and nodding. Mr. Hall looks relieved.",
            },
        ],
    },
    {
        "lesson": "l99",
        "chars": "Andy: Young boy (8yo). Lucy: Young girl (6yo). ",
        "scene": "A garden with a fruit tree. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Andy is climbing a pear tree in the garden. Lucy is standing below, looking up.",
            },
            {
                "id": "falling",
                "desc": "Andy has slipped and is holding onto a branch, looking scared. Lucy is shouting for help.",
            },
            {
                "id": "safe_down",
                "desc": "Andy is back on the ground, holding his knee. Lucy is helping him walk back to the house.",
            },
        ],
    },
    {
        "lesson": "l101",
        "chars": "Mrs. Williams: Young mother. Jimmy: Young boy (now on holiday). ",
        "scene": "A living room and a beach. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mrs. Williams is reading a colorful postcard in her living room. She looks happy.",
            },
            {
                "id": "beach_scene",
                "desc": "Flashback or picture: Jimmy is on a sunny beach, building a sandcastle. The sea is blue.",
            },
            {
                "id": "writing_back",
                "desc": "Mrs. Williams is sitting at a desk, writing a letter back to Jimmy. A cup of tea is nearby.",
            },
        ],
    },
    {
        "lesson": "l103",
        "chars": "Gary: Young man. Richard: His friend. ",
        "scene": "A school corridor or classroom. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Gary and Richard are standing in a school corridor, looking at a notice board with exam results.",
            },
            {
                "id": "talking_test",
                "desc": "Gary is talking excitedly to Richard about his French test. Richard looks impressed.",
            },
            {
                "id": "studying",
                "desc": "Gary and Richard sitting at a wooden desk, sharing a French textbook. They are focused.",
            },
        ],
    },
    {
        "lesson": "l105",
        "chars": "The Boss: Middle-aged man. Sandra: Young woman (secretary). ",
        "scene": "A professional office with a typewriter. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Boss is looking at a typed letter, pointing out a mistake. Sandra looks apologetic.",
            },
            {
                "id": "typing_again",
                "desc": "Sandra is typing busily at her mechanical typewriter, trying to be careful.",
            },
            {
                "id": "final_check",
                "desc": "The Boss is reading the new letter and nodding with approval. Sandra looks relieved.",
            },
        ],
    },
    {
        "lesson": "l107",
        "chars": "Lady: Elegant woman. Shop Assistant: Young woman. ",
        "scene": "A dress shop. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Lady is trying on a blue dress in front of a mirror. It looks much too small for her.",
            },
            {
                "id": "assistant_brings_large",
                "desc": "The Shop Assistant is bringing a larger size of the same blue dress. The Lady looks hopeful.",
            },
            {
                "id": "happy_customer",
                "desc": "The Lady is now wearing the larger dress, which fits perfectly. She is smiling at the assistant.",
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
        return

    for task in BATCH_6:
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
                + " High consistency. Studio Ghibli style."
            )
            img = gemini_generate_image(api_key, model, prompt)
            if img:
                out_path.write_bytes(img)
                time.sleep(3)


if __name__ == "__main__":
    main()
