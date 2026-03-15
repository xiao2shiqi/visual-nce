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

NCE2_BATCH_5 = [
    {
        "lesson": "l81",
        "chars": "Prisoner. Guards. ",
        "scene": "A prison and a wall. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A prisoner is looking out of a barred window at a high stone wall.",
            },
            {
                "id": "climbing_wall",
                "desc": "The prisoner is climbing over the high prison wall with a rope. It is dark outside.",
            },
            {
                "id": "running_free",
                "desc": "The prisoner is running through a field under the moonlight, looking back at the prison.",
            },
        ],
    },
    {
        "lesson": "l82",
        "chars": "Fishermen. Sea Monster. ",
        "scene": "The ocean. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Fishermen on a small boat are looking at something strange in the water.",
            },
            {
                "id": "monster_head",
                "desc": "A large, scaly head of a sea monster appears above the waves. The fishermen look shocked.",
            },
            {
                "id": "just_a_fish",
                "desc": "The 'monster' is actually a very large, unusual fish caught in their net.",
            },
        ],
    },
    {
        "lesson": "l83",
        "chars": "Politician. Crowd. ",
        "scene": "A city square. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A politician is standing on a platform, making a speech to a large crowd. Flags are waving.",
            },
            {
                "id": "cheering_crowd",
                "desc": "The crowd is cheering and clapping after the election results are announced.",
            },
            {
                "id": "new_office",
                "desc": "The politician is sitting in a large new office, looking at a stack of papers.",
            },
        ],
    },
    {
        "lesson": "l84",
        "chars": "Bus Drivers. Strikers. ",
        "scene": "A bus depot. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A group of bus drivers are standing outside a depot with 'ON STRIKE' signs.",
            },
            {
                "id": "empty_streets",
                "desc": "A busy city street with no buses, people are walking or cycling instead.",
            },
            {
                "id": "returning_to_work",
                "desc": "The drivers are shaking hands with a manager and getting back onto their buses.",
            },
        ],
    },
    {
        "lesson": "l85",
        "chars": "Mr. Page: Old man (80yo). Students. ",
        "scene": "A university classroom. ",
        "items": [
            {
                "id": "scene1",
                "desc": "An elderly man (Mr. Page) is sitting in a classroom with much younger students. He is taking notes.",
            },
            {
                "id": "talking_to_professor",
                "desc": "Mr. Page is talking to a young professor after class. Both look very interested.",
            },
            {
                "id": "graduation",
                "desc": "Mr. Page in a graduation cap and gown, holding a diploma. He is smiling proudly.",
            },
        ],
    },
    {
        "lesson": "l86",
        "chars": "Pilot. Airplane. ",
        "scene": "An airplane cockpit. ",
        "items": [
            {
                "id": "scene1",
                "desc": "An airplane is flying erratically through the clouds. It looks out of control.",
            },
            {
                "id": "pilot_struggling",
                "desc": "The Pilot inside the cockpit is frantically pulling on the controls. Warning lights are flashing.",
            },
            {
                "id": "safe_landing",
                "desc": "The plane has landed safely on a grassy field. Fire engines are nearby. The pilot is stepping out.",
            },
        ],
    },
    {
        "lesson": "l87",
        "chars": "Man (Narrator). Detective. ",
        "scene": "A police station. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A man is being questioned by a detective in a small, dimly lit room.",
            },
            {
                "id": "alibi_photo",
                "desc": "The man is showing the detective a photograph as proof of his alibi. The detective is looking at it through a magnifying glass.",
            },
            {
                "id": "walking_out",
                "desc": "The man is walking out of the police station, looking relieved. The detective is watching him go.",
            },
        ],
    },
    {
        "lesson": "l88",
        "chars": "Miners. ",
        "scene": "A dark mine shaft. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A group of miners are trapped in a dark, narrow mine shaft. Their headlamps are the only light.",
            },
            {
                "id": "rescue_drill",
                "desc": "A large drill is breaking through the ceiling of the mine shaft. Dust is falling.",
            },
            {
                "id": "emerging_to_light",
                "desc": "The miners are being pulled up to the surface, squinting at the bright sunlight. Families are waiting.",
            },
        ],
    },
    {
        "lesson": "l89",
        "chars": "Man (Narrator). Guest. ",
        "scene": "A dinner party. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A man is making a toast at a dinner party. He looks a bit nervous.",
            },
            {
                "id": "embarrassed_face",
                "desc": "The man has just made a 'slip of the tongue'. He is blushing and covering his mouth. The guests look confused.",
            },
            {
                "id": "laughing_it_off",
                "desc": "Everyone at the table is laughing after the mistake is explained. A friendly atmosphere.",
            },
        ],
    },
    {
        "lesson": "l90",
        "chars": "Fish: A small fish. Narrator. ",
        "scene": "A kitchen. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is looking into a refrigerator, which is almost empty. 'What's for supper?'",
            },
            {
                "id": "frying_fish",
                "desc": "The Narrator is frying a single small fish in a large pan. It looks very lonely.",
            },
            {
                "id": "eating_supper",
                "desc": "The Narrator is sitting at the table, eating his simple supper with a piece of bread.",
            },
        ],
    },
    {
        "lesson": "l91",
        "chars": "Three Men. Hot Air Balloon. ",
        "scene": "The sky. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A colorful hot air balloon is floating high above a beautiful landscape. Three men are in the basket.",
            },
            {
                "id": "view_from_above",
                "desc": "The view from the balloon: tiny houses and winding rivers far below. The men are pointing.",
            },
            {
                "id": "landing_in_tree",
                "desc": "The balloon basket has got stuck in the branches of a large tree. The men are looking for a way down.",
            },
        ],
    },
    {
        "lesson": "l92",
        "chars": "Young Man. Policeman. ",
        "scene": "A street with a car. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A young man is driving a car while looking at a map. He is not paying attention to the road.",
            },
            {
                "id": "narrow_escape",
                "desc": "The car has narrowly missed a fruit stall. Oranges are rolling everywhere. A Policeman is blowing a whistle.",
            },
            {
                "id": "being_reprimanded",
                "desc": "The Policeman is talking sternly to the young man. The man looks ashamed. Asking for trouble.",
            },
        ],
    },
    {
        "lesson": "l93",
        "chars": "Ambassador. Gift. ",
        "scene": "A grand palace. ",
        "items": [
            {
                "id": "scene1",
                "desc": "An Ambassador is handing a beautifully wrapped gift to a King in a grand palace room.",
            },
            {
                "id": "opening_gift",
                "desc": "The King is opening the gift. Inside is a rare and beautiful golden bird statue.",
            },
            {
                "id": "displaying_gift",
                "desc": "The golden bird is being placed on a velvet cushion in a museum or treasury. It is glowing.",
            },
        ],
    },
    {
        "lesson": "l94",
        "chars": "Young Athletes. ",
        "scene": "A school gymnasium. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A group of young children are practicing gymnastics in a gymnasium. They are very energetic.",
            },
            {
                "id": "talented_boy",
                "desc": "A young boy is performing a perfect backflip. His coach is watching with pride.",
            },
            {
                "id": "team_photo",
                "desc": "The group of young 'future champions' are posing for a photo with their medals.",
            },
        ],
    },
    {
        "lesson": "l95",
        "chars": "Narrator: Young man. ",
        "scene": "A fantasy world. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is walking through a magical forest with giant mushrooms and glowing flowers.",
            },
            {
                "id": "talking_animal",
                "desc": "The Narrator is talking to a small, wise-looking fox with two tails. The fox is sitting on a stump.",
            },
            {
                "id": "flying_carpet",
                "desc": "The Narrator is flying over a city of crystal towers on a colorful carpet. Pure fantasy.",
            },
        ],
    },
    {
        "lesson": "l96",
        "chars": "Villagers. Skeleton. ",
        "scene": "A village at night. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A group of villagers are gathered in a dark street, looking at something scary.",
            },
            {
                "id": "skeleton_appearing",
                "desc": "A white skeleton is walking down the street. It is actually just someone in a costume for a prank.",
            },
            {
                "id": "mystery_revealed",
                "desc": "The person in the skeleton costume has taken off the mask, and everyone is laughing. The dead return as a joke.",
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

    for task in NCE2_BATCH_5:
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
