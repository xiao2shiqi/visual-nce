import json
import os


def process_file(path, updates):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]

        sid = seg["id"]
        if sid in updates["roles"]:
            seg["role"] = updates["roles"][sid]
        if sid in updates["images"]:
            seg["image"] = updates["images"][sid]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# L45
process_file(
    "src/data/lessons/nce1-l45.json",
    {
        "roles": {
            "s1": "Boss",
            "s2": "Bob",
            "s3": "Boss",
            "s4": "Bob",
            "s5": "Bob",
            "s6": "Boss",
            "s7": "Boss",
            "s8": "Bob",
            "s9": "Bob",
            "s10": "Pamela",
            "s11": "Bob",
            "s12": "Pamela",
            "s13": "Pamela",
            "s14": "Bob",
            "s15": "Bob",
            "s16": "Pamela",
            "s17": "Pamela",
            "s18": "Pamela",
        },
        "images": {
            "s1": "/images/nce1/l45/scene1.png",
            "s9": "/images/nce1/l45/pamela_office.png",
            "s16": "/images/nce1/l45/terrible_handwriting.png",
        },
    },
)

# L47
process_file(
    "src/data/lessons/nce1-l47.json",
    {
        "roles": {
            "s1": "Christine",
            "s2": "Ann",
            "s3": "Christine",
            "s4": "Ann",
            "s5": "Christine",
            "s6": "Ann",
            "s7": "Christine",
            "s8": "Ann",
            "s9": "Ann",
            "s10": "Ann",
            "s11": "Christine",
            "s12": "Ann",
            "s13": "Christine",
            "s14": "Ann",
        },
        "images": {
            "s1": "/images/nce1/l47/scene1.png",
            "s5": "/images/nce1/l47/sugar_no_milk.png",
            "s11": "/images/nce1/l47/biscuits.png",
        },
    },
)

# L49
process_file(
    "src/data/lessons/nce1-l49.json",
    {
        "roles": {
            "s1": "Butcher",
            "s2": "Mrs. Bird",
            "s3": "Butcher",
            "s4": "Mrs. Bird",
            "s5": "Butcher",
            "s6": "Mrs. Bird",
            "s7": "Butcher",
            "s8": "Butcher",
            "s9": "Mrs. Bird",
            "s10": "Mrs. Bird",
            "s11": "Butcher",
            "s12": "Butcher",
            "s13": "Mrs. Bird",
            "s14": "Mrs. Bird",
            "s15": "Butcher",
        },
        "images": {
            "s1": "/images/nce1/l49/scene1.png",
            "s8": "/images/nce1/l49/steak_mince.png",
        },
    },
)

# L51
process_file(
    "src/data/lessons/nce1-l51.json",
    {
        "roles": {
            "s1": "Traveler",
            "s2": "Dimitri",
            "s3": "Traveler",
            "s4": "Dimitri",
            "s5": "Traveler",
            "s6": "Dimitri",
            "s7": "Dimitri",
            "s8": "Traveler",
            "s9": "Dimitri",
            "s10": "Dimitri",
            "s11": "Traveler",
            "s12": "Dimitri",
            "s13": "Dimitri",
            "s14": "Traveler",
            "s15": "Dimitri",
            "s16": "Dimitri",
        },
        "images": {
            "s1": "/images/nce1/l51/scene1.png",
            "s6": "/images/nce1/l51/spring_windy.png",
            "s16": "/images/nce1/l51/winter_snow.png",
        },
    },
)

print("Batch 2 Updates Done.")
