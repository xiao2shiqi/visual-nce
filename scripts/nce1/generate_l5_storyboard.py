#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 5: Nice to Meet You.
# Story: Mr. Blake introduces new students one by one to the class.
# Each introduction: Mr. Blake gestures toward the student, THAT STUDENT is
# the clear focal point of the image.
# Characters: Mr. Blake (teacher), Sophie (French), Hans (German),
#             Naoko (Japanese), Chang-woo (Korean), Luming (Chinese), Xiaohui (Chinese)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm classroom morning light, cheerful welcoming mood. "
)

SCENE = (
    "Location: a bright 1960s language school classroom — "
    "rows of wooden desks and chairs, large windows with morning sunlight, "
    "a chalkboard at the front, world maps and small national flags on the walls. "
    "Keep the classroom architecture, morning light, and wooden furniture consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_BLAKE = (
    "Character MR. BLAKE: middle-aged man, approximately 40-45 years old, "
    "short brown hair slightly greying, kind professional face, "
    "wearing a classic grey suit jacket over a white shirt with a blue tie. "
    "CRITICAL: grey suit + white shirt + blue tie — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the bright classroom from the front. "
            "Mr. Blake (grey suit, blue tie) stands at the front of the class near the chalkboard "
            "with a warm welcoming smile, holding a register book. "
            "Students sit at wooden desks — mostly seen from behind or as silhouettes. "
            "Morning light through large windows. Warm, cheerful classroom atmosphere. "
            "No individual student is the focus — this is a wide overview shot."
        ),
    },
    {
        "id": "sophie_intro",
        "desc": (
            "FOCAL CHARACTER: SOPHIE — a young French woman, approximately 22 years old, "
            "with auburn hair worn loose to her shoulders, wearing a light blue floral dress. "
            "Sophie stands at her desk, hands clasped in front of her, smiling warmly at the class. "
            "She is clearly the MAIN SUBJECT of this frame — shown clearly from the front, centre-frame. "
            "Mr. Blake stands slightly to one side, gesturing toward her with one hand. "
            "Sophie's face and outfit are the clear focal point. Warm classroom light behind her."
        ),
    },
    {
        "id": "hans_intro",
        "desc": (
            "FOCAL CHARACTER: HANS — a young German man, approximately 22 years old, "
            "with short blond hair and a friendly open face, wearing a light blue shirt. "
            "Hans sits at his desk and raises one hand in a cheerful wave at the camera, "
            "grinning broadly. He is the MAIN SUBJECT — shown clearly, centre-frame. "
            "Mr. Blake stands to one side gesturing toward Hans with one hand. "
            "Hans's face and wave are the clear focal point. Classroom background."
        ),
    },
    {
        "id": "naoko_intro",
        "desc": (
            "FOCAL CHARACTER: NAOKO — a young Japanese woman, approximately 22 years old, "
            "with straight black bob hair, wearing a soft pink blouse. "
            "Naoko sits at her desk and bows her head slightly with a polite, gentle smile. "
            "She is the MAIN SUBJECT — shown clearly, centre-frame. "
            "Mr. Blake stands to one side gesturing toward her with one hand. "
            "Naoko's face and graceful bow are the clear focal point. Classroom background."
        ),
    },
    {
        "id": "changwoo_intro",
        "desc": (
            "FOCAL CHARACTER: CHANG-WOO — a young Korean man, approximately 22 years old, "
            "with short dark hair and an enthusiastic grin, wearing a pale yellow shirt. "
            "Chang-woo sits at his desk and gives a big cheerful wave toward the viewer. "
            "He is the MAIN SUBJECT — shown clearly and prominently, centre-frame. "
            "Mr. Blake stands to one side gesturing toward Chang-woo with one hand. "
            "Chang-woo's face and energetic wave are the clear focal point. Classroom background."
        ),
    },
    {
        "id": "luming_intro",
        "desc": (
            "FOCAL CHARACTER: LUMING — a young Chinese man, approximately 22 years old, "
            "with short neat dark hair and a polite composed expression, wearing a neat white shirt. "
            "COMPOSITION: Luming is shown in LARGE CLOSE-UP in the RIGHT FOREGROUND of the frame, "
            "his face and upper body filling at least half the image. "
            "He smiles calmly at the viewer and nods politely. "
            "Mr. Blake is visible SMALL in the LEFT BACKGROUND, gesturing toward Luming. "
            "CRITICAL: Luming must be the dominant, large foreground character. "
            "Mr. Blake must be smaller and in the background. Classroom setting behind them."
        ),
    },
    {
        "id": "xiaohui_intro",
        "desc": (
            "FOCAL CHARACTER: XIAOHUI — a young Chinese woman, approximately 22 years old, "
            "with black hair worn in a neat bun, bright warm eyes, wearing a soft pink top. "
            "Xiaohui sits at her desk and smiles warmly and brightly at the viewer. "
            "She is the MAIN SUBJECT — shown clearly and prominently, centre-frame. "
            "Mr. Blake stands to one side gesturing toward Xiaohui with one hand. "
            "Xiaohui's face and warm smile are the clear focal point. Classroom background."
        ),
    },
]
