import json
import os

directory = 'src/data/lessons'
files = sorted([f for f in os.listdir(directory) if f.endswith('.json') and f.startswith('nce')])

summary = {
    'nce1': {'total': 0, 'missing_trans': 0, 'missing_analysis': 0},
    'nce2': {'total': 0, 'missing_trans': 0, 'missing_analysis': 0},
    'nce3': {'total': 0, 'missing_trans': 0, 'missing_analysis': 0},
    'nce4': {'total': 0, 'missing_trans': 0, 'missing_analysis': 0}
}

details = []

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lesson_id = data.get('id', filename.replace('.json', ''))
    segments = data.get('segments', [])

    book = None
    if filename.startswith('nce1-'): book = 'nce1'
    elif filename.startswith('nce2-'): book = 'nce2'
    elif filename.startswith('nce3-'): book = 'nce3'
    elif filename.startswith('nce4-'): book = 'nce4'

    if not book:
        continue

    summary[book]['total'] += 1

    missing_trans = 0
    missing_analysis = 0

    for seg in segments:
        if not seg.get('translation') or seg.get('translation').strip() == '':
            missing_trans += 1

        analysis = seg.get('analysis')
        if not analysis or not isinstance(analysis, dict) or 'words' not in analysis or not analysis['words']:
            missing_analysis += 1

    if missing_trans > 0 or missing_analysis > 0:
        summary[book]['missing_trans'] += missing_trans
        summary[book]['missing_analysis'] += missing_analysis
        details.append({
            'lesson': lesson_id,
            'total': len(segments),
            'trans': missing_trans,
            'analysis': missing_analysis
        })

# Print summary
print("=" * 80)
print("NCE1-4 中文字幕和句子解析缺失统计")
print("=" * 80)
print()

for book in ['nce1', 'nce2', 'nce3', 'nce4']:
    s = summary[book]
    if s['total'] > 0:
        print(f"{book.upper()}:")
        print(f"  总课程数: {s['total']}")
        print(f"  缺失中文字幕: {s['missing_trans']} 个句子")
        print(f"  缺失句子解析: {s['missing_analysis']} 个句子")
        print()

print("=" * 80)
print("NCE4 详细课程列表 (按缺失数量排序)")
print("=" * 80)
print()

# Sort NCE4 lessons by total missing
nce4_details = [d for d in details if d['lesson'].startswith('nce4')]
nce4_details.sort(key=lambda x: x['trans'] + x['analysis'], reverse=True)

print(f"{'课程':<15} | {'总句子':<8} | {'缺字幕':<8} | {'缺解析':<8} | {'缺失率':<8}")
print("-" * 70)
for d in nce4_details:
    missing_rate = f"{((d['trans'] + d['analysis']) / d['total'] * 100):.1f}%"
    print(f"{d['lesson']:<15} | {d['total']:<8} | {d['trans']:<8} | {d['analysis']:<8} | {missing_rate:<8}")
