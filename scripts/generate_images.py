#!/usr/bin/env python3
import argparse
import ast
import base64
import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "public" / "images"
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_SUFFIX = (
    " Maintain high character and background consistency. "
    "Studio Ghibli watercolor style."
)


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def normalize_prompt(text: str) -> str:
    return " ".join(text.strip().split())


def lesson_number_from_path(path: Path) -> Optional[int]:
    match = re.search(r"l(\d+)", path.stem)
    return int(match.group(1)) if match else None


def parse_markdown_prompts(file_path: Path) -> List[Dict]:
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8")
    lessons = []
    pattern = r"## Lesson (\d+)(?::\s*Scene\s*(\d+))?:\s*(.*?)(?=\n## Lesson|\Z)"
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        lesson_num = int(match.group(1))
        scene_num = int(match.group(2)) if match.group(2) else 1
        section = match.group(3)
        prompt_match = re.search(
            r"\*\*Prompt:\*\*\s*\n\s*>\s*(.*?)(?:\n\s*\n|$)", section, re.DOTALL
        )
        if not prompt_match:
            continue
        lessons.append(
            {
                "lesson": lesson_num,
                "filename": f"scene{scene_num}.png",
                "prompt": normalize_prompt(prompt_match.group(1)),
                "source": str(file_path.resolve().relative_to(ROOT)),
            }
        )

    return lessons


def parse_storyboard_script(file_path: Path) -> List[Dict]:
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    lesson_num = lesson_number_from_path(file_path)
    if lesson_num is None:
        raise ValueError(f"Unable to infer lesson number from {file_path.name}")

    master_parts: List[str] = []
    storyboard: Optional[List[Dict]] = None

    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        name = target.id

        if name == "STORYBOARD":
            storyboard = ast.literal_eval(node.value)
            continue

        if name == "STYLE" or name == "SCENE" or name.startswith("CHAR_"):
            value = ast.literal_eval(node.value)
            if isinstance(value, str):
                master_parts.append(value)

    if not storyboard:
        raise ValueError(f"No STORYBOARD found in {file_path}")

    master_prompt = "".join(master_parts)
    tasks = []
    for order, item in enumerate(storyboard):
        scene_id = item["id"]
        desc = item["desc"]
        tasks.append(
            {
                "lesson": lesson_num,
                "order": order,
                "filename": f"{scene_id}.png",
                "prompt": normalize_prompt(master_prompt + desc + DEFAULT_SUFFIX),
                "source": str(file_path.resolve().relative_to(ROOT)),
            }
        )
    return tasks


def gemini_generate_image(
    api_key: str,
    model: str,
    prompt: str,
    retries: int,
    reference_image: Optional[bytes] = None,
) -> Optional[bytes]:
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    if reference_image:
        parts = [
            {
                "text": (
                    "REFERENCE IMAGE FOR CONSISTENCY: The following image is scene 1 of this lesson. "
                    "You MUST keep all character appearances strictly identical to this reference — "
                    "same face, same hair color and style, same clothing, same body type. "
                    "Only the scene action and composition should change as described below."
                )
            },
            {
                "inlineData": {
                    "mimeType": "image/png",
                    "data": base64.b64encode(reference_image).decode(),
                }
            },
            {"text": prompt},
        ]
    else:
        parts = [{"text": prompt}]
    payload = {
        "contents": [{"role": "user", "parts": parts}],
    }
    data = json.dumps(payload).encode("utf-8")

    for attempt in range(1, retries + 1):
        req = request.Request(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=180) as resp:
                full_resp = json.loads(resp.read().decode("utf-8"))
            parts = (
                full_resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            )
            for part in parts:
                inline_data = part.get("inlineData")
                if inline_data and inline_data.get("data"):
                    return base64.b64decode(inline_data["data"])
            raise RuntimeError(f"Response contained no inline image data: {full_resp}")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            message = f"HTTP {exc.code}: {body}"
        except Exception as exc:
            message = str(exc)

        if attempt == retries:
            raise RuntimeError(message)

        wait_seconds = min(10, attempt * 2)
        print(
            f"Request failed (attempt {attempt}/{retries}): {message}. "
            f"Retrying in {wait_seconds}s...",
            flush=True,
        )
        time.sleep(wait_seconds)

    return None


