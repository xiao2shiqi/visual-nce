#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 23: Which Glasses?
# Story: A man asks Jane (shop assistant) for some glasses (drinking glasses).
# Jane asks which ones. She points to some — Man says no, the ones on the shelf.
# Jane fetches the right glasses and hands them over. Man thanks her.
# Characters: Man (customer), Jane (shop assistant)
# Note: "glasses" here = drinking glasses / tumblers (杯子), NOT eyeglasses.
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cosy shop interior light, nostalgic 1960s British atmosphere. "
)

SCENE = (
    "Location: a warm, cosy British kitchenware or glassware shop — "
    "wooden shelves and display counters lined with rows of drinking glasses, "
    "tumblers, and cups of different sizes and colours, "
    "warm amber overhead lighting, polished wooden counter. "
    "Keep the wooden shelves, glassware displays, and warm amber lighting consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_MAN = (
    "Character MAN: a polite professional man, approximately 38-42 years old, "
    "short neat dark brown hair, clean-shaven, friendly composed expression, "
    "wearing a smart charcoal grey suit jacket over a white shirt with a dark navy tie. "
    "CRITICAL: charcoal grey suit + white shirt + dark navy tie + dark brown hair — NEVER change. "
    "He looks like a well-dressed, educated gentleman shopping for glassware. "
)

CHAR_JANE = (
    "Character JANE: a cheerful young shop assistant, approximately 24-26 years old, "
    "auburn hair pinned up neatly with a few loose strands, warm helpful expression, "
    "wearing a neat cream-coloured blouse with a dark green cardigan. "
    "CRITICAL: cream blouse + dark green cardigan + auburn pinned-up hair — NEVER change. "
    "She looks like a kind, efficient young shop assistant. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the warm glassware shop interior. "
            "The Man (charcoal grey suit, white shirt, dark navy tie, dark brown hair) "
            "stands at the wooden counter, gesturing toward the shelves behind Jane with a polite expression. "
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "stands behind the counter, smiling helpfully. "
            "Shelves lined with rows of drinking glasses — tumblers, tall glasses, short glasses — fill the background. "
            "Warm amber shop light. Show both characters clearly. Cosy, inviting atmosphere."
        ),
    },
    {
        "id": "pointing_shelf",
        "desc": (
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "stands in front of wooden display shelves packed with drinking glasses and tumblers. "
            "She gestures toward one group of glasses on the shelf with a questioning expression — "
            "tilting her head as if to say 'these ones here?'. "
            "The shelves clearly show multiple sets of glasses — clear glass tumblers, coloured glasses, etc. "
            "The Man (charcoal grey suit) stands slightly behind her, watching with a mildly uncertain expression. "
            "Show both characters and the glass-filled shelves clearly. Warm shop lighting."
        ),
    },
    {
        "id": "which_glasses",
        "desc": (
            "Focus on a wooden shelf: a clearly visible set of TALL CLEAR DRINKING GLASSES "
            "stands prominently on an upper shelf — these are the ones the Man wants. "
            "The Man (charcoal grey suit, white shirt, dark navy tie) stands close to the shelf, "
            "pointing directly at the tall clear glasses with one finger — his expression showing certainty. "
            "Jane (cream blouse, dark green cardigan) stands beside him, reaching toward those glasses, "
            "her face showing recognition — 'Oh, THOSE ones on the shelf!'. "
            "The tall clear glasses on the shelf are the visual focal point. "
            "Show both characters and the glasses clearly. Warm amber shop lighting."
        ),
    },
    {
        "id": "handing_glasses",
        "desc": (
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "carefully holds out a set of tall clear drinking glasses toward the Man with both hands and a warm smile. "
            "The Man (charcoal grey suit, white shirt, dark navy tie) extends his hands to receive them, "
            "looking pleased and satisfied. "
            "The tall clear drinking glasses are clearly visible being passed between them — the focal action. "
            "Warm amber shop light. Show both characters and the glasses clearly."
        ),
    },
    {
        "id": "thanking",
        "desc": (
            "The Man (charcoal grey suit, white shirt, dark navy tie, dark brown hair) "
            "holds the tall clear drinking glasses contentedly, "
            "turning back toward Jane with a warm, appreciative smile and a slight nod of thanks. "
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "smiles back warmly from behind the counter — a pleasant, satisfied expression. "
            "Warm amber shop light. Show both characters clearly. "
            "The glasses are visible in the Man's hands. Friendly, warm ending atmosphere."
        ),
    },
]
