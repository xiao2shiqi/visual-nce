
import json
import os
import re

def count_words(text):
    return len(re.findall(r'\w+', text))

lessons_dir = 'src/data/lessons'
incomplete_lessons = []

for filename in sorted(os.listdir(lessons_dir)):
    if filename.startswith('nce2-l') and filename.endswith('.json'):
        filepath = os.path.join(lessons_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            total_missing = 0
            total_sparse = 0
            for segment in data.get('segments', []):
                text_word_count = count_words(segment.get('text', ''))
                analysis_word_count = len(segment.get('analysis', {}).get('words', []))
                
                if analysis_word_count == 0:
                    total_missing += 1
                elif analysis_word_count < text_word_count * 0.5:
                    total_sparse += 1
            
            if total_missing > 0 or total_sparse > 0:
                incomplete_lessons.append({
                    'file': filename,
                    'missing': total_missing,
                    'sparse': total_sparse
                })

for item in incomplete_lessons:
    print(f"{item['file']}: {item['missing']} missing, {item['sparse']} sparse")
