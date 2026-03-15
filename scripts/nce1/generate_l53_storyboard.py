#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 53: An Interesting Climate
# Story: Hans asks Jim about English weather. Jim describes England's mild
# but changeable climate: cold/windy in the North and East, wet in the West,
# sometimes warm in the South. They discuss seasons: Jim likes spring/summer
# (long days, early sunrise); dislikes autumn/winter (short days, late sunrise).
# England's weather is not great, but it's certainly interesting — favourite
# subject of conversation!
# Characters: JIM (English man), HANS (European man)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm conversational atmosphere, gentle British mood. "
)

SCENE = (
    "Location: a cosy British setting — "
    "perhaps a living room, a pub, or a café interior, "
    "with a window showing the outside weather, "
    "warm indoor lamp light. "
    "Keep the indoor conversational setting for the first frame; "
    "subsequent frames show scenic English landscapes in different moods. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_JIM = (
    "Character JIM: a friendly English man, approximately 30-35 years old, "
    "short sandy/light brown hair, cheerful easy-going expression, "
    "wearing a navy blue jumper/sweater and light grey trousers. "
    "CRITICAL: sandy light brown hair + navy blue jumper + light grey trousers — NEVER change. "
)

CHAR_HANS = (
    "Character HANS: a curious European man, approximately 30-35 years old, "
    "short neat blond hair, inquisitive attentive expression, "
    "wearing a dark green jacket over a light shirt. "
    "CRITICAL: short blond hair + dark green jacket + light shirt — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of a cosy British pub or café interior. "
            "JIM (sandy hair, navy blue jumper, light grey trousers) "
            "sits at a small table with a cup of tea, relaxed and expressive — "
            "explaining the English climate with an amused, self-deprecating smile. "
            "HANS (short blond hair, dark green jacket) sits opposite, "
            "leaning forward with a genuinely interested, curious expression. "
            "Through a window behind them: grey cloudy English sky, a light drizzle. "
            "The cosy interior with warm lamp light contrasts with the grey weather outside. "
            "CRITICAL: EXACTLY TWO men — Jim explaining + Hans listening curiously. "
            "Show both characters clearly. Warm cosy British pub/café atmosphere."
        ),
    },
    {
        "id": "north_cold",
        "desc": (
            "Wide panoramic landscape of NORTHERN ENGLAND in cold winter weather. "
            "The scene shows rugged moorland — rolling dark hills, grey stone walls, "
            "bare leafless trees bending in a strong cold wind, "
            "a grey overcast sky with heavy clouds. "
            "The colour palette is cold: grey, dark green, brown — a harsh raw windswept mood. "
            "Perhaps a stone farmhouse or lonely cottage on the moor in the distance. "
            "The wind and cold are the dominant atmosphere — stark, dramatic, cold. "
            "CRITICAL: NO people in this frame — pure scenic English northern landscape. "
            "Show windswept moorland, bare trees, grey sky, cold raw atmosphere."
        ),
    },
    {
        "id": "east_windy",
        "desc": (
            "Wide panoramic landscape of ENGLAND in spring/summer — the favourite seasons. "
            "The scene shows a glorious long summer day — "
            "a lush green English countryside with rolling hills and hedgerows, "
            "wildflowers in bloom, a bright blue sky with a few fluffy clouds, "
            "warm golden afternoon sunlight, "
            "long late-afternoon shadows showing the sun has not yet set. "
            "Birds singing in the trees, a cheerful river in the background. "
            "The mood is joyful, bright, full of light — long days, early sunrise. "
            "CRITICAL: NO people in this frame — pure scenic English summer landscape. "
            "Show bright blue sky, golden sunlight, lush green fields, flowers in bloom."
        ),
    },
    {
        "id": "west_wet",
        "desc": (
            "Wide panoramic landscape of WESTERN ENGLAND on a wet autumn/winter day. "
            "The scene shows a grey wet afternoon — "
            "rain falling steadily over rolling green fields and bare trees, "
            "a low grey sky with heavy rain clouds, "
            "puddles on country lanes, droplets on window glass in the foreground. "
            "The light is dim and fading — short winter day, early darkness approaching. "
            "Long shadows and grey dim light show the short days and long nights. "
            "The mood is gloomy, wet, atmospheric — classic English autumn. "
            "CRITICAL: NO people in this frame — pure scenic English wet western landscape. "
            "Show rain, grey sky, bare trees, gloomy short-day light."
        ),
    },
    {
        "id": "south_warm",
        "desc": (
            "Wide shot of the cosy British pub/café interior again. "
            "JIM (sandy hair, navy blue jumper) and HANS (blond hair, dark green jacket) "
            "sit together at the table, both laughing and shaking their heads with amused warmth. "
            "Jim spreads his hands with a cheerful resigned expression — "
            "'Not very good, but certainly interesting!' "
            "Hans laughs with delight — 'It's your favourite subject of conversation!' "
            "The window behind them shows a characteristically mixed English day — "
            "sun and clouds at the same time. "
            "The atmosphere is light-hearted, warm, and funny. "
            "CRITICAL: EXACTLY TWO men — Jim + Hans both laughing about English weather. "
            "Show both characters clearly enjoying the joke about English weather. "
            "NO other people visible."
        ),
    },
]
