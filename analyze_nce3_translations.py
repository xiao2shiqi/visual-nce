import os
import json

lessons_dir = "/Users/phoenix/Documents/workspace/visual-nce/src/data/lessons"
missing_translations_report = []

for i in range(1, 61):
    filename = f"nce3-l{i}.json"
    filepath = os.path.join(lessons_dir, filename)
    
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            segments = data.get('segments', [])
            total_segments = len(segments)
            # 过滤掉 intro 开头的段落，因为标题往往没有翻译
            content_segments = [s for s in segments if not s.get('id', '').startswith('intro')]
            
            missing_count = 0
            for s in content_segments:
                if not s.get('translation') or s.get('translation').strip() == "":
                    missing_count += 1
            
            if len(content_segments) > 0:
                missing_ratio = missing_count / len(content_segments)
                if missing_count > 0:
                    missing_translations_report.append({
                        "lesson": f"Lesson {i}",
                        "title": data.get('title', ''),
                        "missing_count": missing_count,
                        "total_content_segments": len(content_segments),
                        "missing_ratio": f"{missing_ratio:.1%}"
                    })
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if not missing_translations_report:
    print("所有 NCE 3 课程的翻译似乎都是完整的！")
else:
    print(f"发现 {len(missing_translations_report)} 课存在翻译缺失：")
    print(f"{'课程':<12} | {'缺失段落':<10} | {'总段落':<10} | {'缺失比例':<10} | {'标题'}")
    print("-" * 80)
    for entry in missing_translations_report:
        print(f"{entry['lesson']:<12} | {entry['missing_count']:<10} | {entry['total_content_segments']:<10} | {entry['missing_ratio']:<10} | {entry['title']}")
