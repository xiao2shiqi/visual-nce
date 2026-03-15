#!/usr/bin/env python3

# =============================================================================
# NCE2 Lesson 1: A Private Conversation
# Story: The Writer goes to the theatre. A young couple sitting BEHIND him
# talk loudly. He complains; they reply rudely: "This is a private conversation!"
#
# SPATIAL RULE (CRITICAL):
#   The Writer sits CLOSER to the stage than the couple.
#   The stage is at the FRONT of the image.
#   The Writer's ROW is in the FOREGROUND / MIDDLE of the shot.
#   The Young Man and Young Woman sit in the row BEHIND the Writer —
#   physically further from the stage, further back in the auditorium.
#   When the Writer faces the stage, his BACK is to the couple.
#   The couple is NEVER shown in front of or beside the Writer.
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cinematic theatre lighting, gentle nostalgic mood. "
)

SCENE = (
    "Location: a classic old-fashioned English theatre auditorium — ornate gold balcony trim, "
    "rows of deep red velvet seats receding toward the back of the house, "
    "soft amber wall sconces, a brightly lit stage with heavy red curtains at the FRONT of the image. "
    "SPATIAL LAYOUT (enforce in every frame): the stage is at the front/bottom of the frame; "
    "seat rows recede away from the stage toward the back. The Writer sits in a row CLOSER to the stage. "
    "The Young Couple sit in the row DIRECTLY BEHIND the Writer — further from the stage than the Writer. "
    "Keep theatre architecture, lighting direction, and row layout strictly consistent across ALL frames. "
    "Strictly inside the theatre. NO outdoor or lobby elements. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_WRITER = (
    "Character THE WRITER: middle-aged British man, approximately 45 years old, "
    "tidy light brown hair combed neatly to one side, slim clean-shaven face, "
    "wearing a dark grey suit jacket, crisp white shirt, and a dark burgundy necktie. "
    "He sits facing the stage — his back naturally faces the row behind him. "
    "CRITICAL: grey suit + white shirt + burgundy tie — NEVER change. "
    "He is ALWAYS visibly older and slimmer than the Young Man. "
    "NEVER place any other characters in front of or beside the Writer — only BEHIND him. "
)

CHAR_YOUNG_MAN = (
    "Character THE YOUNG MAN: early twenties, short messy black hair, animated lively expression, "
    "wearing a cobalt blue crew-neck sweater and dark charcoal trousers. "
    "He sits in the row DIRECTLY BEHIND the Writer — he is ALWAYS further from the stage than the Writer. "
    "CRITICAL: cobalt blue sweater — NEVER changes. Always younger and behind the Writer. "
)

CHAR_YOUNG_WOMAN = (
    "Character THE YOUNG WOMAN: early twenties, long chestnut-brown hair worn loose, "
    "cheerful expressive face, wearing a soft yellow floral dress. "
    "She sits beside the Young Man in the row BEHIND the Writer. "
    "CRITICAL: yellow floral dress + chestnut hair — NEVER change. Always in the row behind the Writer. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot. The brightly lit stage with red curtains fills the background. "
            "The Writer sits alone in a good seat in a middle row, facing the stage — we see his back and the side of his face. "
            "The Young Man and Young Woman are NOT yet visible. "
            "Other audience members are tiny silhouettes further back. "
            "Atmosphere: elegant, warm, immersive. The play on stage looks colourful and interesting."
        ),
    },
    {
        "id": "couple_chatting",
        "desc": (
            "Side-angle medium shot showing THREE ROWS of seats in depth: "
            "stage glow is at the FRONT-LEFT of frame. "
            "ROW 1 (nearest stage, foreground): The Writer sits facing forward toward the stage — we see his back. "
            "ROW 2 (behind Writer, middle ground): The Young Man and Young Woman lean together chatting loudly. "
            "The Young Man wears cobalt blue sweater; the Young Woman wears yellow floral dress. "
            "The Writer's shoulders tense. Stage light illuminates the front. "
            "SPATIAL RULE: the couple's seats are PHYSICALLY FURTHER FROM THE STAGE than the Writer's seat. "
            "Do NOT place the couple at the same depth or in front of the Writer. "
            "CONFIRM: Writer row = foreground closer to stage. Couple row = behind Writer further from stage."
        ),
    },
    {
        "id": "writer_turns_angry",
        "desc": (
            "The Writer has twisted sharply around in his seat to look BACKWARD over his shoulder. "
            "We see the Writer from the front — he faces us, having turned away from the stage. "
            "His body is in the FOREGROUND (closest to stage). Behind him (further from stage) sit "
            "the Young Man (cobalt blue sweater) and Young Woman (yellow floral dress) in the NEXT ROW BACK. "
            "The couple's seats are visibly BEHIND the Writer's seat — higher up in the auditorium, further from stage. "
            "The Writer glares backward at them over his shoulder. "
            "SPATIAL RULE: couple must appear at a GREATER DISTANCE FROM THE STAGE than the Writer. "
            "The stage (not visible) is BEHIND the camera / behind the Writer. "
            "Do NOT show the couple at the same row level or in front of the Writer. "
            "Show all three characters. CONFIRM: Writer row = foreground/nearer stage. Couple row = background/further from stage."
        ),
    },
    {
        "id": "writer_complains",
        "desc": (
            "The Writer has turned around in his seat and is leaning backward toward the couple behind him, "
            "speaking angrily with a raised hand. His body is turned so he faces the couple in the row behind. "
            "The Young Man listens with a dismissive expression. The Young Woman looks unconcerned. "
            "Nearby audience members in adjacent rows glance over in surprise. "
            "The stage is visible far in the foreground below. Show all three characters clearly. "
            "NO text, NO speech bubbles anywhere."
        ),
    },
    {
        "id": "couple_rude",
        "desc": (
            "Medium shot on the couple in the row behind the Writer. "
            "The Young Man faces forward toward the Writer (who sits in front of him, closer to the stage) "
            "with a rude dismissive expression — chin raised, one hand waving the Writer away. "
            "The Young Woman beside him looks casually unconcerned. "
            "The Writer's head and shoulders are visible in the foreground ROW IN FRONT of the couple, "
            "looking shocked and affronted. "
            "CONFIRM: Writer's row is in front (closer to stage). Couple's row is behind (further from stage)."
        ),
    },
    {
        "id": "private_conversation",
        "desc": (
            "Final confrontation. The Young Man leans forward from his rear row toward the Writer in the row ahead, "
            "pointing a finger with rude confident authority. "
            "The Young Woman sits calmly beside him. "
            "The Writer sits in the row in front, turned around to face them, mouth open in disbelief. "
            "CONFIRM: Writer is in the nearer row (closer to stage). Couple is in the row behind. "
            "Amber theatre lighting. Stage glow visible in the far front background. No text anywhere."
        ),
    },
]
