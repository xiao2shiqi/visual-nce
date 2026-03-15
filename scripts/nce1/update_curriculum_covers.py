import json

path = "src/data/curriculum.json"
with open(path, "r", encoding="utf-8") as f:
    cur = json.load(f)

lessons_to_update = [
    "nce1-l37",
    "nce1-l39",
    "nce1-l41",
    "nce1-l43",
    "nce1-l45",
    "nce1-l47",
    "nce1-l49",
    "nce1-l51",
    "nce1-l53",
    "nce1-l55",
    "nce1-l57",
    "nce1-l59",
]

for book in cur["books"]:
    if book["id"] == "nce1":
        for lesson in book["lessons"]:
            if lesson["id"] in lessons_to_update:
                lid_short = lesson["id"].split("-")[1]
                lesson["image"] = f"/images/nce1/{lid_short}/scene1.png"

with open(path, "w", encoding="utf-8") as f:
    json.dump(cur, f, indent=2, ensure_ascii=False)

print("Curriculum updated.")
