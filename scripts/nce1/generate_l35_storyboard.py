#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 35: Our Village
# Story: Narrator describes their English village — in a valley between two hills,
# on a river. A couple walks along the river bank. A boy swims across the river.
# The school building is beside a park (school LEFT, park RIGHT).
# Children come out of school, some go into the park.
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm English countryside light, idyllic peaceful mood. "
)

SCENE = (
    "Location: a picturesque English village — "
    "stone cottages with gardens, a church with a spire, "
    "a calm river running through the village, "
    "rolling green hills on both sides of the valley, "
    "warm soft daylight and lush greenery. "
    "Keep the stone cottages, green hills, and calm river consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_COUPLE = (
    "Characters THE COUPLE: a pleasant middle-aged husband and wife, approximately 40-45 years old. "
    "Husband: short grey-brown hair, wearing a brown jacket and dark green scarf. "
    "Wife: short auburn hair, wearing a cream coat. "
    "CRITICAL: husband brown jacket + green scarf; wife cream coat + auburn hair — NEVER change. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide panoramic aerial-view of the idyllic English village nestled IN A VALLEY. "
            "TWO GENTLE GREEN HILLS rise on the LEFT side and the RIGHT side of the frame, "
            "with the village sitting in the valley BETWEEN them. "
            "The village has stone cottages, a church with a stone spire, and winding lanes. "
            "A calm river flows through the village at the bottom of the valley. "
            "Green fields and trees surround the cottages. Blue sky with soft clouds above. "
            "CRITICAL: the village must be clearly IN A VALLEY with hills on both sides. "
            "This is a wide scenic landscape — no individual people visible."
        ),
    },
    {
        "id": "walking_bank",
        "desc": (
            "A pleasant middle-aged couple walks together along a grassy RIVER BANK. "
            "Husband (short grey-brown hair, brown jacket, dark green scarf) "
            "walks on the LEFT, arm linked with his wife. "
            "Wife (short auburn hair, cream coat) walks beside him, smiling contentedly. "
            "They walk along the LEFT bank of the calm river — "
            "the river and green opposite bank are visible on their right. "
            "Green grass path along the river bank, trees in background, gentle daylight. "
            "CRITICAL: EXACTLY TWO people — husband + wife — walking along the LEFT bank. "
            "The couple on the river bank is the focal point."
        ),
    },
    {
        "id": "boy_swimming",
        "desc": (
            "FOCAL CHARACTER: a young boy, approximately 12-14 years old, "
            "actively SWIMMING across the calm river. "
            "He is shown mid-stroke in the water — arms extended in a front crawl, "
            "head turning to breathe, water splashing around him. "
            "The river fills the frame — green banks on both sides, "
            "showing he is swimming ACROSS the river from one bank toward the other. "
            "The swimming boy in the water is the sole focal point. "
            "CRITICAL: ONLY the boy swimming — no other people in this frame. "
            "The river and both green banks frame the scene."
        ),
    },
    {
        "id": "school_park",
        "desc": (
            "Wide shot showing TWO BUILDINGS side by side. "
            "On the LEFT: a solid 1960s British SCHOOL BUILDING — "
            "red brick with large windows, an entrance door, and a flagpole. "
            "On the RIGHT: a green PUBLIC PARK — "
            "with iron park gates, trees, a lawn, and a path. "
            "The school is clearly on the LEFT; the park is clearly on the RIGHT. "
            "They are BESIDE each other — the school's right side touching/near the park entrance. "
            "Blue sky above, warm daylight. No people in this establishing shot. "
            "CRITICAL: school on LEFT + park on RIGHT — both clearly visible as the main subjects."
        ),
    },
    {
        "id": "children_action",
        "desc": (
            "Dynamic scene outside the school building. "
            "The red brick school building entrance is on the LEFT side of the frame. "
            "Several school children (boys and girls, approximately 8-12 years old, "
            "wearing school uniforms) are STREAMING OUT of the school doorway — "
            "coming through the entrance, moving outward with energy and excitement. "
            "On the RIGHT side of the frame: the park entrance/iron gates are visible. "
            "Some of the children are already heading/running toward the park gates on the right. "
            "CRITICAL: children must be clearly COMING OUT of the school (LEFT) "
            "and GOING INTO the park (RIGHT). "
            "Show the school entrance on the left + park gates on the right + "
            "children moving from school toward park."
        ),
    },
]
