import json


def set_roles(lid, mapping):
    path = f"src/data/lessons/nce1-{lid}.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for seg in data["segments"]:
        if seg["id"] in mapping:
            seg["role"] = mapping[seg["id"]]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# L37
set_roles(
    "l37",
    {
        "s1": "Dan",
        "s2": "Dan",
        "s3": "George",
        "s4": "George",
        "s5": "Dan",
        "s6": "Dan",
        "s7": "George",
        "s8": "George",
        "s9": "Dan",
        "s10": "George",
        "s11": "Dan",
        "s12": "George",
        "s13": "Dan",
        "s14": "George",
        "s15": "Dan",
        "s16": "George",
        "s17": "Dan",
        "s18": "George",
    },
)

# L39
set_roles(
    "l39",
    {
        "s1": "Sam",
        "s2": "Penny",
        "s3": "Penny",
        "s4": "Penny",
        "s5": "Sam",
        "s6": "Sam",
        "s7": "Penny",
        "s8": "Penny",
        "s9": "Penny",
        "s10": "Sam",
        "s11": "Penny",
        "s12": "Sam",
    },
)

# L41
set_roles(
    "l41",
    {
        "s1": "Sam",
        "s2": "Penny",
        "s3": "Sam",
        "s4": "Penny",
        "s5": "Sam",
        "s6": "Penny",
        "s7": "Penny",
        "s8": "Penny",
        "s9": "Penny",
        "s10": "Penny",
        "s11": "Penny",
        "s12": "Penny",
        "s13": "Penny",
        "s14": "Penny",
        "s15": "Penny",
        "s16": "Sam",
    },
)  # Actually Penny lists the items mostly.

# L43
set_roles(
    "l43",
    {
        "s1": "Penny",
        "s2": "Sam",
        "s3": "Sam",
        "s4": "Penny",
        "s5": "Sam",
        "s6": "Penny",
        "s7": "Sam",
        "s8": "Penny",
        "s9": "Sam",
        "s10": "Penny",
        "s11": "Sam",
        "s12": "Penny",
        "s13": "Sam",
        "s14": "Penny",
        "s15": "Sam",
        "s16": "Penny",
        "s17": "Sam",
    },
)

# L45 (Already checked, but re-applying)
set_roles(
    "l45",
    {
        "s1": "Boss",
        "s2": "Bob",
        "s3": "Boss",
        "s4": "Bob",
        "s5": "Bob",
        "s6": "Boss",
        "s7": "Boss",
        "s8": "Bob",
        "s9": "Bob",
        "s10": "Pamela",
        "s11": "Bob",
        "s12": "Pamela",
        "s13": "Pamela",
        "s14": "Bob",
        "s15": "Bob",
        "s16": "Pamela",
        "s17": "Pamela",
        "s18": "Pamela",
    },
)

# L59
set_roles(
    "l59",
    {
        "s1": "Lady",
        "s2": "Shopkeeper",
        "s3": "Lady",
        "s4": "Lady",
        "s5": "Shopkeeper",
        "s6": "Shopkeeper",
        "s7": "Shopkeeper",
        "s8": "Shopkeeper",
        "s9": "Lady",
        "s10": "Lady",
        "s11": "Shopkeeper",
        "s12": "Lady",
        "s13": "Shopkeeper",
        "s14": "Lady",
        "s15": "Lady",
        "s16": "Shopkeeper",
        "s17": "Lady",
        "s18": "Shopkeeper",
        "s19": "Lady",
    },
)

print("Role corrections complete.")
