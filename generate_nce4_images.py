import os
import re
import sys
import time
import subprocess
import google.generativeai as genai
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "imagen-3.0-generate-001"
PROMPTS_FILE = "nce4_missing_images_prompts.md"
OUTPUT_BASE_DIR = "public/images/nce4"

def setup_api():
    if not API_KEY:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please export your API key: export GEMINI_API_KEY='your_key'")
        return False
    genai.configure(api_key=API_KEY)
    return True

def parse_prompts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lessons = []
    
    parts = re.split(r'## Lesson (\d+):', content)
    
    for i in range(1, len(parts), 2):
        lesson_num = int(parts[i])
        section_content = parts[i+1]
        
        prompt_match = re.search(r'\*\*Prompt:\*\*\s*\n\s*>\s*(.*?)(?:\n\s*\n|$)', section_content, re.DOTALL)
        if prompt_match:
            prompt = prompt_match.group(1).strip()
            prompt = prompt.replace('\n', ' ')
            lessons.append({
                'lesson': lesson_num,
                'prompt': prompt
            })
    
    return lessons

def git_push_progress():
    try:
        print("\n" + "="*50)
        print("Rate limited! Pushing current progress to git...")
        print("="*50)
        
        subprocess.run(["git", "add", "public/images/nce4/"], check=True)
        
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            subprocess.run(["git", "commit", "-m", "feat: add NCE4 lesson images (partial - rate limited)"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Successfully pushed progress to git!")
        else:
            print("No new changes to push.")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        return False

def generate_image(prompt, output_dir):
    try:
        print(f"Generating image for prompt: {prompt[:50]}...")
        model = genai.ImageGenerationModel(MODEL_NAME)
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="16:9",
        )
        
        if response.images:
            image = response.images[0]
            
            scene_path = os.path.join(output_dir, "scene1.png")
            image.save(scene_path)
            print(f"Saved {scene_path}")
            
            create_thumbnail(scene_path, output_dir)
            return True, None
        else:
            print("No images returned.")
            return False, None
            
    except Exception as e:
        error_msg = str(e).lower()
        if "rate" in error_msg or "quota" in error_msg or "limit" in error_msg or "429" in error_msg:
            print(f"Rate limited: {e}")
            return False, "rate_limited"
        print(f"Failed to generate image: {e}")
        return False, str(e)

def create_thumbnail(image_path, output_dir):
    try:
        with Image.open(image_path) as img:
            base_width = 400
            w_percent = (base_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            thumb_path = os.path.join(output_dir, "thumbnail.png")
            img.save(thumb_path)
            print(f"Saved {thumb_path}")
    except Exception as e:
        print(f"Failed to create thumbnail: {e}")

def main():
    if not setup_api():
        return

    print(f"Reading prompts from {PROMPTS_FILE}...")
    lessons = parse_prompts(PROMPTS_FILE)
    print(f"Found {len(lessons)} lessons to process.")

    generated_count = 0
    
    for item in lessons:
        lesson_num = item['lesson']
        prompt = item['prompt']
        
        lesson_dir = os.path.join(OUTPUT_BASE_DIR, f"l{lesson_num}")
        if not os.path.exists(lesson_dir):
            os.makedirs(lesson_dir)
            print(f"Created directory: {lesson_dir}")
        
        if os.path.exists(os.path.join(lesson_dir, "scene1.png")):
            print(f"Image for Lesson {lesson_num} already exists. Skipping.")
            continue
            
        print(f"Processing Lesson {lesson_num}...")
        success, error = generate_image(prompt, lesson_dir)
        
        if success:
            print(f"Successfully finished Lesson {lesson_num}")
            generated_count += 1
            time.sleep(2)
        elif error == "rate_limited":
            print(f"Rate limited at Lesson {lesson_num}")
            if generated_count > 0:
                git_push_progress()
            print(f"\nGenerated {generated_count} images before rate limit.")
            print(f"Resume from Lesson {lesson_num} when rate limit resets.")
            sys.exit(0)
        else:
            print(f"Failed to finish Lesson {lesson_num}")
            time.sleep(5)

    print(f"\nCompleted! Generated {generated_count} images total.")
    
    if generated_count > 0:
        git_push_progress()

if __name__ == "__main__":
    main()
