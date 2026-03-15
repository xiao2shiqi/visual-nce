#!/usr/bin/env python3

# =============================================================================
# NCE2 Lesson 25: Do the English Speak English?
# Story: A young foreign man arrives at a dark London railway station and
# struggles to understand the local porter's thick English accent.
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cinematic lighting with deep shadows, "
    "nostalgic 1960s atmosphere. "
)

SCENE = (
    "Location: a grand Victorian London railway station — large arched iron-and-glass ceiling, "
    "dark soot-stained brick walls, amber gas-lamp-style platform lights casting warm pools of light "
    "in the surrounding dimness, wisps of steam from a departed train, worn wooden trolleys and "
    "leather luggage on the platform. "
    "Keep the station architecture, lamp positions, platform width, and lighting direction "
    "strictly consistent across ALL frames. "
    "No captions, no speech bubbles, no subtitles, no text signs readable in English, "
    "no split panels anywhere in any image. "
)

CHAR_WRITER = (
    "Character THE WRITER: young adult man, approximately 25 years old, "
    "short neat black hair, light olive skin, slender build, "
    "wearing a dark navy wool overcoat with a small turned-up collar, "
    "a burgundy scarf, and carrying a large brown leather travel bag on his left shoulder. "
    "His face shows a slightly anxious but polite expression. "
    "He is the FOREIGNER and ALWAYS appears younger and slimmer than the Porter. "
    "CRITICAL: navy overcoat + burgundy scarf + brown leather bag — these NEVER change. "
)

CHAR_PORTER = (
    "Character THE PORTER: stocky middle-aged English railway porter, approximately 50 years old, "
    "greying temples and short grey-brown hair, ruddy weathered face with a broad friendly smile, "
    "wearing a dark navy railway uniform jacket with brass buttons and a matching flat porter's cap. "
    "He has a sturdy, barrel-chested build and is clearly taller and heavier than the Writer. "
    "CRITICAL: dark navy uniform + brass buttons + flat cap — these NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the grand Victorian station platform at night. "
            "The Writer has just arrived — he stands alone near a trolley of luggage, "
            "looking slightly overwhelmed by the vast dark station around him. "
            "He grips his brown leather travel bag tightly with both hands. "
            "In the mid-distance, the Porter stands beside a luggage trolley under an amber lamp. "
            "Steam drifts across the platform. No other characters visible. "
            "Atmosphere: grand, dark, slightly intimidating but beautiful."
        ),
    },
    {
        "id": "writer_asks_porter",
        "desc": (
            "Medium shot on the station platform. The Writer stands facing the Porter directly. "
            "The Writer's posture is upright and careful — he is speaking very slowly and clearly, "
            "enunciating every syllable, with one hand slightly raised in a polite gesture. "
            "His expression is earnest and focused. The Porter stands listening, cap on head, "
            "hands at his sides, with a neutral attentive expression. "
            "Amber platform lamp overhead illuminates both faces. "
            "Show BOTH characters from roughly waist-up in the same frame."
        ),
    },
    {
        "id": "porter_confused",
        "desc": (
            "Medium close-up on the station platform. The Porter tilts his head sideways "
            "with a puzzled, baffled expression — eyebrows raised, lips pursed — clearly "
            "not understanding the Writer's careful pronunciation. "
            "The Writer in the foreground is repeating his question, leaning slightly forward, "
            "holding up a finger as if saying 'one more time'. "
            "Both characters visible in the same frame. No text, no speech elements."
        ),
    },
    {
        "id": "porter_replies",
        "desc": (
            "Medium shot. Now it is the Porter's turn to speak. He talks with confident energy, "
            "gesturing broadly with one hand toward the station exit, speaking at normal rapid pace "
            "in his thick regional accent. His expression is helpful and friendly. "
            "The Writer stands opposite him, looking completely baffled — mouth slightly open, "
            "brow furrowed, unable to follow a single word. "
            "Contrasting energy: Porter animated and confident, Writer frozen in confusion."
        ),
    },
    {
        "id": "says_foreigner",
        "desc": (
            "Medium two-shot. The Writer places one hand on his chest in a self-introduction gesture, "
            "clearly saying 'I am a foreigner' — his expression is apologetic and earnest. "
            "The Porter reacts with a look of gentle understanding, nodding slowly, "
            "now beginning to speak more slowly and deliberately. "
            "Both face each other on the dimly lit platform, the amber lamp behind them. "
            "The Porter's posture softens slightly with sympathy."
        ),
    },
    {
        "id": "both_smile",
        "desc": (
            "Warm medium shot. The Writer and the Porter are looking at each other directly "
            "and both sharing a genuine, warm smile — a moment of human connection across "
            "the language barrier. The Writer's tension has relaxed; his shoulders are lower. "
            "The Porter's broad friendly face is lit up with a kind grin. "
            "Soft amber light from the platform lamp bathes the scene. "
            "Atmosphere: warm, funny, and touching. This is the emotional peak of the story."
        ),
    },
    {
        "id": "you_learn_english",
        "desc": (
            "Final scene on the platform. The Porter points a friendly finger at the Writer "
            "with an encouraging expression, as if delivering a cheerful verdict. "
            "The Writer stands slightly apart, looking thoughtful and wry — a hint of amused "
            "disbelief on his face as he reflects on what he has just experienced. "
            "In the wide background, other passengers of different types pass by on the platform, "
            "suggesting the diversity of English accents and people. "
            "Mood: gently comic and reflective. Warm amber station lighting."
        ),
    },
]
