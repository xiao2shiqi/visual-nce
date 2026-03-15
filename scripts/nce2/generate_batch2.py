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

NCE2_BATCH_2 = [
    {
        "lesson": "l21",
        "chars": "Man (Narrator). People at a party. ",
        "scene": "An airplane. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Inside a small vintage airplane. The Narrator is looking out of the window at the clouds.",
            },
            {
                "id": "aeroplane_shaking",
                "desc": "The airplane is shaking in a storm. The Narrator looks worried.",
            },
            {
                "id": "party_talk",
                "desc": "Flashback or comparison: People talking at a party in a well-lit room.",
            },
        ],
    },
    {
        "lesson": "l22",
        "chars": "Narrator: Young man. Jane: Young woman. ",
        "scene": "A beach. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator and Jane walking on a sandy beach. A glass bottle is floating in the sea.",
            },
            {
                "id": "finding_bottle",
                "desc": "Narrator picking up the glass bottle from the water. There is a paper inside.",
            },
            {
                "id": "reading_note",
                "desc": "Narrator and Jane reading the note from the bottle. They both look surprised.",
            },
        ],
    },
    {
        "lesson": "l23",
        "chars": "Mrs. Bird: Woman in 40s. Narrator. ",
        "scene": "A construction site. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mrs. Bird and the Narrator standing in front of a half-built house with scaffolding.",
            },
            {
                "id": "pointing_rooms",
                "desc": "Mrs. Bird pointing to where the rooms will be in the new house. She looks excited.",
            },
            {
                "id": "completed_house",
                "desc": "The beautiful finished house with a garden. Mrs. Bird is waving from the front door.",
            },
        ],
    },
    {
        "lesson": "l24",
        "chars": "Narrator: Young man. His Friend: Young man. ",
        "scene": "A rainy street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator and his friend walking in the rain under a large black umbrella.",
            },
            {
                "id": "splashed_by_car",
                "desc": "A vintage car splashing water on the Narrator. He looks very upset.",
            },
            {
                "id": "friend_laughing",
                "desc": "The friend is laughing, saying 'It could be worse!' while the Narrator dries himself.",
            },
        ],
    },
    {
        "lesson": "l25",
        "chars": "Narrator: Young man. Porter: Man in uniform. ",
        "scene": "A train station. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator at a London train station, looking confused at a sign.",
            },
            {
                "id": "talking_to_porter",
                "desc": "Narrator asking a Porter for help. The Porter is speaking with a strong accent.",
            },
            {
                "id": "understanding",
                "desc": "Narrator finally understanding the Porter. Both are smiling.",
            },
        ],
    },
    {
        "lesson": "l26",
        "chars": "Young Man (Narrator). Art Critic: Man in a suit. ",
        "scene": "Art gallery. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator looking at a modern abstract painting in a gallery. He looks puzzled.",
            },
            {
                "id": "critic_explaining",
                "desc": "The Art Critic is explaining the painting to the Narrator, gesturing with his hands.",
            },
            {
                "id": "child_painting",
                "desc": "Comparison: A small child happily finger-painting on a large canvas.",
            },
        ],
    },
    {
        "lesson": "l27",
        "chars": "Narrator: Young man. ",
        "scene": "A wet night in a city. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator walking down a shiny, wet city street at night. Neon signs are reflected in the puddles.",
            },
            {
                "id": "lost_in_rain",
                "desc": "Narrator looking at a map under a street lamp in the rain.",
            },
            {
                "id": "finding_hotel",
                "desc": "Narrator arriving at a warm, brightly lit hotel entrance. Relieved.",
            },
        ],
    },
    {
        "lesson": "l28",
        "chars": "Policeman. Jasper White: Man in 40s. ",
        "scene": "A street with a car. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jasper White's car is parked in a 'NO PARKING' zone. A Policeman is looking at it.",
            },
            {
                "id": "jasper_arriving",
                "desc": "Jasper White running towards his car, looking worried as the Policeman writes a ticket.",
            },
            {
                "id": "jasper_explaining",
                "desc": "Jasper White pointing to his watch, trying to explain to the Policeman.",
            },
        ],
    },
    {
        "lesson": "l29",
        "chars": "Captain Fawcett: Man in a pilot's uniform. Narrator. ",
        "scene": "An airfield. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Captain Fawcett standing next to a small plane. He looks like a hero.",
            },
            {
                "id": "flying_over_mountains",
                "desc": "The plane flying over high, snow-capped mountains. Dramatic view.",
            },
            {
                "id": "landing_safely",
                "desc": "The plane landing on a small airstrip. People are cheering.",
            },
        ],
    },
    {
        "lesson": "l30",
        "chars": "Narrator: Young man. His Friend: Young man. ",
        "scene": "A sports field. ",
        "items": [
            {
                "id": "scene1",
                "desc": "People playing polo on horses. The Narrator and his friend are watching from the sidelines.",
            },
            {
                "id": "falling_off_horse",
                "desc": "Action shot: A player falling off his horse during the polo match. Dust is flying.",
            },
            {
                "id": "talking_sports",
                "desc": "Narrator and friend discussing the match over a drink.",
            },
        ],
    },
    {
        "lesson": "l31",
        "chars": "Frank Hall: Man in 30s. Workers. ",
        "scene": "A factory. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Frank Hall standing in a large, busy factory with many machines.",
            },
            {
                "id": "working_hard",
                "desc": "Frank Hall working at a machine, looking very focused and determined.",
            },
            {
                "id": "success_office",
                "desc": "Frank Hall now in a nice office, looking at charts showing his success.",
            },
        ],
    },
    {
        "lesson": "l32",
        "chars": "Narrator: Young woman. Detectives. ",
        "scene": "A large department store. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is shopping in a large, modern department store. She is looking at dresses.",
            },
            {
                "id": "detective_watching",
                "desc": "A plain-clothes detective is watching the Narrator from behind a shelf.",
            },
            {
                "id": "store_exit",
                "desc": "The Narrator leaving the store, having bought several things. She looks happy.",
            },
        ],
    },
    {
        "lesson": "l33",
        "chars": "Narrator: Young man. Girl: Young woman. ",
        "scene": "A dark cave or woods. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator and a girl walking through a dark, misty forest. They look a bit lost.",
            },
            {
                "id": "entering_cave",
                "desc": "They are entering a dark cave opening. The Narrator is holding a flashlight.",
            },
            {
                "id": "seeing_light",
                "desc": "They see a bright light at the end of the cave. Relieved and happy.",
            },
        ],
    },
    {
        "lesson": "l34",
        "chars": "Dan: Young man. His Wife: Young woman. ",
        "scene": "A messy kitchen. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Dan is in a very messy kitchen with a mountain of dirty dishes. He looks overwhelmed.",
            },
            {
                "id": "washing_dishes",
                "desc": "Dan is busily washing dishes, bubbles everywhere. He is working very fast.",
            },
            {
                "id": "wife_returns",
                "desc": "Dan's wife returns home to find a clean kitchen. She looks surprised and happy.",
            },
        ],
    },
    {
        "lesson": "l35",
        "chars": "Thief: Man in dark clothes. Narrator. ",
        "scene": "A house at night. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A thief is climbing through a window into a dark house at night.",
            },
            {
                "id": "narrator_waking",
                "desc": "The Narrator waking up in bed, having heard a noise. He looks alert.",
            },
            {
                "id": "police_arriving",
                "desc": "A police car with flashing lights outside the house. The thief is being caught.",
            },
        ],
    },
    {
        "lesson": "l36",
        "chars": "Debbie: Young woman swimmer. ",
        "scene": "The English Channel. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Debbie is standing on a cold, grey beach in her swimsuit, ready to swim.",
            },
            {
                "id": "swimming_hard",
                "desc": "Debbie swimming in the rough, choppy sea. A small boat is nearby for safety.",
            },
            {
                "id": "reaching_france",
                "desc": "Debbie reaching the French shore, looking exhausted but victorious. People are cheering.",
            },
        ],
    },
    {
        "lesson": "l37",
        "chars": "Athletes, Crowd. ",
        "scene": "Olympic Stadium. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Wide shot of an Olympic stadium with the Olympic flame burning. Athletes are parading.",
            },
            {
                "id": "running_race",
                "desc": "Athletes in a 100m sprint, running very fast. The crowd is a blur of color.",
            },
            {
                "id": "medal_ceremony",
                "desc": "A winning athlete standing on the podium, receiving a gold medal. Very emotional.",
            },
        ],
    },
    {
        "lesson": "l38",
        "chars": "Narrator: Young man. ",
        "scene": "A beautiful island (the West Indies). ",
        "items": [
            {
                "id": "scene1",
                "desc": "Narrator sitting on a palm-fringed beach with turquoise water. Perfect weather.",
            },
            {
                "id": "palm_trees_wind",
                "desc": "A sudden storm on the island. Palm trees are bending in the strong wind.",
            },
            {
                "id": "sunset_beach",
                "desc": "The storm has passed, and the Narrator is watching a spectacular sunset over the calm sea.",
            },
        ],
    },
    {
        "lesson": "l39",
        "chars": "Narrator: Young man. Doctor: Middle-aged man. ",
        "scene": "A medical clinic. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is in a doctor's waiting room, looking at a health poster.",
            },
            {
                "id": "doctor_checkup",
                "desc": "The Doctor is checking the Narrator's heartbeat with a stethoscope. Narrator looks nervous.",
            },
            {
                "id": "all_right_now",
                "desc": "The Doctor is smiling and giving the Narrator a thumbs-up. Narrator looks relieved.",
            },
        ],
    },
    {
        "lesson": "l40",
        "chars": "Mrs. Rumbold: Woman in 40s. Guests. ",
        "scene": "A dinner party. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A group of people sitting around a large dinner table, talking and eating.",
            },
            {
                "id": "mrs_rumbold_talking",
                "desc": "Mrs. Rumbold is talking animatedly to her neighbor at the table. He is listening politely.",
            },
            {
                "id": "funny_story",
                "desc": "Everyone at the table is laughing at a story. A very jolly atmosphere.",
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

    for task in NCE2_BATCH_2:
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
