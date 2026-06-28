#!/usr/bin/env python3
"""
Lesson data validation script.

Usage:
    python3 scripts/validate_lessons.py            # validate all books
    python3 scripts/validate_lessons.py nce1       # validate one book
    python3 scripts/validate_lessons.py nce2 nce3  # validate multiple books

Exit code: 0 = all pass, 1 = failures found.
"""

import json
import os
import re
import sys
import glob

LESS_DIR = "src/data/lessons"
AUDIO_DIR = "public/audio"

# ── Rules ────────────────────────────────────────────────────────────────────

# In NCE2/3/4, body segments must NOT use generic Man/Woman.
# Only Narrator or named characters are allowed.
NCE234_FORBIDDEN_ROLES = {"Man", "Woman"}

# NCE1 still allows Man/Woman only for lessons that genuinely have
# unnamed characters (we flag anything still using the bare label
# so a human can confirm it's intentional).
NCE1_WARN_ROLES = {"Man", "Woman"}

# Required fields on every segment.
REQUIRED_FIELDS = {"id", "role", "text", "startTime", "endTime"}

# ── Helpers ──────────────────────────────────────────────────────────────────

def lrc_timestamps(lrc_path):
    """Return list of (time_seconds, text) from an .lrc file."""
    result = []
    with open(lrc_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", line)
            if not m:
                continue
            t = int(m.group(1)) * 60 + float(m.group(2))
            text = m.group(3).strip()
            if text:
                result.append((t, text))
    return result

def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

# ── Per-lesson checks ─────────────────────────────────────────────────────────

def check_lesson(path, book):
    errors = []
    warnings = []

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"], []

    segments = data.get("segments", [])
    if not segments:
        errors.append("no segments found")
        return errors, warnings

    # ── 1. Required fields ──────────────────────────────────────────────────
    for seg in segments:
        missing = REQUIRED_FIELDS - seg.keys()
        if missing:
            errors.append(f"segment {seg.get('id','?')} missing fields: {missing}")

    # ── 2. startTime < endTime ──────────────────────────────────────────────
    for seg in segments:
        st = seg.get("startTime")
        et = seg.get("endTime")
        if st is not None and et is not None and st >= et:
            errors.append(
                f"segment {seg['id']}: startTime({st}) >= endTime({et})"
            )

    # ── 3 & 4. Body segments ────────────────────────────────────────────────
    body_segs = [s for s in segments if not str(s.get("id", "")).startswith("intro")]

    # No overlapping body segments.
    # Intro-segment overlaps are a known historical data issue in NCE3/NCE4
    # (the "Listen to the tape…" phrase has no LRC entry so intro_3/intro_4
    # share timestamps). We only flag overlaps among body segments.
    body_ordered = sorted(
        [s for s in body_segs if s.get("startTime") is not None],
        key=lambda s: s["startTime"],
    )
    for i in range(len(body_ordered) - 1):
        a, b = body_ordered[i], body_ordered[i + 1]
        if a.get("endTime") is not None and b.get("startTime") is not None:
            if a["endTime"] > b["startTime"] + 0.05:  # 50ms tolerance
                errors.append(
                    f"overlap: {a['id']} ends {a['endTime']:.2f} but "
                    f"{b['id']} starts {b['startTime']:.2f}"
                )

    # ── Role rules ──────────────────────────────────────────────────────────

    if book in ("nce2", "nce3", "nce4"):
        for seg in body_segs:
            role = seg.get("role", "")
            if role in NCE234_FORBIDDEN_ROLES:
                errors.append(
                    f"segment {seg['id']}: role='{role}' not allowed in {book.upper()} "
                    f"(use Narrator or a named character)"
                )
    elif book == "nce1":
        for seg in body_segs:
            role = seg.get("role", "")
            if role in NCE1_WARN_ROLES:
                warnings.append(
                    f"segment {seg['id']}: role='{role}' — confirm this is intentional"
                )

    # ── 5. Timing drift vs .lrc (>2s threshold, body segments only) ───────
    # Skips intro_1 (lesson number) and intro_2 (title) because NCE3/NCE4
    # LRC files do not include the "Listen to the tape…" phrase and the
    # lesson title is at a different position than the LRC expects.
    audio = data.get("audio", "")
    if audio:
        lrc_name = os.path.basename(audio).replace(".mp3", ".lrc")
        lrc_path = os.path.join(AUDIO_DIR, book, lrc_name)
        if os.path.exists(lrc_path):
            lrc = lrc_timestamps(lrc_path)
            lrc_norm = [(t, norm(en)) for t, en in lrc]
            skip_ids = {"intro_1", "intro_2", "intro_3"}
            for seg in segments:
                if seg.get("id") in skip_ids:
                    continue
                jt = seg.get("startTime")
                jtext = norm(seg.get("text", ""))
                if not jtext or jt is None:
                    continue
                cands = [(t, en) for t, en in lrc_norm if en == jtext or
                         (jtext and (jtext in en or en in jtext))]
                if not cands:
                    continue
                best = min(cands, key=lambda c: abs(c[0] - jt))
                # Skip if segment text is a SUFFIX of the matched LRC line
                # (split sentence: first half has the LRC timestamp, second
                # half correctly starts later — drift is expected, not a bug)
                if best[1] != jtext and best[1].endswith(jtext):
                    continue
                diff = jt - best[0]
                if abs(diff) > 2.0:
                    errors.append(
                        f"segment {seg['id']}: timing drift {diff:+.1f}s "
                        f"(json={jt:.2f}, lrc={best[0]:.2f})"
                    )

    return errors, warnings

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    books_arg = sys.argv[1:] if len(sys.argv) > 1 else ["nce1", "nce2", "nce3", "nce4"]
    books = [b.lower() for b in books_arg]

    total_lessons = 0
    total_errors = 0
    total_warnings = 0
    failed_lessons = []

    for book in books:
        pattern = os.path.join(LESS_DIR, f"{book}-l*.json")
        files = sorted(
            glob.glob(pattern),
            key=lambda f: int(re.search(r"l(\d+)", f).group(1)),
        )
        if not files:
            print(f"[WARN] No files found for {book}")
            continue

        book_errors = 0
        book_warnings = 0
        print(f"\n{'─'*60}")
        print(f"  {book.upper()}  ({len(files)} lessons)")
        print(f"{'─'*60}")

        for f in files:
            n = int(re.search(r"l(\d+)", f).group(1))
            errors, warnings = check_lesson(f, book)
            total_lessons += 1
            if errors:
                book_errors += len(errors)
                total_errors += len(errors)
                failed_lessons.append(f"{book}-L{n}")
                print(f"  FAIL  {book}-L{n}")
                for e in errors:
                    print(f"        ERROR: {e}")
            if warnings:
                book_warnings += len(warnings)
                total_warnings += len(warnings)
                print(f"  WARN  {book}-L{n}")
                for w in warnings:
                    print(f"        WARN:  {w}")

        status = "PASS" if book_errors == 0 else "FAIL"
        print(f"\n  {book.upper()} result: {status}  "
              f"({book_errors} errors, {book_warnings} warnings)")

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_lessons} lessons, {total_errors} errors, "
          f"{total_warnings} warnings")
    if total_errors == 0:
        print("ALL CHECKS PASSED ✓")
    else:
        print(f"FAILED LESSONS ({len(failed_lessons)}): {', '.join(failed_lessons)}")
    print(f"{'='*60}")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
