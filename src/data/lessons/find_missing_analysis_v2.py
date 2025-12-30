import json
import os
import sys

directory = '/Users/phoenix/Documents/workspace-personal/visual-nce/src/data/lessons'
print(f"Scanning directory: {directory}")

files = sorted([f for f in os.listdir(directory) if f.endswith('.json') and (f.startswith('nce1-') or f.startswith('nce2-'))])
print(f"Found {len(files)} files to check.")

results = []

for filename in files:
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    lesson_id = data.get('id', filename.replace('.json', ''))
    segments = data.get('segments', [])

    missing_count = 0
    incomplete_count = 0
    
    if not segments:
         print(f"{filename}: No segments found")
         continue

    for seg in segments:
        if 'analysis' not in seg:
            missing_count += 1
        else:
            analysis = seg['analysis']
            if not analysis: # analysis is null or empty dict
                incomplete_count += 1
            elif isinstance(analysis, dict) and 'words' in analysis:
                if not analysis['words']: # words list is empty
                    incomplete_count += 1
                # If words exists and is not empty, we assume it's good for now, 
                # unless user implies "grammar" is missing. 
                # For now just checking "words" as my previous inspection suggested.
            elif isinstance(analysis, dict) and 'words' not in analysis:
                 # analysis exists but no words key?
                 incomplete_count += 1

    if missing_count > 0 or incomplete_count > 0:
        results.append({
            'id': lesson_id,
            'file': filename,
            'missing': missing_count,
            'incomplete': incomplete_count,
            'total': len(segments)
        })

print(f"{'Lesson ID':<15} | {'File':<15} | {'Missing':<8} | {'Incomplete':<10} | {'Total':<6}")
print("-" * 65)
for r in results:
    print(f"{r['id']:<15} | {r['file']:<15} | {r['missing']:<8} | {r['incomplete']:<10} | {r['total']:<6}")

