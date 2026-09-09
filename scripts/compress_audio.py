#!/usr/bin/env python3
"""Audio compression script for Visual NCE.

Compresses speech MP3 files (voice reading, no background music) to 64kbps mono MP3.
Features:
- Safe sidecar output by default (never overwrites source files unless explicitly configured).
- Supports --dry-run for zero-risk impact evaluation.
- Preserves directory hierarchy (e.g. nce1/, nce2/, nce3/, nce4/).
- Strips redundant 212KB embedded Sina Weibo watermark cover pictures by default (saving ~58MB across 277 files).
- Multi-threaded batch processing with resume support.
"""

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_DIR = ROOT / "public" / "audio"
DEFAULT_OUTPUT_DIR = ROOT / "public" / "audio_compressed"


def check_ffmpeg() -> bool:
    """Verify that ffmpeg and ffprobe are installed and accessible."""
    return bool(shutil.which("ffmpeg")) and bool(shutil.which("ffprobe"))


def probe_audio(path: Path) -> dict:
    """Get audio metadata (duration, bitrate, sample rate, channels, cover art)."""
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {}
    data = json.loads(res.stdout)
    fmt = data.get("format", {})
    streams = data.get("streams", [])
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    has_cover = any(s.get("codec_type") == "video" for s in streams)

    return {
        "duration": float(fmt.get("duration") or audio_stream.get("duration") or 0.0),
        "bitrate": int(fmt.get("bit_rate") or audio_stream.get("bit_rate") or 0),
        "sample_rate": int(audio_stream.get("sample_rate") or 0),
        "channels": int(audio_stream.get("channels") or 0),
        "has_cover": has_cover,
    }


