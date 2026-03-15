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


# L53
process_file(
    "src/data/lessons/nce1-l53.json",
    {
        "roles": {
            "s1": "Traveler",
            "s2": "Dimitri",
            "s3": "Traveler",
            "s4": "Dimitri",
            "s5": "Woman",
            "s6": "Dimitri",
            "s7": "Narrator",
            "s8": "Dimitri",
            "s9": "Woman",
            "s10": "Dimitri",
            "s11": "Dimitri",
            "s12": "Woman",
            "s13": "Dimitri",
            "s14": "Dimitri",
            "s15": "Woman",
        },
        "images": {
            "s1": "/images/nce1/l53/scene1.png",
            "s5": "/images/nce1/l53/north_east.png",
            "s6": "/images/nce1/l53/west_south.png",
        },
    },
)

# L55
process_file(
    "src/data/lessons/nce1-l55.json",
    {
        "roles": {},  # Mostly Narrator in original, but let's keep it consistent
        "images": {
            "s1": "/images/nce1/l55/scene1.png",
            "s4": "/images/nce1/l55/housework_friends.png",
            "s13": "/images/nce1/l55/evening_tv.png",
        },
    },
)

# L57
process_file(
    "src/data/lessons/nce1-l57.json",
    {
        "roles": {},
        "images": {
            "s1": "/images/nce1/l57/scene1.png",
            "s4": "/images/nce1/l57/mrs_sawyer_shops.png",
            "s7": "/images/nce1/l57/tea_garden.png",
            "s10": "/images/nce1/l57/children_playing.png",
            "s14": "/images/nce1/l57/mr_sawyer_book.png",
        },
    },
)

# L59
process_file(
    "src/data/lessons/nce1-l59.json",
    {
        "roles": {
            "s1": "Lady",
            "s2": "Shopkeeper",
            "s3": "Lady",
            "s4": "Lady",
            "s5": "Shopkeeper",
            "s6": "Shopkeeper",
            "s7": "Shopkeeper",
            "s8": "Shopkeeper",
            "s9": "Lady",
            "s10": "Lady",
            "s11": "Shopkeeper",
            "s12": "Lady",
            "s13": "Shopkeeper",
            "s14": "Lady",
            "s15": "Lady",
            "s16": "Shopkeeper",
            "s17": "Lady",
            "s18": "Shopkeeper",
            "s19": "Lady",
        },
        "images": {
            "s1": "/images/nce1/l59/scene1.png",
            "s10": "/images/nce1/l59/buying_glue.png",
            "s13": "/images/nce1/l59/no_chalk.png",
            "s19": "/images/nce1/l59/forgetting_change.png",
        },
    },
)

print("Batch 3 Updates Done.")
