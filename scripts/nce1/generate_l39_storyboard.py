#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 39: Don't Drop It!
# Story: Sam holds a beautiful vase and wants to put it on the table.
# Penny takes it from him — "Give it to me!"
# Sam wants to put it in front of the window. Penny says "Don't put it there!"
# Penny directs Sam to put it on the shelf.
# Sam places it successfully — they admire the lovely vase and flowers.
# Characters: SAM (man), PENNY (woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British home interior light, cosy domestic mood. "
)

SCENE = (
    "Location: a cosy 1960s British living room — "
    "a wooden shelf unit on one wall, a window with soft curtains, "
    "a small table with a vase on display, patterned wallpaper, "
    "a warm lamp casting golden light. "
    "Keep the wooden shelf, curtained window, patterned wallpaper, and warm lamp consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_SAM = (
    "Character SAM: a friendly British man, approximately 30-35 years old, "
    "short neatly combed dark hair, warm pleasant face, "
    "wearing a white shirt with a light brown V-neck sweater and dark trousers. "
    "CRITICAL: white shirt + light brown V-neck sweater + dark trousers + short dark hair — NEVER change. "
    "He carries a beautiful ceramic vase with care. "
)

CHAR_PENNY = (
    "Character PENNY: a pleasant British woman, approximately 28-33 years old, "
    "short wavy chestnut hair, expressive and animated face, "
    "wearing a light blue blouse and a floral apron. "
    "CRITICAL: chestnut wavy hair + light blue blouse + floral apron — NEVER change. "
    "She is clearly directing and protecting the vase with firm but fond authority. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the cosy 1960s British living room. "
            "SAM (white shirt, light brown sweater, dark trousers) stands in the centre "
            "holding a BEAUTIFUL CERAMIC VASE carefully with both hands, "
            "looking at it with a slightly puzzled expression — wondering where to put it. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands nearby, "
            "watching Sam with an attentive, slightly anxious expression. "
            "The wooden shelf unit is visible on the wall in the background. "
            "The curtained window lets in soft afternoon light. "
            "CRITICAL: EXACTLY TWO people — Sam holding the vase + Penny watching. "
            "The beautiful ceramic vase in Sam's hands is the focal prop. "
            "Show both characters clearly. Warm cosy living room atmosphere."
        ),
    },
    {
        "id": "handing_vase",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the vase handover between the two characters. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) "
            "reaches out firmly with both hands toward the BEAUTIFUL CERAMIC VASE, "
            "her expression protective and determined — 'Give it to me!' "
            "SAM (white shirt, light brown V-neck sweater) "
            "holds the vase out toward Penny with a slightly yielding expression, "
            "beginning to hand it over. "
            "The BEAUTIFUL CERAMIC VASE is the focal prop between their outstretched hands. "
            "CRITICAL: EXACTLY TWO people — Penny firmly taking the vase + Sam handing it over. "
            "The moment of handing the vase between them is the key visual action. "
            "Do NOT show the full room — focus on the two characters and the vase."
        ),
    },
    {
        "id": "vase_shelf",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the wooden shelf and the placement action. "
            "SAM (white shirt, light brown V-neck sweater) carefully reaches up "
            "to place the BEAUTIFUL CERAMIC VASE onto a WOODEN SHELF on the wall. "
            "His hands hold the vase gently as he positions it on the shelf. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands beside him, "
            "pointing at the EXACT SPOT on the shelf with one finger, "
            "guiding Sam with a firm but pleased expression — 'Put it here, on this shelf.' "
            "The WOODEN SHELF and the VASE being placed on it are the dominant visual elements. "
            "CRITICAL: EXACTLY TWO people — Sam carefully placing vase on shelf + Penny directing. "
            "The shelf with the vase being placed is the key visual action. "
            "Do NOT show the full room — focus on the shelf area, the vase, and both characters."
        ),
    },
    {
        "id": "successful_placement",
        "desc": (
            "Wide shot of the living room. "
            "The BEAUTIFUL CERAMIC VASE now sits perfectly on the WOODEN SHELF, "
            "filled with LOVELY COLOURFUL FLOWERS — roses and wildflowers in bloom — "
            "looking elegant and decorative on the shelf. "
            "SAM (white shirt, light brown V-neck sweater) and "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) "
            "both stand back, side by side, looking at the vase with admiration and satisfaction. "
            "Sam has a pleased smile; Penny looks content and happy. "
            "The VASE WITH LOVELY FLOWERS on the shelf is the visual centrepiece. "
            "Warm golden lamp light fills the cosy room. "
            "CRITICAL: EXACTLY TWO people — Sam + Penny both admiring the vase. "
            "The successfully placed vase with beautiful flowers is the star of this frame."
        ),
    },
]