def discover_prompts_file(book: str) -> Optional[Path]:
    candidates = [
        ROOT / f"{book}_missing_images_prompts.md",
        ROOT / f"{book}_prompts.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def collect_tasks(
    book: str,
    start: int,
    end: int,
    source_mode: str,
    prompts_override: Optional[str],
    storyboard_override: Optional[str],
) -> List[Dict]:
    tasks_by_lesson: Dict[int, List[Dict]] = {}

    if source_mode in {"auto", "markdown"}:
        prompts_file = (
            Path(prompts_override) if prompts_override else discover_prompts_file(book)
        )
        if prompts_file and prompts_file.exists():
            for task in parse_markdown_prompts(prompts_file):
                tasks_by_lesson.setdefault(task["lesson"], []).append(task)

    if source_mode in {"auto", "storyboard"}:
        storyboard_files: List[Path] = []
        if storyboard_override:
            storyboard_files = [Path(storyboard_override)]
        else:
            # Check both the scripts/ directory and book-specific subdirectories
            storyboard_files = sorted(
                (ROOT / "scripts").glob("generate_l*_storyboard.py")
            )
            storyboard_files += sorted(
                (ROOT / "scripts" / book).glob("generate_l*_storyboard.py")
            )

        for storyboard_file in storyboard_files:
            try:
                for task in parse_storyboard_script(storyboard_file):
                    tasks_by_lesson.setdefault(task["lesson"], []).append(task)
            except Exception as exc:
                print(
                    f"Warning: Skipping storyboard {storyboard_file.name}: {exc}",
                    flush=True,
                )

    selected = []
    for lesson in range(start, end + 1):
        lesson_tasks = tasks_by_lesson.get(lesson, [])
        if not lesson_tasks:
            continue

        if source_mode == "auto":
            storyboard_tasks = [
                task
                for task in lesson_tasks
                if task["source"].endswith("_storyboard.py")
            ]
            selected.extend(storyboard_tasks or lesson_tasks)
            continue

        selected.extend(lesson_tasks)

    # Storyboard tasks preserve STORYBOARD list order (via "order" field).
    # Markdown tasks fall back to filename sort.
    return sorted(selected, key=lambda item: (item["lesson"], item.get("order", 9999), item["filename"]))


def main():
    parser = argparse.ArgumentParser(
        description="Visual NCE image generator for markdown prompts and storyboard scripts."
    )
    parser.add_argument(
        "--book", default="nce1", help="Book ID (nce1, nce2, nce3, nce4)"
    )
    parser.add_argument("--start", type=int, default=1, help="First lesson number")
    parser.add_argument("--end", type=int, default=150, help="Last lesson number")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--prompts", help="Explicit markdown prompts file path")
    parser.add_argument("--storyboard", help="Explicit storyboard script path")
    parser.add_argument(
        "--source",
        choices=["auto", "markdown", "storyboard"],
        default="auto",
        help="Prompt source selection",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=2.0,
        help="Delay between successful generations in seconds",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of API retries per image",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print matched tasks without generating images",
    )
    args = parser.parse_args()

    load_env_file(ROOT / ".env")
    api_key = os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("VERTEX_IMAGE_MODEL", DEFAULT_MODEL)

    if not api_key:
        if not args.dry_run:
            print("Error: GOOGLE_API_KEY not found in .env", flush=True)
        return

    tasks = collect_tasks(
        book=args.book,
        start=args.start,
        end=args.end,
        source_mode=args.source,
        prompts_override=args.prompts,
        storyboard_override=args.storyboard,
    )

    print(f"Matched {len(tasks)} image tasks.", flush=True)
    if not tasks:
        print(
            f"No prompts found for {args.book} lessons {args.start}-{args.end}.",
            flush=True,
        )
        return

    for task in tasks:
        print(
            f"L{task['lesson']} -> {task['filename']} ({task['source']})",
            flush=True,
        )

    if args.dry_run:
        return

    print(f"Using model: {model}", flush=True)
    # anchor_image: first successfully generated image per lesson, used as visual reference
    anchor_by_lesson: Dict[int, bytes] = {}
    for task in tasks:
        lesson = task["lesson"]
        out_dir = DEFAULT_OUTPUT_DIR / args.book / f"l{lesson}"
        out_path = out_dir / task["filename"]

        if out_path.exists() and not args.force:
            print(f"Skipping L{lesson} {task['filename']} (exists)", flush=True)
            # Load existing file as anchor if we don't have one yet
            if lesson not in anchor_by_lesson:
                anchor_by_lesson[lesson] = out_path.read_bytes()
            continue

        reference = anchor_by_lesson.get(lesson)
        if reference:
            print(
                f"Generating {args.book} L{lesson} -> {task['filename']} (with reference anchor)...",
                flush=True,
            )
        else:
            print(
                f"Generating {args.book} L{lesson} -> {task['filename']} (anchor frame)...",
                flush=True,
            )
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            img_bytes = gemini_generate_image(
                api_key=api_key,
                model=model,
                prompt=task["prompt"],
                retries=args.retries,
                reference_image=reference,
            )
            if img_bytes:
                out_path.write_bytes(img_bytes)
                print(f"Saved: {out_path}", flush=True)
                if lesson not in anchor_by_lesson:
                    anchor_by_lesson[lesson] = img_bytes
                    print(f"  -> Set as anchor for L{lesson}", flush=True)
            else:
                print(f"Failed: {out_path}", flush=True)
            time.sleep(args.sleep)
        except Exception as exc:
            print(f"Error L{lesson} {task['filename']}: {exc}", flush=True)


if __name__ == "__main__":
    main()
