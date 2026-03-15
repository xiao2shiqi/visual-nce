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

        if sid in image_map:
            seg["image"] = f"/images/nce2/{lid}/{image_map[sid]}.png"
        else:
            try:
                target_num = int(sid[1:])
            except:
                target_num = 0
            best_num = -1
            current_img = f"/images/nce2/{lid}/scene1.png"
            for start_sid, img_name in image_map.items():
                try:
                    start_num = int(start_sid[1:])
                except:
                    continue
                if start_num <= target_num and start_num > best_num:
                    best_num = start_num
                    current_img = f"/images/nce2/{lid}/{img_name}.png"
            seg["image"] = current_img
    if "thumbnail" in data:
        del data["thumbnail"]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


CONFIG = {
    "l41": {
        "images": {"s1": "scene1", "s5": "husband_laughing", "s10": "hat_on_table"}
    },
    "l42": {
        "images": {"s1": "scene1", "s5": "neighbor_knocking", "s10": "piano_delivery"}
    },
    "l43": {
        "images": {"s1": "scene1", "s5": "dropping_supplies", "s10": "explorer_waving"}
    },
    "l44": {
        "images": {"s1": "scene1", "s5": "seeing_something", "s10": "finding_treasure"}
    },
    "l45": {
        "images": {"s1": "scene1", "s5": "returning_wallet", "s10": "sam_whistling"}
    },
    "l46": {
        "images": {"s1": "scene1", "s5": "car_breaking_down", "s10": "walking_home"}
    },
    "l47": {
        "images": {"s1": "scene1", "s5": "ghost_drinking", "s10": "ghost_disappearing"}
    },
    "l48": {
        "images": {"s1": "scene1", "s5": "friend_ignoring", "s10": "friend_leaving"}
    },
    "l49": {"images": {"s1": "scene1", "s5": "falling_dream", "s10": "waking_up"}},
    "l50": {
        "images": {"s1": "scene1", "s5": "fast_driving", "s10": "arriving_destination"}
    },
    "l51": {
        "images": {"s1": "scene1", "s5": "finding_money", "s10": "handing_to_police"}
    },
    "l52": {
        "images": {"s1": "scene1", "s5": "dog_on_carpet", "s10": "cleaning_carpet"}
    },
    "l53": {
        "images": {
            "s1": "scene1",
            "s5": "narrator_seeing_snake",
            "s10": "snake_slithering",
        }
    },
    "l54": {"images": {"s1": "scene1", "s5": "mother_shocked", "s10": "bath_time"}},
    "l55": {
        "images": {"s1": "scene1", "s5": "finding_nothing", "s10": "finding_old_coin"}
    },
    "l56": {"images": {"s1": "scene1", "s5": "jet_in_sky", "s10": "pilot_smiling"}},
    "l57": {
        "images": {
            "s1": "scene1",
            "s5": "sitting_in_car",
            "s10": "assistant_explaining",
        }
    },
    "l58": {
        "images": {"s1": "scene1", "s5": "old_friend_arrives", "s10": "happy_ride"}
    },
    "l59": {"images": {"s1": "scene1", "s5": "dog_wants_in", "s10": "dog_indecisive"}},
    "l60": {"images": {"s1": "scene1", "s5": "reading_palm", "s10": "future_vision"}},
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"])
print("NCE 2 Batch 3 JSONs updated.")
