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
    "l81": {"images": {"s1": "scene1", "s5": "climbing_wall", "s10": "running_free"}},
    "l82": {"images": {"s1": "scene1", "s5": "monster_head", "s10": "just_a_fish"}},
    "l83": {"images": {"s1": "scene1", "s5": "cheering_crowd", "s10": "new_office"}},
    "l84": {
        "images": {"s1": "scene1", "s5": "empty_streets", "s10": "returning_to_work"}
    },
    "l85": {
        "images": {"s1": "scene1", "s5": "talking_to_professor", "s10": "graduation"}
    },
    "l86": {
        "images": {"s1": "scene1", "s5": "pilot_struggling", "s10": "safe_landing"}
    },
    "l87": {"images": {"s1": "scene1", "s5": "alibi_photo", "s10": "walking_out"}},
    "l88": {
        "images": {"s1": "scene1", "s5": "rescue_drill", "s10": "emerging_to_light"}
    },
    "l89": {
        "images": {"s1": "scene1", "s5": "embarrassed_face", "s10": "laughing_it_off"}
    },
    "l90": {"images": {"s1": "scene1", "s5": "frying_fish", "s10": "eating_supper"}},
    "l91": {
        "images": {"s1": "scene1", "s5": "view_from_above", "s10": "landing_in_tree"}
    },
    "l92": {
        "images": {"s1": "scene1", "s5": "narrow_escape", "s10": "being_reprimanded"}
    },
    "l93": {"images": {"s1": "scene1", "s5": "opening_gift", "s10": "displaying_gift"}},
    "l94": {"images": {"s1": "scene1", "s5": "talented_boy", "s10": "team_photo"}},
    "l95": {"images": {"s1": "scene1", "s5": "talking_animal", "s10": "flying_carpet"}},
    "l96": {
        "images": {
            "s1": "scene1",
            "s5": "skeleton_appearing",
            "s10": "mystery_revealed",
        }
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"])
print("NCE 2 Batch 5 JSONs updated.")
