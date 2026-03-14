# Project Rules

## Image Style Rule (Mandatory)

- All course images in this project must use a Studio Ghibli-inspired illustration style.
- This rule applies to every lesson image and thumbnail across all books (NCE1, NCE2, NCE3, NCE4).
- Do not use photorealistic, 3D-rendered, or non-Ghibli visual styles for course images.

## Image Generation Protocol (Visual Storyboard Standard)

- **Official Tool**: All images must be generated using `scripts/generate_images.py`.
- **Primary Model**: `gemini-3.1-flash-image-preview` (Nano Banana 2).
- **Storyboard Rule**: 
    1. **Master Specs**: Every lesson MUST define a set of consistency anchors (Character descriptions and Scene location) that are included in every prompt within that lesson.
    2. **Default Background**: Each lesson MUST provide a primary image (e.g., `scene1.png`) representing the main interaction. This path MUST be used in both `src/data/curriculum.json` and the root `image` field of the lesson's JSON data to ensure seamless transition from Home to Lesson view.
    3. **Stable Intro**: Segments corresponding to titles, instructions, or narrator questions (non-dialogue) SHOULD NOT have their own `image` field, ensuring the default background is displayed consistently during the introduction.
    4. **Dialogue Switching**: Only dialogue segments or key action changes SHOULD have a private `image` field to trigger a storyboard change.
- **Visual Consistency**: High emphasis on maintaining same clothing (e.g., "white long-sleeved blouse") and objects (e.g., "specific floral handbag") across frames.
- **Visual Style**: Strictly Studio Ghibli illustration style with watercolor textures.
- **Output Naming**: Use descriptive names like `man_waves.png`, `woman_turns.png` for storyboard frames.
- **Instant Switch**: Images must switch immediately without transition effects (Fade/Slide) to maintain a snappy, storyboard feel.