def compress_file(
    src: Path,
    dst: Path,
    bitrate: str = "64k",
    strip_cover: bool = True,
    dry_run: bool = False,
    force: bool = False,
) -> dict:
    """Compress a single audio file.

    Returns a dict with execution statistics and status.
    """
    orig_size = src.stat().st_size

    if not force and dst.exists() and dst.stat().st_size > 0:
        return {
            "status": "skipped",
            "file": src.name,
            "orig_size": orig_size,
            "new_size": dst.stat().st_size,
        }

    if dry_run:
        meta = probe_audio(src)
        dur = meta.get("duration", 0.0)
        # 64kbps = 8000 B/s + ~1KB ID3/Xing metadata
        est_audio_bytes = int(dur * (int(bitrate.rstrip("kK")) * 1000 / 8))
        est_meta_bytes = 1024 + (218000 if not strip_cover and meta.get("has_cover") else 0)
        est_new_size = est_audio_bytes + est_meta_bytes
        return {
            "status": "dry_run",
            "file": src.name,
            "orig_size": orig_size,
            "new_size": est_new_size,
            "duration": dur,
        }

    dst.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-y", "-i", str(src)]
    if strip_cover:
        cmd.append("-vn")
    else:
        cmd.extend(["-c:v", "copy"])

    cmd.extend([
        "-c:a", "libmp3lame",
        "-b:a", bitrate,
        "-ac", "1",
        str(dst)
    ])

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {
            "status": "error",
            "file": src.name,
            "orig_size": orig_size,
            "new_size": 0,
            "error": res.stderr.strip().splitlines()[-1] if res.stderr else "Unknown ffmpeg error",
        }

    new_size = dst.stat().st_size
    return {
        "status": "success",
        "file": src.name,
        "orig_size": orig_size,
        "new_size": new_size,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compress NCE audio recordings to 64kbps mono MP3 for Cloudflare deployment."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Path to input audio directory (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Path to sidecar output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--bitrate",
        type=str,
        default="64k",
        help="Target audio bitrate (default: 64k)",
    )
    parser.add_argument(
        "--keep-cover",
        action="store_true",
        default=False,
        help="Keep embedded APIC cover art images (default: strip redundant ~212KB Sina Weibo watermark covers)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate compression without writing files or calling ffmpeg",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files in output directory",
    )
    parser.add_argument(
        "--workers",
        "-j",
        type=int,
        default=min(8, os.cpu_count() or 4),
        help="Number of concurrent ffmpeg workers (default: 4-8)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit processing to first N files (useful for quick testing)",
    )
    args = parser.parse_args()

    if not check_ffmpeg():
        print("Error: ffmpeg and/or ffprobe are not found in PATH.", file=sys.stderr)
        print("Please install ffmpeg (e.g. brew install ffmpeg).", file=sys.stderr)
        sys.exit(1)

    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()

    if input_dir == output_dir and not args.dry_run:
        print(
            "Safety Error: Target output directory cannot be identical to input directory!\n"
            "This script defaults to a sidecar directory (e.g. public/audio_compressed) to prevent data loss.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Collect MP3 files
    mp3_files = sorted(input_dir.rglob("*.mp3"))
    if args.limit:
        mp3_files = mp3_files[:args.limit]

    total_files = len(mp3_files)
    if total_files == 0:
        print(f"No .mp3 files found in {input_dir}")
        return

    strip_cover = not args.keep_cover
    print("=" * 68)
    print(" 🎙️ Visual NCE - Audio Compression Utility")
    print("=" * 68)
    print(f" Source Directory : {input_dir}")
    print(f" Target Directory : {output_dir}")
    print(f" Total MP3 Files  : {total_files}")
    print(f" Target Bitrate   : {args.bitrate} mono (ac=1)")
    print(f" Strip Cover Art  : {'YES (strip ~212KB watermark images)' if strip_cover else 'NO (preserve cover art)'}")
    print(f" Mode             : {'DRY RUN (simulation only)' if args.dry_run else 'ACTIVE RUN'}")
    print(f" Workers          : {args.workers}")
    print("=" * 68)

    start_time = time.time()
    results = []

    def task(src: Path):
        rel = src.relative_to(input_dir)
        dst = output_dir / rel
        return compress_file(
            src=src,
            dst=dst,
            bitrate=args.bitrate,
            strip_cover=strip_cover,
            dry_run=args.dry_run,
            force=args.force,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(task, f): f for f in mp3_files}
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)
            completed += 1
            status = res["status"]
            orig = res["orig_size"]
            new = res.get("new_size", 0)
            ratio = ((orig - new) / orig * 100) if orig > 0 else 0

            if completed % 25 == 0 or completed == total_files or total_files <= 10:
                print(
                    f"[{completed:3d}/{total_files:3d}] ({status:7s}) {res['file'][:32]:<32} "
                    f"{orig/1024:6.1f}KB -> {new/1024:6.1f}KB (-{ratio:4.1f}%)"
                )

    elapsed = time.time() - start_time
    total_orig = sum(r["orig_size"] for r in results)
    total_new = sum(r["new_size"] for r in results)
    total_saved = total_orig - total_new
    saved_ratio = (total_saved / total_orig * 100) if total_orig > 0 else 0

    success_cnt = sum(1 for r in results if r["status"] in ("success", "dry_run"))
    skipped_cnt = sum(1 for r in results if r["status"] == "skipped")
    error_cnt = sum(1 for r in results if r["status"] == "error")

    print("\n" + "=" * 68)
    print(" 📊 Compression Summary Report")
    print("=" * 68)
    print(f" Completed in     : {elapsed:.2f} seconds")
    print(f" Files Processed  : {success_cnt} succeeded, {skipped_cnt} skipped, {error_cnt} failed")
    print(f" Original Volume  : {total_orig / (1024*1024):.2f} MB ({total_orig:,} bytes)")
    print(f" Compressed Volume: {total_new / (1024*1024):.2f} MB ({total_new:,} bytes)")
    print(f" Storage Saved    : {total_saved / (1024*1024):.2f} MB ({saved_ratio:.2f}%)")
    print("=" * 68)


if __name__ == "__main__":
    main()
