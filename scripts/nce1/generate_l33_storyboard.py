#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 33: A Fine Day
# Story: The Jones family walks over a bridge on a fine sunny day.
# There are boats on the river. Mr. & Mrs. Jones look at boats.
# Sally watches a big ship going under the bridge.
# Tim looks at an aeroplane flying over the river.
# Characters: Mr. Jones, Mrs. Jones, Sally (young girl), Tim (young boy)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm sunny English riverside afternoon light, cheerful family outing mood. "
)

SCENE = (
    "Location: a sunny English riverside scene — "
    "a wide stone bridge over a calm river, "
    "several boats and a large ship on the blue river, "
    "green banks with trees, blue sky with a few fluffy white clouds, "
    "warm golden afternoon sunlight. "
    "Keep the stone bridge, blue river, green banks, and bright sunny sky consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_MR_JONES = (
    "Character MR. JONES: a friendly British father, approximately 38-42 years old, "
    "short dark hair with a side parting, warm pleasant face, "
    "wearing a brown tweed jacket over a white shirt with grey trousers. "
    "CRITICAL: brown tweed jacket + white shirt + grey trousers + dark side-parted hair — NEVER change. "
)

CHAR_MRS_JONES = (
    "Character MRS. JONES: a pleasant British mother, approximately 35-40 years old, "
    "shoulder-length chestnut brown hair, warm smiling expression, "
    "wearing a coral pink blouse and navy blue skirt. "
    "CRITICAL: coral pink blouse + navy blue skirt + chestnut hair — NEVER change. "
)

CHAR_SALLY = (
    "Character SALLY: a young girl, approximately 9-10 years old, "
    "long blonde hair tied in a ponytail, bright curious expression, "
    "wearing a yellow sundress. "
    "CRITICAL: blonde ponytail + yellow sundress — NEVER change. "
)

CHAR_TIM = (
    "Character TIM: a young boy, approximately 8-10 years old, "
    "short dark hair, enthusiastic energetic expression, "
    "wearing a red t-shirt and brown shorts. "
    "CRITICAL: short dark hair + red t-shirt + brown shorts — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide sunny scene: the Jones family walks together across a wide stone bridge. "
            "Mr. Jones (brown tweed jacket, grey trousers) walks in the centre, smiling. "
            "Mrs. Jones (coral pink blouse, navy skirt) walks beside him, looking happy. "
            "Sally (yellow sundress, blonde ponytail) skips ahead on the bridge. "
            "Tim (red t-shirt, brown shorts) walks beside his parents, looking around excitedly. "
            "The stone bridge spans a calm blue river with green banks below. "
            "Blue sky with a few fluffy white clouds, warm golden sunlight. "
            "CRITICAL: EXACTLY FOUR family members — Mr. Jones + Mrs. Jones + Sally + Tim. "
            "Show all four characters clearly walking over the bridge. Cheerful sunny atmosphere."
        ),
    },
    {
        "id": "boats_on_river",
        "desc": (
            "View from the bridge looking DOWN at the calm blue river below. "
            "On the river: several small wooden rowing boats and sailboats drift gently — "
            "clearly visible on the shimmering blue water. "
            "Mr. Jones (brown tweed jacket) and Mrs. Jones (coral pink blouse) "
            "stand at the bridge railing side by side, leaning forward slightly, "
            "looking down at the boats with pleasure. "
            "The boats on the river are the visual focal point — clearly visible below. "
            "Green river banks with trees visible in the background. "
            "CRITICAL: EXACTLY TWO adults — Mr. Jones + Mrs. Jones looking at the boats. "
            "Sally and Tim are NOT in this frame."
        ),
    },
    {
        "id": "sally_ship",
        "desc": (
            "FOCAL CHARACTER: SALLY — young girl, blonde ponytail, yellow sundress. "
            "Sally stands at the stone bridge railing, leaning over it with wide excited eyes, "
            "gazing at a LARGE SHIP that is sailing directly UNDER THE BRIDGE below her. "
            "The large ship — with its tall funnel — is clearly visible passing under the bridge arch. "
            "Sally's face shows wonder and delight as she watches the big ship. "
            "COMPOSITION: Sally in foreground at the railing; large ship visible through/below the bridge arch. "
            "CRITICAL: Sally is the ONLY person in this frame — no other family members. "
            "The large ship going UNDER THE BRIDGE is the key visual element."
        ),
    },
    {
        "id": "tim_aeroplane",
        "desc": (
            "FOCAL CHARACTER: TIM — young boy, short dark hair, red t-shirt, brown shorts. "
            "Tim stands on the bridge, head tilted back, looking up at the sky with huge excited eyes "
            "and pointing upward with one finger. "
            "HIGH ABOVE in the sky: a small AEROPLANE flies over the river — clearly visible against the blue sky. "
            "The aeroplane is flying OVER THE RIVER — river and green banks visible below in the background. "
            "Tim's upward gaze and pointing gesture are the focal action. "
            "CRITICAL: Tim is the ONLY person in this frame — no other family members. "
            "The aeroplane flying over the river is the key visual element. Bright sunny blue sky."
        ),
    },
]
