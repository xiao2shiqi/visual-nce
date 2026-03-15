#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 51: A Pleasant Climate
# Story: Two travelers discuss Greece's climate across the four seasons.
# Traveler asks Dimitri about spring (windy in March, warm in April/May),
# summer (hot, sun every day), autumn (warm in Sep/Oct, cold in Nov),
# winter (often cold, sometimes snows).
# Characters: TRAVELER (English man), DIMITRI (Greek man)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm European travel atmosphere, friendly conversational mood. "
)

SCENE = (
    "Location: a European café or train station, "
    "or a sunny outdoor setting — "
    "a small table with two chairs, perhaps with Greek architecture or Mediterranean scenery in the background, "
    "warm comfortable setting for conversation. "
    "Keep the conversational setting consistent across the first frame; "
    "subsequent frames show the Greek landscape in different seasons. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_TRAVELER = (
    "Character THE TRAVELER: a curious British man, approximately 35-40 years old, "
    "short light brown hair, inquisitive and friendly expression, "
    "wearing a light beige jacket over a white shirt, "
    "with a small travel bag. "
    "CRITICAL: light brown hair + beige jacket + white shirt — NEVER change. "
)

CHAR_DIMITRI = (
    "Character DIMITRI: a warm Greek man, approximately 35-40 years old, "
    "dark curly hair, olive skin, warm expressive face, "
    "wearing a white short-sleeved shirt and dark trousers. "
    "CRITICAL: dark curly hair + olive skin + white short-sleeved shirt + dark trousers — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of a sunny outdoor café with Mediterranean atmosphere. "
            "THE TRAVELER (light brown hair, beige jacket, white shirt) "
            "sits at a small café table, leaning forward with a curious, friendly expression — "
            "'Where do you come from? What's the climate like?' "
            "DIMITRI (dark curly hair, olive skin, white short-sleeved shirt) "
            "sits across from the Traveler, spreading his hands warmly — "
            "'I come from Greece. It's very pleasant!' "
            "Behind them: a blue sky, whitewashed walls, hints of Mediterranean scenery. "
            "The small café table with two cups of coffee between them. "
            "CRITICAL: EXACTLY TWO men — the Traveler asking + Dimitri explaining warmly. "
            "Show both characters clearly. Sunny Mediterranean café atmosphere."
        ),
    },
    {
        "id": "spring_windy",
        "desc": (
            "Wide landscape of the Greek countryside in SPRING. "
            "The scene shows a WINDY March day — trees and grass bending in the breeze, "
            "scattered white clouds racing across a blue sky, "
            "wildflowers beginning to bloom on green hillsides. "
            "In the foreground: a small Greek village with whitewashed houses. "
            "The wind is the dominant atmosphere — leaves blowing, flags fluttering. "
            "It feels alive and fresh — a breezy, pleasant spring in Greece. "
            "CRITICAL: NO people in this frame — this is a scenic landscape illustration of Greek spring. "
            "Show windswept trees, blue sky with rushing clouds, green hills, Greek village."
        ),
    },
    {
        "id": "summer_hot",
        "desc": (
            "Wide landscape of Greece in SUMMER. "
            "The scene shows a blazing HOT summer day — "
            "a brilliant deep blue Mediterranean sea, white sandy beach, "
            "a clear cloudless blue sky with a large bright sun overhead, "
            "golden sunlight pouring down on whitewashed houses on hillsides. "
            "The atmosphere is gloriously hot and radiant — "
            "the sun dominates the sky, the colours are rich and saturated. "
            "Olive trees and bougainvillea in bloom. "
            "CRITICAL: NO people in this frame — this is a scenic landscape of Greek summer heat. "
            "Show blazing sun, deep blue sea, golden light, Mediterranean scenery."
        ),
    },
    {
        "id": "autumn_warm",
        "desc": (
            "Wide landscape of Greece in AUTUMN. "
            "The scene shows a warm AUTUMN day — "
            "golden and amber-leafed trees on gentle hillsides, "
            "a warm soft haze in the October sunlight, "
            "ripening grapes and olive harvests visible in vineyards, "
            "the sky a soft warm blue with high thin clouds. "
            "The atmosphere is mellow, warm, and golden — "
            "the colours are amber, gold, and russet. "
            "Some dark grey clouds on the horizon hint at November rain to come. "
            "CRITICAL: NO people in this frame — this is a scenic landscape of Greek autumn warmth. "
            "Show golden trees, warm amber light, vineyards, soft autumn sky."
        ),
    },
    {
        "id": "winter_snow",
        "desc": (
            "Wide landscape of Greece in WINTER. "
            "The scene shows a cold WINTER day — "
            "whitewashed Greek village houses dusted lightly with SNOW, "
            "bare trees with snow on branches, "
            "grey winter clouds in the sky, soft snowflakes falling gently, "
            "a cold bluish-grey light over the landscape. "
            "The snowfall is light but clear — this is not a blizzard, "
            "just occasional gentle snow as Greece does sometimes get in winter. "
            "The familiar whitewashed walls now have a light dusting of white snow. "
            "CRITICAL: NO people in this frame — this is a scenic landscape of Greece in winter snow. "
            "Show snow-dusted whitewashed houses, bare trees, gentle snowfall, grey winter sky."
        ),
    },
]
