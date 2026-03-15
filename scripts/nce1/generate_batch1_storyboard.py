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

# Batch 1: 37, 39, 41, 43
TASKS = [
    {
        "lesson": "l37",
        "chars": "Character George: A man in his 30s with short dark hair, wearing a work apron over a white shirt. Character Dan: His male friend, wearing a blue sweater. ",
        "scene": "Location: A home workshop/garage with wood planks and tools. ",
        "items": [
            {
                "id": "scene1",
                "desc": "George is working hard at a wooden workbench, sawing a piece of wood. Dan is standing nearby watching him.",
            },
            {
                "id": "hammer",
                "desc": "Dan is handing a large heavy hammer to George. There is another smaller hammer on the bench.",
            },
            {
                "id": "painting_pink",
                "desc": "George is holding a paintbrush and a can of bright pink paint, looking at the half-finished bookcase with a smile.",
            },
        ],
    },
    {
        "id": "batch_penny_sam",
        "chars": "Character Penny: A young woman with auburn hair, wearing a light green dress. Character Sam: A man with short brown hair, wearing a beige cardigan and trousers. ",
        "lessons": [
            {
                "lesson": "l39",
                "scene": "Location: A sunny living room with a large window and a wooden shelf. ",
                "items": [
                    {
                        "id": "scene1",
                        "desc": "Penny is holding a beautiful blue ceramic vase. Sam is reaching out his hands, offering to help. They are in the living room.",
                    },
                    {
                        "id": "vase_shelf",
                        "desc": "Sam is carefully placing the blue vase on a high wooden shelf. Penny is watching anxiously, hands clasped. A vase of flowers is already on the table.",
                    },
                ],
            },
            {
                "lesson": "l41",
                "scene": "Location: A dining room with a wooden chair. ",
                "items": [
                    {
                        "id": "scene1",
                        "desc": "Penny is carrying a large, heavy brown shopping bag. Sam is pulling out a chair for her.",
                    },
                    {
                        "id": "bag_contents",
                        "desc": "The shopping bag is on the chair. Penny and Sam are taking items out: a loaf of bread, a bottle of milk, and a tin of tobacco are visible on the table.",
                    },
                ],
            },
            {
                "lesson": "l43",
                "scene": "Location: A cozy 1970s kitchen. ",
                "items": [
                    {
                        "id": "scene1",
                        "desc": "Sam is in the kitchen, looking a bit confused. Penny is standing at the door, asking him to make tea.",
                    },
                    {
                        "id": "kitchen_search",
                        "desc": "Sam is looking behind a large teapot on the counter, searching for the tea tin. A silver kettle is on the stove.",
                    },
                    {
                        "id": "kettle_boiling",
                        "desc": "The silver kettle on the stove is whistling and steam is coming out. Sam is holding two white cups he found in the cupboard.",
                    },
                ],
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
        if "lessons" in task:
            for sub in task["lessons"]:
                process_lesson(
                    sub["lesson"],
                    task["chars"],
                    sub["scene"],
                    sub["items"],
                    root,
                    api_key,
                    model,
                )
        else:
            process_lesson(
                task["lesson"],
                task["chars"],
                task["scene"],
                task["items"],
                root,
                api_key,
                model,
            )


def process_lesson(lesson, chars, scene, items, root, api_key, model):
    out_dir = root / "public" / "images" / "nce1" / lesson
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"🎨 Generating {lesson}...")
    for item in items:
        out_path = out_dir / f"{item['id']}.png"
        if out_path.exists():
            continue
        print(f"  -> {item['id']}")
        prompt = (
            STYLE
            + chars
            + scene
            + item["desc"]
            + " Studio Ghibli style, high consistency."
        )
        img = gemini_generate_image(api_key, model, prompt)
        if img:
            out_path.write_bytes(img)
            time.sleep(2)


if __name__ == "__main__":
    main()
