#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 27: Mrs. Smith's Living Room
# Story: Narrator describes Mrs. Smith's LARGE living room.
# Items: TV near window (magazines on top), table (newspapers on it),
#        armchairs near the table, stereo near the door (books on top),
#        pictures on the wall.
# Character: Mrs. Smith (same as L25)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cosy 1960s British living room light, nostalgic domestic mood. "
)

SCENE = (
    "Location: a large, warm 1960s British living room — "
    "patterned wallpaper in warm cream and sage green, thick carpet on the floor, "
    "large windows with curtains letting in soft afternoon light, "
    "a fireplace on one wall, wooden furniture. "
    "Keep the patterned wallpaper, thick carpet, and warm afternoon light consistent across ALL frames. "
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
            "Wide establishing shot of the LARGE 1960s British living room. "
            "Mrs. Smith (pale blue dress, white apron, light brown set hair) "
            "stands near the centre of her spacious living room with a proud expression, "
            "gesturing broadly at the room. "
            "The room is clearly LARGE and well-furnished. "
            "Visible in the room: a TV set near the window on the right, "
            "a table with armchairs, a stereo unit near the door on the left, "
            "framed pictures on the patterned wallpaper walls. "
            "Afternoon light through large curtained windows. Warm, comfortable atmosphere."
        ),
    },
    {
        "id": "tv_magazines",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the TV area by the window. "
            "A 1960s boxy television set stands on a wooden cabinet NEAR THE WINDOW — "
            "the window with curtains is clearly visible immediately behind or beside the TV, "
            "showing daylight through the curtains. "
            "ON TOP of the television: several MAGAZINES are stacked or spread out. "
            "Mrs. Smith (pale blue dress, white apron) stands to one side, "
            "gesturing toward the TV and magazines. "
            "CRITICAL: the TV must be visibly NEAR THE WINDOW. Magazines must be ON TOP of the TV. "
            "This is NOT a wide room shot — focus tightly on the TV + window area."
        ),
    },
    {
        "id": "table_newspapers",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on a wooden side table in the living room. "
            "A sturdy wooden side table stands in the living room. "
            "ON THE TABLE: several NEWSPAPERS are laid out — folded broadsheet newspapers, "
            "clearly visible as the focal items on the table surface. "
            "Mrs. Smith (pale blue dress, white apron) stands beside the table, "
            "pointing at the newspapers with a matter-of-fact expression. "
            "Patterned wallpaper visible behind. Thick carpet visible below. "
            "CRITICAL: newspapers must be clearly ON TOP of the table. "
            "This is NOT a wide room shot — focus on the table + newspapers."
        ),
    },
    {
        "id": "armchairs",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the armchair arrangement. "
            "Two or three cosy upholstered armchairs are grouped NEAR A TABLE — "
            "the table is clearly visible beside or between the armchairs. "
            "The armchairs are comfortable, 1960s British style with floral or solid fabric. "
            "Mrs. Smith (pale blue dress, white apron) stands beside one armchair, "
            "placing one hand on its back with a welcoming gesture. "
            "Thick carpet on the floor. Patterned wallpaper behind. "
            "CRITICAL: armchairs must be visibly NEAR THE TABLE. "
            "This is NOT a wide room shot — focus tightly on the armchair group."
        ),
    },
    {
        "id": "stereo_books",
        "desc": (
            "COMPOSITION: TIGHT MEDIUM SHOT. The stereo unit fills the RIGHT HALF of the frame. "
            "A 1960s hi-fi stereo wooden cabinet with a turntable lid, speaker grille, and control dials "
            "stands in the FOREGROUND, very close to the camera. "
            "The DOOR FRAME is clearly visible immediately to the left of the stereo — "
            "door and stereo share the frame together, confirming stereo is NEAR THE DOOR. "
            "ON TOP of the stereo cabinet: a STACK OF BOOKS — 3-4 books piled up, clearly visible. "
            "Mrs. Smith (pale blue dress, white apron) stands to the right of the stereo, "
            "resting one hand on top of the books with a pleased smile. "
            "CRITICAL: stereo cabinet must be the LARGE DOMINANT element in the frame, "
            "NOT a small background object. Books must be visibly ON TOP. Door must be beside it. "
            "Do NOT show the full room — this is a CLOSE-UP of the stereo + door corner only."
        ),
    },
    {
        "id": "pictures_wall",
        "desc": (
            "COMPOSITION: MEDIUM SHOT looking at the living room WALL. "
            "The patterned wallpaper wall fills most of the frame. "
            "ON THE WALL: two or three framed PICTURES / paintings hang clearly — "
            "landscapes or still-life paintings in ornate frames, "
            "hanging at eye level, well-spaced on the wall. "
            "Mrs. Smith (pale blue dress, white apron) stands in front of the wall, "
            "looking up at the pictures with a pleased expression. "
            "CRITICAL: pictures must be clearly ON THE WALL — the wall and picture frames "
            "must be the dominant visual elements. "
            "This is NOT a wide room shot — focus on the wall + pictures."
        ),
    },
]
