import glob
import json
import os

files = glob.glob('/Users/phoenix/Documents/workspace-personal/visual-nce/src/data/lessons/nce2-l*.json')

def get_lesson_num(fpath):
    try:
        filename = os.path.basename(fpath)
        num_part = filename.split('-l')[1].split('.')[0]
        return int(num_part)
    except:
        return 0

files.sort(key=get_lesson_num)

task_file_path = '/Users/phoenix/Documents/workspace-personal/visual-nce/nce2_analysis_tasks.md'

with open(task_file_path, 'w', encoding='utf-8') as task_file:
    task_file.write("# NCE 2 Analysis Completion Tasks\n\n")
    task_file.write("The following lessons have segments with incomplete sentence analysis (empty `words` array).\n\n")

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                lesson_id = data.get('id', os.path.basename(fpath))
                segments = data.get('segments', [])
                
                missing_count = 0
                for seg in segments:
                    text = seg.get('text', '').strip()
                    if not text: continue
                    
                    analysis = seg.get('analysis', {})
                    if not analysis:
                        missing_count += 1
                    elif not analysis.get('words'):
                        missing_count += 1
                
                if missing_count > 0:
                    task_file.write(f"- [ ] **{lesson_id}**: {missing_count} segments missing analysis\n")
                    
            except Exception as e:
                print(f"Error reading {fpath}: {e}")

print(f"Task list generated at: {task_file_path}")
