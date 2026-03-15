#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 3: Sorry, Sir.
# Story: A young man comes to the cloakroom to collect his coat and umbrella.
# The attendant brings a red umbrella — wrong one. After searching, finds the
# correct dark green umbrella. The young man thanks him warmly.
# Characters: Young Man (customer), Attendant (older clerk)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm classic English interior light, nostalgic mood. "
)

SCENE = (
    "Location: a classic 1960s British theatre or hotel cloakroom — "
    "wooden-panelled counter, rows of coats and umbrellas hanging on numbered hooks behind, "
    "small numbered tags on each item, warm amber wall lighting, polished wooden floor. "
    "Keep the cloakroom interior, counter, coat racks, and warm lighting consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_CUSTOMER = (
    "Character THE YOUNG MAN: young man, approximately 22-25 years old, "
    "short black hair, neat appearance, polite expression, "
    "wearing a brown corduroy jacket over a white collared shirt and dark trousers. "
    "CRITICAL: brown corduroy jacket + white collar visible — NEVER change. "
    "He looks like a young professional or student. NOT middle-aged. "
)

CHAR_ATTENDANT = (
    "Character THE ATTENDANT: older man, approximately 60-65 years old, "
    "balding with white hair on the sides, kind wrinkled face, round spectacles, "
    "wearing a grey knitted vest over a light blue shirt with a dark tie. "
    "CRITICAL: round spectacles + grey vest + balding white-sided hair — NEVER change. "
    "He looks like a helpful, experienced cloakroom attendant. Clearly elderly. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the cloakroom counter. "
            "The Attendant stands behind the wooden counter, looking attentive and helpful. "
            "The Young Man stands on the other side of the counter, "
            "holding out a small paper cloakroom ticket toward the Attendant. "
            "Rows of hanging coats and umbrellas are visible on numbered hooks behind the Attendant. "
            "Warm amber light. Show both characters clearly."
        ),
    },
    {
        "id": "searching",
        "desc": (
            "Behind the counter, the Attendant searches carefully through a long row of hanging coats "
            "and umbrellas, leaning close to examine the small numbered tags on each item. "
            "His round spectacles are perched on his nose as he squints at the numbers. "
            "The Young Man waits patiently on the other side of the counter, watching. "
            "Show both characters. Atmosphere: methodical, slightly comic."
        ),
    },
    {
        "id": "wrong_umbrella",
        "desc": (
            "The Attendant has placed a dark coat on the counter and is holding out "
            "a bright red umbrella toward the Young Man. "
            "The Young Man is politely shaking his head 'no' — "
            "his hand raised slightly, eyebrows raised, expression apologetic but firm. "
            "The Attendant looks puzzled. Show both characters and the red umbrella clearly."
        ),
    },
    {
        "id": "showing_correct",
        "desc": (
            "The Attendant has returned to the coat rack and is now holding up "
            "a dark green umbrella, showing it over the counter toward the Young Man. "
            "The Young Man's expression shifts — his eyes widen with recognition, "
            "leaning forward slightly. "
            "Show both characters and the dark green umbrella prominently. "
            "The wrong red umbrella is back on its hook in the background."
        ),
    },
    {
        "id": "receiving_correct",
        "desc": (
            "The Young Man is smiling broadly, reaching out to take the dark green umbrella "
            "from the Attendant with both hands. "
            "The Attendant smiles back, looking relieved and pleased. "
            "The dark coat is folded over the counter between them. "
            "Warm, satisfying atmosphere. Show both characters clearly."
        ),
    },
    {
        "id": "exit",
        "desc": (
            "The Young Man walks away from the counter toward the exit, "
            "dark coat over one arm and dark green umbrella in hand, "
            "turning back to give a final wave of thanks. "
            "The Attendant waves back from behind the counter with a warm smile. "
            "Charming, warm atmosphere. Show both characters."
        ),
    },
]
