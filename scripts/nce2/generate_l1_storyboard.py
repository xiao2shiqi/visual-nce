#!/usr/bin/env python3

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cinematic theatre lighting, gentle nostalgic mood. "
)

SCENE = (
    "Location: a classic old-fashioned English theatre auditorium with ornate gold trim, "
    "red velvet seats, balcony boxes, soft amber wall lamps, and a brightly lit stage with "
    "red curtains during a live play. Keep the theatre architecture, stage position, seat rows, "
    "and lighting direction consistent across all frames. No captions, no speech bubbles, no subtitles, "
    "no split panels, and no visible written words anywhere in the theatre. "
)

CHAR_WRITER = (
    "Character Writer: middle-aged British man, tidy light brown hair combed to the side, "
    "slim face, wearing a neat grey suit, white shirt, and dark red tie. He is seated near the "
    "front with a clear view of the stage. He is only a normal audience member and should not hold a "
    "notebook, pen, program, or any extra object unless explicitly requested. "
)

CHAR_YOUNG_MAN = (
    "Character Young Man: early twenties, short messy black hair, lively expression, "
    "wearing a cobalt blue crew-neck sweater and dark trousers. "
)

CHAR_YOUNG_WOMAN = (
    "Character Young Woman: early twenties, long chestnut-brown hair, cheerful expression, "
    "wearing a soft yellow floral dress. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the theatre. The Writer sits comfortably in a very good seat, "
            "facing the interesting play on stage. The atmosphere feels elegant, calm, and immersive. "
            "He is simply watching the play."
        ),
    },
    {
        "id": "young_couple_talking",
        "desc": (
            "The Writer is seated in the foreground, while the young man and young woman are clearly seated in the row "
            "directly behind him. They lean toward each other and talk loudly with animated hands, while the Writer tries "
            "to focus on the stage and looks distracted."
        ),
    },
    {
        "id": "writer_turns_angrily",
        "desc": (
            "The Writer has turned round in his seat and is glaring angrily at the young couple behind him. "
            "The couple are still chatting and paying no attention to him. No signs, captions, or written text anywhere."
        ),
    },
    {
        "id": "writer_complains",
        "desc": (
            "The Writer turns round again and speaks angrily toward the young couple, clearly saying he cannot hear "
            "a word of the play. His posture is tense and frustrated, while nearby audience members glance over in surprise. "
            "Single cinematic frame only, no speech bubbles, no captions, no subtitles, and no written text anywhere."
        ),
    },
    {
        "id": "young_man_replies_rudely",
        "desc": (
            "The young man looks back at the Writer with a rude, dismissive expression and gestures sharply as he replies. "
            "The young woman stays beside him, still unconcerned. The stage remains visible in the background. "
            "Show only these three key characters clearly. The Writer must have empty hands, with no program, no paper, "
            "and no visible text anywhere."
        ),
    },
    {
        "id": "private_conversation_reply",
        "desc": (
            "Final confrontation in the theatre. The young man is turned toward the Writer and speaking with rude confidence, "
            "making it clear he means 'This is a private conversation!' The young woman sits beside him, unconcerned. The Writer "
            "has turned back toward them in disbelief and anger. Show all three characters in one normal theatre shot with the "
            "same seat row relationship as earlier frames."
        ),
    },
]
