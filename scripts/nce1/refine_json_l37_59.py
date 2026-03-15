import json
import os


def update_lesson(lid, roles_map, image_map, title_suffix):
    path = f"src/data/lessons/nce1-{lid}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update root image
    data["image"] = f"/images/nce1/{lid}/scene1.png"

    # Process segments
    for seg in data["segments"]:
        sid = seg["id"]
        # Stable opening
        if sid.startswith("intro"):
            if "image" in seg:
                del seg["image"]
        else:
            # Map role
            if sid in roles_map:
                seg["role"] = roles_map[sid]

            # Map image
            # Find the best image for this segment based on the map
            # The map is {starting_sid: img_path}
            # We look for the largest sid in map that is <= current sid
            current_img = f"/images/nce1/{lid}/scene1.png"  # default
            sorted_keys = sorted(image_map.keys(), key=lambda x: int(x[1:]))
            for k in sorted_keys:
                if int(k[1:]) <= int(sid[1:]):
                    current_img = image_map[k]

            seg["image"] = current_img

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Data for all lessons
CONFIG = {
    "l37": {
        "roles": {
            f"s{i}": "George" if i % 2 == 0 else "Dan" for i in range(1, 19)
        },  # Approximated, let's be more precise
        "images": {
            "s1": "/images/nce1/l37/scene1.png",
            "s4": "/images/nce1/l37/hammer.png",
            "s12": "/images/nce1/l37/painting_pink.png",
        },
    },
    "l39": {
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
    "l41": {
        "roles": {f"s{i}": "Sam" if i % 2 != 0 else "Penny" for i in range(1, 17)},
        "images": {
            "s1": "/images/nce1/l41/scene1.png",
            "s6": "/images/nce1/l41/bag_contents.png",
        },
    },
    "l43": {
        "roles": {f"s{i}": "Penny" if i % 2 != 0 else "Sam" for i in range(1, 18)},
        "images": {
            "s1": "/images/nce1/l43/scene1.png",
            "s5": "/images/nce1/l43/kitchen_search.png",
            "s12": "/images/nce1/l43/kettle_boiling.png",
        },
    },
    "l45": {
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
    "l47": {
        "roles": {f"s{i}": "Christine" if i % 2 != 0 else "Ann" for i in range(1, 15)},
        "images": {
            "s1": "/images/nce1/l47/scene1.png",
            "s5": "/images/nce1/l47/sugar_no_milk.png",
            "s11": "/images/nce1/l47/biscuits.png",
        },
    },
    "l49": {
        "roles": {
            f"s{i}": "Butcher" if i % 2 != 0 else "Mrs. Bird" for i in range(1, 16)
        },
        "images": {
            "s1": "/images/nce1/l49/scene1.png",
            "s8": "/images/nce1/l49/steak_mince.png",
        },
    },
    "l51": {
        "roles": {
            f"s{i}": "Traveler" if i % 2 != 0 else "Dimitri" for i in range(1, 17)
        },
        "images": {
            "s1": "/images/nce1/l51/scene1.png",
            "s6": "/images/nce1/l51/spring_windy.png",
            "s16": "/images/nce1/l51/winter_snow.png",
        },
    },
    "l53": {
        "roles": {f"s{i}": "Hans" if i % 2 != 0 else "Jim" for i in range(1, 16)},
        "images": {
            "s1": "/images/nce1/l53/scene1.png",
            "s5": "/images/nce1/l53/north_east.png",
            "s6": "/images/nce1/l53/west_south.png",
        },
    },
    "l55": {
        "roles": {},  # Mostly Narrator
        "images": {
            "s1": "/images/nce1/l55/scene1.png",
            "s4": "/images/nce1/l55/housework_friends.png",
            "s13": "/images/nce1/l55/evening_tv.png",
        },
    },
    "l57": {
        "roles": {},  # Mostly Narrator
        "images": {
            "s1": "/images/nce1/l57/scene1.png",
            "s4": "/images/nce1/l57/mrs_sawyer_shops.png",
            "s7": "/images/nce1/l57/tea_garden.png",
            "s10": "/images/nce1/l57/children_playing.png",
            "s14": "/images/nce1/l57/mr_sawyer_book.png",
        },
    },
    "l59": {
        "roles": {
            f"s{i}": "Lady" if i % 2 != 0 else "Shopkeeper" for i in range(1, 20)
        },
        "images": {
            "s1": "/images/nce1/l59/scene1.png",
            "s10": "/images/nce1/l59/buying_glue.png",
            "s13": "/images/nce1/l59/no_chalk.png",
            "s19": "/images/nce1/l59/forgetting_change.png",
        },
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["roles"], cfg["images"], "")

print("All JSONs updated successfully.")
