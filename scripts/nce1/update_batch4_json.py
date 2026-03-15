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
    "l61": {
        "images": {"s1": "scene1", "s10": "doctor_arrives", "s15": "medicine"},
        "roles": {
            f"s{i}": "Mrs. Williams" if i % 2 != 0 else "Doctor" for i in range(1, 20)
        },
    },
    "l63": {
        "images": {"s1": "scene1", "s8": "jimmy_up", "s15": "doctor_leaving"},
        "roles": {
            f"s{i}": "Doctor" if i % 2 != 0 else "Mrs. Williams" for i in range(1, 20)
        },
    },
    "l65": {
        "images": {"s1": "scene1", "s8": "key_exchange", "s12": "jill_smiling"},
        "roles": {f"s{i}": "Jill" if i % 2 != 0 else "Jack" for i in range(1, 15)},
    },
    "l67": {
        "images": {"s1": "scene1", "s10": "mowing_lawn", "s15": "tea_time"},
        "roles": {},
    },
    "l69": {
        "images": {"s1": "scene1", "s5": "cars_speeding", "s10": "finish_line"},
        "roles": {},
    },
    "l71": {
        "images": {"s1": "scene1", "s8": "jane_pointing", "s15": "ron_working"},
        "roles": {f"s{i}": "Jane" if i % 2 != 0 else "Ron" for i in range(1, 20)},
    },
    "l73": {
        "images": {"s1": "scene1", "s8": "pointing_way", "s15": "walking_away"},
        "roles": {
            f"s{i}": "Stranger" if i % 2 != 0 else "Local Man" for i in range(1, 20)
        },
    },
    "l75": {
        "images": {"s1": "scene1", "s8": "trying_shoes", "s15": "choosing_another"},
        "roles": {f"s{i}": "Lady" if i % 2 != 0 else "Assistant" for i in range(1, 20)},
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"], cfg.get("roles"))
print("Batch 4 JSONs updated.")
