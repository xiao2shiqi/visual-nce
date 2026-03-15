#!/usr/bin/env python3

# =============================================================================
# NCE2 Lesson 4: An Exciting Trip
# Story: The narrator received a letter from brother Tim, a young engineer
# working in Australia for the first time abroad. Tim has driven to Alice Springs
# and will fly to Perth — finding the whole trip very exciting.
# Characters: Narrator (young adult, reads letter at home) + Tim (young engineer in Australia)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm vibrant lighting, adventurous nostalgic mood. "
)

SCENE = (
    "Two main locations: "
    "(1) A cozy 1960s English living room with a wooden armchair, a small writing desk, "
    "a fireplace, and afternoon light through net curtains — for the narrator's home scenes. "
    "(2) The vast Australian outback — brilliant red-orange desert, dramatic rock formations, "
    "eucalyptus trees, endless blue sky, dusty dirt roads — for Tim's scenes in Australia. "
    "Keep each location's colour palette and architecture strictly consistent within its scenes. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_NARRATOR = (
    "Character THE NARRATOR: young adult, approximately 25-28 years old, "
    "neatly combed dark hair, clean-shaven friendly face, slim build, "
    "wearing a light grey V-neck pullover over a collared shirt and dark trousers. "
    "CRITICAL: grey pullover + collared shirt — NEVER change. Clearly young, NOT middle-aged. "
)

CHAR_TIM = (
    "Character TIM (the brother): young man, approximately 24-27 years old, "
    "short sandy-brown hair slightly windswept, energetic enthusiastic expression, "
    "wearing a khaki short-sleeved shirt, beige cargo trousers, and sturdy work boots. "
    "He carries a small engineer's notebook in his chest pocket. "
    "CRITICAL: khaki shirt + beige trousers + engineer notebook — NEVER change. "
    "He looks like a cheerful young engineer on his first big adventure. NOT middle-aged. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Interior of the narrator's cozy English living room. "
            "The Narrator sits in an armchair holding an opened envelope and a letter, "
            "reading with an expression of delight and excitement. "
            "An Australian postage stamp is visible on the envelope. "
            "Warm afternoon light through net curtains. "
            "Only the Narrator is present. Atmosphere: homely, curious, warm."
        ),
    },
    {
        "id": "tim_at_work",
        "desc": (
            "Australian scene. Tim stands confidently at an industrial construction or engineering site "
            "in the Australian outback. He holds his engineer's notebook and gestures toward large machinery, "
            "talking with workers nearby. "
            "Red-orange Australian landscape stretches behind him under a bright blue sky. "
            "Tim looks proud and capable. Show Tim clearly with one or two worker silhouettes nearby. "
            "CRITICAL OUTFIT: Tim MUST wear his khaki short-sleeved shirt and beige cargo trousers. "
            "He does NOT wear a grey sweater or V-neck pullover — those belong to a different character. "
            "Tim is a field engineer in khaki workwear, NOT an office person."
        ),
    },
    {
        "id": "tim_in_outback",
        "desc": (
            "Wide shot of the Australian outback. Tim drives a sturdy Australian car "
            "along a long dusty red dirt road stretching to the horizon. "
            "Dramatic red rock formations (like Uluru-style landscape) rise in the distance. "
            "Sparse eucalyptus trees dot the vast flat landscape under a blazing blue sky. "
            "Tim's face is visible through the windscreen — grinning with excitement. "
            "The scene feels vast, remote, and thrilling."
        ),
    },
    {
        "id": "tim_at_darwin",
        "desc": (
            "A small Australian regional airfield. Tim stands on the tarmac beside a small propeller plane, "
            "holding his travel bag, looking up at the plane with eager excitement. "
            "A pilot or ground crew member is near the plane. "
            "Clear blue Australian sky, warm golden light. "
            "Tim looks adventurous and ready for his next leg of the journey. "
            "Show Tim clearly in the foreground. Plane and airfield in background. "
            "CRITICAL OUTFIT: Tim MUST wear his khaki short-sleeved shirt and beige cargo trousers. "
            "CRITICAL NO TEXT: absolutely NO text, NO words, NO letters anywhere on the plane, "
            "NO country name, NO airline name, NO registration number, NO signage of any kind. "
            "Pure illustration — completely text-free."
        ),
    },
    {
        "id": "finding_exciting",
        "desc": (
            "Wide panoramic shot. Tim stands alone at the edge of a breathtaking Australian landscape — "
            "red desert, ancient rock formations, and an enormous vibrant sunset sky of orange and purple. "
            "He stands with arms slightly outstretched, looking at the horizon with pure wonder and joy. "
            "The scale of the landscape dwarfs him — he is a small figure against an immense beautiful world. "
            "This is the emotional climax: a young man experiencing the world for the first time. "
            "Only Tim is visible. Atmosphere: awe, freedom, excitement."
        ),
    },
]
