#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 1: Excuse me
# Story: A young man finds a woman's handbag left behind in a building corridor.
# He runs after her, asks if it's her handbag. She confirms and thanks him warmly.
# Characters: Young Man (Ben), Young Woman (Anna)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm indoor English light, gentle nostalgic mood. "
)

SCENE = (
    "Location: a bright 1960s British building corridor — polished wooden floorboards, "
    "tall sash windows letting in warm afternoon sunlight, cream-painted walls, "
    "a wooden bench near the entrance, coat hooks on the wall. "
    "Keep the corridor architecture, warm light, and wooden floor consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_BEN = (
    "Character BEN: young man, approximately 22-25 years old, "
    "short neat brown hair, friendly open face, slim build, "
    "wearing a green V-neck sweater over a light blue collared shirt and dark trousers. "
    "CRITICAL: green V-neck sweater + light blue collar visible — NEVER change. "
    "He looks like a polite young student or office worker. NOT middle-aged. "
)

CHAR_ANNA = (
    "Character ANNA: young woman, approximately 22-25 years old, "
    "short black bob hair, bright curious eyes, neat appearance, "
    "wearing a white high-neck long-sleeve blouse and a knee-length blue skirt. "
    "CRITICAL: black bob hair + white blouse + blue skirt — NEVER change. "
    "She looks like a cheerful young professional. NOT middle-aged. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the bright corridor. "
            "A small, elegant silver-grey handbag sits on the wooden bench near the window. "
            "Ben has just noticed it and is bending down to pick it up with a surprised expression. "
            "Warm afternoon sunlight streams through the tall sash window. "
            "Anna is not yet visible — only Ben and the handbag. "
            "Atmosphere: warm, curious, slightly comic."
        ),
    },
    {
        "id": "man_approaches",
        "desc": (
            "Ben is walking briskly down the corridor holding the silver handbag, "
            "looking ahead with urgency. "
            "In the distance at the far end of the corridor, Anna is seen from behind, "
            "walking away — her black bob hair and blue skirt visible. "
            "Ben is trying to catch up to her. Show both characters clearly in one frame."
        ),
    },
    {
        "id": "woman_turns",
        "desc": (
            "Ben has caught up to Anna and taps her gently on the shoulder. "
            "Anna turns around with a surprised and curious expression, "
            "her black bob hair swinging as she turns. "
            "Ben looks polite and slightly out of breath. "
            "They are face to face in the corridor. Show both characters clearly."
        ),
    },
    {
        "id": "handbag_show",
        "desc": (
            "Ben holds the silver-grey handbag up between them at chest height, "
            "looking at Anna with a polite questioning expression. "
            "Anna looks at the handbag with wide eyes and dawning recognition. "
            "Warm corridor light. Show both characters and the handbag clearly."
        ),
    },
    {
        "id": "woman_smiles",
        "desc": (
            "Anna's face lights up with a bright, relieved smile. "
            "She reaches out both hands towards the handbag, clearly delighted. "
            "Ben smiles back warmly, pleased to have helped. "
            "The handbag passes between them. Warm atmosphere. Show both clearly."
        ),
    },
    {
        "id": "thank_you",
        "desc": (
            "Anna holds her silver handbag close to her chest with both hands, "
            "looking at Ben with a grateful, happy expression. "
            "Ben nods politely with a modest smile. "
            "They stand together in the warm afternoon corridor light. "
            "Atmosphere: warm, friendly, satisfying conclusion."
        ),
    },
]
