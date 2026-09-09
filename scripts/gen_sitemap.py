#!/usr/bin/env python3
"""
gen_sitemap.py - Generate full sitemap.xml for Visual NCE from curriculum.json.

Usage:
    python3 scripts/gen_sitemap.py [--curriculum PATH] [--output PATH] [--lastmod YYYY-MM-DD] [--url-style STYLE]

URL Styles:
    - hash (default):       https://nce.xiao27.com/#nce1-l1 (matches App.vue hash router)
    - hash-lesson:          https://nce.xiao27.com/#/lesson/nce1-l1 (legacy sitemap format)
    - path:                 https://nce.xiao27.com/lesson/nce1-l1 (standard path for future history mode / SSG)
"""

import argparse
import datetime
import json
import os
import sys
import xml.etree.ElementTree as ET

DEFAULT_BASE_URL = "https://nce.xiao27.com"
DEFAULT_LASTMOD = "2026-09-09"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate full sitemap.xml from curriculum.json."
    )
    parser.add_argument(
        "--curriculum",
        default="src/data/curriculum.json",
        help="Path to curriculum.json (default: src/data/curriculum.json)",
    )
    parser.add_argument(
        "--output",
        default="public/sitemap.xml",
        help="Path to output sitemap.xml (default: public/sitemap.xml)",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Site base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--lastmod",
        default=DEFAULT_LASTMOD,
        help=f"Last modification date in YYYY-MM-DD (default: {DEFAULT_LASTMOD})",
    )
    parser.add_argument(
        "--url-style",
        choices=["hash", "hash-lesson", "path"],
        default="hash",
        help="URL format style: 'hash' (/#id), 'hash-lesson' (/#/lesson/id), or 'path' (/lesson/id). Default: hash",
    )
    return parser.parse_args()


def load_curriculum(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Curriculum file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_lesson_url(base_url, lesson_id, style):
    clean_base = base_url.rstrip("/")
    if style == "hash-lesson":
        return f"{clean_base}/#/lesson/{lesson_id}"
    elif style == "hash":
        return f"{clean_base}/#{lesson_id}"
    elif style == "path":
        return f"{clean_base}/lesson/{lesson_id}"
    else:
        raise ValueError(f"Unknown url-style: {style}")


def generate_sitemap_xml(curriculum_data, base_url, lastmod, url_style):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<urlset xmlns="{SITEMAP_NS}">')

    # Homepage
    clean_base = base_url.rstrip("/")
    lines.append("  <!-- Homepage -->")
    lines.append("  <url>")
    lines.append(f"    <loc>{clean_base}/</loc>")
    lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append("    <changefreq>weekly</changefreq>")
    lines.append("    <priority>1.0</priority>")
    lines.append("  </url>")

    books = curriculum_data.get("books", [])
    book_stats = []

    for book in books:
        book_id = book.get("id", "")
        book_title = book.get("title", "")
        subtitle = book.get("subtitle", book_id.upper())
        lessons = book.get("lessons", [])

        lines.append("")
        lines.append(f"  <!-- {subtitle} Lessons ({book_title}) -->")

        count = 0
        for lesson in lessons:
            lesson_id = lesson.get("id")
            if not lesson_id:
                continue
            loc = build_lesson_url(base_url, lesson_id, url_style)
            lines.append("  <url>")
            lines.append(f"    <loc>{loc}</loc>")
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
            lines.append("    <changefreq>monthly</changefreq>")
            lines.append("    <priority>0.8</priority>")
            lines.append("  </url>")
            count += 1

        book_stats.append((book_id, subtitle, count))

    lines.append("</urlset>")
    lines.append("")  # newline at EOF

    xml_content = "\n".join(lines)
    return xml_content, book_stats


def validate_xml(xml_content):
    """
    Validate that the generated string is well-formed XML and conforms to sitemap schema basics.
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        raise ValueError(f"Generated content is not valid XML: {e}")

    expected_tag = f"{{{SITEMAP_NS}}}urlset"
    if root.tag != expected_tag:
        raise ValueError(f"Unexpected root tag: got {root.tag}, expected {expected_tag}")

    url_elements = root.findall(f"{{{SITEMAP_NS}}}url")
    if not url_elements:
        raise ValueError("Sitemap does not contain any <url> elements")

    for idx, url_elem in enumerate(url_elements):
        loc = url_elem.find(f"{{{SITEMAP_NS}}}loc")
        lastmod = url_elem.find(f"{{{SITEMAP_NS}}}lastmod")
        if loc is None or not loc.text:
            raise ValueError(f"URL entry #{idx+1} is missing <loc>")
        if lastmod is None or not lastmod.text:
            raise ValueError(f"URL entry #{idx+1} is missing <lastmod>")

    return len(url_elements)


def main():
    args = parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    curriculum_path = (
        args.curriculum
        if os.path.isabs(args.curriculum)
        else os.path.join(project_root, args.curriculum)
    )
    output_path = (
        args.output
        if os.path.isabs(args.output)
        else os.path.join(project_root, args.output)
    )

    print(f"Loading curriculum from: {curriculum_path}")
    curriculum_data = load_curriculum(curriculum_path)

    print(
        f"Generating sitemap (Base URL: {args.base_url}, Lastmod: {args.lastmod}, Style: {args.url_style})..."
    )
    xml_content, book_stats = generate_sitemap_xml(
        curriculum_data,
        base_url=args.base_url,
        lastmod=args.lastmod,
        url_style=args.url_style,
    )

    print("Validating generated XML...")
    url_count = validate_xml(xml_content)
    print(f"✓ XML validation PASSED: {url_count} valid <url> elements found.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"✓ Sitemap successfully written to: {output_path}")
    print("\nSummary:")
    print(f"  - Total URLs: {url_count}")
    print(f"  - Homepage: 1")
    for book_id, subtitle, count in book_stats:
        print(f"  - {subtitle} ({book_id}): {count} lessons")
    print(f"  - Output file size: {len(xml_content.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
