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
    "l77": {
        "images": {"s1": "scene1", "s8": "dentist_surgery", "s15": "extraction"},
        "roles": {
            f"s{i}": "Nurse" if i % 2 != 0 else "Mr. Crookes" for i in range(1, 20)
        },
    },
    "l79": {
        "images": {"s1": "scene1", "s8": "supermarket", "s15": "unpacking"},
        "roles": {},
    },
    "l81": {
        "images": {"s1": "scene1", "s8": "eating_beef", "s15": "dessert"},
        "roles": {},
    },
    "l83": {
        "images": {"s1": "scene1", "s8": "locked_suitcases", "s15": "taxi_arrives"},
        "roles": {f"s{i}": "Sam" if i % 2 != 0 else "Penny" for i in range(1, 20)},
    },
    "l85": {
        "images": {"s1": "scene1", "s8": "sidewalk_cafe", "s15": "notre_dame"},
        "roles": {},
    },
    "l87": {
        "images": {"s1": "scene1", "s8": "policeman_notes", "s15": "tow_truck"},
        "roles": {
            f"s{i}": "Mr. Wood" if i % 2 != 0 else "Policeman" for i in range(1, 20)
        },
    },
    "l89": {
        "images": {"s1": "scene1", "s8": "garden_view", "s15": "inside_house"},
        "roles": {f"s{i}": "Nigel" if i % 2 != 0 else "Ian" for i in range(1, 20)},
    },
    "l91": {
        "images": {"s1": "scene1", "s8": "catherine_visits", "s15": "ian_reading"},
        "roles": {f"s{i}": "Ian" if i % 2 != 0 else "Catherine" for i in range(1, 20)},
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"], cfg.get("roles"))
print("Batch 5 JSONs updated.")
