#!/usr/bin/env python3
"""
更新 curriculum.json 中已完成翻译的 NCE4 课程图片路径
"""

import json

# 已完成翻译的 NCE4 课程（34 课）
completed_lessons = [
    'nce4-l1', 'nce4-l10', 'nce4-l11', 'nce4-l12', 'nce4-l13', 'nce4-l14', 'nce4-l15', 'nce4-l16',
    'nce4-l17', 'nce4-l18', 'nce4-l19', 'nce4-l20', 'nce4-l21', 'nce4-l22', 'nce4-l23', 'nce4-l24',
    'nce4-l25', 'nce4-l26', 'nce4-l27', 'nce4-l28', 'nce4-l29', 'nce4-l3', 'nce4-l30', 'nce4-l31',
    'nce4-l32', 'nce4-l33', 'nce4-l34', 'nce4-l35', 'nce4-l36', 'nce4-l37', 'nce4-l38', 'nce4-l39',
    'nce4-l4'
]

# 读取 curriculum.json
with open('src/data/curriculum.json', 'r', encoding='utf-8') as f:
    curriculum = json.load(f)

# 找到 NCE4
for book in curriculum['books']:
    if book['id'] == 'nce4':
        for lesson in book['lessons']:
            if lesson['id'] in completed_lessons:
                # 提取课程编号
                lesson_num = lesson['id'].split('-')[1]  # e.g., 'l1' from 'nce4-l1'
                # 更新图片路径
                lesson['image'] = f"/images/nce4/{lesson_num}/scene1.jpg"
                print(f"✓ Updated {lesson['id']}: {lesson['image']}")

# 保存更新后的 curriculum.json
with open('src/data/curriculum.json', 'w', encoding='utf-8') as f:
    json.dump(curriculum, f, indent=2, ensure_ascii=False)

print(f"\n✅ 总计更新了 {len(completed_lessons)} 个课程的图片路径")
