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
    "l61": {"images": {"s1": "scene1", "s5": "astronaut_repair", "s10": "clear_view"}},
    "l62": {"images": {"s1": "scene1", "s5": "finding_safe", "s10": "opening_safe"}},
    "l63": {"images": {"s1": "scene1", "s5": "spilling_drink", "s10": "apologizing"}},
    "l64": {
        "images": {"s1": "scene1", "s5": "workers_meeting", "s10": "train_passing"}
    },
    "l65": {"images": {"s1": "scene1", "s5": "jumbo_escaping", "s10": "jumbo_stopped"}},
    "l66": {"images": {"s1": "scene1", "s5": "getting_stung", "s10": "eating_honey"}},
    "l67": {
        "images": {"s1": "scene1", "s5": "scientists_observing", "s10": "lava_flow"}
    },
    "l68": {"images": {"s1": "scene1", "s5": "persistent_effort", "s10": "jar_opens"}},
    "l69": {"images": {"s1": "scene1", "s5": "seeing_land", "s10": "landing_on_beach"}},
    "l70": {"images": {"s1": "scene1", "s5": "finding_gold", "s10": "shark_appearing"}},
    "l71": {"images": {"s1": "scene1", "s5": "clock_face", "s10": "interior_bells"}},
    "l72": {
        "images": {
            "s1": "scene1",
            "s5": "high_speed_run",
            "s10": "campbell_celebrating",
        }
    },
    "l73": {
        "images": {"s1": "scene1", "s5": "leading_runner", "s10": "breaking_record"}
    },
    "l74": {"images": {"s1": "scene1", "s5": "fans_waiting", "s10": "singing_at_home"}},
    "l75": {
        "images": {"s1": "scene1", "s5": "helicopter_rescue", "s10": "safe_on_land"}
    },
    "l76": {"images": {"s1": "scene1", "s5": "friend_tricked", "s10": "another_trick"}},
    "l77": {
        "images": {
            "s1": "scene1",
            "s5": "surgeons_working",
            "s10": "patient_recovering",
        }
    },
    "l78": {
        "images": {"s1": "scene1", "s5": "buying_last_one", "s10": "clock_at_home"}
    },
    "l79": {
        "images": {
            "s1": "scene1",
            "s5": "view_above_clouds",
            "s10": "arriving_sunny_place",
        }
    },
    "l80": {"images": {"s1": "scene1", "s5": "inside_palace", "s10": "fire_scene"}},
}

for lid, cfg in CONFIG.items():
    update_lesson(lid, cfg["images"])
print("NCE 2 Batch 4 JSONs updated.")
