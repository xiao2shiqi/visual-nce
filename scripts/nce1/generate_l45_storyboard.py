#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 45: The Boss's Letter
# Story: The Boss calls Bob into his office and asks where Pamela is.
# She's next door in her office. Boss wants Pamela to type a letter.
# Bob delivers the letter to Pamela. She agrees but then cries out:
# She can't type it — she can't READ it! The boss's handwriting is terrible!
# Characters: BOSS (authoritative older man), BOB (office worker man),
#             PAMELA (secretary woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British office interior light, professional mood. "
)

SCENE = (
    "Location: a 1960s British office building — "
    "a boss's office with a large wooden desk, papers and documents, a desk lamp, "
    "a connecting door to the next room, wooden panelled walls, "
    "warm office light from a desk lamp and a window. "
    "Keep the wooden desks, office papers, desk lamp, and professional atmosphere consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_BOSS = (
    "Character THE BOSS: an authoritative British office manager, approximately 50-55 years old, "
    "silver grey hair neatly combed, firm but fair expression, "
    "wearing a dark navy three-piece suit with a white shirt and red tie, "
    "seated behind a large wooden desk. "
    "CRITICAL: silver grey hair + dark navy three-piece suit + red tie — NEVER change. "
)

CHAR_BOB = (
    "Character BOB: a young British office worker, approximately 25-30 years old, "
    "short neat brown hair, polite and attentive expression, "
    "wearing a mid-grey suit with a white shirt and plain dark tie. "
    "CRITICAL: short brown hair + mid-grey suit + white shirt + dark tie — NEVER change. "
)

CHAR_PAMELA = (
    "Character PAMELA: a professional British secretary, approximately 25-30 years old, "
    "short neat blonde hair, competent and cheerful expression, "
    "wearing a light rose pink blouse and a dark grey pencil skirt. "
    "CRITICAL: short blonde hair + light rose pink blouse + dark grey pencil skirt — NEVER change. "
    "She sits at a typewriter at her own desk. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the BOSS'S OFFICE. "
            "THE BOSS (silver grey hair, dark navy three-piece suit, red tie) "
            "sits behind a large wooden desk covered in papers and documents, "
            "looking toward the door with an authoritative, beckoning expression — "
            "'Can you come here a minute please, Bob?' "
            "BOB (short brown hair, mid-grey suit, dark tie) stands respectfully "
            "in the office doorway, attentive and polite — 'Yes, sir?' "
            "The wooden desk with papers and the desk lamp are clearly visible. "
            "CRITICAL: EXACTLY TWO people — the Boss at his desk + Bob in the doorway. "
            "NO other people visible anywhere in the frame — no background figures, no one through doors or windows. "
            "Show both characters clearly. Professional 1960s office atmosphere."
        ),
    },
    {
        "id": "handing_letter",
        "desc": (
            "COMPOSITION: MEDIUM SHOT in the Boss's office, focused on the letter handover. "
            "THE BOSS (silver grey hair, dark navy three-piece suit, red tie) "
            "sits at his desk and holds out a HANDWRITTEN LETTER — a single sheet of paper "
            "covered in messy, scrawled, barely legible handwriting — toward Bob. "
            "BOB (short brown hair, mid-grey suit, dark tie) stands before the desk, "
            "reaching out to take the letter with a dutiful expression. "
            "The HANDWRITTEN LETTER between the Boss's and Bob's hands is the focal prop. "
            "CRITICAL: EXACTLY TWO people — Boss handing letter + Bob taking it. "
            "The letter must be clearly a single sheet with scrawled handwriting on it. "
            "Do NOT show the full room. No readable text on the letter."
        ),
    },
    {
        "id": "pamela_office",
        "desc": (
            "Wide shot of PAMELA'S ADJACENT OFFICE. "
            "PAMELA (short blonde hair, rose pink blouse, dark grey pencil skirt) "
            "sits at her TYPEWRITER desk, looking at BOB with a surprised, concerned expression, "
            "holding the HANDWRITTEN LETTER up and squinting at it with visible difficulty. "
            "BOB (short brown hair, mid-grey suit, dark tie) stands before her desk "
            "watching her struggle with concern — 'What's the matter?' "
            "The TYPEWRITER on Pamela's desk and the LETTER she holds are the focal elements. "
            "The office has a 1960s typewriter, papers on the desk, warm light. "
            "CRITICAL: EXACTLY TWO people — Pamela at her desk holding the letter + Bob standing. "
            "NO other people visible anywhere — no background figures, no one through any door or window. "
            "The letter and the typewriter together tell the story of the problem."
        ),
    },
    {
        "id": "terrible_handwriting",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of Pamela's office. "
            "PAMELA (short blonde hair, rose pink blouse, dark grey pencil skirt) "
            "sits at her desk, holding the letter at arm's length away from her, "
            "turning her face AWAY from the letter with an expression of total disgust "
            "and bewilderment — eyes screwed shut or looking sideways in exasperation. "
            "She holds the letter with one hand at a distance, almost like it smells bad. "
            "The letter is held FACE AWAY from the viewer — we see the BLANK BACK of the letter, "
            "showing only white paper, NO text visible. "
            "BOB (short brown hair, mid-grey suit) stands beside her with his hands raised helplessly, "
            "a sympathetic grimace on his face. "
            "CRITICAL: EXACTLY TWO people — Pamela reacting with disgust to the letter + Bob looking helpless. "
            "NO other people visible anywhere. "
            "CRITICAL: The letter shows its BLANK BACK — absolutely NO text visible anywhere in the frame."
        ),
    },
]
