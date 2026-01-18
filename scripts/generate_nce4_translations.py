#!/usr/bin/env python3
"""
Script to generate Chinese translations and word analysis for NCE4 lessons.
This script reads NCE4 lesson files and generates:
1. Chinese translations for segments without them
2. Word analysis (parts of speech and meanings) for segments without them
"""

import json
import os
import sys

def generate_translation(text):
    """Generate Chinese translation for English text."""
    # This is a placeholder - in production, you would use an API or AI service
    # For now, return empty to indicate manual translation needed
    return ""

def generate_word_analysis(text):
    """Generate word analysis for English text."""
    # This is a placeholder - in production, you would use NLP/AI
    # For now, return empty words list
    return {"words": []}

def process_lesson(filepath, lesson_id):
    """Process a single lesson file to add missing translations and analysis."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    segments = data.get('segments', [])
    updated_count = 0
    missing_translation = []
    missing_analysis = []

    for seg in segments:
        seg_id = seg.get('id', 'unknown')
        text = seg.get('text', '')

        # Check translation
        if not seg.get('translation') or seg.get('translation').strip() == '':
            missing_translation.append({'id': seg_id, 'text': text})

        # Check analysis
        analysis = seg.get('analysis')
        if not analysis or not isinstance(analysis, dict) or 'words' not in analysis or not analysis['words']:
            missing_analysis.append({'id': seg_id, 'text': text})

    return {
        'id': lesson_id,
        'total': len(segments),
        'missing_translation': missing_translation,
        'missing_analysis': missing_analysis
    }

def main():
    lessons_dir = 'src/data/lessons'
    files = sorted([f for f in os.listdir(lessons_dir) if f.endswith('.json') and f.startswith('nce4-')])

    all_results = []

    for filename in files:
        filepath = os.path.join(lessons_dir, filename)
        result = process_lesson(filepath, filename.replace('.json', ''))
        all_results.append(result)

    # Print summary
    print("NCE4 Translation and Analysis Requirements")
    print("=" * 80)
    print()

    total_trans = 0
    total_analysis = 0

    for result in all_results:
        trans_count = len(result['missing_translation'])
        analysis_count = len(result['missing_analysis'])
        total_trans += trans_count
        total_analysis += analysis_count

        if trans_count > 0 or analysis_count > 0:
            print(f"{result['id']}: {result['total']} segments")
            if trans_count > 0:
                print(f"  Missing translations: {trans_count}")
            if analysis_count > 0:
                print(f"  Missing analysis: {analysis_count}")
            print()

    print("=" * 80)
    print(f"TOTAL: {total_trans} translations needed, {total_analysis} analysis needed")
    print("=" * 80)

    # Export detailed list for processing
    export_file = 'nce4_missing_content.json'
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_translations': total_trans,
                'total_analysis': total_analysis
            },
            'lessons': all_results
        }, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed report saved to: {export_file}")

if __name__ == '__main__':
    main()
