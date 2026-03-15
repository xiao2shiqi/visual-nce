#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 17: How do you do?
# Story: Mr. Jackson gives Mr. Richards a tour of the office, introducing staff.
# Nicola Grey & Claire Taylor: keyboard operators — very hard-working.
# Michael Baker & Jeremy Short: sales reps — NOT very busy (lazy!).
# Jim: young office assistant.
# Characters: Mr. Jackson (manager), Mr. Richards (visitor), Nicola, Claire,
#             Michael, Jeremy, Jim
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1970s office interior light, nostalgic professional mood. "
)

SCENE = (
    "Location: a large open-plan 1970s British office — "
    "rows of wooden desks with mechanical typewriters, "
    "tall windows overlooking a city street, "
    "filing cabinets and bookshelves along the walls, "
    "warm fluorescent overhead light and natural daylight. "
    "Keep the office layout, wooden desks, windows, and warm lighting consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words or signs. "
)

CHAR_JACKSON = (
    "Character MR. JACKSON: senior manager, approximately 50-55 years old, "
    "neatly combed grey hair, authoritative but friendly face, "
    "wearing a dark navy suit jacket with a crisp white shirt and a red tie. "
    "CRITICAL: dark navy suit + red tie + grey hair — NEVER change. "
    "He looks like a confident, experienced office manager. "
)

CHAR_RICHARDS = (
    "Character MR. RICHARDS: business visitor, approximately 40-45 years old, "
    "short brown hair, wearing round tortoiseshell glasses, "
    "wearing a brown tweed suit jacket over a pale shirt. "
    "CRITICAL: brown tweed suit + round glasses — NEVER change. "
    "He looks like a curious, observant visiting businessman. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the office entrance area. "
            "Mr. Jackson (dark navy suit, red tie, grey hair) stands with Mr. Richards "
            "(brown tweed suit, round glasses), gesturing broadly across the busy open-plan office. "
            "Office desks, typewriters, and windows with city light are visible behind them. "
            "Mr. Jackson looks proud and welcoming; Mr. Richards looks impressed and curious. "
            "Show both men clearly. Professional, warm atmosphere."
        ),
    },
    {
        "id": "keyboard_operators",
        "desc": (
            "Two young women sit at adjacent wooden desks typing busily on large mechanical typewriters. "
            "NICOLA GREY: dark-haired young woman, approximately 25 years old, "
            "wearing a smart navy blue blouse, typing with focused concentration. "
            "CLAIRE TAYLOR: blonde-haired young woman, approximately 25 years old, "
            "wearing a smart green blouse, also typing energetically. "
            "Both women look industrious, professional, and very hard at work. "
            "Mr. Jackson stands nearby gesturing toward them with an approving expression. "
            "Mr. Richards watches from one side, nodding. "
            "Show all four characters. Office background with typewriters and filing cabinets."
        ),
    },
    {
        "id": "sales_reps",
        "desc": (
            "Two young men lean casually against a desk in the office, clearly not busy. "
            "MICHAEL BAKER: young man, approximately 28 years old, light brown hair, "
            "wearing a pale blue shirt and a loosened tie, arms crossed, smirking. "
            "JEREMY SHORT: young man, approximately 28 years old, dark hair, "
            "wearing a white shirt with tie, hands in pockets, looking bored. "
            "Both men look relaxed, idle, and completely unbothered. "
            "Mr. Richards stands nearby watching them with a raised eyebrow and unimpressed expression. "
            "Show all three characters clearly. Office background."
        ),
    },
    {
        "id": "introductions",
        "desc": (
            "Mr. Richards shakes hands with Michael Baker while Jeremy Short stands beside them. "
            "Mr. Richards (brown tweed suit, round glasses) reaches out his hand formally. "
            "Michael (pale blue shirt, loosened tie) shakes it with a casual grin. "
            "Jeremy (white shirt) watches with a lazy half-smile. "
            "Mr. Jackson (navy suit, red tie) stands to one side with a slight grimace — "
            "clearly aware his sales reps are not making a great impression. "
            "Show all four characters. Office background."
        ),
    },
    {
        "id": "jim",
        "desc": (
            "FOCAL CHARACTER: JIM — a young office assistant, approximately 18-20 years old, "
            "with slightly messy dark hair and an eager expression, "
            "wearing a white shirt and a grey waistcoat. "
            "Jim is shown prominently in the FOREGROUND carrying a large stack of papers and files, "
            "looking energetic and purposeful as he hurries across the office. "
            "Mr. Richards and Mr. Jackson are visible smaller in the background watching him. "
            "CRITICAL: Jim must be the large foreground focal character. "
            "Warm office light. Show the busy, youthful energy."
        ),
    },
]
