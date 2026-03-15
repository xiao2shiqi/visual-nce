#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 29: Come In, Amy.
# Story: Mrs. Jones calls Amy (the maid) into an untidy bedroom and gives her
# instructions: shut door, open window/air room, put clothes in wardrobe,
# make the bed, dust dressing table, sweep the floor.
# Characters: Mrs. Jones (employer), Amy (young maid)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British bedroom interior light, cosy domestic mood. "
)

SCENE = (
    "Location: a 1960s British bedroom — "
    "floral wallpaper in soft pink and cream, wooden floorboards with a rug, "
    "a single bed with a headboard, a wooden wardrobe, a dressing table with a mirror, "
    "a window with net curtains. "
    "Keep the floral wallpaper, wooden furniture, and warm light consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_JONES = (
    "Character MRS. JONES: an authoritative but kind British employer, approximately 45-50 years old, "
    "dark hair neatly pinned up in a bun, composed and poised expression, "
    "wearing a smart navy blue dress with a pearl necklace. "
    "CRITICAL: navy blue dress + dark hair in bun + pearl necklace — NEVER change. "
    "She looks like a well-dressed, confident English homeowner. "
)

CHAR_AMY = (
    "Character AMY: a young maid, approximately 20-23 years old, "
    "light brown hair pulled back under a small white cap, eager attentive expression, "
    "wearing a grey maid's dress with a white collar and a white apron. "
    "CRITICAL: grey dress + white apron + white cap + light brown hair — NEVER change. "
    "She looks like a cheerful, capable young domestic worker. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the UNTIDY bedroom. "
            "Mrs. Jones (navy blue dress, dark hair in bun, pearl necklace) "
            "stands near the doorway, gesturing at the messy room with a disapproving expression. "
            "Amy (grey dress, white apron, white cap) stands just inside the doorway, "
            "looking around the room with an attentive, ready expression. "
            "The bedroom is clearly UNTIDY: clothes scattered on the floor, "
            "the bed unmade with crumpled bedding, items out of place. "
            "Floral wallpaper, wooden wardrobe, dressing table with mirror visible. "
            "CRITICAL: EXACTLY TWO people — ONE Mrs. Jones + ONE Amy. Show both characters clearly."
        ),
    },
    {
        "id": "shut_door",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on Amy at the door. "
            "Amy (grey dress, white apron, white cap) stands at the bedroom door, "
            "pushing it firmly closed with both hands — her back slightly toward us, "
            "turning her head to look back into the room. "
            "The wooden door fills much of the right side of the frame. "
            "Mrs. Jones (navy blue dress) is visible in the background inside the room, watching. "
            "CRITICAL: Amy shutting the door is the central action. "
            "EXACTLY TWO people — Amy at door + Mrs. Jones in background."
        ),
    },
    {
        "id": "air_room",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on Amy at the window. "
            "Amy (grey dress, white apron, white cap) stands at the bedroom window, "
            "pushing it open wide with both hands — fresh air and daylight flowing in. "
            "The net curtains billow gently inward with the breeze. "
            "Amy looks pleased as the fresh air enters the room. "
            "The open window with billowing curtains is the visual focal point. "
            "Mrs. Jones (navy blue dress) stands to one side watching with approval. "
            "CRITICAL: Amy opening window + breeze coming in is the central action. "
            "EXACTLY TWO people — Amy at window + Mrs. Jones watching."
        ),
    },
    {
        "id": "wardrobe",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on Amy at the open wardrobe. "
            "Amy (grey dress, white apron, white cap) stands in front of the open wooden wardrobe, "
            "carefully placing and hanging clothes inside it — arms reaching into the wardrobe. "
            "Several garments are draped over her arm; the wardrobe is open showing clothes inside. "
            "The open wardrobe with clothes fills the right side of the frame. "
            "Mrs. Jones (navy blue dress) watches from behind Amy, pointing at the wardrobe. "
            "CRITICAL: Amy putting clothes INTO the open wardrobe is the central action. "
            "EXACTLY TWO people — Amy at wardrobe + Mrs. Jones watching."
        ),
    },
    {
        "id": "make_bed",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on Amy making the bed. "
            "Amy (grey dress, white apron, white cap) leans over the bed, "
            "smoothing and tucking the white bedsheet with both hands — "
            "her posture bent forward over the bed in the action of bed-making. "
            "The bed with its headboard fills the centre of the frame. "
            "The bedding is being neatly arranged — pillows being straightened. "
            "Mrs. Jones (navy blue dress) stands at the foot of the bed, arms folded, supervising. "
            "CRITICAL: Amy making/smoothing the bed is the central action. "
            "EXACTLY TWO people — Amy making bed + Mrs. Jones supervising."
        ),
    },
    {
        "id": "sweep_floor",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on Amy sweeping the floor. "
            "Amy (grey dress, white apron, white cap) holds a long-handled broom "
            "and sweeps the wooden bedroom floor with energetic strokes — "
            "her body leaning into the sweeping motion. "
            "A small pile of dust and debris is visible being swept. "
            "The broom and sweeping action fills the foreground. "
            "Mrs. Jones (navy blue dress) stands in the background doorway, watching with approval. "
            "CRITICAL: Amy sweeping the floor with a broom is the central action. "
            "EXACTLY TWO people — Amy sweeping + Mrs. Jones in background."
        ),
    },
]
