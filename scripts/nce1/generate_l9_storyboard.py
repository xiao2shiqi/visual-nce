#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 9: How Are You Today?
# Story: Steven and Helen bump into each other on a sunny park path.
# They greet each other cheerfully, ask how each other is, mention Tony
# (Helen's son) and Emma (Steven's wife), then say goodbye and go separate ways.
# Characters: Steven (young man), Helen (young woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm sunny outdoor English park light, cheerful friendly mood. "
)

SCENE = (
    "Location: a pleasant English park path on a sunny day — "
    "a wide tree-lined path with green grass on either side, "
    "colourful flower beds, old-fashioned park benches, "
    "dappled sunlight through leafy trees overhead. "
    "Keep the park path, green trees, flower beds, and warm sunlight consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_STEVEN = (
    "Character STEVEN: young man, approximately 22-25 years old, "
    "short dark hair, relaxed cheerful expression, "
    "wearing a bright orange crew-neck sweater and dark blue jeans. "
    "CRITICAL: orange sweater + dark jeans — NEVER change. "
    "He looks like a happy, easygoing young man. NOT middle-aged. "
)

CHAR_HELEN = (
    "Character HELEN: young woman, approximately 22-25 years old, "
    "shoulder-length warm brown hair, bright cheerful smile, "
    "wearing a light yellow dress with a white cardigan over it. "
    "CRITICAL: light yellow dress + white cardigan + brown hair — NEVER change. "
    "She looks like a friendly, healthy young woman. NOT middle-aged. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the sunny park path. "
            "Steven and Helen have just spotted each other coming from opposite directions "
            "and are both raising a hand in surprised, happy greeting. "
            "They are still a few steps apart on the path. "
            "Trees and flower beds visible on either side. "
            "Warm sunlight, cheerful atmosphere. Show both characters clearly."
        ),
    },
    {
        "id": "meeting",
        "desc": (
            "Steven and Helen now stand face to face on the path, smiling broadly "
            "as they greet each other. "
            "Steven's orange sweater and Helen's yellow dress are clearly visible. "
            "They look genuinely pleased to meet. "
            "Park background with flower beds and trees. Show both characters clearly."
        ),
    },
    {
        "id": "helen_healthy",
        "desc": (
            "Close-medium shot of Helen, smiling radiantly and looking very healthy and energetic. "
            "She stands straight with a bright expression, clearly in good spirits. "
            "Her light yellow dress and white cardigan are clearly visible. "
            "Steven is visible beside her, watching her with a pleased expression. "
            "Warm park sunlight. Show both characters."
        ),
    },
    {
        "id": "steven_fine",
        "desc": (
            "Close-medium shot of Steven, nodding contentedly and smiling — "
            "he looks relaxed, healthy, and at ease. "
            "His orange sweater is clearly visible. "
            "He gestures casually with one hand as he replies. "
            "Helen is visible beside him, listening warmly. "
            "Dappled park light. Show both characters."
        ),
    },
    {
        "id": "tony_fine",
        "desc": (
            "Helen talks about Tony — she gestures fondly, perhaps miming a child's height "
            "with one hand held low, smiling warmly as she mentions him. "
            "Her expression is affectionate and proud. "
            "Steven listens and nods with an interested smile. "
            "Show both characters on the sunny park path."
        ),
    },
    {
        "id": "emma_fine",
        "desc": (
            "Steven mentions Emma — he gestures with a warm, fond expression, "
            "looking happy as he talks about her. "
            "Helen nods and smiles back in understanding. "
            "Show both characters on the park path. Warm sunlight and flower beds visible."
        ),
    },
    {
        "id": "goodbye",
        "desc": (
            "Wide shot of the park path. "
            "Steven and Helen have turned and are walking away from each other "
            "in opposite directions along the path. "
            "They each look back over their shoulders, waving goodbye with a smile. "
            "The warm park stretches behind each of them. "
            "Charming, cheerful parting atmosphere. Show both characters clearly."
        ),
    },
]
