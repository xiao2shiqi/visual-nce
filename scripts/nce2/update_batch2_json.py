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
    "l21": {"images": {"s1": "scene1", "s5": "aeroplane_shaking", "s10": "party_talk"}},
    "l22": {"images": {"s1": "scene1", "s5": "finding_bottle", "s10": "reading_note"}},
    "l23": {
        "images": {"s1": "scene1", "s5": "pointing_rooms", "s10": "completed_house"}
    },
    "l24": {
        "images": {"s1": "scene1", "s5": "splashed_by_car", "s10": "friend_laughing"}
    },
    "l25": {
        "images": {"s1": "scene1", "s5": "talking_to_porter", "s10": "understanding"}
    },
    "l26": {
        "images": {"s1": "scene1", "s5": "critic_explaining", "s10": "child_painting"}
    },
    "l27": {"images": {"s1": "scene1", "s5": "lost_in_rain", "s10": "finding_hotel"}},
    "l28": {
        "images": {"s1": "scene1", "s5": "jasper_arriving", "s10": "jasper_explaining"}
    },
    "l29": {
        "images": {
            "s1": "scene1",
            "s5": "flying_over_mountains",
            "s10": "landing_safely",
        }
    },
    "l30": {
        "images": {"s1": "scene1", "s5": "falling_off_horse", "s10": "talking_sports"}
    },
    "l31": {"images": {"s1": "scene1", "s5": "working_hard", "s10": "success_office"}},
    "l32": {
        "images": {"s1": "scene1", "s5": "detective_watching", "s10": "store_exit"}
    },
    "l33": {"images": {"s1": "scene1", "s5": "entering_cave", "s10": "seeing_light"}},
    "l34": {"images": {"s1": "scene1", "s5": "washing_dishes", "s10": "wife_returns"}},
    "l35": {
        "images": {"s1": "scene1", "s5": "narrator_waking", "s10": "police_arriving"}
    },
    "l36": {
        "images": {"s1": "scene1", "s5": "swimming_hard", "s10": "reaching_france"}
    },
    "l37": {"images": {"s1": "scene1", "s5": "running_race", "s10": "medal_ceremony"}},
    "l38": {"images": {"s1": "scene1", "s5": "palm_trees_wind", "s10": "sunset_beach"}},
    "l39": {"images": {"s1": "scene1", "s5": "doctor_checkup", "s10": "all_right_now"}},
    "l40": {
        "images": {"s1": "scene1", "s5": "mrs_rumbold_talking", "s10": "funny_story"}
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"])
print("NCE 2 Batch 2 JSONs updated.")
