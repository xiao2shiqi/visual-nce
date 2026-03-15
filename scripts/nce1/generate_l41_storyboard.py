#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 41: Penny's Bag
# Story: Sam notices Penny's heavy shopping bag. He offers to take it ("Here!")
# Penny asks to put it on a chair. Sam asks what's in it.
# Penny lists: cheese, bread, soap, chocolate, milk, sugar, coffee, tea, tobacco.
# Sam teases — is that tin of tobacco for Penny?
# Penny laughs — it's certainly not for Sam!
# Characters: SAM (man), PENNY (woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British home interior light, cosy domestic mood. "
)

SCENE = (
    "Location: a cosy 1960s British home — "
    "a kitchen or living room hallway with a wooden chair near the door, "
    "a kitchen table, patterned wallpaper, warm lamp light. "
    "Keep the wooden chair, kitchen table, patterned wallpaper, and warm light consistent across ALL frames. "
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
            "Wide shot near the front door of the British home. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) "
            "carries a LARGE HEAVY SHOPPING BAG — a bulging cloth or wicker shopping bag — "
            "clearly weighed down, one arm straining slightly with the weight. "
            "SAM (white shirt, light brown V-neck sweater) stands beside her "
            "looking at the bag with a concerned, helpful expression — 'Is that bag heavy?' "
            "He reaches out with one hand as if offering to take the heavy bag. "
            "The HEAVY SHOPPING BAG is the focal prop. "
            "CRITICAL: EXACTLY TWO people — Sam noticing the heavy bag + Penny carrying it. "
            "Show both characters clearly. Warm home hallway atmosphere."
        ),
    },
    {
        "id": "bag_on_chair",
        "desc": (
            "COMPOSITION: MEDIUM SHOT showing the chair and the bag placement action. "
            "SAM (white shirt, light brown V-neck sweater) sets the LARGE HEAVY SHOPPING BAG "
            "down onto a WOODEN CHAIR beside the wall — the bag lands on the chair with weight. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands nearby "
            "pointing at the chair, directing Sam with a pleased expression — 'Put it on this chair.' "
            "The WOODEN CHAIR with the HEAVY BAG on it is the focal element. "
            "CRITICAL: EXACTLY TWO people — Sam placing bag on chair + Penny directing. "
            "The bag on the wooden chair is the key visual. "
            "Do NOT show the full room — focus on the chair, bag, and both characters."
        ),
    },
    {
        "id": "cheese_bread",
        "desc": (
            "COMPOSITION: CLOSE-UP of the kitchen table with grocery items laid out. "
            "On the table, clearly arranged and individually visible: "
            "a WEDGE OF YELLOW CHEESE, a ROUND BROWN LOAF OF BREAD, "
            "a BAR OF WHITE SOAP (rectangular), and a BAR OF CHOCOLATE (dark brown, wrapped). "
            "These four items are laid out neatly on the kitchen table, filling the frame. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands behind the table "
            "pointing at or gesturing toward the items as she lists them. "
            "SAM (white shirt, light brown V-neck sweater) stands opposite, listening with curiosity. "
            "CRITICAL: EXACTLY TWO people — Penny listing items + Sam listening. "
            "The four grocery items on the table are the focal visual elements. "
            "Do NOT show the full room — keep focus on the table items and both characters."
        ),
    },
    {
        "id": "soap_milk",
        "desc": (
            "COMPOSITION: CLOSE-UP of the kitchen table with more grocery items displayed. "
            "On the table, clearly arranged and individually visible: "
            "a GLASS BOTTLE OF MILK (white liquid, glass bottle with silver foil cap — NO label text), "
            "a PLAIN PAPER BAG OF WHITE SUGAR (no text on it), "
            "a SMALL BROWN PAPER BAG OF COFFEE (no text, recognisable by brown colour), "
            "a SMALL WRAPPED PAPER PACKET OF TEA (plain wrapping, no text), "
            "and a ROUND CYLINDRICAL TIN CAN for tobacco (plain unlabelled tin, no text). "
            "ALL PACKAGING IS BLANK — NO writing, NO brand names, NO labels on any item. "
            "These five items are laid out neatly on the kitchen table, filling the frame. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) stands behind the table "
            "gesturing at the items, listing them out. "
            "SAM (white shirt, light brown V-neck sweater) stands opposite, watching with curiosity. "
            "CRITICAL: EXACTLY TWO people — Penny listing items + Sam observing. "
            "CRITICAL: ABSOLUTELY NO text, letters, numbers, or words on any item in the frame. "
            "The grocery items on the table are the focal visual elements. "
            "Do NOT show the full room."
        ),
    },
    {
        "id": "bag_contents",
        "desc": (
            "Wide shot of the cosy 1960s kitchen. "
            "The WOODEN CHAIR in the foreground has the EMPTY SHOPPING BAG resting on it. "
            "On the KITCHEN TABLE: ALL the groceries are spread out — "
            "a yellow wedge of cheese, a round loaf of bread, a white rectangular bar of soap, "
            "a brown bar of chocolate, a glass bottle of milk, a plain paper sugar bag, "
            "a small brown coffee packet, a small tea packet, and a plain cylindrical tin can. "
            "ALL PACKAGING IS BLANK — NO writing, NO labels, NO brand names on ANY item. "
            "PENNY (chestnut wavy hair, light blue blouse, floral apron) holds up the PLAIN TIN CAN "
            "with a teasing, amused smile — showing it to Sam playfully. "
            "SAM (white shirt, light brown V-neck sweater) stands with arms folded, "
            "grinning with mock indignation. "
            "The TIN CAN held by Penny and Sam's amused grin are the focal action. "
            "CRITICAL: EXACTLY TWO people — Penny holding tin playfully + Sam reacting with grin. "
            "CRITICAL: ABSOLUTELY NO text, letters, numbers, or words anywhere in the frame. "
            "The full spread of groceries on the table sets the context."
        ),
    },
]
