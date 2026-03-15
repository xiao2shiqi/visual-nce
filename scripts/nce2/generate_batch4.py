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

NCE2_BATCH_4 = [
    {
        "lesson": "l61",
        "chars": "Astronauts. Hubble Telescope. ",
        "scene": "Space. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Hubble space telescope floating high above the blue Earth.",
            },
            {
                "id": "astronaut_repair",
                "desc": "An astronaut in a spacesuit performing repairs on the telescope outside a shuttle.",
            },
            {
                "id": "clear_view",
                "desc": "The clear, sharp image of a distant colorful nebula through the telescope.",
            },
        ],
    },
    {
        "lesson": "l62",
        "chars": "Firemen. Narrator. ",
        "scene": "A burnt-out building. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A burnt-out wooden building, smoking slightly. Firemen are still spraying water.",
            },
            {
                "id": "finding_safe",
                "desc": "A fireman is carrying a heavy black safe out of the ruins. It looks undamaged.",
            },
            {
                "id": "opening_safe",
                "desc": "The Narrator and a locksmith opening the safe. Inside are some charred papers and jewelry.",
            },
        ],
    },
    {
        "lesson": "l63",
        "chars": "Jeremy: Young man. Guests. ",
        "scene": "A garden party. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jeremy is at a garden party, telling a story to a group of laughing people.",
            },
            {
                "id": "spilling_drink",
                "desc": "Jeremy accidentally spills a red drink on a lady's white dress. She looks shocked and not amused.",
            },
            {
                "id": "apologizing",
                "desc": "Jeremy is trying to wipe the dress with a handkerchief, looking very embarrassed. The lady is walking away.",
            },
        ],
    },
    {
        "lesson": "l64",
        "chars": "Workers. The Channel Tunnel. ",
        "scene": "Under the sea. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A huge boring machine digging the Channel Tunnel deep underground.",
            },
            {
                "id": "workers_meeting",
                "desc": "French and British workers meeting in the middle of the tunnel, shaking hands.",
            },
            {
                "id": "train_passing",
                "desc": "A fast train speeding through the completed tunnel. Bright lights.",
            },
        ],
    },
    {
        "lesson": "l65",
        "chars": "Jumbo: A large elephant. Policemen. ",
        "scene": "A circus and a street. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Jumbo the elephant performing in a circus ring. People are cheering.",
            },
            {
                "id": "jumbo_escaping",
                "desc": "Jumbo is walking down a city street, looking calm but scaring the traffic. Policemen are chasing him.",
            },
            {
                "id": "jumbo_stopped",
                "desc": "Jumbo has stopped at a bakery, eating some buns. The baker is smiling.",
            },
        ],
    },
    {
        "lesson": "l66",
        "chars": "Narrator: Young man. Bees. ",
        "scene": "A garden with beehives. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is standing near some wooden beehives in a sunny garden. Bees are buzzing.",
            },
            {
                "id": "getting_stung",
                "desc": "The Narrator has been stung on the nose and is looking pained in a mirror.",
            },
            {
                "id": "eating_honey",
                "desc": "The Narrator is happily eating a large piece of honeycomb on toast. Worth it.",
            },
        ],
    },
    {
        "lesson": "l67",
        "chars": "Scientists. Volcano. ",
        "scene": "A volcanic island. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A huge volcano erupting, with smoke and lava. Wide shot of the island.",
            },
            {
                "id": "scientists_observing",
                "desc": "Scientists in protective gear looking at the volcano through instruments.",
            },
            {
                "id": "lava_flow",
                "desc": "Close-up of orange glowing lava flowing down the mountainside towards the sea.",
            },
        ],
    },
    {
        "lesson": "l68",
        "chars": "Elizabeth: Young woman. ",
        "scene": "A kitchen. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Elizabeth is trying to open a stubborn jar of jam in her kitchen. She is pulling hard.",
            },
            {
                "id": "persistent_effort",
                "desc": "Elizabeth is now using a towel and a knife to try and open the jar. Her face is red.",
            },
            {
                "id": "jar_opens",
                "desc": "The jar has finally popped open. Elizabeth is smiling, holding a piece of bread.",
            },
        ],
    },
    {
        "lesson": "l69",
        "chars": "Narrator: Young man. ",
        "scene": "A boat at sea. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is on a small boat in the middle of the ocean. It is a calm day.",
            },
            {
                "id": "seeing_land",
                "desc": "The Narrator looking through binoculars and seeing a small green island on the horizon.",
            },
            {
                "id": "landing_on_beach",
                "desc": "The Narrator pulling his boat up onto the sandy beach of the desert island.",
            },
        ],
    },
    {
        "lesson": "l70",
        "chars": "Divers. Shipwreck. ",
        "scene": "Underwater. ",
        "items": [
            {
                "id": "scene1",
                "desc": "Divers swimming around a large, sunken shipwreck on the sea floor. Bubbles everywhere.",
            },
            {
                "id": "finding_gold",
                "desc": "A diver has found a wooden chest full of gold coins. He is signaling to his partner.",
            },
            {
                "id": "shark_appearing",
                "desc": "A large shark is swimming nearby. The divers are looking wary. Red for danger.",
            },
        ],
    },
    {
        "lesson": "l71",
        "chars": "Big Ben. Crowd. ",
        "scene": "London. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Big Ben clock tower against a cloudy London sky. People are walking on the bridge.",
            },
            {
                "id": "clock_face",
                "desc": "Close-up of the giant clock face of Big Ben. The hands are moving.",
            },
            {
                "id": "interior_bells",
                "desc": "Inside the tower, showing the huge bells ready to strike. Mechanical gears visible.",
            },
        ],
    },
    {
        "lesson": "l72",
        "chars": "Donald Campbell: Man in racing gear. Bluebird car. ",
        "scene": "A salt flat. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The sleek blue 'Bluebird' racing car on a vast, white salt flat. It looks extremely fast.",
            },
            {
                "id": "high_speed_run",
                "desc": "Bluebird speeding across the flats, kicking up a trail of white salt dust.",
            },
            {
                "id": "campbell_celebrating",
                "desc": "Donald Campbell standing by his car, waving to a cheering crowd. A new record.",
            },
        ],
    },
    {
        "lesson": "l73",
        "chars": "Athletes. Crowd. ",
        "scene": "A running track. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A group of runners at the start of a long-distance race. They look focused.",
            },
            {
                "id": "leading_runner",
                "desc": "One runner is far ahead of the others, looking strong and steady. The crowd is cheering.",
            },
            {
                "id": "breaking_record",
                "desc": "The lead runner crossing the finish line and looking at the stadium clock. A new record holder.",
            },
        ],
    },
    {
        "lesson": "l74",
        "chars": "Famous Singer: Woman in a glamorous dress. ",
        "scene": "A quiet villa. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A once-famous singer is sitting alone in her beautiful, quiet villa garden. She looks peaceful.",
            },
            {
                "id": "fans_waiting",
                "desc": "A few loyal fans are waiting outside the villa gates, hoping for a glimpse of her.",
            },
            {
                "id": "singing_at_home",
                "desc": "The singer is playing the piano and singing softly to herself in her living room.",
            },
        ],
    },
    {
        "lesson": "l75",
        "chars": "Crew of a small boat. ",
        "scene": "A stormy sea. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A small fishing boat being tossed about by huge waves in a storm. SOS signal being sent.",
            },
            {
                "id": "helicopter_rescue",
                "desc": "A rescue helicopter hovering over the boat, lowering a winch. The crew is waving.",
            },
            {
                "id": "safe_on_land",
                "desc": "The crew being wrapped in blankets on a safe harbor dock. They look relieved.",
            },
        ],
    },
    {
        "lesson": "l76",
        "chars": "Narrator: Young man. Friend: Young man. ",
        "scene": "An office. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is pointing at his friend's shoes, laughing. It's April Fools' Day.",
            },
            {
                "id": "friend_tricked",
                "desc": "The friend is looking at his shoes, realizing they are two different colors. He looks sheepish.",
            },
            {
                "id": "another_trick",
                "desc": "The friend is now trying to trick someone else with a fake spider on their desk.",
            },
        ],
    },
    {
        "lesson": "l77",
        "chars": "Patient: Young man. Surgeons. ",
        "scene": "A hospital operating room. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The patient is being wheeled into an operating room. He looks a bit nervous.",
            },
            {
                "id": "surgeons_working",
                "desc": "The surgeons in their green scrubs and masks are busily working under bright lights.",
            },
            {
                "id": "patient_recovering",
                "desc": "The patient is sitting up in bed a few days later, eating some soup. A successful operation.",
            },
        ],
    },
    {
        "lesson": "l78",
        "chars": "Narrator: Young man. Shopkeeper. ",
        "scene": "A small shop. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The Narrator is looking at a beautiful old clock in a small shop window.",
            },
            {
                "id": "buying_last_one",
                "desc": "The Shopkeeper is handing the clock to the Narrator, saying it's the last one.",
            },
            {
                "id": "clock_at_home",
                "desc": "The Narrator is placing the clock on his own mantelpiece. It fits perfectly.",
            },
        ],
    },
    {
        "lesson": "l79",
        "chars": "Travelers. Airplane. ",
        "scene": "An airport and the sky. ",
        "items": [
            {
                "id": "scene1",
                "desc": "A large crowd of people boarding a big jet plane at a busy airport.",
            },
            {
                "id": "view_above_clouds",
                "desc": "The view from the plane window: fluffy white clouds and a deep blue sky.",
            },
            {
                "id": "arriving_sunny_place",
                "desc": "The plane landing at a tropical airport with palm trees. People are stepping out into the sun.",
            },
        ],
    },
    {
        "lesson": "l80",
        "chars": "Visitors. Crystal Palace. ",
        "scene": "London 1851. ",
        "items": [
            {
                "id": "scene1",
                "desc": "The magnificent glass and iron Crystal Palace building in London. Many people in Victorian dress.",
            },
            {
                "id": "inside_palace",
                "desc": "Inside the palace, showing exotic plants and inventions from all over the world.",
            },
            {
                "id": "fire_scene",
                "desc": "Flashback or historical: The palace is on fire at night, a huge glow in the sky.",
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

    for task in NCE2_BATCH_4:
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
