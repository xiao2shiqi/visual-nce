import json


def set_all_narrator(lid):
    path = f"src/data/lessons/nce1-{lid}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for seg in data["segments"]:
        seg["role"] = "Narrator"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


set_all_narrator("l55")
set_all_narrator("l57")
print("L55/L57 set to Narrator.")
