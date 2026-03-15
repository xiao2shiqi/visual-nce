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

NCE2_BATCH_3 = [
    {
        "lesson": "l41",
        "chars": "Woman (Narrator). Her Husband. ",
        "scene": "A living room. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is wearing a very large, strange hat with feathers. Her husband is looking at it with a shocked expression.",
            },
            {
                "id": "husband_laughing",
                "desc": "The husband is laughing at the hat. The Narrator looks annoyed and is looking in a mirror.",
            },
            {
                "id": "hat_on_table",
                "desc": "The strange hat is sitting on a table. It looks like a bird's nest.",
            },
        ],
    },
    {
        "lesson": "l42",
        "chars": "Narrator: Young man. Neighbors. ",
        "scene": "An apartment. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is trying to play a large bass fiddle in his small apartment. It's very loud.",
            },
            {
                "id": "neighbor_knocking",
                "desc": "A neighbor is knocking on the wall, looking angry. The Narrator is still playing.",
            },
            {
                "id": "piano_delivery",
                "desc": "Two men are delivering a large grand piano to the Narrator's apartment. Neighbors are watching in despair.",
            },
        ],
    },
    {
        "lesson": "l43",
        "chars": "Explorer: Man in flight gear. ",
        "scene": "The South Pole. ",
        "items": [
            {
                "id": "scene1",
                "desc": "An airplane flying over the vast, white, icy landscape of the South Pole.",
            },
            {
                "id": "dropping_supplies",
                "desc": "The airplane is dropping supply crates with parachutes onto the snow.",
            },
            {
                "id": "explorer_waving",
                "desc": "A lone explorer on the snow is waving to the plane above.",
            },
        ],
    },
    {
        "lesson": "l44",
        "chars": "Mrs. Anne Sterling: Woman in 30s. ",
        "scene": "A forest at night. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mrs. Sterling is walking through a dark forest at night. She looks brave.",
            },
            {
                "id": "seeing_something",
                "desc": "She has stopped and is pointing her flashlight at something in the trees. Her eyes are wide.",
            },
            {
                "id": "finding_treasure",
                "desc": "She has found an old wooden box half-buried in the ground. It looks mysterious.",
            },
        ],
    },
    {
        "lesson": "l45",
        "chars": "Sam Benton: Man in 40s. ",
        "scene": "A village street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Sam Benton is walking down a village street, looking very happy and proud.",
            },
            {
                "id": "returning_wallet",
                "desc": "Sam is handing a lost wallet to an old man. The old man is smiling and thanking him.",
            },
            {
                "id": "sam_whistling",
                "desc": "Sam is walking away, whistling a tune, looking like he has a clear conscience.",
            },
        ],
    },
    {
        "lesson": "l46",
        "chars": "Narrator: Young man. ",
        "scene": "A vintage car and a rough road. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is driving a very small, old vintage car. It looks very uncomfortable.",
            },
            {
                "id": "car_breaking_down",
                "desc": "Steam is coming out of the car's engine. The Narrator is standing by the side of the road, looking frustrated.",
            },
            {
                "id": "walking_home",
                "desc": "The Narrator is walking home in the dark, leaving the broken car behind.",
            },
        ],
    },
    {
        "lesson": "l47",
        "chars": "Ghost: Faint transparent figure. Narrator. ",
        "scene": "A haunted house. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is sitting in a dark room with a single candle. A faint ghost figure is appearing behind him.",
            },
            {
                "id": "ghost_drinking",
                "desc": "The ghost is picking up a glass of wine from the table. The Narrator is watching, terrified.",
            },
            {
                "id": "ghost_disappearing",
                "desc": "The ghost is fading away into the wall. The Narrator is clutching his chest.",
            },
        ],
    },
    {
        "lesson": "l48",
        "chars": "Narrator: Young man. Friend: Young man. ",
        "scene": "A library or office. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is trying to tell his friend something important, but the friend is busily writing.",
            },
            {
                "id": "friend_ignoring",
                "desc": "The friend is still writing, not looking up. The Narrator is looking frustrated.",
            },
            {
                "id": "friend_leaving",
                "desc": "The friend has suddenly stood up and is leaving the room, still not having listened to the Narrator.",
            },
        ],
    },
    {
        "lesson": "l49",
        "chars": "Narrator: Young man. ",
        "scene": "A mountain side. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is climbing a steep mountain path. The view is spectacular.",
            },
            {
                "id": "falling_dream",
                "desc": "The Narrator is falling through the air (a dream). He looks terrified.",
            },
            {
                "id": "waking_up",
                "desc": "The Narrator is waking up in his bed, sweating and looking relieved. It was just a dream.",
            },
        ],
    },
    {
        "lesson": "l50",
        "chars": "Narrator: Young man. Driver: Man. ",
        "scene": "A car. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is sitting in the back of a vintage car, looking out of the window.",
            },
            {
                "id": "fast_driving",
                "desc": "The car is speeding down a narrow country road. The Narrator is holding on tight.",
            },
            {
                "id": "arriving_destination",
                "desc": "The car has stopped at a beautiful old inn. The Narrator is stepping out, looking a bit dizzy.",
            },
        ],
    },
    {
        "lesson": "l51",
        "chars": "Hugh Williams: Man in 30s. ",
        "scene": "A garden and a house. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Hugh Williams is working in his garden, pruning some bushes.",
            },
            {
                "id": "finding_money",
                "desc": "Hugh has found a small bag of money hidden in the bushes. He looks amazed.",
            },
            {
                "id": "handing_to_police",
                "desc": "Hugh is at a police station, handing the bag of money to a sergeant. He looks honest.",
            },
        ],
    },
    {
        "lesson": "l52",
        "chars": "Narrator: Young man. ",
        "scene": "A living room with a new carpet. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A beautiful, colorful new carpet is spread out on the living room floor. The Narrator is admiring it.",
            },
            {
                "id": "dog_on_carpet",
                "desc": "A muddy dog is running across the brand new carpet. The Narrator is shouting 'No!'",
            },
            {
                "id": "cleaning_carpet",
                "desc": "The Narrator is on his hands and knees, trying to clean the mud off the carpet. He looks tired.",
            },
        ],
    },
    {
        "lesson": "l53",
        "chars": "Snake: A long thin snake. Narrator. ",
        "scene": "A desert or a garden. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A long snake is sunning itself on a hot rock in a garden.",
            },
            {
                "id": "narrator_seeing_snake",
                "desc": "The Narrator has seen the snake and has jumped back in surprise.",
            },
            {
                "id": "snake_slithering",
                "desc": "The snake is slithering away into the long grass. The Narrator is watching it carefully.",
            },
        ],
    },
    {
        "lesson": "l54",
        "chars": "Child: Young girl (4yo). Mother: Young woman. ",
        "scene": "A kitchen with jam. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A young girl is covered in red jam. Her face, hands, and dress are sticky.",
            },
            {
                "id": "mother_shocked",
                "desc": "The Mother is standing in the kitchen doorway, looking shocked at the messy child.",
            },
            {
                "id": "bath_time",
                "desc": "The girl is in a bathtub full of bubbles, looking happy and clean again.",
            },
        ],
    },
    {
        "lesson": "l55",
        "chars": "Narrator: Young man. ",
        "scene": "A rocky field. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is digging in a rocky field with a spade. He looks like he's searching for something.",
            },
            {
                "id": "finding_nothing",
                "desc": "The Narrator is sitting on a rock, looking disappointed. There is only a pile of dirt and stones.",
            },
            {
                "id": "finding_old_coin",
                "desc": "The Narrator is holding up a small, dirty old coin he just found. He looks surprised.",
            },
        ],
    },
    {
        "lesson": "l56",
        "chars": "Pilot: Man in a flight suit. ",
        "scene": "A supersonic jet. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A sleek, silver supersonic jet is taking off from a runway. A huge cloud of smoke is behind it.",
            },
            {
                "id": "jet_in_sky",
                "desc": "The jet is high in the sky, trailing a long white vapor trail.",
            },
            {
                "id": "pilot_smiling",
                "desc": "The Pilot inside the cockpit, looking calm and confident as he flies faster than sound.",
            },
        ],
    },
    {
        "lesson": "l57",
        "chars": "Madam: Elegant woman. Shop Assistant: Man. ",
        "scene": "A car showroom. ",
        "items": [
            {
                "id": "scene1",
                "desc": "An elegant woman is looking at a small, stylish car in a showroom. The assistant is talking to her.",
            },
            {
                "id": "sitting_in_car",
                "desc": "The woman is sitting in the driver's seat of the car, looking at the dashboard. She looks pleased.",
            },
            {
                "id": "assistant_explaining",
                "desc": "The assistant is pointing to the engine of the car, explaining something to the woman.",
            },
        ],
    },
    {
        "lesson": "l58",
        "chars": "Narrator: Young man. ",
        "scene": "A rainy street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is standing in the rain, looking miserable because he missed his bus.",
            },
            {
                "id": "old_friend_arrives",
                "desc": "An old friend in a car has pulled up next to the Narrator, waving him to get in.",
            },
            {
                "id": "happy_ride",
                "desc": "The Narrator and his friend are laughing in the dry, warm car. A blessing in disguise.",
            },
        ],
    },
    {
        "lesson": "l59",
        "chars": "Dog: A small terrier. Narrator. ",
        "scene": "A house and a garden. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A small dog is standing at the back door, wanting to go out. The Narrator is opening the door.",
            },
            {
                "id": "dog_wants_in",
                "desc": "A few minutes later, the same dog is at the door, wanting to come back in. It is raining.",
            },
            {
                "id": "dog_indecisive",
                "desc": "The dog is standing in the doorway, unable to decide whether to stay in or go out.",
            },
        ],
    },
    {
        "lesson": "l60",
        "chars": "Fortune Teller: Old woman with a headscarf. Young Woman. ",
        "scene": "A fairground tent. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A young woman is sitting in a dark tent with a fortune teller. There is a crystal ball on the table.",
            },
            {
                "id": "reading_palm",
                "desc": "The fortune teller is looking closely at the young woman's palm. The woman looks nervous.",
            },
            {
                "id": "future_vision",
                "desc": "Flashback or vision: The young woman is walking in a beautiful garden with a handsome man.",
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

    for task in NCE2_BATCH_3:
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
