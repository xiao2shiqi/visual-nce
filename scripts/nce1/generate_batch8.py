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

BATCH_8 = [
    {
        "lesson": "l125",
        "chars": "Susan: Young woman. Terrence: Young man. ",
        "scene": "A living room. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Susan and Terrence are sitting in a living room, drinking tea. There is a teapot and two cups on the table.",
            },
            {
                "id": "tea_pour",
                "desc": "Susan is pouring more tea into Terrence's cup. He is looking at her and smiling.",
            },
            {
                "id": "cookies",
                "desc": "Terrence is taking a cookie from a plate. They are both enjoying their tea time.",
            },
        ],
    },
    {
        "lesson": "l127",
        "chars": "Famous Actress (Kate): Beautiful woman in a stylish dress. Interviewer: Man with a microphone. ",
        "scene": "A glamorous hotel lobby or red carpet. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A crowd of photographers are taking pictures of a beautiful actress (Kate) on a red carpet. She is waving and smiling.",
            },
            {
                "id": "interview",
                "desc": "The Interviewer is talking to Kate. She is holding a bouquet of flowers and looking elegant.",
            },
            {
                "id": "signing_autograph",
                "desc": "Kate is signing an autograph for a young fan. She looks kind and professional.",
            },
        ],
    },
    {
        "lesson": "l129",
        "chars": "Gary: Young man. Policeman: Man in uniform on a motorcycle. ",
        "scene": "A road with a vintage sports car. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Gary is driving a fast vintage red sports car down a country road. He looks excited.",
            },
            {
                "id": "police_chase",
                "desc": "A Policeman on a motorcycle is chasing Gary's car, signaling him to pull over with a siren.",
            },
            {
                "id": "ticketed",
                "desc": "Gary is standing by his car, looking sheepish, as the Policeman writes him a speeding ticket.",
            },
        ],
    },
    {
        "lesson": "l131",
        "chars": "Martin: Young man. His Friend: Young man. ",
        "scene": "A pub or a living room. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Martin and his friend are sitting at a table, looking at a newspaper with sports results. They look like they are having a bet.",
            },
            {
                "id": "winning_moment",
                "desc": "Martin is jumping up with joy, holding the newspaper. His friend looks surprised and a bit disappointed.",
            },
            {
                "id": "cheers",
                "desc": "Martin and his friend are raising their glasses in a toast. Martin is very happy.",
            },
        ],
    },
    {
        "lesson": "l133",
        "chars": "Reporter: Man with a microphone. Crowd. ",
        "scene": "A busy city street with a big news screen. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A large crowd of people is gathered around a big electronic news screen in a city square. The news is 'Sensational'.",
            },
            {
                "id": "reporter_live",
                "desc": "A news reporter is speaking into a microphone, with the busy city square in the background.",
            },
            {
                "id": "shocked_faces",
                "desc": "Close-up of several people in the crowd, looking shocked or amazed at the news on the screen.",
            },
        ],
    },
    {
        "lesson": "l135",
        "chars": "Headmaster: Older man with glasses. Student: Young man. ",
        "scene": "The Headmaster's office. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Headmaster is sitting at a large wooden desk, looking at a report card. The Student is standing in front of him, looking nervous.",
            },
            {
                "id": "pointing_report",
                "desc": "The Headmaster is pointing at something on the report and talking seriously. The student is listening carefully.",
            },
            {
                "id": "shaking_hands",
                "desc": "The Headmaster is now smiling and shaking the student's hand. The student looks relieved and happy.",
            },
        ],
    },
    {
        "lesson": "l137",
        "chars": "Julie: Young woman. Her Husband: Young man. ",
        "scene": "A bedroom and a tropical island. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Julie is waking up in her bed, looking dreamy and happy. Her husband is bringing her a cup of tea.",
            },
            {
                "id": "dream_island",
                "desc": "Flashback or dream: Julie is sitting under a palm tree on a white sandy beach with turquoise water.",
            },
            {
                "id": "talking_dream",
                "desc": "Julie is sitting up in bed, excitedly telling her husband about her pleasant dream. He is listening with a smile.",
            },
        ],
    },
    {
        "lesson": "l139",
        "chars": "John: Man in 30s. Mary: His wife. ",
        "scene": "A dark hallway and a telephone. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Mary is standing in a dark hallway, looking a bit scared. She is holding a heavy vase as a weapon.",
            },
            {
                "id": "john_arrives",
                "desc": "The front door opens and John enters, carrying his briefcase. He looks surprised to see Mary with a vase.",
            },
            {
                "id": "laughing_together",
                "desc": "John and Mary are laughing in the hallway after the misunderstanding. The light is now on.",
            },
        ],
    },
    {
        "lesson": "l141",
        "chars": "Sally: Young girl (5yo). Mother: Young woman. ",
        "scene": "A train compartment. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Sally is sitting by the window of a train compartment, looking out with wonder. Her Mother is sitting next to her.",
            },
            {
                "id": "passing_scenery",
                "desc": "View from the train window: green fields, cows, and a small village passing by. Sally is pointing at them.",
            },
            {
                "id": "arrival",
                "desc": "Sally and her Mother are stepping off the train onto a busy station platform. Sally is holding her mother's hand.",
            },
        ],
    },
    {
        "lesson": "l143",
        "chars": "Andy: Young boy (8yo). Lucy: Young girl (6yo). ",
        "scene": "A sunny forest path. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Andy and Lucy are walking along a path through a beautiful green forest. Sunlight is filtering through the leaves.",
            },
            {
                "id": "finding_flowers",
                "desc": "Lucy is stooping down to pick some colorful wildflowers. Andy is looking at a bird in a tree.",
            },
            {
                "id": "woods_exit",
                "desc": "Andy and Lucy emerging from the woods into a bright open field. They look tired but happy.",
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

    for task in BATCH_8:
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
