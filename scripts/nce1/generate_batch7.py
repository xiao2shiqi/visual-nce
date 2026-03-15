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

BATCH_7 = [
    {
        "lesson": "l109",
        "chars": "Charlotte: Young woman. Jane: Her friend. ",
        "scene": "A cozy coffee shop. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Charlotte and Jane are sitting at a small table in a coffee shop, drinking coffee and talking.",
            },
            {
                "id": "coffee_chat",
                "desc": "Charlotte is explaining a 'good idea' to Jane. She looks excited and is gesturing with her hands.",
            },
            {
                "id": "walking_out",
                "desc": "Charlotte and Jane walking out of the coffee shop into a sunny street, still talking and smiling.",
            },
        ],
    },
    {
        "lesson": "l111",
        "chars": "Mr. Saville: Man in 40s. Shop Assistant: Man in a suit. ",
        "scene": "A luxury car showroom. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mr. Saville is looking at a very expensive, shiny silver car in a showroom. The Shop Assistant is talking to him.",
            },
            {
                "id": "engine_view",
                "desc": "The Shop Assistant is showing Mr. Saville the engine of the expensive car. It looks very clean and powerful.",
            },
            {
                "id": "signing_papers",
                "desc": "Mr. Saville is sitting at a desk with the assistant, signing some papers. He looks very pleased with himself.",
            },
        ],
    },
    {
        "lesson": "l113",
        "chars": "Conductor: Man in a bus conductor uniform. Passenger (Mr. Scott): Man in 30s. ",
        "scene": "Inside a red double-decker bus. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Conductor is asking Mr. Scott for his fare. Mr. Scott is searching his pockets for 'small change'.",
            },
            {
                "id": "no_change",
                "desc": "Mr. Scott is showing the Conductor a large bank note. The Conductor is shaking his head, pointing to his coin bag.",
            },
            {
                "id": "change_found",
                "desc": "Mr. Scott finally finds some coins in a different pocket. The Conductor is handing him a ticket.",
            },
        ],
    },
    {
        "lesson": "l115",
        "chars": "Jim: Young man. Helen: Young woman. ",
        "scene": "A living room and front door. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jim and Helen are sitting in their living room. Helen is looking at the door, having heard a knock.",
            },
            {
                "id": "opening_door",
                "desc": "Jim is opening the wooden front door. It is dark outside. A neighbor is standing there.",
            },
            {
                "id": "neighbor_talk",
                "desc": "The Neighbor is returning a book to Jim at the door. Helen is watching from the sofa.",
            },
        ],
    },
    {
        "lesson": "l117",
        "chars": "Tommy: Young boy (5yo). Mother: Young woman. ",
        "scene": "A bright kitchen. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Tommy is sitting at the kitchen table, eating a bowl of cereal. His Mother is pouring milk for him.",
            },
            {
                "id": "messy_eating",
                "desc": "Tommy has spilled some milk on the table. He looks sheepish. His Mother is bringing a cloth to clean it.",
            },
            {
                "id": "finished_breakfast",
                "desc": "Tommy has finished his breakfast and is standing on his chair, reaching for a toy on the counter.",
            },
        ],
    },
    {
        "lesson": "l119",
        "chars": "Narrator/Characters in a story. ",
        "scene": "A forest or a dark road. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A man is walking alone down a dark, misty road at night. Tall trees are on both sides.",
            },
            {
                "id": "strange_noise",
                "desc": "The man has stopped and is looking back into the darkness, looking startled. He heard a strange noise.",
            },
            {
                "id": "mystery_solved",
                "desc": "A small dog runs out from the trees, wagging its tail. The man looks relieved and is laughing.",
            },
        ],
    },
    {
        "lesson": "l121",
        "chars": "Man in a Hat: Man with a distinctive large hat. Bystanders. ",
        "scene": "A busy city square. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A man wearing a very large, unusual hat is walking through a busy city square. People are turning to look at him.",
            },
            {
                "id": "pointing_crowd",
                "desc": "A group of children are pointing at the man in the hat and laughing. He is walking confidently.",
            },
            {
                "id": "close_up_hat",
                "desc": "Close-up of the unusual hat. It has a colorful feather and a strange shape. The man's face shows a slight smile.",
            },
        ],
    },
    {
        "lesson": "l123",
        "chars": "Traveler: Young man. Travel Agent: Woman in an office. ",
        "scene": "A travel agency office. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Traveler is sitting at a desk in a travel agency, looking at brochures of Australia. The Travel Agent is pointing at a map.",
            },
            {
                "id": "view_of_sydney",
                "desc": "Flashback or picture: The Sydney Opera House under a bright blue sky. A sailboat is in the harbor.",
            },
            {
                "id": "booking_trip",
                "desc": "The Traveler is handing his passport to the agent to book the trip. He looks very excited.",
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

    for task in BATCH_7:
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
