#!/usr/bin/env python3
import os, base64, json, time, sys
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

BATCH_4 = [
    {
        "lesson": "l61",
        "chars": "Mrs. Williams: Young mother, brown hair. Jimmy: Young boy (8yo), in bed. Doctor: Middle-aged man with glasses and a stethoscope. ",
        "scene": "A cozy bedroom. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jimmy lying in bed looking ill. Mrs. Williams is sitting on the edge of the bed, feeling his forehead.",
            },
            {
                "id": "doctor_arrives",
                "desc": "The Doctor is standing by the bed, examining Jimmy with a thermometer. Mrs. Williams is watching anxiously.",
            },
            {
                "id": "medicine",
                "desc": "The Doctor is handing a small bottle of medicine to Mrs. Williams. Jimmy is sitting up slightly.",
            },
        ],
    },
    {
        "lesson": "l63",
        "chars": "Mrs. Williams: Young mother. Jimmy: Young boy (8yo). Doctor: Middle-aged man. ",
        "scene": "A cozy bedroom. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jimmy is sitting up in bed, looking much better and smiling. The Doctor is packing his bag.",
            },
            {
                "id": "jimmy_up",
                "desc": "Jimmy is getting out of bed, putting on his slippers. Mrs. Williams is holding a glass of water.",
            },
            {
                "id": "doctor_leaving",
                "desc": "The Doctor is at the door, waving goodbye. Mrs. Williams and Jimmy are waving back.",
            },
        ],
    },
    {
        "lesson": "l65",
        "chars": "Jill: Young woman, blonde hair. Jack: Young man, brown hair. ",
        "scene": "A modern 1970s living room. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jill is sitting on a sofa, looking at a magazine. Jack is standing near her, pointing at something.",
            },
            {
                "id": "key_exchange",
                "desc": "Jack is handing a silver door key to Jill. She looks a bit surprised.",
            },
            {
                "id": "jill_smiling",
                "desc": "Jill is standing by the door, holding the key and smiling confidently at Jack.",
            },
        ],
    },
    {
        "lesson": "l67",
        "chars": "Mr. Johnson: Man in 40s. Mrs. Johnson: Woman in 40s. Children: Boy and girl. ",
        "scene": "Countryside and garden. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Johnson family is standing in their beautiful garden on a sunny Saturday afternoon. They look happy.",
            },
            {
                "id": "mowing_lawn",
                "desc": "Mr. Johnson is pushing a manual lawn mower on the green grass. The children are playing nearby.",
            },
            {
                "id": "tea_time",
                "desc": "The whole family is sitting around a wooden table in the garden, having tea and cakes.",
            },
        ],
    },
    {
        "lesson": "l69",
        "chars": "Race cars, crowds of people. ",
        "scene": "A 1970s race track. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Wide shot of a race track. Several colorful vintage race cars are at the starting line. Crowds are waving flags.",
            },
            {
                "id": "cars_speeding",
                "desc": "Action shot of the race cars speeding around a corner, kicking up dust. The red car is in the lead.",
            },
            {
                "id": "finish_line",
                "desc": "The red race car crossing the finish line. The driver is waving a hand in victory.",
            },
        ],
    },
    {
        "lesson": "l71",
        "chars": "Jane: Young woman, dark hair. Ron: Young man, messy hair, looking a bit lazy. ",
        "scene": "A small apartment. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jane is standing in the living room, looking annoyed. Ron is slumped in an armchair, reading a comic.",
            },
            {
                "id": "jane_pointing",
                "desc": "Jane is pointing at a pile of dirty dishes in the sink. Ron is looking up with a sheepish grin.",
            },
            {
                "id": "ron_working",
                "desc": "Ron is finally standing up and starting to wash the dishes. Jane is watching him with her arms crossed.",
            },
        ],
    },
    {
        "lesson": "l73",
        "chars": "Stranger: Man in a trench coat and hat. Local Man: Man in a sweater. ",
        "scene": "A busy 1970s London street corner. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Stranger is holding a map and asking the Local Man for directions on a street corner. Red buses in background.",
            },
            {
                "id": "pointing_way",
                "desc": "The Local Man is pointing down a long street (King Street). The Stranger is nodding and looking that way.",
            },
            {
                "id": "walking_away",
                "desc": "The Stranger is walking away towards King Street, waving a hand in thanks. The Local Man is walking in the opposite direction.",
            },
        ],
    },
    {
        "lesson": "l75",
        "chars": "Lady: Elegant woman in a fur-trimmed coat. Shop Assistant: Young woman in a uniform. ",
        "scene": "A high-end shoe shop. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Lady is sitting on a velvet chair in a shoe shop. The Shop Assistant is showing her a pair of black high heels.",
            },
            {
                "id": "trying_shoes",
                "desc": "The Lady is trying on one of the black shoes. She looks uncomfortable and is pinching her toe.",
            },
            {
                "id": "choosing_another",
                "desc": "The Shop Assistant is bringing a different, more comfortable pair of flat shoes. The Lady looks interested.",
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

    for task in BATCH_4:
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
