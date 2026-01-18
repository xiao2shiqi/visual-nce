import json
import os

lessons_dir = 'src/data/lessons'
images_dir = 'public/images'

# Check if images exist in both public and static directories
def check_image_exists(image_path):
    # Check in public/images
    public_path = os.path.join('public', image_path.lstrip('/'))
    if os.path.exists(public_path):
        return True, 'public'

    # Check in static/images (old location)
    static_path = os.path.join('static', image_path.lstrip('/'))
    if os.path.exists(static_path):
        return True, 'static'

    return False, None

files = sorted([f for f in os.listdir(lessons_dir) if f.endswith('.json') and f.startswith('nce')])

summary = {
    'nce1': {'total': 0, 'missing_images': 0, 'missing_thumb_images': 0},
    'nce2': {'total': 0, 'missing_images': 0, 'missing_thumb_images': 0},
    'nce3': {'total': 0, 'missing_images': 0, 'missing_thumb_images': 0},
    'nce4': {'total': 0, 'missing_images': 0, 'missing_thumb_images': 0}
}

details = []
missing_thumb_details = []

for filename in files:
    filepath = os.path.join(lessons_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lesson_id = data.get('id', filename.replace('.json', ''))

    book = None
    if filename.startswith('nce1-'): book = 'nce1'
    elif filename.startswith('nce2-'): book = 'nce2'
    elif filename.startswith('nce3-'): book = 'nce3'
    elif filename.startswith('nce4-'): book = 'nce4'

    if not book:
        continue

    summary[book]['total'] += 1

    # Check main image
    image_path = data.get('image', '')
    image_exists = False
    image_location = None

    if image_path:
        image_exists, image_location = check_image_exists(image_path)

    if not image_exists:
        summary[book]['missing_images'] += 1
        details.append({
            'lesson': lesson_id,
            'image': image_path,
            'file': filename
        })

    # Check thumbnail image
    thumb_image_path = data.get('thumbImage', '')
    thumb_exists = False

    if thumb_image_path:
        thumb_exists, _ = check_image_exists(thumb_image_path)

    if not thumb_exists and thumb_image_path:
        summary[book]['missing_thumb_images'] += 1
        missing_thumb_details.append({
            'lesson': lesson_id,
            'thumbImage': thumb_image_path,
            'file': filename
        })

# Print summary
print("=" * 80)
print("NCE1-4 图片缺失统计")
print("=" * 80)
print()

for book in ['nce1', 'nce2', 'nce3', 'nce4']:
    s = summary[book]
    if s['total'] > 0:
        print(f"{book.upper()}:")
        print(f"  总课程数: {s['total']}")
        print(f"  缺失主图片: {s['missing_images']} 课")
        print(f"  缺失缩略图: {s['missing_thumb_images']} 课")
        print()

total_missing = sum(summary[book]['missing_images'] for book in summary)
total_thumb_missing = sum(summary[book]['missing_thumb_images'] for book in summary)

print("=" * 80)
print(f"总计: {total_missing} 课缺失主图片, {total_thumb_missing} 课缺失缩略图")
print("=" * 80)

# Print details if there are missing images
if details:
    print()
    print("=" * 80)
    print("缺失主图片的课程详情")
    print("=" * 80)
    print()
    print(f"{'课程':<15} | {'文件名':<20} | {'图片路径'}")
    print("-" * 80)
    for d in details:
        print(f"{d['lesson']:<15} | {d['file']:<20} | {d['image']}")

if missing_thumb_details:
    print()
    print("=" * 80)
    print("缺失缩略图的课程详情")
    print("=" * 80)
    print()
    print(f"{'课程':<15} | {'文件名':<20} | {'缩略图路径'}")
    print("-" * 80)
    for d in missing_thumb_details:
        print(f"{d['lesson']:<15} | {d['file']:<20} | {d['thumbImage']}")
