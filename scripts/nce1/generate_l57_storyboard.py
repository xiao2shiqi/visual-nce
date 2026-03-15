#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 57: An Unusual Day
# Story: An unusual Saturday for the Sawyer family. Normally children go by car,
# but today they are walking to school. Mrs. Sawyer normally stays home,
# but this morning she is going shopping. Normally she drinks tea inside,
# but this afternoon she's in the garden. Children normally do homework,
# but tonight they are playing in the garden. Mr. Sawyer normally reads
# his newspaper, but tonight he is reading an interesting book.
# Characters: MR. SAWYER, MRS. SAWYER, CHILDREN (boy + girl)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British suburban family life, cheerful domestic mood. "
)

SCENE = (
    "Location: 87 King Street and the local neighbourhood — "
    "the red brick terraced house with a small back garden, "
    "a local high street with shops, and a pleasant garden with flowers. "
    "Keep the red brick terrace exterior, cosy interior, and the back garden consistent. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_MR_SAWYER = (
    "Character MR. SAWYER: a pleasant British father, approximately 38-42 years old, "
    "short dark hair with a side parting, kind dependable face, "
    "wearing a dark grey suit for work, or comfortable casual clothes at home. "
    "CRITICAL: dark hair with side parting — NEVER change. "
)

CHAR_MRS_SAWYER = (
    "Character MRS. SAWYER: a warm British housewife, approximately 35-40 years old, "
    "short wavy brown hair, cheerful capable expression, "
    "wearing a light floral dress and sometimes a cardigan or coat when out. "
    "CRITICAL: wavy brown hair + light floral dress — NEVER change. "
)

CHAR_CHILDREN = (
    "Characters THE CHILDREN: a boy approximately 9-10 years old (short brown hair, "
    "school uniform — grey shorts, white shirt, dark blazer) "
    "and a girl approximately 8-9 years old (blonde pigtails, "
    "school uniform — grey skirt, white blouse, dark cardigan). "
    "CRITICAL: boy in grey school uniform + girl with blonde pigtails in grey skirt — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the pavement outside 87 King Street on a sunny morning. "
            "The TWO CHILDREN (BOY in grey school uniform + GIRL with blonde pigtails in grey skirt) "
            "are WALKING along the pavement carrying school bags on their backs. "
            "They walk side by side, both looking cheerful and slightly surprised — "
            "this is unusual, they normally go by car! "
            "The red brick terraced street is clearly visible around them. "
            "Morning light, bright and fresh. "
            "CRITICAL: EXACTLY TWO children — boy + girl — walking to school on foot. "
            "Show both children clearly with school bags on backs. No adults in this frame. "
            "The unusual walking-to-school detail is the focal point."
        ),
    },
    {
        "id": "mrs_sawyer_shops",
        "desc": (
            "COMPOSITION: MEDIUM SHOT inside a 1960s British greengrocer's shop interior. "
            "MRS. SAWYER (wavy brown hair, light floral dress, green coat, wicker basket on arm) "
            "stands at a wooden counter or beside a display of fresh vegetables and fruit — "
            "colourful apples, oranges, carrots, and cabbages piled on a wooden stall. "
            "She holds up an apple or orange, inspecting it with a pleased expression. "
            "Her wicker basket already has some groceries inside. "
            "The interior of the greengrocer's: wooden crates, vegetables, warm shop light. "
            "NO shop signs, no wall text, no price tags, NO writing anywhere. "
            "CRITICAL: ONLY MRS. SAWYER in the frame — she shops alone inside the greengrocer's. "
            "CRITICAL: ABSOLUTELY ZERO text, letters, numbers, or words anywhere in the frame."
        ),
    },
    {
        "id": "tea_garden",
        "desc": (
            "Wide shot of the sunny back garden of 87 King Street in the afternoon. "
            "MRS. SAWYER (wavy brown hair, light floral dress) "
            "sits in a garden chair at a small garden table, "
            "enjoying a cup of tea outdoors in the sunshine. "
            "A teapot and cup are on the garden table beside her. "
            "The back garden has flowers in bloom, a lawn, a fence, "
            "and the red brick house wall behind her. "
            "Mrs. Sawyer looks pleasantly relaxed, enjoying the warm afternoon sun. "
            "CRITICAL: ONLY MRS. SAWYER in the garden — drinking tea outside in the sunshine. "
            "Show her clearly in the sunny back garden. No other people in this frame."
        ),
    },
    {
        "id": "children_playing",
        "desc": (
            "Wide shot of the back garden in the early evening. "
            "The TWO CHILDREN (BOY in grey school uniform + GIRL with blonde pigtails) "
            "are PLAYING happily in the garden — perhaps kicking a ball, "
            "or playing chase, or playing with a hoop on the lawn. "
            "Both children are laughing and energetic, clearly enjoying themselves. "
            "The garden with flowers and the garden fence is visible. "
            "Soft evening light. "
            "CRITICAL: EXACTLY TWO children — boy + girl — playing in the garden. "
            "Show both children clearly playing outdoors. No adults in this frame. "
            "The unusual evening playtime (instead of homework) is the focal point."
        ),
    },
    {
        "id": "mr_sawyer_book",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the cosy sitting room at night. "
            "MR. SAWYER (dark hair with side parting, dark grey suit jacket off, shirt and tie loosened) "
            "sits in his armchair, completely absorbed in reading a BOOK — "
            "a thick hardback book held in both hands, eyes focused on the pages. "
            "His expression shows genuine interest and enjoyment — this is an unusual treat. "
            "On the side table beside him: a FOLDED NEWSPAPER left untouched. "
            "The contrast between the usual newspaper (ignored) and the book (being read) is key. "
            "Warm lamplight falls on him, fireplace glowing in the background. "
            "CRITICAL: ONLY MR. SAWYER in this frame — reading his book. "
            "The BOOK in his hands is the focal prop; the untouched newspaper beside him is the contrast. "
            "No text visible on the book cover or newspaper."
        ),
    },
]
