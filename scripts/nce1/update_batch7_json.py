import json, os


def update_lesson(lid, image_map, roles_map=None):
    path = f"src/data/lessons/nce1-{lid}.json"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["image"] = f"/images/nce1/{lid}/scene1.png"
    for seg in data["segments"]:
        sid = seg["id"]
        if sid.startswith("intro"):
            if "image" in seg:
                del seg["image"]
            continue
        if roles_map and sid in roles_map:
            seg["role"] = roles_map[sid]
        target_num = int(sid[1:])
        best_num = -1
        current_img = f"/images/nce1/{lid}/scene1.png"
        for start_sid, img_name in image_map.items():
            start_num = int(start_sid[1:])
            if start_num <= target_num and start_num > best_num:
                best_num = start_num
                current_img = f"/images/nce1/{lid}/{img_name}.png"
        seg["image"] = current_img
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


CONFIG = {
    "l109": {
        "images": {"s1": "scene1", "s8": "coffee_chat", "s15": "walking_out"},
        "roles": {f"s{i}": "Charlotte" if i % 2 != 0 else "Jane" for i in range(1, 20)},
    },
    "l111": {
        "images": {"s1": "scene1", "s8": "engine_view", "s15": "signing_papers"},
        "roles": {
            f"s{i}": "Mr. Saville" if i % 2 != 0 else "Assistant" for i in range(1, 20)
        },
    },
    "l113": {
        "images": {"s1": "scene1", "s8": "no_change", "s15": "change_found"},
        "roles": {
            f"s{i}": "Conductor" if i % 2 != 0 else "Mr. Scott" for i in range(1, 20)
        },
    },
    "l115": {
        "images": {"s1": "scene1", "s8": "opening_door", "s15": "neighbor_talk"},
        "roles": {f"s{i}": "Jim" if i % 2 != 0 else "Helen" for i in range(1, 20)},
    },
    "l117": {
        "images": {"s1": "scene1", "s8": "messy_eating", "s15": "finished_breakfast"},
        "roles": {f"s{i}": "Tommy" if i % 2 != 0 else "Mother" for i in range(1, 20)},
    },
    "l119": {
        "images": {"s1": "scene1", "s8": "strange_noise", "s15": "mystery_solved"},
        "roles": {},
    },
    "l121": {
        "images": {"s1": "scene1", "s8": "pointing_crowd", "s15": "close_up_hat"},
        "roles": {},
    },
    "l123": {
        "images": {"s1": "scene1", "s8": "view_of_sydney", "s15": "booking_trip"},
        "roles": {f"s{i}": "Traveler" if i % 2 != 0 else "Agent" for i in range(1, 20)},
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"], cfg.get("roles"))
print("Batch 7 JSONs updated.")
