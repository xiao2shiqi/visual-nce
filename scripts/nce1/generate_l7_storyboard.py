#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 7: Are You a Teacher?
# Story: Robert introduces himself as a new student to Sophie at a language school.
# They exchange names, then ask about each other's jobs: Sophie is a keyboard
# operator; Robert is an engineer.
# Characters: Robert (young man), Sophie (young woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm indoor study light, friendly relaxed mood. "
)

SCENE = (
    "Location: a sunny 1960s language school study area — "
    "wooden tables and chairs, large windows with warm daylight, "
    "bookshelves in the background, notepads and pens on the tables. "
    "Keep the study area furniture, warm light, and wooden interior consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_ROBERT = (
    "Character ROBERT: young man, approximately 22-25 years old, "
    "short neat brown hair, friendly confident expression, slim build, "
    "wearing a green knitted sweater over a white collared shirt and dark trousers. "
    "CRITICAL: green knitted sweater + white collar visible — NEVER change. "
    "He looks like a cheerful young engineer or student. NOT middle-aged. "
)

CHAR_SOPHIE = (
    "Character SOPHIE: young woman, approximately 22-24 years old, "
    "auburn hair worn loose to the shoulders, elegant polite expression, "
    "wearing a light blue dress with a small floral pattern. "
    "CRITICAL: auburn hair + light blue floral dress — NEVER change. "
    "She looks like a poised, friendly young professional. NOT middle-aged. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the study area. "
            "Robert and Sophie are seated at the same wooden table, "
            "facing each other with notebooks and pens in front of them. "
            "Robert is introducing himself — smiling, gesturing toward himself. "
            "Sophie watches him with a friendly, curious expression. "
            "Warm daylight through the window. Show both characters clearly."
        ),
    },
    {
        "id": "robert_intro",
        "desc": (
            "Robert points to himself with one hand and smiles broadly, "
            "clearly saying his name. He looks confident and friendly. "
            "His green knitted sweater is clearly visible. "
            "Sophie is visible in the frame watching him with an interested smile. "
            "Show both characters clearly at the study table."
        ),
    },
    {
        "id": "sophie_intro",
        "desc": (
            "Sophie smiles and introduces herself, touching her own chest lightly "
            "with her fingertips in a graceful gesture. "
            "Her auburn hair and light blue floral dress are clearly visible. "
            "She looks poised and friendly. "
            "Robert is visible in the frame, listening with a warm smile. "
            "Show both characters clearly at the study table."
        ),
    },
    {
        "id": "talking_job",
        "desc": (
            "Robert leans forward slightly across the table, asking Sophie a question "
            "with an open, curious expression — gesturing with both hands as if asking. "
            "Sophie tilts her head thoughtfully, preparing to answer. "
            "Their notepads are on the table between them. "
            "Warm, conversational atmosphere. Show both characters clearly."
        ),
    },
    {
        "id": "keyboard_operator",
        "desc": (
            "Sophie explains her job — she makes a graceful typing gesture with her fingers "
            "as if at a keyboard, looking confident and professional. "
            "Her expression is animated and friendly. "
            "Robert watches her gesture with a look of interested understanding. "
            "Show both characters. Sophie's light blue floral dress is clearly visible."
        ),
    },
    {
        "id": "engineer",
        "desc": (
            "Robert explains his job as an engineer, gesturing with his hands "
            "as if drawing plans or working with tools — looking proud and happy. "
            "His green knitted sweater is clearly visible. "
            "Sophie nods with an impressed, interested smile. "
            "Show both characters. Warm study room light."
        ),
    },
]
