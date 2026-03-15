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
    "l93": {
        "images": {"s1": "scene1", "s8": "neighbour_talk", "s15": "tea_invite"},
        "roles": {f"s{i}": "Nigel" if i % 2 != 0 else "Ian" for i in range(1, 20)},
    },
    "l95": {
        "images": {"s1": "scene1", "s8": "station_master", "s15": "boarding"},
        "roles": {f"s{i}": "George" if i % 2 != 0 else "Ken" for i in range(1, 20)},
    },
    "l97": {
        "images": {"s1": "scene1", "s8": "opening_case", "s15": "cleared"},
        "roles": {
            f"s{i}": "Mr. Hall" if i % 2 != 0 else "Officer" for i in range(1, 20)
        },
    },
    "l99": {
        "images": {"s1": "scene1", "s8": "falling", "s15": "safe_down"},
        "roles": {f"s{i}": "Andy" if i % 2 != 0 else "Lucy" for i in range(1, 20)},
    },
    "l101": {
        "images": {"s1": "scene1", "s8": "beach_scene", "s15": "writing_back"},
        "roles": {},
    },
    "l103": {
        "images": {"s1": "scene1", "s8": "talking_test", "s15": "studying"},
        "roles": {f"s{i}": "Gary" if i % 2 != 0 else "Richard" for i in range(1, 20)},
    },
    "l105": {
        "images": {"s1": "scene1", "s8": "typing_again", "s15": "final_check"},
        "roles": {f"s{i}": "Boss" if i % 2 != 0 else "Sandra" for i in range(1, 20)},
    },
    "l107": {
        "images": {
            "s1": "scene1",
            "s8": "assistant_brings_large",
            "s15": "happy_customer",
        },
        "roles": {f"s{i}": "Lady" if i % 2 != 0 else "Assistant" for i in range(1, 20)},
    },
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"], cfg.get("roles"))
print("Batch 6 JSONs updated.")
