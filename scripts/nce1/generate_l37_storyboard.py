#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 37: Making a Bookcase
# Story: George is working hard making a bookcase. Dan asks what he's doing.
# George asks for the big hammer; Dan hands it over.
# George plans to paint it PINK — it's for his daughter Susan.
# Characters: George (DIY man), Dan (his friend/neighbour)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British home workshop light, cheerful domestic mood. "
)

SCENE = (
    "Location: a British home garden or garage workshop — "
    "a wooden workbench with tools and wood planks, sawdust on the floor, "
    "shelves with tins of paint, a garden fence or garage wall in background, "
    "warm afternoon light. "
    "Keep the workbench, wood planks, garden fence, and warm light consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_GEORGE = (
    "Character GEORGE: a capable friendly British man, approximately 35-40 years old, "
    "short brown hair, cheerful focused expression, "
    "wearing a blue checked flannel shirt with rolled-up sleeves and grey work trousers, "
    "and a brown leather apron. "
    "CRITICAL: blue checked shirt + rolled sleeves + brown apron + short brown hair — NEVER change. "
    "He looks like an enthusiastic DIY hobbyist. "
)

CHAR_DAN = (
    "Character DAN: a friendly British neighbour, approximately 35-40 years old, "
    "short dark hair, relaxed curious expression, "
    "wearing a light grey jumper/sweater and dark trousers. "
    "CRITICAL: light grey jumper + dark trousers + short dark hair — NEVER change. "
    "He looks like a friendly, curious onlooker. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the garden workshop. "
            "George (blue checked shirt, rolled sleeves, brown apron) is working hard "
            "at the workbench — sawing or hammering wood planks with energy and concentration. "
            "Sawdust flies, wood planks and tools are spread around the workbench. "
            "Dan (light grey jumper, dark trousers) has just walked up, "
            "watching George with an impressed, curious expression. "
            "CRITICAL: EXACTLY TWO men — George working hard + Dan watching. "
            "Show both characters clearly. Warm workshop atmosphere."
        ),
    },
    {
        "id": "pointing_wood",
        "desc": (
            "Dan (light grey jumper) gestures questioningly at the wood planks and construction "
            "with a curious expression — 'What are you making?' "
            "George (blue checked shirt, brown apron) stands proudly beside a HALF-BUILT BOOKCASE "
            "— several wooden shelves partially assembled, visible as a bookcase taking shape. "
            "George points at the bookcase with a satisfied grin. "
            "The half-constructed wooden bookcase is the visual focal point. "
            "CRITICAL: EXACTLY TWO men — Dan asking + George showing bookcase. "
            "The partially-built bookcase must be clearly visible."
        ),
    },
    {
        "id": "hammer",
        "desc": (
            "COMPOSITION: MEDIUM SHOT focused on the hammer handover. "
            "On the workbench: TWO HAMMERS clearly visible — "
            "one SMALL hammer and one LARGE hammer side by side. "
            "Dan (light grey jumper) holds up the LARGE hammer toward George, "
            "offering it with a helpful expression. "
            "George (blue checked shirt, brown apron) reaches out to take the BIG hammer, "
            "nodding with approval. "
            "The two hammers — small and large — must both be clearly visible "
            "so the contrast is obvious. "
            "CRITICAL: EXACTLY TWO men + TWO hammers (one small, one big). "
            "George taking the BIG hammer from Dan is the focal action."
        ),
    },
    {
        "id": "painting_start",
        "desc": (
            "Dan (light grey jumper) stands back with arms folded, "
            "asking George what he plans to do next — looking at the completed bookcase. "
            "George (blue checked shirt, brown apron) stands beside the now-COMPLETED BOOKCASE "
            "holding a paintbrush in one hand and a tin of paint in the other, "
            "announcing his plan to paint it with a confident smile. "
            "The completed unpainted wooden bookcase stands clearly visible beside George. "
            "CRITICAL: EXACTLY TWO men — Dan asking + George ready to paint. "
            "The completed bookcase + paintbrush are the focal elements."
        ),
    },
    {
        "id": "painting_pink",
        "desc": (
            "George (blue checked shirt, brown apron) is actively PAINTING THE BOOKCASE PINK — "
            "applying bright PINK paint to the wooden shelves with a large paintbrush, "
            "the bookcase clearly turning PINK before our eyes. "
            "Pink paint drips and splatters are visible. "
            "Dan (light grey jumper) stands to one side with a comically surprised/amused expression, "
            "eyebrows raised — reacting to the bright pink colour with disbelief. "
            "The PINK bookcase being painted is the dominant visual element. "
            "CRITICAL: the bookcase colour must be clearly and vividly PINK. "
            "EXACTLY TWO men — George painting pink + Dan reacting with surprise."
        ),
    },
]
