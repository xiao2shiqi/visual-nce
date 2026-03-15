#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 47: A Cup of Coffee
# Story: Christine offers Ann a cup of coffee. Ann says yes please.
# Christine asks about sugar (yes please) and milk (no thank you).
# Both prefer black coffee. Christine offers biscuits — Ann accepts one.
# Characters: CHRISTINE (host woman), ANN (guest woman)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British living room afternoon light, cosy friendly mood. "
)

SCENE = (
    "Location: a cosy 1960s British living room — "
    "a low coffee table with cups and saucers, a small sofa and armchairs, "
    "a sideboard with a coffee pot, a window with soft net curtains, "
    "warm afternoon light, floral wallpaper. "
    "Keep the coffee table, armchairs, sideboard, and warm light consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_CHRISTINE = (
    "Character CHRISTINE: a pleasant British woman, approximately 30-35 years old, "
    "short neat auburn hair, warm hospitable expression, "
    "wearing a cream blouse and a light brown cardigan. "
    "CRITICAL: short auburn hair + cream blouse + light brown cardigan — NEVER change. "
    "She is the hostess, pouring or serving coffee. "
)

CHAR_ANN = (
    "Character ANN: a friendly British woman, approximately 30-35 years old, "
    "shoulder-length dark hair, relaxed and pleased expression, "
    "wearing a navy blue blouse and a grey skirt. "
    "CRITICAL: shoulder-length dark hair + navy blue blouse + grey skirt — NEVER change. "
    "She is the guest, sitting and receiving coffee. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the cosy 1960s British living room. "
            "CHRISTINE (short auburn hair, cream blouse, light brown cardigan) "
            "sits in an armchair beside the coffee table, looking pleasantly at Ann — "
            "'Do you like coffee?' "
            "ANN (shoulder-length dark hair, navy blue blouse, grey skirt) "
            "sits in the opposite armchair, smiling and nodding — 'Yes, I do.' "
            "On the coffee table between them: an empty cup and saucer. "
            "The low coffee table is between both women. "
            "CRITICAL: EXACTLY TWO women — Christine + Ann sitting in armchairs opposite each other. "
            "Show both characters clearly. Warm cosy living room atmosphere."
        ),
    },
    {
        "id": "ann_coffee",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of Christine pouring and Ann receiving coffee. "
            "CHRISTINE (short auburn hair, cream blouse, light brown cardigan) "
            "stands at the sideboard or leans over the coffee table, "
            "pouring COFFEE from a coffee pot into a white cup and saucer. "
            "ANN (shoulder-length dark hair, navy blue blouse, grey skirt) "
            "sits in her armchair watching with anticipation, leaning forward slightly — "
            "'Yes, please, Christine.' "
            "The COFFEE POT pouring into the CUP is the focal action. "
            "Warm coffee steam visible rising from the cup. "
            "CRITICAL: EXACTLY TWO women — Christine pouring coffee + Ann waiting eagerly. "
            "Do NOT show the full room — focus on the coffee pouring action."
        ),
    },
    {
        "id": "sugar_no_milk",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the coffee table with the coffee cups. "
            "On the coffee table: TWO white cups of black coffee — no milk. "
            "A SUGAR BOWL is on the table between the cups. "
            "A MILK JUG is also on the table but set aside, slightly apart. "
            "CHRISTINE (short auburn hair, cream blouse, light brown cardigan) "
            "holds the SUGAR BOWL toward Ann, offering it. "
            "ANN (shoulder-length dark hair, navy blue blouse, grey skirt) "
            "reaches for the sugar, giving a small approving nod — 'Yes, please.' "
            "Both women look relaxed and friendly. "
            "CRITICAL: EXACTLY TWO women — Christine offering sugar + Ann accepting. "
            "The SUGAR BOWL offered + MILK JUG set aside tells the story. "
            "No text on any items. Do NOT show the full room."
        ),
    },
    {
        "id": "biscuits",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the coffee table with biscuits. "
            "On the coffee table: two cups of black coffee. "
            "CHRISTINE (short auburn hair, cream blouse, light brown cardigan) "
            "holds out a PLATE OF BISCUITS — several round plain biscuits on a plate — "
            "toward Ann with a friendly, inviting smile — 'Do you want one?' "
            "ANN (shoulder-length dark hair, navy blue blouse, grey skirt) "
            "reaches forward to take a biscuit from the plate with a pleased smile — "
            "'Yes, please.' "
            "The PLATE OF BISCUITS between the two women is the focal prop. "
            "CRITICAL: EXACTLY TWO women — Christine offering biscuits + Ann taking one. "
            "Do NOT show the full room. No text on the plate or biscuits."
        ),
    },
]
