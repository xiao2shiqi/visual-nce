#!/usr/bin/env python3

# =============================================================================
# NCE1 Lesson 11: Is This Your Shirt?
# Story: The teacher finds a white shirt in the classroom. He asks Dave if it's
# his — Dave says no (his shirt is light blue). The teacher calls Tim and
# throws the white shirt across the classroom to him. Tim catches it — it's his!
# Characters: Teacher (Mr.), Dave (schoolboy), Tim (schoolboy)
# =============================================================================

STYLE = (
    "Studio Ghibli-inspired illustration style, delicate watercolor textures, "
    "soft hand-drawn lines, warm 1960s classroom light, charming school atmosphere. "
)

SCENE = (
    "Location: a classic 1960s British school classroom — "
    "rows of wooden desks and chairs with schoolchildren, "
    "a chalkboard at the front, tall windows with daylight, "
    "a teacher's desk at the front with books and chalk. "
    "Keep the classroom layout, wooden desks, chalkboard, and warm daylight consistent across ALL frames. "
    "NO captions, NO speech bubbles, NO subtitles, NO split panels, NO visible written words. "
)

CHAR_TEACHER = (
    "Character THE TEACHER: middle-aged man, approximately 40-45 years old, "
    "short brown hair, kind steady eyes, neat professional appearance, "
    "wearing a brown tweed blazer over a white shirt and a green tie. "
    "CRITICAL: brown tweed blazer + green tie — NEVER change. "
    "He looks like a firm but good-natured British school teacher. "
)

CHAR_DAVE = (
    "Character DAVE: young schoolboy, approximately 12-14 years old, "
    "short dark hair, cheeky but honest expression, "
    "wearing a light blue school shirt. "
    "CRITICAL: light blue school shirt — NEVER change. His shirt is NOT white. "
    "He sits at a desk near the front of the class. "
)

CHAR_TIM = (
    "Character TIM: young schoolboy, approximately 12-14 years old, "
    "blond hair, bright cheerful expression, "
    "wearing a light blue school shirt. "
    "CRITICAL: blond hair + light blue school shirt — NEVER change. "
    "He sits at a desk toward the back of the class. "
)

STORYBOARD = [
    {
        "id": "scene1",
        "desc": (
            "Wide shot of the classroom. The Teacher stands at the front, "
            "holding up a FOLDED WHITE SHIRT and examining its label with a puzzled look. "
            "Dave sits at a desk nearby, watching the Teacher curiously. "
            "Other students are visible at their desks in the background. "
            "The white shirt is clearly visible — it is distinctly white, not blue. "
            "Show Teacher, Dave, and the white shirt clearly."
        ),
    },
    {
        "id": "dave_denies",
        "desc": (
            "The Teacher holds the white shirt toward Dave with a questioning look. "
            "Dave is shaking his head firmly 'no' — he points to his own light blue shirt "
            "to show the Teacher that his shirt is blue, not white. "
            "Dave's expression is honest and slightly amused. "
            "CRITICAL: Dave wears a light blue shirt — the white shirt is NOT Dave's. "
            "Show both Teacher and Dave clearly with the shirts distinguishable."
        ),
    },
    {
        "id": "teacher_thinks",
        "desc": (
            "The Teacher holds the white shirt in one hand and looks thoughtfully "
            "toward the back of the classroom, turning away from Dave. "
            "His expression is concentrated — searching for who the shirt belongs to. "
            "Students visible at their desks in the background. "
            "Tim is dimly visible at the back. Show the Teacher clearly."
        ),
    },
    {
        "id": "calling_tim",
        "desc": (
            "The Teacher cups one hand to his mouth and calls out loudly toward the back "
            "of the classroom — looking directly at Tim who sits at a desk at the back. "
            "Tim looks up from his work with a surprised expression. "
            "The white shirt is still in the Teacher's other hand. "
            "Show Teacher in the foreground and Tim visible in the background. "
            "The classroom stretches between them."
        ),
    },
    {
        "id": "throwing_shirt",
        "desc": (
            "The Teacher has thrown the folded white shirt through the air across the classroom. "
            "The white shirt is shown mid-flight — clearly visible in the air, "
            "floating between the Teacher at the front and Tim at the back. "
            "The Teacher watches with a satisfied expression. "
            "Tim at the back is reaching up, ready to catch. "
            "Show the dramatic mid-air shirt, Teacher, and Tim."
        ),
    },
    {
        "id": "tim_catches",
        "desc": (
            "Tim is catching the white shirt with both hands, grinning broadly. "
            "He holds the white shirt up triumphantly — clearly delighted and slightly surprised. "
            "His blond hair and light blue school shirt are clearly visible underneath. "
            "Classmates nearby look on with amused smiles. "
            "The Teacher watches from the front with a satisfied nod. "
            "Show Tim clearly. Cheerful, comic classroom atmosphere."
        ),
    },
]
