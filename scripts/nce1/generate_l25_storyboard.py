#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 25: Mrs. Smith's Kitchen
# Story: Narrator describes Mrs. Smith's small kitchen.
# Items: white refrigerator (on the right), blue electric cooker (on the left),
#        table in the middle, empty bottle and clean cup on the table.
# Character: Mrs. Smith (briefly establishes the scene)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cosy 1960s British kitchen light, nostalgic domestic mood. "
)

SCENE = (
    "Location: a small, warm 1960s British kitchen — "
    "tiled walls in cream and pale blue, linoleum floor, "
    "a window above the sink letting in soft daylight, "
    "wooden cupboards and shelves, warm homely atmosphere. "
    "Keep the cream-and-blue tiled walls, wooden cupboards, and warm kitchen light consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_SMITH = (
    "Character MRS. SMITH: a warm, tidy British housewife, approximately 40-45 years old, "
    "short light brown hair neatly set, gentle pleasant face, "
    "wearing a pale blue house dress with a white apron. "
    "CRITICAL: pale blue dress + white apron + light brown set hair — NEVER change. "
    "She looks like a cheerful, capable 1960s British homemaker. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the small 1960s British kitchen. "
            "Mrs. Smith (pale blue dress, white apron, light brown set hair) "
            "stands in the centre of her kitchen with a proud, welcoming expression, "
            "gesturing gently at her tidy kitchen. "
            "The kitchen is clearly SMALL but neat and organised. "
            "On the LEFT wall: a BLUE electric cooker is clearly visible. "
            "On the RIGHT wall: a WHITE refrigerator is clearly visible. "
            "A wooden table stands in the MIDDLE of the room. "
            "Cream and pale blue tiled walls. Warm kitchen light. Show the full kitchen layout."
        ),
    },
    {
        "id": "refrigerator",
        "desc": (
            "Close focus on the RIGHT side of the kitchen. "
            "A large WHITE refrigerator stands prominently against the right wall — "
            "clearly white in colour, clean and modern for the 1960s, "
            "with a simple chrome handle on the door. "
            "Mrs. Smith (pale blue dress, white apron) stands beside it on the left, "
            "placing one hand on it with a satisfied expression. "
            "The refrigerator is the visual focal point — WHITE, on the RIGHT side. "
            "Cream tiled wall background. Warm kitchen light. CRITICAL: refrigerator must be WHITE."
        ),
    },
    {
        "id": "cooker",
        "desc": (
            "COMPOSITION: TIGHT CLOSE-UP shot focused entirely on the BLUE electric cooker. "
            "The cooker fills at least 60% of the frame. "
            "A BLUE electric cooker/stove — clearly and vividly BLUE — "
            "with electric hotplates on top and an oven below, "
            "1960s rounded style with chrome knobs, flush against the left wall. "
            "Mrs. Smith (pale blue dress, white apron) stands to the RIGHT of the cooker, "
            "pointing at it with one finger and a proud smile. "
            "CRITICAL: this is NOT a wide kitchen shot. It is a CLOSE-UP of the BLUE COOKER. "
            "The cooker must be the dominant element filling most of the frame. "
            "Cream tiled wall visible closely behind it. CRITICAL: cooker colour must be clearly BLUE."
        ),
    },
    {
        "id": "table",
        "desc": (
            "A simple wooden kitchen table stands clearly in the MIDDLE of the small kitchen floor. "
            "The table is centred in the frame — the blue cooker faintly visible on the left wall, "
            "the white refrigerator faintly visible on the right wall, "
            "showing the table is truly in the middle of the room. "
            "The table has a clean white tablecloth. "
            "Mrs. Smith (pale blue dress, white apron) stands slightly to one side, "
            "gesturing at the table with a proud expression. "
            "Warm kitchen light. Show the table's central position clearly."
        ),
    },
    {
        "id": "bottle_cup",
        "desc": (
            "Close-up of the kitchen table surface. "
            "On the table: ONE glass bottle — clearly EMPTY (transparent, no liquid inside) — "
            "stands on the LEFT side of the table. "
            "ONE ceramic cup — clearly CLEAN and spotless, white with a simple blue pattern — "
            "sits on the RIGHT side of the table. "
            "The EMPTY BOTTLE and CLEAN CUP are the visual focal points — shown large and clearly. "
            "The white tablecloth is visible beneath them. "
            "Warm kitchen light from above. "
            "CRITICAL: the bottle must look visibly EMPTY (transparent, no liquid). "
            "The cup must look CLEAN and pristine."
        ),
    },
]
