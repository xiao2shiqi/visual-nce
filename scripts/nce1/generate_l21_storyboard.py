#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 21: Which Book?
# Story: A man asks Jane (library assistant) for a book. Jane asks which one.
# She points to one book on the shelf — Man says no, the red one.
# Jane finds the red book and hands it to him. He thanks her.
# Characters: Man (customer), Jane (library assistant)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm cosy library light, nostalgic bookshop atmosphere. "
)

SCENE = (
    "Location: a warm classic British library or bookshop — "
    "tall wooden bookshelves packed with colourful books of different sizes, "
    "a polished wooden counter desk, warm amber overhead lighting, "
    "a small window letting in soft daylight. "
    "Keep the wooden bookshelves, warm amber lighting, and wooden counter consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words on books. "
)

CHAR_MAN = (
    "Character MAN: a polite professional man, approximately 38-42 years old, "
    "short neat dark brown hair, clean-shaven, friendly composed expression, "
    "wearing a smart charcoal grey suit jacket over a white shirt with a dark navy tie. "
    "CRITICAL: charcoal grey suit + white shirt + dark navy tie + dark brown hair — NEVER change. "
    "He looks like a well-dressed, educated gentleman browsing a library. "
)

CHAR_JANE = (
    "Character JANE: a cheerful young library assistant, approximately 24-26 years old, "
    "auburn hair pinned up neatly with a few loose strands, warm helpful expression, "
    "wearing a neat cream-coloured blouse with a dark green cardigan. "
    "CRITICAL: cream blouse + dark green cardigan + auburn pinned-up hair — NEVER change. "
    "She looks like a kind, efficient young librarian. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide establishing shot of the warm library interior. "
            "The Man (charcoal grey suit, white shirt, dark navy tie, dark brown hair) "
            "stands at the wooden counter, looking across at Jane with a polite, expectant expression. "
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "stands behind or beside the counter, smiling helpfully. "
            "Tall bookshelves packed with colourful books fill the background behind them. "
            "Warm amber library light. Show both characters clearly. Cosy, welcoming atmosphere."
        ),
    },
    {
        "id": "pointing_shelf",
        "desc": (
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "stands in front of a large wooden bookshelf packed with books of many colours. "
            "She extends one arm upward, pointing toward a section of the shelf with a questioning expression — "
            "tilting her head slightly as if asking 'this one?'. "
            "The bookshelf fills the background with many different coloured books — blue, green, yellow, etc. "
            "The Man (charcoal grey suit) stands a step behind her, watching with a slight frown of uncertainty. "
            "Show both characters clearly. Warm library lighting."
        ),
    },
    {
        "id": "which_book",
        "desc": (
            "Focus on the bookshelf: a clearly visible THICK RED BOOK stands out on the shelf "
            "among other blue, green and yellow books. "
            "The Man (charcoal grey suit, white shirt, dark navy tie) stands close to the shelf, "
            "pointing at the red book with one finger — his face showing certainty and a slight smile. "
            "Jane (cream blouse, dark green cardigan) stands beside him, reaching toward the red book, "
            "her face showing understanding — 'Oh, THAT one!'. "
            "The red book is clearly the visual focal point — make it prominently visible on the shelf. "
            "Show both characters and the red book clearly. Warm library lighting."
        ),
    },
    {
        "id": "handing_book",
        "desc": (
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "holds out a thick red book toward the Man with both hands and a warm smile. "
            "The Man (charcoal grey suit, white shirt, dark navy tie) extends his hands to receive it, "
            "looking pleased and grateful. "
            "The red book is clearly visible being passed between them — the focal action of the scene. "
            "Warm amber library light. Show both characters and the red book clearly."
        ),
    },
    {
        "id": "thanking",
        "desc": (
            "The Man (charcoal grey suit, white shirt, dark navy tie, dark brown hair) "
            "holds the thick red book under one arm contentedly, "
            "turning back toward Jane with a warm, appreciative smile and a slight nod of thanks. "
            "Jane (cream blouse, dark green cardigan, auburn pinned-up hair) "
            "smiles back warmly from behind the counter — a pleasant, satisfied expression. "
            "Warm amber library light. Show both characters clearly. "
            "The red book is visible under the Man's arm. Friendly, warm ending atmosphere."
        ),
    },
]
