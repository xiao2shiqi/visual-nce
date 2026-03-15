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
        try:
            target_num = int(sid[1:])
        except:
            target_num = 0
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
    "l125": {
        "images": {"s1": "scene1", "s8": "tea_pour", "s15": "cookies"},
        "roles": {f"s{i}": "Susan" if i % 2 != 0 else "Terrence" for i in range(1, 20)},
    },
    "l127": {
        "images": {"s1": "scene1", "s8": "interview", "s15": "signing_autograph"},
        "roles": {},
    },
    "l129": {
        "images": {"s1": "scene1", "s8": "police_chase", "s15": "ticketed"},
        "roles": {f"s{i}": "Gary" if i % 2 != 0 else "Policeman" for i in range(1, 20)},
    },
    "l131": {
        "images": {"s1": "scene1", "s8": "winning_moment", "s15": "cheers"},
        "roles": {},
    },
    "l133": {
        "images": {"s1": "scene1", "s8": "reporter_live", "s15": "shocked_faces"},
        "roles": {},
    },
    "l135": {
        "images": {"s1": "scene1", "s8": "pointing_report", "s15": "shaking_hands"},
        "roles": {
            f"s{i}": "Headmaster" if i % 2 != 0 else "Student" for i in range(1, 20)
        },
    },
    "l137": {
        "images": {"s1": "scene1", "s8": "dream_island", "s15": "talking_dream"},
        "roles": {f"s{i}": "Julie" if i % 2 != 0 else "Husband" for i in range(1, 20)},
    },
    "l139": {
        "images": {"s1": "scene1", "s8": "john_arrives", "s15": "laughing_together"},
        "roles": {f"s{i}": "Mary" if i % 2 != 0 else "John" for i in range(1, 20)},
    },
    "l141": {
        "images": {"s1": "scene1", "s8": "passing_scenery", "s15": "arrival"},
        "roles": {},
    },
    "l143": {
        "images": {"s1": "scene1", "s8": "finding_flowers", "s15": "woods_exit"},
        "roles": {},
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"], cfg.get("roles"))
print("Batch 8 JSONs updated.")
