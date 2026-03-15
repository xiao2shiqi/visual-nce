#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 59: Is That All?
# Story: A lady shops at a stationer's. She buys large envelopes,
# writing paper (only large pads available), and a bottle of glue.
# She asks for a large box of chalk but only small boxes are available.
# She declines the small chalk. The shopkeeper asks "Is that all?"
# Then asks "What else do you want?" — she wants her CHANGE!
# Characters: THE LADY (customer), THE SHOPKEEPER (male)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British stationer's shop light, cheerful retail mood. "
)

SCENE = (
    "Location: a traditional 1960s British stationer's shop — "
    "a wooden counter with shelves behind displaying envelopes, writing pads, "
    "boxes of chalk, pens and pencils, bottles of glue, and stationery items, "
    "warm shop lighting, a cash register on the counter. "
    "Keep the wooden counter, shelves of stationery, and warm shop light consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_SHOPKEEPER = (
    "Character THE SHOPKEEPER: a helpful British shop assistant, approximately 45-50 years old, "
    "short thinning grey hair, round cheerful face, "
    "wearing a white shirt with a brown waistcoat and reading glasses on the end of his nose. "
    "CRITICAL: thinning grey hair + white shirt + brown waistcoat + reading glasses — NEVER change. "
    "He stands behind the wooden counter. "
)

CHAR_LADY = (
    "Character THE LADY: a pleasant British woman customer, approximately 40-45 years old, "
    "short neat dark hair, decisive and polite expression, "
    "wearing a burgundy/dark red coat and carrying a handbag. "
    "CRITICAL: short dark hair + burgundy dark red coat + handbag — NEVER change. "
    "She stands on the customer side of the counter. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the traditional 1960s British stationer's shop interior. "
            "THE SHOPKEEPER (thinning grey hair, white shirt, brown waistcoat, reading glasses) "
            "stands behind the wooden counter, looking attentively at the lady — "
            "holding up or reaching for ENVELOPES. "
            "Two sizes of envelope are visible on the counter — SMALL and LARGE. "
            "THE LADY (short dark hair, burgundy coat, handbag) "
            "stands at the customer side of the counter, pointing to the LARGE envelopes. "
            "The shelves behind the shopkeeper show stationery — pads, envelopes, pens. "
            "No text visible on any items or shelves. "
            "CRITICAL: EXACTLY TWO people — Shopkeeper + Lady at the counter. "
            "Show both characters clearly. Traditional 1960s stationer's shop atmosphere."
        ),
    },
    {
        "id": "writing_paper",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the counter with writing pads. "
            "THE SHOPKEEPER (thinning grey hair, brown waistcoat) "
            "places a LARGE WRITING PAD on the counter, gesturing apologetically — "
            "he only has large ones, not small. "
            "On the counter: ONE LARGE WRITING PAD clearly visible. "
            "THE LADY (dark hair, burgundy coat) nods and accepts the large pad. "
            "The LARGE WRITING PAD on the counter is the focal prop. "
            "CRITICAL: EXACTLY TWO people — Shopkeeper offering large writing pad + Lady accepting. "
            "The large writing pad on the counter is the key visual. "
            "Do NOT show the full shop. No text on the writing pad cover."
        ),
    },
    {
        "id": "buying_glue",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the counter. "
            "THE SHOPKEEPER (thinning grey hair, brown waistcoat) "
            "places a SMALL GLASS BOTTLE OF GLUE on the counter. "
            "The bottle is a classic 1960s glue bottle with a rubber cap — plain, no label text. "
            "THE LADY (dark hair, burgundy coat) "
            "points first at the glue bottle (accepting it), "
            "then holds up a finger asking for MORE — she also wants chalk. "
            "On the counter: the large envelopes already purchased, the writing pad, and now the glue bottle. "
            "The GLUE BOTTLE is the focal new prop. "
            "CRITICAL: EXACTLY TWO people — Shopkeeper placing glue + Lady requesting chalk too. "
            "Do NOT show the full shop. No text on any item."
        ),
    },
    {
        "id": "no_chalk",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the counter with chalk boxes. "
            "THE SHOPKEEPER (thinning grey hair, brown waistcoat) "
            "holds up a SMALL BOX OF CHALK in one hand and shakes his head apologetically — "
            "he only has small boxes, not large ones. "
            "THE LADY (dark hair, burgundy coat) "
            "holds up one hand declining — 'No, thank you.' "
            "She looks politely firm in her refusal of the small chalk box. "
            "TWO CHALK BOXES are visible: one SMALL (being held up) and one SMALL beside it — "
            "no large box available. "
            "The SMALL CHALK BOX is the focal prop. "
            "CRITICAL: EXACTLY TWO people — Shopkeeper showing small chalk box + Lady declining. "
            "Do NOT show the full shop. No text on any boxes."
        ),
    },
    {
        "id": "forgetting_change",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the counter. "
            "THE LADY (dark hair, burgundy coat) has turned to leave, "
            "pausing with one foot turned back, looking back at the Shopkeeper "
            "with a firm, slightly amused expression — 'I want my change!' "
            "THE SHOPKEEPER (thinning grey hair, brown waistcoat) "
            "stands behind the counter looking sheepish and flustered, "
            "reaching into the cash register or fumbling with coins. "
            "On the counter: her purchases — large envelopes, writing pad, and glue bottle. "
            "The CASH REGISTER and the SHOPKEEPER'S sheepish face are the focal elements. "
            "CRITICAL: EXACTLY TWO people — Lady demanding her change + Shopkeeper looking sheepish. "
            "The moment of the Lady asking for change is the comic focal point. "
            "Do NOT show the full shop. No text on any item."
        ),
    },
]
