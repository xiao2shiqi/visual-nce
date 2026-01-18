import json
import os
from collections import defaultdict

directory = 'src/data/lessons'
files = sorted([f for f in os.listdir(directory) if f.endswith('.json') and f.startswith('nce')])

results = {
    'nce1': [],
    'nce2': [],
    'nce3': [],
    'nce4': []
}

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

    # Determine which book this lesson belongs to
    book = None
    if filename.startswith('nce1-'):
        book = 'nce1'
    elif filename.startswith('nce2-'):
        book = 'nce2'
    elif filename.startswith('nce3-'):
        book = 'nce3'
    elif filename.startswith('nce4-'):
        book = 'nce4'

    if not book:
        continue

    missing_translation = []
    missing_analysis = []

    for seg in segments:
        seg_id = seg.get('id', 'unknown')
        text = seg.get('text', '')

        # Check if translation is missing or empty
        if not seg.get('translation') or seg.get('translation').strip() == '':
            missing_translation.append({'id': seg_id, 'text': text})

        # Check if analysis is missing or has no words
        analysis = seg.get('analysis')
        if not analysis or not isinstance(analysis, dict):
            missing_analysis.append({'id': seg_id, 'text': text})
        elif 'words' not in analysis or not analysis['words']:
            missing_analysis.append({'id': seg_id, 'text': text})

    if missing_translation or missing_analysis:
        results[book].append({
            'id': lesson_id,
            'file': filename,
            'missing_translation': missing_translation,
            'missing_analysis': missing_analysis,
            'total_segments': len(segments)
        })

# Print summary by book
for book in ['nce1', 'nce2', 'nce3', 'nce4']:
    book_results = results[book]
    print(f"\n{'='*80}")
    print(f"{book.upper()}: {len(book_results)} lessons with missing translations or analysis")
    print(f"{'='*80}")

    for lesson in book_results:
        print(f"\n{lesson['id']} ({lesson['file']}):")
        print(f"  Total segments: {lesson['total_segments']}")

        if lesson['missing_translation']:
            print(f"  Missing translation ({len(lesson['missing_translation'])}):")
            for seg in lesson['missing_translation'][:3]:  # Show first 3
                print(f"    - {seg['id']}: {seg['text'][:50]}...")
            if len(lesson['missing_translation']) > 3:
                print(f"    ... and {len(lesson['missing_translation']) - 3} more")

        if lesson['missing_analysis']:
            print(f"  Missing analysis ({len(lesson['missing_analysis'])}):")
            for seg in lesson['missing_analysis'][:3]:  # Show first 3
                print(f"    - {seg['id']}: {seg['text'][:50]}...")
            if len(lesson['missing_analysis']) > 3:
                print(f"    ... and {len(lesson['missing_analysis']) - 3} more")

# Print overall summary
print(f"\n{'='*80}")
print("OVERALL SUMMARY")
print(f"{'='*80}")
total_lessons = sum(len(results[book]) for book in results)
print(f"Total lessons with missing content: {total_lessons}")
for book in ['nce1', 'nce2', 'nce3', 'nce4']:
    print(f"  {book}: {len(results[book])} lessons")
