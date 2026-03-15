#!/usr/bin/env python3

# =============================================================================
# NCE2 Lesson 3: Please Send Me a Card
# Story: The Writer holidays in Italy. He enjoys it but keeps procrastinating
# on writing postcards. On the last day he buys 37 cards — but writes none.
# Characters: ONE MAN (Writer), ONE MAN (Italian Waiter) — no other characters.
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm sunny Mediterranean lighting, cheerful nostalgic mood. "
)

SCENE = (
    "Location: sunny 1960s Italy — sunlit piazzas with terracotta-tiled rooftops, "
    "golden stone buildings with shuttered windows, flowering window boxes, "
    "a lively outdoor cafe with round tables and striped umbrellas, "
    "and a cozy Italian hotel room with a wooden desk and a large stack of blank postcards. "
    "Keep warm golden Italian sunlight, terracotta colour palette, and Mediterranean architecture "
    "consistent across all outdoor frames. "
    "Strictly in Italy — NO English streets, NO English buildings. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO readable text anywhere. "
)

CHAR_WRITER = (
    "Character THE WRITER: young adult man, approximately 28 years old, "
    "short neatly combed dark brown hair, slim build, friendly curious face, "
    "wearing a light sky-blue short-sleeved linen shirt and beige chino trousers, "
    "with a small tan canvas shoulder bag. "
    "CRITICAL: sky-blue linen shirt + beige trousers + tan shoulder bag — these NEVER change. "
    "He looks like a typical young British tourist on holiday."
)

CHAR_WAITER = (
    "Character THE ITALIAN WAITER: friendly cheerful man, approximately 35 years old, "
    "dark wavy hair, warm olive skin, a broad genuine smile, "
    "wearing a crisp white shirt, black waistcoat, black trousers, and a long white apron. "
    "CRITICAL: white shirt + black waistcoat + white apron — these NEVER change. "
    "He appears ONLY in the cafe scene. He is clearly Italian and hospitable."
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of a beautiful sunny Italian piazza. "
            "The Writer sits contentedly alone at an outdoor cafe table, a small espresso cup in front of him, "
            "gazing happily at the golden stone buildings and blue sky around him. "
            "His canvas shoulder bag hangs on the chair. "
            "Colourful flowers cascade from window boxes. Other tourists pass in the far background. "
            "Atmosphere: joyful, warm, carefree Italian holiday."
        ),
    },
    {
        "id": "waiter_teaches",
        "desc": (
            "Medium shot at the outdoor cafe table. The friendly Italian Waiter stands beside the Writer's table, "
            "leaning forward with a warm smile, pointing at objects on the table and clearly teaching the Writer "
            "Italian words — gesturing to the espresso cup, the bread basket, the menu. "
            "The Writer listens with delight and tries to repeat the words, smiling and gesturing back. "
            "An open Italian-English book is on the table between them. "
            "Show both characters in one frame. Sunny piazza in background."
        ),
    },
    {
        "id": "writer_reads_book",
        "desc": (
            "The Writer sits alone at a sunny cafe table or on a piazza bench, "
            "holding the open Italian book close to his face, brow furrowed in confusion. "
            "He clearly cannot understand a single word — the book looks impossibly foreign. "
            "His expression is comic bewilderment. In the background, a postcard display rack "
            "spins in the breeze outside a nearby shop. He glances at it with a guilty look. "
            "Only the Writer is present in this frame."
        ),
    },
    {
        "id": "buying_cards",
        "desc": (
            "Morning scene. The Writer stands at a bright Italian street kiosk or stationery shop, "
            "looking very determined and purposeful. He is pointing at a large display of colourful postcards "
            "and gesturing with both hands — clearly buying a very large stack. "
            "The shop vendor hands him an enormous bundle of postcards. "
            "The Writer looks pleased with his decisive action. Sunny Italian street behind him. "
            "Only the Writer and the kiosk vendor are present."
        ),
    },
    {
        "id": "writer_gives_up",
        "desc": (
            "Interior of a small Italian hotel room. The Writer sits slumped at a wooden desk, "
            "surrounded by a massive pile of blank postcards spread across the desk and floor. "
            "Pens, envelopes, and cards are everywhere — but every single card is completely blank. "
            "He stares at the cards with a helpless, defeated expression — arms slightly raised, "
            "shoulders hunched, as if surrendering. Late afternoon golden light streams through shuttered windows. "
            "Only the Writer is in this frame. Comic and charming atmosphere."
        ),
    },
]
