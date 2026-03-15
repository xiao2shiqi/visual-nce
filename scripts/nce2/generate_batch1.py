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

NCE2_BATCH_1 = [
    {
        "lesson": "l1",
        "chars": "Man: Young man. Woman: Young woman. Narrator. ",
        "scene": "Theatre. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Inside a dark theatre. The Narrator is sitting behind a young man and woman who are talking loudly.",
            },
            {
                "id": "angry_narrator",
                "desc": "The Narrator looking very angry at the couple.",
            },
            {
                "id": "turning_round",
                "desc": "The young man turns round and looks at the narrator with a rude expression.",
            },
        ],
    },
    {
        "lesson": "l2",
        "chars": "Aunt Lucy: Elderly woman. Narrator: Young man. ",
        "scene": "Bedroom. ",
        "items": [
            {"id": "scene1", "desc": "Narrator in bed, waking up at 1pm."},
            {"id": "aunt_lucy_phone", "desc": "Narrator on telephone to Aunt Lucy."},
            {
                "id": "breakfast_lunch",
                "desc": "Narrator sitting at table with breakfast while Aunt Lucy looks on, shocked.",
            },
        ],
    },
    {
        "lesson": "l3",
        "chars": "Narrator: Young man. ",
        "scene": "Italy. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator in sunny Italian square with many postcards.",
            },
            {"id": "writing_cards", "desc": "Narrator's hand writing a postcard."},
            {"id": "postcards_final", "desc": "Large stack of finished postcards."},
        ],
    },
    {
        "lesson": "l4",
        "chars": "Narrator: Young man. Friend: Young man. ",
        "scene": "Airfield. ",
        "items": [
            {"id": "scene1", "desc": "Narrator and friend next to small plane."},
            {"id": "flying_high", "desc": "Small plane flying over green hills."},
            {"id": "scared_narrator", "desc": "Narrator looking nervous inside plane."},
        ],
    },
    {
        "lesson": "l5",
        "chars": "Mr. Scott: Man in suit. ",
        "scene": "Garage. ",
        "items": [
            {"id": "scene1", "desc": "Mr. Scott at his new garage with vintage cars."},
            {
                "id": "wrong_number",
                "desc": "Mr. Scott answering telephone, looking confused.",
            },
            {"id": "pigeon_post", "desc": "Carrier pigeon flying towards the garage."},
        ],
    },
    {
        "lesson": "l6",
        "chars": "Percy Buttons: Beggar. Mrs. Thompson: Woman. ",
        "scene": "House door. ",
        "items": [
            {"id": "scene1", "desc": "Percy Buttons at front door asking for meal."},
            {"id": "thompson_food", "desc": "Mrs. Thompson handing food to Percy."},
            {"id": "percy_working", "desc": "Percy Buttons sweeping the path."},
        ],
    },
    {
        "lesson": "l7",
        "chars": "Inspector Hall: Man in coat. Thief: Man. ",
        "scene": "Airport. ",
        "items": [
            {"id": "scene1", "desc": "Inspector waiting at airport."},
            {"id": "thief_caught", "desc": "Inspector searching man's bag."},
            {"id": "diamonds_found", "desc": "Inspector holding sparkly diamonds."},
        ],
    },
    {
        "lesson": "l8",
        "chars": "Joe Sanders: Man. ",
        "scene": "Garden. ",
        "items": [
            {"id": "scene1", "desc": "Joe working in prize-winning garden."},
            {
                "id": "neighbors_jealous",
                "desc": "Neighbors looking over fence enviously.",
            },
            {"id": "joe_proud", "desc": "Joe holding trophy for Best Garden."},
        ],
    },
    {
        "lesson": "l9",
        "chars": "Narrator: Young man. Brother: Young man. ",
        "scene": "Snowy street. ",
        "items": [
            {"id": "scene1", "desc": "Narrator walking through snowstorm."},
            {"id": "brother_waiting", "desc": "Brother at door, happy to see him."},
            {"id": "warm_fire", "desc": "Sitting by fireplace, drinking hot soup."},
        ],
    },
    {
        "lesson": "l10",
        "chars": "Narrator: Young woman. Father: Man. ",
        "scene": "Living room. ",
        "items": [
            {"id": "scene1", "desc": "Narrator playing clavichord."},
            {"id": "broken_instrument", "desc": "Broken string on clavichord."},
            {
                "id": "modern_jazz",
                "desc": "Playing modern jazz piano, father covering ears.",
            },
        ],
    },
    {
        "lesson": "l11",
        "chars": "Anthony: Young man. Friend: Young man. ",
        "scene": "Bank/Restaurant. ",
        "items": [
            {"id": "scene1", "desc": "Anthony looking at empty wallet outside bank."},
            {"id": "friend_pays", "desc": "Friend paying for dinner."},
            {"id": "paying_back", "desc": "Anthony handing money back to friend."},
        ],
    },
    {
        "lesson": "l12",
        "chars": "Tom: Young man. Captain: Man in uniform. ",
        "scene": "Harbor. ",
        "items": [
            {"id": "scene1", "desc": "Tom waving goodbye to ship."},
            {"id": "captain_ship", "desc": "Captain on bridge of ship."},
            {"id": "return_home", "desc": "Tom welcoming ship back."},
        ],
    },
    {
        "lesson": "l13",
        "chars": "Greenwood Boys: Band. Fans. ",
        "scene": "Concert. ",
        "items": [
            {"id": "scene1", "desc": "Band on stage, fans screaming."},
            {"id": "airport_arrival", "desc": "Band at airport, surrounded by fans."},
            {"id": "bus_ride", "desc": "Band in tour bus, waving."},
        ],
    },
    {
        "lesson": "l14",
        "chars": "Young man and woman. ",
        "scene": "Train. ",
        "items": [
            {"id": "scene1", "desc": "Man and woman in train compartment."},
            {
                "id": "trying_to_speak",
                "desc": "Man trying to speak English, woman confused.",
            },
            {"id": "laughing_together", "desc": "Realizing they speak same language."},
        ],
    },
    {
        "lesson": "l15",
        "chars": "Secretary: Woman. Mr. Harmsworth: Man. ",
        "scene": "Office. ",
        "items": [
            {"id": "scene1", "desc": "Secretary entering office, worried."},
            {"id": "good_news", "desc": "Harmsworth telling good news."},
            {"id": "celebration", "desc": "Office staff celebrating with cake."},
        ],
    },
    {
        "lesson": "l16",
        "chars": "Policeman. Driver: Man. ",
        "scene": "Street. ",
        "items": [
            {"id": "scene1", "desc": "Policeman stopped car at corner."},
            {"id": "polite_request", "desc": "Policeman making polite request."},
            {"id": "driving_away", "desc": "Car driving away slowly."},
        ],
    },
    {
        "lesson": "l17",
        "chars": "Jennifer: Woman. Friend: Woman. ",
        "scene": "Party. ",
        "items": [
            {"id": "scene1", "desc": "Jennifer at party, looks young."},
            {"id": "telling_truth", "desc": "Jennifer telling real age to friend."},
            {"id": "always_young", "desc": "Jennifer looking in mirror."},
        ],
    },
    {
        "lesson": "l18",
        "chars": "Mr. West: Man. ",
        "scene": "Driveway. ",
        "items": [
            {"id": "scene1", "desc": "Mr. West washing car."},
            {"id": "strange_habit", "desc": "Mr. West gardening in suit."},
            {"id": "explaining", "desc": "Explaining habit to neighbor."},
        ],
    },
    {
        "lesson": "l19",
        "chars": "Theater Manager. Fans. ",
        "scene": "Box office. ",
        "items": [
            {"id": "scene1", "desc": "SOLD OUT sign at box office."},
            {"id": "pleading", "desc": "Fan pleading for ticket."},
            {"id": "lucky_break", "desc": "Manager handing ticket to fan."},
        ],
    },
    {
        "lesson": "l20",
        "chars": "Man in boat. ",
        "scene": "River. ",
        "items": [
            {"id": "scene1", "desc": "Man alone in rowing boat, fishing."},
            {"id": "struggling", "desc": "Struggling to pull in large fish."},
            {"id": "success", "desc": "Proudly holding huge fish."},
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

    for task in NCE2_BATCH_1:
        out_dir = root / "public" / "images" / "nce2" / task["lesson"]
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"🎨 Generating nce2 {task['lesson']}...")
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
