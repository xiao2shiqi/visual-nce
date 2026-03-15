#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 31: Where's Sally?
# Story: Jean asks Jack about Sally and Tim. Sally is sitting under a tree.
# Tim is climbing the tree. The dog is running across the grass after a cat.
# Characters: Jean (adult woman), Jack (adult man),
#             Sally (young girl), Tim (young boy), dog, cat
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm sunny British garden afternoon light, cheerful outdoor mood. "
)

SCENE = (
    "Location: a sunny 1960s British suburban garden — "
    "a large leafy oak tree in the centre of a green lawn, "
    "flower beds along a low brick wall, a garden path, "
    "warm golden afternoon sunlight, blue sky with fluffy clouds. "
    "Keep the oak tree, green lawn, brick wall, and warm sunlight consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_JEAN = (
    "Character JEAN: a pleasant British woman, approximately 30-35 years old, "
    "short wavy auburn hair, curious and animated expression, "
    "wearing a light green summer dress. "
    "CRITICAL: auburn wavy hair + light green dress — NEVER change. "
)

CHAR_JACK = (
    "Character JACK: a friendly British man, approximately 30-35 years old, "
    "short brown hair, relaxed pleasant face, "
    "wearing a light blue short-sleeved shirt and beige trousers. "
    "CRITICAL: short brown hair + light blue shirt + beige trousers — NEVER change. "
)

CHAR_SALLY = (
    "Character SALLY: a young girl, approximately 9-10 years old, "
    "long blonde hair tied in a ponytail, peaceful contented expression, "
    "wearing a yellow sundress. "
    "CRITICAL: blonde ponytail + yellow sundress — NEVER change. "
)

CHAR_TIM = (
    "Character TIM: a young boy, approximately 8-10 years old, "
    "short dark hair, adventurous grinning expression, "
    "wearing a red t-shirt and brown shorts. "
    "CRITICAL: short dark hair + red t-shirt + brown shorts — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the British garden on a sunny afternoon. "
            "Jean (auburn wavy hair, light green dress) stands on the garden path, "
            "gesturing toward the garden with a questioning expression. "
            "Jack (short brown hair, light blue shirt, beige trousers) stands beside her, "
            "pointing toward the large oak tree in the garden with a relaxed smile. "
            "The sunny garden with the large oak tree, green lawn, and flower beds is clearly visible. "
            "CRITICAL: EXACTLY TWO adults in this frame — Jean + Jack. "
            "Show both characters clearly. Warm afternoon garden light."
        ),
    },
    {
        "id": "sally_under_tree",
        "desc": (
            "FOCAL CHARACTER: SALLY — a young girl, approximately 9-10 years old, "
            "with long blonde hair in a ponytail and a peaceful expression, "
            "wearing a yellow sundress. "
            "Sally sits cross-legged on the grass UNDER a large leafy oak tree, "
            "leaning her back against the tree trunk, looking content and relaxed. "
            "Dappled sunlight through the oak leaves falls on her. "
            "The large tree trunk is clearly behind her; green lawn surrounds her. "
            "CRITICAL: Sally is the ONLY person in this frame — no other characters. "
            "Sally under the tree is the sole focal point. Warm garden light."
        ),
    },
    {
        "id": "tim_climbing",
        "desc": (
            "FOCAL CHARACTER: TIM — a young boy, approximately 8-10 years old, "
            "with short dark hair and a grinning adventurous expression, "
            "wearing a red t-shirt and brown shorts. "
            "Tim is shown ACTIVELY CLIMBING a large oak tree — "
            "his hands gripping a branch above, feet pushing off the trunk, "
            "body in motion climbing upward. He looks thrilled and energetic. "
            "The tree trunk and branches fill the frame. "
            "CRITICAL: Tim is the ONLY person in this frame — no other characters. "
            "Tim climbing the tree is the sole focal point. Sunny sky behind the treetop."
        ),
    },
    {
        "id": "dog_running",
        "desc": (
            "A lively medium-sized dog — a cheerful brown and white terrier — "
            "runs at full speed ACROSS the green lawn, "
            "all four legs extended in a bounding run, ears flying, tongue out. "
            "The green garden grass fills the background. "
            "The running dog is the SOLE focal point — shown large and dynamic in the centre. "
            "Motion lines or slight blur suggest speed. "
            "CRITICAL: ONLY the dog — no people in this frame. "
            "The dog running across the grass is the sole focus. Sunny garden background."
        ),
    },
    {
        "id": "dog_after_cat",
        "desc": (
            "DYNAMIC CHASE SCENE across the garden lawn. "
            "A brown and white terrier dog runs at full speed in pursuit, "
            "chasing an orange tabby cat that darts ahead of it. "
            "The CAT runs in the FOREGROUND slightly ahead, looking back with wide eyes. "
            "The DOG runs just behind the cat, mouth open, ears back, fully committed to the chase. "
            "Both animals are moving rapidly across the green grass. "
            "CRITICAL: EXACTLY ONE dog + ONE cat — no people in this frame. "
            "The dog-chasing-cat action across the lawn is the sole focal point. "
            "Bright sunny garden with green grass."
        ),
    },
]
