import json
import os


def update_lesson(lid, image_map, role_map=None):
    path = f"src/data/lessons/nce1-{lid}.json"
    if not os.path.exists(path):
        print(f"Skipping {lid} (not found)")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update root image to always be scene1.png
    data["image"] = f"/images/nce1/{lid}/scene1.png"

    for seg in data["segments"]:
        sid = seg["id"]

        # Stable opening: remove image from intro segments
        if sid.startswith("intro"):
            if "image" in seg:
                del seg["image"]
            continue

        # Role update if map provided
        if role_map and sid in role_map:
            seg["role"] = role_map[sid]

        # Image mapping
        # image_map is {sid_start: img_name}
        # Find the latest sid_start that is <= current sid (based on numeric part)
        current_img = f"/images/nce1/{lid}/scene1.png"

        # Parse numeric parts of IDs like 's1', 's10'
        def get_num(s):
            try:
                return int(s[1:])
            except:
                return 0

        target_num = get_num(sid)
        best_num = -1

        for start_sid, img_name in image_map.items():
            start_num = get_num(start_sid)
            if start_num <= target_num and start_num > best_num:
                best_num = start_num
                current_img = f"/images/nce1/{lid}/{img_name}.png"

        seg["image"] = current_img

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Define mappings for each lesson
# We want to switch images every few segments to keep it dynamic.

CONFIG = {
    "l37": {
        "images": {
            "s1": "scene1",
            "s2": "pointing_wood",
            "s4": "hammer",
            "s11": "painting_start",
            "s12": "painting_pink",
        }
    },
    "l39": {
        "images": {
            "s1": "scene1",
            "s2": "handing_vase",
            "s8": "vase_shelf",
            "s12": "successful_placement",
        }
    },
    "l41": {
        "images": {
            "s1": "scene1",
            "s4": "bag_on_chair",
            "s6": "cheese_bread",
            "s10": "soap_milk",
            "s15": "bag_contents",
        }
    },
    "l43": {
        "images": {
            "s1": "scene1",
            "s3": "checking_kettle",
            "s5": "kitchen_search",
            "s12": "finding_cups",
            "s16": "kettle_boiling",
        }
    },
    "l45": {
        "images": {
            "s1": "scene1",
            "s4": "handing_letter",
            "s9": "pamela_office",
            "s16": "terrible_handwriting",
        }
    },
    "l47": {
        "images": {
            "s1": "scene1",
            "s3": "ann_coffee",
            "s5": "sugar_no_milk",
            "s11": "biscuits",
        }
    },
    "l49": {
        "images": {
            "s1": "scene1",
            "s3": "showing_lamb",
            "s7": "steak_mince",
            "s11": "showing_chicken",
        }
    },
    "l51": {
        "images": {
            "s1": "scene1",
            "s5": "spring_windy",
            "s8": "summer_hot",
            "s11": "autumn_warm",
            "s14": "winter_snow",
        }
    },
    "l53": {
        "images": {
            "s1": "scene1",
            "s5": "north_cold",
            "s6": "east_windy",
            "s11": "west_wet",
            "s14": "south_warm",
        }
    },
    "l55": {
        "images": {
            "s1": "scene1",
            "s4": "housework",
            "s6": "lunch_noon",
            "s7": "housework_friends",
            "s13": "evening_tv",
        }
    },
    "l57": {
        "images": {
            "s1": "scene1",
            "s4": "mrs_sawyer_shops",
            "s7": "tea_garden",
            "s10": "children_playing",
            "s14": "mr_sawyer_book",
        }
    },
    "l59": {
        "images": {
            "s1": "scene1",
            "s4": "writing_paper",
            "s10": "buying_glue",
            "s13": "no_chalk",
            "s19": "forgetting_change",
        }
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"])

print("Dynamic JSON updates completed.")
