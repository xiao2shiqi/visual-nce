import json
import os

# Heuristic to patch remaining missing analysis fields with empty structure
# so the UI doesn't crash, even if we don't have perfect dictionary data for them yet.

directory = '/Users/phoenix/Documents/workspace-personal/visual-nce/src/data/lessons'
files = sorted([f for f in os.listdir(directory) if f.endswith('.json') and f.startswith('nce2-')])

for filename in files:
    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modified = False
        for seg in data.get('segments', []):
            if 'analysis' not in seg:
                # Add empty analysis to ensure structure consistency
                seg['analysis'] = {"words": []}
                modified = True
            elif seg['analysis'] is None:
                seg['analysis'] = {"words": []}
                modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Patched structure for {filename}")

    except Exception as e:
        print(f"Error handling {filename}: {e}")
