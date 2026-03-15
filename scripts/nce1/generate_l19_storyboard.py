#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 19: Tired and Thirsty
# Story: Mother is walking with Andy and Lucy in the park. The children are
# tired and thirsty. Mother finds a bench for them to sit. The children are
# still not all right. Mother spots an ice cream man, buys two ice creams.
# The children are happy and thankful.
# Characters: Mother, Andy (young boy), Lucy (young girl)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm sunny afternoon park light, cheerful family mood. "
)

SCENE = (
    "Location: a pleasant English park on a sunny afternoon — "
    "a wide paved path lined with large leafy green trees, "
    "wooden park benches, flower beds, green grass, "
    "warm golden sunlight filtering through the tree canopy. "
    "Keep the park path, green trees, benches, and warm sunlight consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_MOTHER = (
    "Character MOTHER: kind woman, approximately 32-35 years old, "
    "light brown shoulder-length hair worn loose, warm caring expression, "
    "wearing a simple pale yellow summer dress and carrying a small floral handbag. "
    "CRITICAL: pale yellow dress + light brown hair + floral handbag — NEVER change. "
    "She looks like a warm, attentive young mother. NOT elderly. "
)

CHAR_ANDY = (
    "Character ANDY: young boy, approximately 8-9 years old, "
    "short messy dark hair, lively face, "
    "wearing a blue-and-white striped t-shirt and dark blue shorts. "
    "CRITICAL: striped blue-white t-shirt + dark blue shorts + messy dark hair — NEVER change. "
    "He looks like a cheerful, energetic young boy. "
)

CHAR_LUCY = (
    "Character LUCY: young girl, approximately 6-7 years old, "
    "blonde hair in two pigtails tied with small pink ribbons, sweet expression, "
    "wearing a light pink sundress with white trim. "
    "CRITICAL: blonde pigtails + pink sundress — NEVER change. "
    "She looks like an adorable, sweet little girl. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the sunny park path. "
            "Mother walks ahead, looking back with concern at the two children. "
            "Andy (striped t-shirt, shorts) trudges along looking exhausted — "
            "feet dragging, shoulders drooping, wiping his forehead. "
            "Lucy (pink sundress, blonde pigtails) walks beside him looking equally drained, "
            "fanning her face with one hand. "
            "Both children look genuinely tired and thirsty. "
            "Warm park setting with trees and path. Show all three characters clearly."
        ),
    },
    {
        "id": "bench",
        "desc": (
            "Mother points toward a wooden park bench under a large shady tree nearby. "
            "Her expression is kind and encouraging. "
            "Andy and Lucy both look at the bench — their faces lighting up with relief. "
            "Lucy reaches toward the bench eagerly; Andy looks grateful. "
            "The shady bench is clearly visible in the background. "
            "Show all three characters clearly. Warm afternoon park light."
        ),
    },
    {
        "id": "sitting",
        "desc": (
            "Andy and Lucy sit together on the wooden park bench under the tree shade. "
            "They are slumped slightly — still looking hot and thirsty despite sitting. "
            "Andy's head droops a little; Lucy fans herself weakly. "
            "Mother stands in front of them, leaning forward with a worried, caring expression. "
            "Dappled light through the tree above. Show all three characters clearly."
        ),
    },
    {
        "id": "ice_cream_man",
        "desc": (
            "CRITICAL CHARACTER COUNT: this scene contains EXACTLY THREE people — "
            "ONE adult woman (Mother) + ONE boy (Andy) + ONE girl (Lucy). "
            "Do NOT duplicate Andy or Lucy. Do NOT add any extra children. "
            "Mother suddenly spots something and points with excitement. "
            "In the background along the park path, a cheerful ice cream vendor stands "
            "beside a brightly painted ice cream cart with a colourful umbrella. "
            "Andy (striped blue-white t-shirt, dark blue shorts) stands to Mother's left "
            "with wide eyes and an amazed expression, completely forgetting his tiredness. "
            "Lucy (pink sundress, blonde pigtails) stands to Mother's right, "
            "grabbing Mother's sleeve with both hands, equally excited. "
            "Mother (pale yellow dress) stands between them, pointing at the cart, smiling with delight. "
            "Show all three characters and the ice cream cart clearly. CONFIRM: 1 boy + 1 girl only."
        ),
    },
    {
        "id": "buying",
        "desc": (
            "Mother stands at the ice cream cart, handing coins to the cheerful vendor. "
            "The vendor hands her two large ice cream cones — one strawberry pink, one chocolate brown. "
            "Andy and Lucy stand on either side of Mother, stretching up on tiptoes, "
            "eyes huge with anticipation. "
            "The colourful cart with its umbrella is clearly visible. "
            "Show Mother, the vendor, both children, and the ice cream cones clearly."
        ),
    },
    {
        "id": "eating",
        "desc": (
            "Andy and Lucy sit happily back on the park bench, each holding and licking "
            "a large ice cream cone with huge smiles — completely transformed from tired to joyful. "
            "Andy holds the chocolate ice cream; Lucy holds the strawberry one. "
            "Mother sits between them on the bench, beaming with satisfaction. "
            "Warm golden afternoon park light. Show all three characters clearly. "
            "The children look completely refreshed and happy."
        ),
    },
]
