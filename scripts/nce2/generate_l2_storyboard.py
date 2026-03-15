#!/usr/bin/env python3

# =============================================================================
# NCE2 Lesson 2: Breakfast or Lunch
# Story: The Writer sleeps in on Sunday. Aunt Lucy phones to say she has
# arrived at the station. She is shocked he is still having breakfast at 1pm.
# Characters: ONE MAN (Writer), ONE WOMAN (Aunt Lucy) — no other characters.
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cozy domestic lighting, gentle nostalgic mood. "
)

SCENE = (
    "Primary location: a cozy 1960s English home — a bedroom with a wooden bed frame, "
    "floral curtains, a bedside table with a black rotary telephone, a small wall clock, "
    "and a writing desk in the corner. The dining area has a small wooden table with "
    "breakfast items: toast rack, teapot, teacup, marmalade jar, and breakfast plate. "
    "Keep the room layout, window position, floral curtain pattern, and warm lighting "
    "strictly consistent across all home frames. "
    "Strictly inside the home or at the railway station platform. NO other locations. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_WRITER = (
    "Character THE WRITER: young British man, approximately 22-25 years old, "
    "tousled messy light brown hair, youthful face with slight stubble, slim build. "
    "He wears blue-and-white striped cotton pajamas throughout all home scenes. "
    "CRITICAL: young face (early 20s), tousled hair, blue-and-white striped pajamas — these NEVER change. "
    "He must look clearly YOUNG — a university-age young man, NOT middle-aged, NOT old. "
)

CHAR_AUNT_LUCY = (
    "Character AUNT LUCY: kindly elderly British woman, approximately 65-70 years old, "
    "neatly styled white-grey hair pinned up, warm rosy face with a surprised expression, "
    "wearing a tasteful lavender-purple wool coat with a small brooch, "
    "a matching small hat, and carrying a brown leather suitcase. "
    "CRITICAL: lavender-purple coat + white-grey hair + brown suitcase — these NEVER change. "
    "She appears ONLY in the railway station scene, NOT in the home. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the cozy bedroom. The Writer is alone, still lying in bed very late in the day, "
            "looking sleepy and comfortable under a blue blanket. "
            "A simple wall clock on the wall clearly shows 1 o'clock in the afternoon. "
            "Warm soft light filters through the floral curtains. Atmosphere: lazy, cozy, Sunday indulgence. "
            "No other people present."
        ),
    },
    {
        "id": "rainy_window",
        "desc": (
            "View from inside the Writer's cozy bedroom toward the window. "
            "The Writer stands or sits near the window looking out. "
            "Outside the glass, it is dark and raining heavily — wet grey streets, "
            "blurred lamplight reflections, raindrops streaming down the glass. "
            "The contrast between the warm cozy interior and the bleak wet outside is clear. "
            "NO other people visible outside."
        ),
    },
    {
        "id": "phone_rings",
        "desc": (
            "The Writer has sat up in bed, still in striped pajamas, and is reaching toward "
            "the black rotary telephone on the bedside table as it begins to ring. "
            "His expression is groggy and surprised by the interruption. "
            "He is alone in the bedroom. The wall clock is still visible showing 1 o'clock. "
            "NO speech bubbles, NO sound effect text, NO visible words anywhere."
        ),
    },
    {
        "id": "aunt_lucy_station",
        "desc": (
            "Scene changes entirely to a small traditional English railway station platform. "
            "Grey soft daylight, a steam train visible in the background having just arrived. "
            "Aunt Lucy stands alone at an old black public telephone mounted on the platform wall, "
            "her brown suitcase on the ground beside her. She speaks cheerfully into the receiver. "
            "Show Aunt Lucy clearly in a single normal cinematic frame. "
            "Do NOT show the Writer. Do NOT show split screens or panels. Do NOT show the home. "
            "NO text, NO signs readable in English."
        ),
    },
    {
        "id": "writer_at_breakfast",
        "desc": (
            "The Writer is now at a small wooden dining table in his home, still in his striped pajamas. "
            "He holds the telephone receiver awkwardly in one hand while eating breakfast — "
            "toast, tea, marmalade on the table. His expression is sheepish and apologetic. "
            "He is alone in this frame. Warm kitchen or dining room light. "
            "The contrast of pajamas + breakfast at 1pm is visually clear."
        ),
    },
    {
        "id": "one_oclock",
        "desc": (
            "Single cinematic frame. The Writer sits at the breakfast table, still in pajamas, "
            "holding the telephone receiver with an embarrassed guilty expression. "
            "A wall clock clearly and prominently shows 1 o'clock. Toast and tea are on the table. "
            "He is the only person visible. "
            "NO split screen, NO collage, NO panels, NO visible text anywhere."
        ),
    },
]
