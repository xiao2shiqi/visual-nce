import json
import os
import re

directory = '/Users/phoenix/Documents/workspace-personal/visual-nce/src/data/lessons'

def check_lesson(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    filename = os.path.basename(filepath)
    lesson_id = data.get('id', filename.replace('.json', ''))
    
    segments = data.get('segments', [])
    if not segments:
        return 'No segments'

    missing_count = 0
    incomplete_count = 0
    total_segments = len(segments)

    for seg in segments:
        if 'analysis' not in seg:
            missing_count += 1
        else:
            analysis = seg['analysis']
            # Check if analysis is empty or words list is empty
            if not analysis or (isinstance(analysis, dict) and not analysis.get('words')):
                incomplete_count += 1

    if missing_count > 0 or incomplete_count > 0:
        return {
            'id': lesson_id,
            'file': filename,
            'missing': missing_count,
            'incomplete': incomplete_count,
            'total': total_segments
        }
    return None

results = []
files = sorted([f for f in os.listdir(directory) if f.endswith('.json') and (f.startswith('nce1-') or f.startswith('nce2-'))])

for filename in files:
    filepath = os.path.join(directory, filename)
    res = check_lesson(filepath)
    if res:
        results.append(res)

print(f"{'Lesson ID':<15} | {'File':<15} | {'Missing':<8} | {'Incomplete':<10} | {'Total':<6}")
print("-" * 65)
for r in results:
    print(f"{r['id']:<15} | {r['file']:<15} | {r['missing']:<8} | {r['incomplete']:<10} | {r['total']:<6}")

