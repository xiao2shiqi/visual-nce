import json
import os


def process_file(path, updates):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Stable opening: remove image from intro
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


# L37
process_file(
    "src/data/lessons/nce1-l37.json",
    {
        "roles": {
            "s1": "Dan",
            "s2": "Dan",
            "s3": "George",
            "s4": "George",
            "s5": "Dan",
            "s6": "George",
            "s7": "Dan",
            "s8": "George",
            "s9": "Dan",
            "s10": "George",
            "s11": "Dan",
            "s12": "George",
            "s13": "Dan",
            "s14": "George",
            "s15": "Dan",
            "s16": "George",
            "s17": "Dan",
            "s18": "George",
        },
        "images": {
            "s1": "/images/nce1/l37/scene1.png",
            "s4": "/images/nce1/l37/hammer.png",
            "s12": "/images/nce1/l37/painting_pink.png",
        },
    },
)

# L39
process_file(
    "src/data/lessons/nce1-l39.json",
    {
        "roles": {
            "s1": "Sam",
            "s2": "Penny",
            "s3": "Sam",
            "s4": "Sam",
            "s5": "Penny",
            "s6": "Sam",
            "s7": "Penny",
            "s8": "Penny",
            "s9": "Penny",
            "s10": "Sam",
            "s11": "Penny",
            "s12": "Sam",
        },
        "images": {
            "s1": "/images/nce1/l39/scene1.png",
            "s8": "/images/nce1/l39/vase_shelf.png",
        },
    },
)

# L41
process_file(
    "src/data/lessons/nce1-l41.json",
    {
        "roles": {
            "s1": "Sam",
            "s2": "Penny",
            "s3": "Sam",
            "s4": "Penny",
            "s5": "Sam",
            "s6": "Penny",
            "s7": "Sam",
            "s8": "Penny",
            "s9": "Sam",
            "s10": "Penny",
            "s11": "Sam",
            "s12": "Penny",
            "s13": "Sam",
            "s14": "Penny",
            "s15": "Sam",
            "s16": "Penny",
        },
        "images": {
            "s1": "/images/nce1/l41/scene1.png",
            "s6": "/images/nce1/l41/bag_contents.png",
        },
    },
)

# L43
process_file(
    "src/data/lessons/nce1-l43.json",
    {
        "roles": {
            "s1": "Penny",
            "s2": "Sam",
            "s3": "Penny",
            "s4": "Sam",
            "s5": "Penny",
            "s6": "Sam",
            "s7": "Penny",
            "s8": "Sam",
            "s9": "Penny",
            "s10": "Sam",
            "s11": "Penny",
            "s12": "Sam",
            "s13": "Penny",
            "s14": "Sam",
            "s15": "Penny",
            "s16": "Sam",
            "s17": "Penny",
        },
        "images": {
            "s1": "/images/nce1/l43/scene1.png",
            "s5": "/images/nce1/l43/kitchen_search.png",
            "s12": "/images/nce1/l43/kettle_boiling.png",
        },
    },
)

print("Batch 1 Updates Done.")
