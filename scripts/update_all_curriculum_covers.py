import json

path = "src/data/curriculum.json"
with open(path, "r", encoding="utf-8") as f:
    cur = json.load(f)

for book in cur["books"]:
    if book["id"] in ["nce1", "nce2"]:
        for lesson in book["lessons"]:
            lid_short = lesson["id"].split("-")[1]
            lesson["image"] = f"/images/{book['id']}/{lid_short}/scene1.png"

with open(path, "w", encoding="utf-8") as f:
    json.dump(cur, f, indent=2, ensure_ascii=False)

print("Curriculum covers updated for all NCE 1 & 2.")
