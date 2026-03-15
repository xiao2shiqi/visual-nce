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

BATCH_5 = [
    {
        "lesson": "l77",
        "chars": "Nurse: Young woman in uniform. Patient (Mr. Crookes): Middle-aged man with a swollen cheek. Dentist: Man in a white coat. ",
        "scene": "A dentist's waiting room and surgery. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mr. Crookes sitting in a waiting room, holding his cheek in pain. The Nurse is talking to him.",
            },
            {
                "id": "dentist_surgery",
                "desc": "Mr. Crookes in the dentist's chair. The Dentist is looking at his teeth with a small mirror.",
            },
            {
                "id": "extraction",
                "desc": "The Dentist holding up a tooth with pliers. Mr. Crookes looks relieved but tired.",
            },
        ],
    },
    {
        "lesson": "l79",
        "chars": "Carol: Young woman with blonde hair. Tom: Her husband, dark hair. ",
        "scene": "A kitchen and supermarket. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Carol is writing a shopping list at the kitchen table. Tom is looking over her shoulder.",
            },
            {
                "id": "supermarket",
                "desc": "Carol pushing a trolley in a bright supermarket, looking for groceries on the shelves.",
            },
            {
                "id": "unpacking",
                "desc": "Carol and Tom unpacking many bags of groceries in the kitchen. They have a lot of food.",
            },
        ],
    },
    {
        "lesson": "l81",
        "chars": "Carol: Young woman. Tom: Young man. ",
        "scene": "A cozy dining room. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Carol is bringing a large platter of roast beef to the table. Tom is sitting down, ready to eat.",
            },
            {
                "id": "eating_beef",
                "desc": "Tom and Carol enjoying their meal of roast beef and potatoes. Steam is rising from the plates.",
            },
            {
                "id": "dessert",
                "desc": "Carol is serving a bowl of fruit for dessert. Both look very satisfied.",
            },
        ],
    },
    {
        "lesson": "l83",
        "chars": "Sam: Man in 30s. Penny: Woman in 30s. ",
        "scene": "A living room with suitcases. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Sam and Penny are packing two large suitcases on the living room floor. Clothes are everywhere.",
            },
            {
                "id": "locked_suitcases",
                "desc": "Sam is struggling to close a very full suitcase. Penny is sitting on it to help.",
            },
            {
                "id": "taxi_arrives",
                "desc": "Sam and Penny standing outside their house with luggage, waving at a taxi arriving.",
            },
        ],
    },
    {
        "lesson": "l85",
        "chars": "Narrator/Travelers. ",
        "scene": "Springtime in Paris. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Wide shot of the Eiffel Tower with pink cherry blossoms in the foreground. People are walking by the river Seine.",
            },
            {
                "id": "sidewalk_cafe",
                "desc": "People sitting at a charming Parisian sidewalk cafe, drinking coffee. Sunny spring weather.",
            },
            {
                "id": "notre_dame",
                "desc": "The Notre Dame cathedral under a clear blue sky. A few clouds and birds flying.",
            },
        ],
    },
    {
        "lesson": "l87",
        "chars": "Mr. Wood: Man in a suit. Policeman: Man in uniform. ",
        "scene": "A road with two crashed cars. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Two vintage cars have collided on a narrow road. Mr. Wood is standing by his car, looking upset.",
            },
            {
                "id": "policeman_notes",
                "desc": "A Policeman is writing in a notebook, talking to Mr. Wood near the crashed cars.",
            },
            {
                "id": "tow_truck",
                "desc": "A tow truck is arriving to take away one of the damaged cars. A crowd has gathered.",
            },
        ],
    },
    {
        "lesson": "l89",
        "chars": "Nigel: Young man. Ian: His friend. ",
        "scene": "Outside an old house. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Nigel and Ian are standing in front of a small, charming old house with a 'FOR SALE' sign in the garden.",
            },
            {
                "id": "garden_view",
                "desc": "Nigel pointing to the overgrown but beautiful garden of the house. Ian looks skeptical.",
            },
            {
                "id": "inside_house",
                "desc": "Nigel and Ian inside an empty, dusty room of the house. Sunlight through the windows shows the dust motes.",
            },
        ],
    },
    {
        "lesson": "l91",
        "chars": "Ian: Man in 30s. Catherine: Woman in 30s. ",
        "scene": "A hospital ward. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Ian is lying in a hospital bed with his leg in a cast, suspended by wires. He looks bored.",
            },
            {
                "id": "catherine_visits",
                "desc": "Catherine is visiting Ian, bringing him some magazines and flowers. She is sitting by the bed.",
            },
            {
                "id": "ian_reading",
                "desc": "Ian is alone in the ward, happily reading one of the magazines Catherine brought.",
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

    for task in BATCH_5:
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
