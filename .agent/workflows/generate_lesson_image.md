---
description: Generate Ghibli-style illustrations and add speaker names to lesson dialogues
---

## Project Features Workflow

This workflow documents two core visual features of the Visual NCE project:
1. **Ghibli-Style Illustrations** - Each lesson has a unique, Ghibli-style cover image
2. **Speaker Name Tags** - Dialogue lines show the specific speaker's name with color-coded badges

---

## Part 1: Generate Ghibli-Style Lesson Image

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

---

## Part 2: Add Speaker Names to Dialogue

When preparing lesson data, add specific speaker names to each dialogue line:

1. **Analyze Dialogue Participants**:
   - Read the lesson JSON file
   - Identify all speaking characters from the story context
   - Map each segment's `role` (Man/Woman/Narrator) to the actual character name

2. **Add Speaker Field**:
   - For each dialogue segment, add a `speaker` field with the character's name
   - Example:
     ```json
     {
       "id": "s1",
       "role": "Man",
       "speaker": "Graham",  // Add this field
       "text": "Is that you, John?",
       ...
     }
     ```

3. **Speaker Mapping Rules**:
   - Analyze the story to identify who is speaking each line
   - Use first names only for cleaner display (e.g., "Graham" not "Graham Turner")
   - Skip adding speaker for `Narrator` role unless it represents a specific character

4. **Color Assignment**:
   - Colors are automatically assigned by the UI component (`DialogueScript.vue`)
   - First speaker gets blue, second gets rose, third gets emerald, etc.
   - Each unique speaker name gets a consistent color throughout the lesson

5. **Example Scripts for Batch Updates**:
   ```bash
   # Python script to add speaker field to segments
   cat lesson.json | python3 -c "
   import json, sys
   data = json.load(sys.stdin)
   # Define speaker mapping based on story analysis
   speaker_map = {'s1': 'Graham', 's2': 'John', ...}
   for seg in data['segments']:
       if seg['id'] in speaker_map:
           seg['speaker'] = speaker_map[seg['id']]
   print(json.dumps(data, ensure_ascii=False, indent=2))
   " > updated_lesson.json
   ```

---

## Color Palette Reference

The speaker badge colors are assigned in order of appearance:

| Order | Speaker | Background | Text |
|-------|---------|------------|------|
| 1st | First speaker | bg-blue-100 | text-blue-600 |
| 2nd | Second speaker | bg-rose-100 | text-rose-600 |
| 3rd | Third speaker | bg-emerald-100 | text-emerald-600 |
| 4th | Fourth speaker | bg-violet-100 | text-violet-600 |
| 5th | Fifth speaker | bg-amber-100 | text-amber-600 |
| 6th | Sixth speaker | bg-cyan-100 | text-cyan-600 |