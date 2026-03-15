#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 55: The Sawyer Family
# Story: The Sawyer family's daily routine. Mr. Sawyer takes the children
# to school, goes to work. Mrs. Sawyer stays home, does housework,
# eats lunch at noon, sees friends in afternoon for tea.
# Evening: children arrive home early, Mr. Sawyer arrives late.
# Night: children do homework then bed; Mr. Sawyer reads paper or watches TV.
# Characters: MR. SAWYER (father), MRS. SAWYER (mother), CHILDREN (son + daughter)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s British suburban family life, cheerful domestic mood. "
)

SCENE = (
    "Location: 87 King Street — a typical 1960s British terraced house and neighbourhood — "
    "red brick terrace with a small front garden, a street with similar houses, "
    "a cosy interior with a sitting room, kitchen, and a small dining area. "
    "Keep the red brick terrace exterior, cosy sitting room, and warm domestic atmosphere consistent. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_MR_SAWYER = (
    "Character MR. SAWYER: a pleasant British father, approximately 38-42 years old, "
    "short dark hair with a side parting, kind dependable face, "
    "wearing a dark grey suit with a white shirt and plain tie for work. "
    "CRITICAL: dark hair with side parting + dark grey suit + white shirt + tie — NEVER change. "
)

CHAR_MRS_SAWYER = (
    "Character MRS. SAWYER: a warm British housewife, approximately 35-40 years old, "
    "short wavy brown hair, cheerful capable expression, "
    "wearing a light floral dress and a white apron at home. "
    "CRITICAL: wavy brown hair + light floral dress + white apron — NEVER change. "
)

CHAR_CHILDREN = (
    "Characters THE CHILDREN: a boy approximately 9-10 years old (short brown hair, "
    "wearing school uniform — grey shorts/trousers, white shirt, dark blazer, school cap) "
    "and a girl approximately 8-9 years old (blonde pigtails, "
    "wearing school uniform — grey skirt, white blouse, dark cardigan). "
    "CRITICAL: boy in grey school uniform + girl in grey skirt and cardigan — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the morning outside 87 King Street — a red brick terraced house. "
            "MR. SAWYER (dark hair, dark grey suit, tie) stands at the front door "
            "with TWO CHILDREN beside him — a BOY in school uniform (grey uniform, school cap) "
            "and a GIRL in school uniform (grey skirt, cardigan). "
            "Mr. Sawyer holds the children's hands, about to walk them to school. "
            "MRS. SAWYER (wavy brown hair, floral dress, white apron) "
            "stands in the doorway waving them goodbye with a warm smile. "
            "The red brick terraced house with small front garden and the street are clearly visible. "
            "Morning light, cheerful suburban atmosphere. "
            "CRITICAL: EXACTLY FOUR family members — Mr. Sawyer + 1 boy + 1 girl + Mrs. Sawyer. "
            "Show all four characters clearly. A typical warm British family morning."
        ),
    },
    {
        "id": "housework",
        "desc": (
            "Wide shot of the interior of the 1960s British home. "
            "MRS. SAWYER (wavy brown hair, light floral dress, white apron) "
            "is clearly doing HOUSEWORK — she might be vacuuming the sitting room carpet "
            "with an upright vacuum cleaner, or dusting shelves, or sweeping. "
            "The cosy sitting room shows a fireplace, armchairs, a sideboard — "
            "a warm 1960s British home interior. "
            "Mrs. Sawyer works diligently with a cheerful expression. "
            "CRITICAL: ONLY MRS. SAWYER in this frame — no other family members. "
            "Show Mrs. Sawyer doing housework in the cosy 1960s British home."
        ),
    },
    {
        "id": "lunch_noon",
        "desc": (
            "COMPOSITION: MEDIUM SHOT of the kitchen/dining area. "
            "MRS. SAWYER (wavy brown hair, floral dress, white apron) "
            "sits alone at the small kitchen table eating her LUNCH — "
            "a simple plate of food (sandwich, soup, or salad) in front of her. "
            "The kitchen clock on the wall shows NOON (12 o'clock). "
            "The house is quiet and empty — just Mrs. Sawyer having her solitary lunch. "
            "Warm kitchen light, a cup of tea beside the plate. "
            "CRITICAL: ONLY MRS. SAWYER in this frame — she eats alone at noon. "
            "The clock showing noon is important. No text on the clock face — just hands at 12."
        ),
    },
    {
        "id": "housework_friends",
        "desc": (
            "Wide shot of the cosy sitting room in the afternoon. "
            "MRS. SAWYER (wavy brown hair, floral dress, apron removed) "
            "sits with TWO FEMALE FRIENDS (friendly British women, 35-45 years old) "
            "around the sitting room coffee table. "
            "On the table: a teapot, cups and saucers, a plate of biscuits. "
            "All three women are chatting and drinking tea, laughing warmly. "
            "Soft afternoon sunlight through the net curtains. "
            "CRITICAL: THREE women — Mrs. Sawyer + two friends — all drinking tea and chatting. "
            "The afternoon tea gathering is the focal activity. Warm friendly atmosphere."
        ),
    },
    {
        "id": "evening_tv",
        "desc": (
            "Wide shot of the cosy sitting room in the evening. "
            "On the LEFT of the scene: two CHILDREN (boy in school uniform + girl) "
            "sit at a small table doing their HOMEWORK — books and pencils open. "
            "Their heads are bent over their work with concentration. "
            "On the RIGHT of the scene: MR. SAWYER (dark grey suit, tie loosened) "
            "sits in an armchair reading a NEWSPAPER. "
            "MRS. SAWYER (floral dress) sits beside him, and they are both looking "
            "toward a TELEVISION SET showing a glowing screen. "
            "The sitting room with a warm fireplace, the television, and the family together. "
            "CRITICAL: EXACTLY FOUR family members — 2 children doing homework + parents watching TV. "
            "Show the warm cosy evening family scene. Firelight and lamplight."
        ),
    },
]
