import json
import os


def update_l25():
    path = "src/data/lessons/nce1-l25.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Stable opening: remove image from intro
    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]
        seg["role"] = "Narrator"  # Descriptive lesson

        if seg["id"] == "s1":
            seg["image"] = "/images/nce1/l25/scene1.png"
        elif seg["id"] in ["s2", "s3", "s4"]:
            seg["image"] = "/images/nce1/l25/refrigerator.png"
        elif seg["id"] in ["s5", "s6", "s7"]:
            seg["image"] = "/images/nce1/l25/cooker.png"
        elif seg["id"] == "s8":
            seg["image"] = "/images/nce1/l25/table.png"
        elif seg["id"] in ["s9", "s10", "s11", "s12"]:
            seg["image"] = "/images/nce1/l25/bottle_cup.png"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_l27():
    path = "src/data/lessons/nce1-l27.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]
        seg["role"] = "Narrator"

        if seg["id"] == "s1":
            seg["image"] = "/images/nce1/l27/scene1.png"
        elif seg["id"] in ["s2", "s3", "s4"]:
            seg["image"] = "/images/nce1/l27/tv_magazines.png"
        elif seg["id"] in ["s5", "s6"]:
            seg["image"] = "/images/nce1/l27/table_newspapers.png"
        elif seg["id"] in ["s7", "s8"]:
            seg["image"] = "/images/nce1/l27/armchairs.png"
        elif seg["id"] in ["s9", "s10", "s11"]:
            seg["image"] = "/images/nce1/l27/stereo_books.png"
        elif seg["id"] in ["s12", "s13"]:
            seg["image"] = "/images/nce1/l27/pictures_wall.png"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_l29():
    path = "src/data/lessons/nce1-l29.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]

        # Role mapping
        if seg["id"] in ["s1", "s2", "s3", "s5", "s6", "s7", "s8", "s9"]:
            seg["role"] = "Mrs. Jones"
        elif seg["id"] == "s4":
            seg["role"] = "Amy"

        # Image mapping
        if seg["id"] == "s1":
            seg["image"] = "/images/nce1/l29/scene1.png"
        elif seg["id"] == "s2":
            seg["image"] = "/images/nce1/l29/shut_door.png"
        elif seg["id"] == "s5":
            seg["image"] = "/images/nce1/l29/air_room.png"
        elif seg["id"] == "s6":
            seg["image"] = "/images/nce1/l29/wardrobe.png"
        elif seg["id"] == "s7":
            seg["image"] = "/images/nce1/l29/make_bed.png"
        elif seg["id"] == "s9":
            seg["image"] = "/images/nce1/l29/sweep_floor.png"
        elif seg["id"] in ["s3", "s4", "s8"]:
            # Use scene1 for generic untidy bedroom shots
            seg["image"] = "/images/nce1/l29/scene1.png"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_l31():
    path = "src/data/lessons/nce1-l31.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]

        # Role mapping
        if seg["id"] in ["s1", "s3", "s5", "s8", "s9", "s11"]:
            seg["role"] = "Jean"
        elif seg["id"] in ["s2", "s4", "s6", "s7", "s10", "s12", "s14"]:
            seg["role"] = "Jack"
        elif seg["id"] == "s13":
            seg["role"] = "Jean"  # Jean observing dog

        # Image mapping
        if seg["id"] in ["s1", "s2", "s3"]:
            seg["image"] = "/images/nce1/l31/scene1.png"
        elif seg["id"] == "s4":
            seg["image"] = "/images/nce1/l31/sally_under_tree.png"
        elif seg["id"] in ["s5", "s6"]:
            seg["image"] = "/images/nce1/l31/scene1.png"
        elif seg["id"] in ["s7", "s8", "s9", "s10"]:
            seg["image"] = "/images/nce1/l31/tim_climbing.png"
        elif seg["id"] in ["s11", "s12"]:
            seg["image"] = "/images/nce1/l31/dog_running.png"
        elif seg["id"] in ["s13", "s14"]:
            seg["image"] = "/images/nce1/l31/dog_after_cat.png"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_l33():
    path = "src/data/lessons/nce1-l33.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]
        seg["role"] = "Narrator"

        if seg["id"] in ["s1", "s2", "s3", "s4"]:
            seg["image"] = "/images/nce1/l33/scene1.png"
        elif seg["id"] in ["s5", "s6"]:
            seg["image"] = "/images/nce1/l33/boats_on_river.png"
        elif seg["id"] in ["s7", "s8"]:
            seg["image"] = "/images/nce1/l33/sally_ship.png"
        elif seg["id"] in ["s9", "s10"]:
            seg["image"] = "/images/nce1/l33/tim_aeroplane.png"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_l35():
    path = "src/data/lessons/nce1-l35.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for seg in data["segments"]:
        if seg["id"].startswith("intro"):
            if "image" in seg:
                del seg["image"]
        seg["role"] = "Narrator"

        if seg["id"] in ["s1", "s2", "s3", "s4", "s5"]:
            seg["image"] = "/images/nce1/l35/scene1.png"
        elif seg["id"] in ["s6", "s7"]:
            seg["image"] = "/images/nce1/l35/walking_bank.png"
        elif seg["id"] in ["s8", "s9"]:
            seg["image"] = "/images/nce1/l35/boy_swimming.png"
        elif seg["id"] in ["s10", "s11", "s12"]:
            seg["image"] = "/images/nce1/l35/school_park.png"
        elif seg["id"] in ["s13", "s14", "s15"]:
            seg["image"] = "/images/nce1/l35/children_action.png"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    update_l25()
    update_l27()
    update_l29()
    update_l31()
    update_l33()
    update_l35()
    print("Updates completed successfully.")
