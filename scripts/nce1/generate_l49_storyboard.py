#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 49: At the Butcher's
# Story: Mrs. Bird shops at the butcher's. The butcher offers beef or lamb.
# She wants beef but the butcher pushes the nice lamb. She picks a steak
# and a pound of mince. Butcher offers chicken — she declines;
# her husband likes steak but not chicken. Butcher admits he doesn't
# like chicken either!
# Characters: BUTCHER (male), MRS. BIRD (female customer)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British butcher's shop light, cheerful market mood. "
)

SCENE = (
    "Location: a traditional 1960s British butcher's shop — "
    "a white tiled counter with cuts of meat displayed, "
    "a hanging rail with cuts of meat in the background, "
    "a weighing scale on the counter, white tiled walls, "
    "sawdust on the floor, warm shop lighting. "
    "Keep the white tiled counter, hanging meat display, and weighing scale consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_BUTCHER = (
    "Character THE BUTCHER: a friendly British shopkeeper, approximately 45-50 years old, "
    "short greying hair, round cheerful red-cheeked face, "
    "wearing a white butcher's coat/apron and a blue and white striped apron underneath, "
    "standing behind the white tiled counter. "
    "CRITICAL: white coat + striped apron + greying hair + red cheeks — NEVER change. "
)

CHAR_MRS_BIRD = (
    "Character MRS. BIRD: a pleasant British housewife, approximately 45-50 years old, "
    "short neat grey-brown hair, sensible and decisive expression, "
    "wearing a dark green coat and carrying a wicker shopping basket. "
    "CRITICAL: short grey-brown hair + dark green coat + wicker basket — NEVER change. "
    "She stands on the customer side of the counter. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the traditional 1960s British butcher's shop. "
            "THE BUTCHER (white coat, blue-striped apron, greying hair, red cheeks) "
            "stands behind the white tiled counter with cuts of meat displayed, "
            "smiling welcomingly at Mrs. Bird — 'Do you want any meat today?' "
            "MRS. BIRD (dark green coat, wicker basket, grey-brown hair) "
            "stands on the customer side of the counter, basket over her arm, "
            "looking at the meat on display with interest — 'Yes, please.' "
            "The white tiled counter with cuts of meat, hanging meat in background, "
            "and weighing scale on the counter are clearly visible. "
            "CRITICAL: EXACTLY TWO people — the Butcher behind counter + Mrs. Bird in front. "
            "Show both characters clearly. Traditional British butcher's shop atmosphere."
        ),
    },
    {
        "id": "showing_lamb",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the butcher's counter. "
            "THE BUTCHER (white coat, striped apron, greying hair) "
            "holds up a LEG OF LAMB — a large bone-in leg joint — toward Mrs. Bird, "
            "displaying it proudly with a persuasive smile — 'This lamb's very good!' "
            "MRS. BIRD (dark green coat, wicker basket) stands at the counter, "
            "looking at the lamb with polite interest but gesturing toward the beef — "
            "she wants BEEF not lamb. "
            "A rack of BEEF cuts is also clearly visible on the counter beside the lamb. "
            "The LEG OF LAMB and BEEF cuts are the focal props. "
            "CRITICAL: EXACTLY TWO people — Butcher showing lamb + Mrs. Bird preferring beef. "
            "Do NOT show the full shop. No text on any meat or signage."
        ),
    },
    {
        "id": "steak_mince",
        "desc": (
            "COMPOSITION: MEDIUM SHOT at the butcher's counter. "
            "On the counter: a THICK RED STEAK and a PILE OF MINCE (ground beef) "
            "are placed clearly side by side. "
            "THE BUTCHER (white coat, striped apron, greying hair) "
            "stands behind the counter, gesturing at the steak with a recommending smile. "
            "MRS. BIRD (dark green coat, wicker basket) leans forward slightly, "
            "pointing at the nice-looking STEAK with an approving expression — "
            "'This is a nice piece. Give me that piece, please.' "
            "And she raises one finger indicating she also wants mince — 'A pound of mince, too.' "
            "The STEAK and MINCE on the counter are the focal props. "
            "CRITICAL: EXACTLY TWO people — Mrs. Bird choosing steak and mince + Butcher serving. "
            "Do NOT show the full shop. No text on any item."
        ),
    },
    {
        "id": "showing_chicken",
        "desc": (
            "COMPOSITION: MEDIUM SHOT at the butcher's counter. "
            "THE BUTCHER (white coat, striped apron, greying hair) "
            "holds up a WHOLE PLUCKED CHICKEN — clearly a raw whole chicken — "
            "toward Mrs. Bird with an enthusiastic expression — 'Do you want a chicken?' "
            "MRS. BIRD (dark green coat, wicker basket) "
            "holds up one hand in polite refusal, shaking her head — 'No, thank you.' "
            "Her expression is kindly but firm — her husband doesn't like chicken. "
            "The WHOLE CHICKEN held by the Butcher is the focal prop. "
            "Both characters share a knowing, slightly amused expression — "
            "the Butcher looking sheepishly sympathetic as he admits he doesn't like chicken either. "
            "CRITICAL: EXACTLY TWO people — Butcher offering chicken + Mrs. Bird declining. "
            "Do NOT show the full shop."
        ),
    },
]
