#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 43: Hurry Up
# Story: Penny asks Sam to make tea. Sam checks the kettle for water.
# Sam searches for the tea behind the teapot — can't find it until Penny points.
# They find cups in the cupboard. The kettle boils — "Hurry up, Sam!"
# Characters: SAM (man), PENNY (woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British kitchen light, cosy domestic mood. "
)

SCENE = (
    "Location: a cosy 1960s British kitchen — "
    "a gas cooker/hob with a whistling kettle on it, wooden kitchen cupboards above, "
    "a wooden counter with a brown ceramic teapot, "
    "patterned wallpaper or tiles, warm overhead lamp light. "
    "Keep the gas cooker, wooden cupboards, brown teapot, and warm kitchen light consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_SAM = (
    "Character SAM: a friendly British man, approximately 30-35 years old, "
    "short neatly combed dark hair, warm pleasant face, "
    "wearing a white shirt with a light brown V-neck sweater and dark trousers. "
    "CRITICAL: white shirt + light brown V-neck sweater + dark trousers + short dark hair — NEVER change. "
)

CHAR_PENNY = (
    "Character PENNY: a pleasant British woman, approximately 28-33 years old, "
    "short wavy chestnut hair, expressive and animated face, "
    "wearing a light blue blouse and a floral apron. "
    "CRITICAL: chestnut wavy hair + light blue blouse + floral apron — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the cosy 1960s British kitchen. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) "
            "stands near the kitchen doorway, looking at SAM with a pleasant request — "
            "'Can you make the tea?' "
            "SAM (white shirt, light brown V-neck sweater) stands in the kitchen "
            "with a willing, ready expression — 'Yes, of course I can!' "
            "The kitchen is clearly visible — gas cooker with kettle on it, "
            "wooden cupboards, brown teapot on the counter. "
            "CRITICAL: EXACTLY TWO people — Penny asking + Sam responding willingly. "
            "Show both characters clearly. Warm cosy kitchen atmosphere."
        ),
    },
    {
        "id": "checking_kettle",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the kettle on the cooker. "
            "SAM (white shirt, light brown V-neck sweater) stands at the gas cooker, "
            "lifting the KETTLE slightly and peering inside or shaking it gently "
            "to check if there is water — his head tilted with a questioning look. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) "
            "stands nearby, nodding reassuringly — 'Yes, there is.' "
            "The GAS COOKER and KETTLE are the focal elements. "
            "The kettle is a classic 1960s British metal kettle. "
            "CRITICAL: EXACTLY TWO people — Sam checking the kettle + Penny confirming. "
            "Do NOT show the full room — focus on the cooker and kettle area."
        ),
    },
    {
        "id": "kitchen_search",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the kitchen counter area. "
            "SAM (white shirt, light brown V-neck sweater) stands at the counter "
            "looking confused and searching — peering around the BROWN CERAMIC TEAPOT "
            "and behind it, trying to find the tea. "
            "His expression shows puzzled searching — 'Where's the tea?' "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands beside him "
            "leaning forward and pointing directly at a small PLAIN TIN or caddy "
            "sitting right IN FRONT OF Sam — it's obvious but Sam keeps missing it. "
            "Penny's expression is amused and exasperated — 'It's in front of you!' "
            "The BROWN TEAPOT and the SMALL TEA CADDY in front of Sam are the focal props. "
            "CRITICAL: EXACTLY TWO people — Sam searching confusedly + Penny pointing at obvious tea. "
            "Do NOT show the full room. No text on any container."
        ),
    },
    {
        "id": "finding_cups",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the kitchen cupboard area. "
            "SAM (white shirt, light brown V-neck sweater) stands on tiptoe "
            "reaching into an OPEN WOODEN KITCHEN CUPBOARD above the counter, "
            "pulling out TWO or THREE plain ceramic cups with a satisfied expression — "
            "'Here they are!' "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands nearby "
            "watching with a pleased, approving expression. "
            "The OPEN CUPBOARD with cups inside, and Sam reaching for them, are the focal elements. "
            "CRITICAL: EXACTLY TWO people — Sam finding cups in cupboard + Penny watching. "
            "Do NOT show the full room. No text or labels on any cups or cupboard."
        ),
    },
    {
        "id": "kettle_boiling",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the cooker and the boiling kettle. "
            "On the GAS COOKER: the KETTLE is clearly BOILING — "
            "steam visibly billowing from the kettle spout, the kettle vibrating slightly. "
            "SAM (white shirt, light brown V-neck sweater) stands at the cooker "
            "ready to pour, looking back over his shoulder with a triumphant expression — "
            "'The kettle's boiling!' "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands nearby "
            "with hands raised in a hurrying gesture — 'Hurry up, Sam!' "
            "The BOILING KETTLE with STEAM is the dominant visual element. "
            "CRITICAL: EXACTLY TWO people — Sam at the boiling kettle + Penny urging him to hurry. "
            "The steam from the kettle should be clearly visible."
        ),
    },
]
