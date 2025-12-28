---
description: Generate a Ghibli-style illustration for a lesson and update the home page.
---

1. **Analyze Lesson Content**:
   - Read the target lesson JSON file (e.g., `src/data/lessons/nce1-l137.json`).
   - Identify the main characters and their genders (Male/Female) from the dialogue/roles.
   - Extract the core scene or theme (e.g., "A Pleasant Dream", lottery, travel).

2. **Generate Image**:
   - **Tool**: Use `generate_image`.
   - **Prompt Style**: "Ghibli Studio style, manga/anime, vibrant, detailed, painterly background".
   - **Content**: Clearly describe characters (Male/Female) and the scene based on analysis.
   - **Technical**: Request high quality but intended for web usage (user prompt: "use compressed picture").
   - **Reference**: Follow the style of existing Book 1/2 illustrations (warm, story-book feel).

3. **Save and Optimize**:
   - Save the image to `public/images/nce{Book}/l{LessonID}/thumbnail.png` (or `.jpg`).
   - If utilizing `run_command` is possible for compression (e.g., `ffmpeg` or `imagemagick`), apply compression to minimize file size while maintaining quality. If not, rely on generation output or default optimization.

4. **Update Configuration**:
   - Edit `src/data/curriculum.json`.
   - Locate the lesson entry.
   - Update the `image` field to point to the new asset (e.g., `/images/nce1/l137/thumbnail.png`).

5. **Verify Display**:
   - Ensure the image appears correctly on the Home Page (`HomeView.vue`).
