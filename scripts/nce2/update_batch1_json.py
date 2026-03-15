import json, os


def update_lesson(lid, image_map, roles_map=None):
    path = f"src/data/lessons/nce2-{lid}.json"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["image"] = f"/images/nce2/{lid}/scene1.png"
    for seg in data["segments"]:
        sid = seg["id"]
        if sid.startswith("intro"):
            if "image" in seg:
                del seg["image"]
            continue
        if roles_map and sid in roles_map:
            seg["role"] = roles_map[sid]

        # Numeric target for NCE2 might be different, let's just use string mapping for specific IDs
        if sid in image_map:
            seg["image"] = f"/images/nce2/{lid}/{image_map[sid]}.png"
        else:
            # Simple inheritance for segments between mapped ones
            target_num = int(sid[1:])
            best_num = -1
            current_img = f"/images/nce2/{lid}/scene1.png"
            for start_sid, img_name in image_map.items():
                start_num = int(start_sid[1:])
                if start_num <= target_num and start_num > best_num:
                    best_num = start_num
                    current_img = f"/images/nce2/{lid}/{img_name}.png"
            seg["image"] = current_img

    # Cleanup potential redundant fields
    if "thumbnail" in data:
        del data["thumbnail"]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


CONFIG = {
    "l1": {"images": {"s1": "scene1", "s4": "angry_narrator", "s10": "turning_round"}},
    "l2": {
        "images": {"s1": "scene1", "s5": "aunt_lucy_phone", "s10": "breakfast_lunch"}
    },
    "l3": {"images": {"s1": "scene1", "s5": "writing_cards", "s10": "postcards_final"}},
    "l4": {"images": {"s1": "scene1", "s5": "flying_high", "s10": "scared_narrator"}},
    "l5": {"images": {"s1": "scene1", "s5": "wrong_number", "s10": "pigeon_post"}},
    "l6": {"images": {"s1": "scene1", "s5": "thompson_food", "s10": "percy_working"}},
    "l7": {"images": {"s1": "scene1", "s5": "thief_caught", "s10": "diamonds_found"}},
    "l8": {"images": {"s1": "scene1", "s5": "neighbors_jealous", "s10": "joe_proud"}},
    "l9": {"images": {"s1": "scene1", "s5": "brother_waiting", "s10": "warm_fire"}},
    "l10": {
        "images": {"s1": "scene1", "s5": "broken_instrument", "s10": "modern_jazz"}
    },
    "l11": {"images": {"s1": "scene1", "s5": "friend_pays", "s10": "paying_back"}},
    "l12": {"images": {"s1": "scene1", "s5": "captain_ship", "s10": "return_home"}},
    "l13": {"images": {"s1": "scene1", "s5": "airport_arrival", "s10": "bus_ride"}},
    "l14": {
        "images": {"s1": "scene1", "s5": "trying_to_speak", "s10": "laughing_together"}
    },
    "l15": {"images": {"s1": "scene1", "s5": "good_news", "s10": "celebration"}},
    "l16": {"images": {"s1": "scene1", "s5": "polite_request", "s10": "driving_away"}},
    "l17": {"images": {"s1": "scene1", "s5": "telling_truth", "s10": "always_young"}},
    "l18": {"images": {"s1": "scene1", "s5": "strange_habit", "s10": "explaining"}},
    "l19": {"images": {"s1": "scene1", "s5": "pleading", "s10": "lucky_break"}},
    "l20": {"images": {"s1": "scene1", "s5": "struggling", "s10": "success"}},
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"])
print("NCE 2 Batch 1 JSONs updated.")
