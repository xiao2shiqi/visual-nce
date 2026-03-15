#!/usr/bin/env python3

# =============================================================================
# NCE2 Lesson 6: Percy Buttons
# Story: The narrator (young woman, just moved house) meets Percy Buttons —
# a cheerful old beggar who does headstands and sings in exchange for a meal.
# A neighbour explains he visits every house on the street monthly.
# Characters: Narrator/Writer (young woman), Percy (old beggar), Neighbour (middle-aged woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm English suburban light, charming nostalgic mood. "
)

SCENE = (
    "Location: a row of charming 1960s English terraced houses on Bridge Street — "
    "red brick facades, small front gardens with low garden walls, "
    "wooden front doors painted in different colours, "
    "net curtains in windows, a garden gate at each house. "
    "The interior shows a cozy kitchen or dining room with a small wooden table, "
    "mismatched chairs, and warm afternoon light. "
    "Keep the house exterior, brick colour, garden gate, and warm lighting consistent across all frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_NARRATOR = (
    "Character THE NARRATOR: young woman, approximately 25-28 years old, "
    "shoulder-length auburn hair, friendly curious face with an open expression, "
    "wearing a light blue floral blouse and a cream cardigan. "
    "CRITICAL: auburn hair + blue floral blouse + cream cardigan — NEVER change. "
    "She looks like a cheerful young homeowner who has just moved in. NOT middle-aged. "
)

CHAR_PERCY = (
    "Character PERCY BUTTONS: old beggar man, approximately 65-70 years old, "
    "scraggly white hair under a battered brown felt hat, weathered wrinkled face with a gap-toothed grin, "
    "wearing a worn patchwork coat covered in mismatched buttons of all colours and sizes, "
    "loose grey trousers, and scuffed old boots. He carries a small canvas sack. "
    "CRITICAL: battered hat + colourful button-covered coat + canvas sack — NEVER change. "
    "He looks eccentric, harmless, and oddly charming. Clearly elderly. "
)

CHAR_NEIGHBOUR = (
    "Character THE NEIGHBOUR: middle-aged woman, approximately 50 years old, "
    "neatly curled grey-brown hair, rosy cheeks, warm gossipy expression, "
    "wearing a floral apron over a navy dress. "
    "CRITICAL: floral apron + navy dress — NEVER change. She appears only in neighbour scenes. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the front of the terraced house on Bridge Street. "
            "The Narrator stands at her open front door looking surprised. "
            "Percy Buttons stands at the garden gate or doorstep — battered hat in hand, "
            "gap-toothed grin on his face, canvas sack over his shoulder. "
            "He looks cheerful and completely at ease, as if this is totally normal. "
            "The row of other terraced houses stretches along the street behind him. "
            "Atmosphere: charming, slightly comic, warm."
        ),
    },
    {
        "id": "percy_performs",
        "desc": (
            "The front garden path of the narrator's house. "
            "Percy Buttons is performing a headstand on the garden path — "
            "upside down, legs straight in the air, his battered hat on the ground nearby, "
            "his colourful button coat hanging around his shoulders as he balances. "
            "His face (upside down) shows a joyful grin. "
            "The Narrator stands at the door watching with wide eyes and an amused half-smile. "
            "Show both characters clearly. Charming and comic atmosphere."
        ),
    },
    {
        "id": "percy_eats",
        "desc": (
            "Interior: the narrator's cozy kitchen. "
            "EXACTLY ONE Percy Buttons sits at the small wooden table — there is only ONE Percy in this scene. "
            "Percy eats a plate of food with great contentment and holds a glass of beer. "
            "His battered hat rests on the table beside him. His colourful button-covered coat is still on. "
            "He looks completely at home and satisfied. "
            "The Narrator (auburn hair, light blue floral blouse, cream cardigan) stands nearby "
            "watching him with a mix of amusement and bemusement. "
            "CRITICAL: Do NOT duplicate Percy — only ONE old man at the table. "
            "Warm kitchen light. Show both characters clearly."
        ),
    },
    {
        "id": "percy_pockets_cheese",
        "desc": (
            "At the narrator's front door or garden gate. "
            "Percy stands saying cheerful goodbye, his canvas sack over one shoulder. "
            "With an impish grin he is carefully tucking a large piece of yellow cheese "
            "into his deep coat pocket among the colourful buttons. "
            "The Narrator stands in the doorway watching with an amused raised eyebrow. "
            "Percy tips his battered hat farewell. "
            "Comic and warm atmosphere. Show both characters clearly."
        ),
    },
    {
        "id": "neighbour_explains",
        "desc": (
            "The garden fence between the narrator's house and the neighbour's house. "
            "The Neighbour (grey-brown curly hair, floral apron over navy dress) leans over the fence "
            "toward the Narrator with a knowing, gossipy expression, explaining everything about Percy "
            "with animated gestures. "
            "The Narrator (auburn shoulder-length hair, light blue floral blouse, cream cardigan) "
            "listens with wide eyes, beginning to understand. "
            "CRITICAL: The Narrator MUST wear her light blue floral blouse and cream cardigan — "
            "do NOT change her outfit from the other frames. "
            "Both women are shown clearly from the front. Garden and brick houses visible behind them. "
            "The Neighbour's floral apron is clearly visible. Warm afternoon light."
        ),
    },
    {
        "id": "monthly_visitor",
        "desc": (
            "Wide shot of Bridge Street. "
            "Percy Buttons — the old beggar man with battered brown felt hat, colourful button-covered coat, "
            "canvas sack over shoulder, and scuffed boots — walks cheerfully along the pavement. "
            "He approaches the next terraced house in the row, battered hat raised in a cheerful greeting. "
            "A row of red-brick terraced houses stretches along the street ahead of him. "
            "Through one window, a curious face peeks out watching him approach. "
            "Percy strides along with the confidence of a man on his regular monthly rounds. "
            "CRITICAL: The main (and only walking) figure is Percy — an OLD ECCENTRIC BEGGAR MAN "
            "in his distinctive button coat, NOT a young woman, NOT a narrator. "
            "No one stands at a doorway in the foreground. Percy walks the street. "
            "Charming, comic, nostalgic atmosphere."
        ),
    },
]
