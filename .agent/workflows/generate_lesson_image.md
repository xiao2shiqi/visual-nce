---
description: Generate Ghibli-style illustrations for lessons
---

## Generate Ghibli-Style Lesson Image

When generating or supplementing images for lessons:

1. **Identify Lessons Needing Images**:
   - Check `src/data/curriculum.json` for lessons with `image: "/images/coming-soon.jpg"`
   - These are lessons that still need Ghibli-style illustrations

2. **Analyze Lesson Content**:
   - Read the target lesson JSON file (e.g., `src/data/lessons/nce1-l139.json`)
   - Identify the main characters and their genders (Male/Female) from the dialogue/roles
   - Extract the core scene or theme based on the story

3. **Generate Image**:
   - **Tool**: Use `generate_image`
   - **Style**: "Ghibli Studio style, anime/manga, vibrant, painterly, detailed background"
   - **Content**: Describe characters (with gender) and the scene clearly
   - **Reference**: Follow the warm, story-book feel of existing illustrations

4. **Save and Optimize**:
   - Save to `public/images/nce{Book}/l{LessonID}/scene1.jpg` (main image)
   - Create compressed `thumbnail.jpg` for homepage display
   - Use image compression tools if available (e.g., imagemagick, ffmpeg)

5. **Update Configuration**:
   - Update `src/data/curriculum.json` with the new thumbnail path
   - Update the lesson JSON file's `image` field with the scene path