import json
import os

directory = '/Users/phoenix/Documents/workspace-personal/visual-nce/src/data/lessons'
files = sorted([f for f in os.listdir(directory) if f.endswith('.json') and f.startswith('nce2-')])

missing_map = {}

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            continue
            
    segments = data.get('segments', [])
    missing_segments = []
    
    for seg in segments:
        header = seg.get('text', '')
        # Check if analysis is missing or words is empty
        if 'analysis' not in seg or not seg['analysis'] or not seg['analysis'].get('words'):
            # simple heuristic: skip if text is extremely short or just headers unless it's a real sentence
            # But user wants "all".
            missing_segments.append({
                'id': seg['id'],
                'text': seg['text']
            })
            
    if missing_segments:
        missing_map[filename] = missing_segments

print(json.dumps(missing_map, indent=2, ensure_ascii=False))
