#!/usr/bin/env python3
"""L137 A Pleasant Dream — 梦境序列补帧（agy 编辑模式管线）。

⚠️ 2026-07-04 起生图管线已切换：Gemini API key 不可用（区域限制），
改用 Antigravity CLI（agy，Google 账号 OAuth，AI Pro 会员额度）。

核心工艺（一致性质变的关键）：
1. 「编辑模式」而非「文生图」——prompt 里强制声明 image EDITING task，
   要求把锚点图（scene1.webp）作为 INPUT IMAGE 传给生图工具，
   模型看到像素后房间/人物几乎零漂移；
2. 每帧只描述「保持一切不变 + 仅有的几处改动」；
3. 输出常落在 ~/.gemini/antigravity-cli/scratch/，跑完要检查并拷回；
4. 出图后必须逐帧 Read 验收（构图/一致性/无文字/长宽比 1376x768 横幅），
   正方形输出（1024x1024）会被播放器裁掉气泡，需带
   "keep the exact same wide landscape framing" 重生成。

本脚本封装单帧调用，STORYBOARD 里是 L137 实际使用的四段编辑指令，
供后续课程复制改写。用法：
    python3 scripts/nce1/generate_l137_storyboard.py [frame_id ...]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "public" / "images" / "nce1" / "l137"
SCRATCH = Path.home() / ".gemini" / "antigravity-cli" / "scratch"

KEEP = (
    "keep the painting exactly as it is — same room, same fireplace, wallpaper, "
    "furniture, same man Brian (tan Fair Isle cardigan), same woman Julie (pale "
    "checked dress, knitting a green sock), same tabby cat, same watercolor style, "
    "same wide composition. "
)

STORYBOARD = {
    "mink_coat": (
        "1) Add a large soft-edged thought bubble in the upper middle, INSIDE THE "
        "BUBBLE ONLY: Julie wearing an elegant brown mink fur coat posing like a "
        "wealthy lady (same face and hair as the woman below). 2) Brian gestures "
        "proudly toward the bubble, still holding his football pools paper. "
        "3) Julie wrinkles her nose, unimpressed, still holding her knitting."
    ),
    "dream_travel": (
        "1) Julie looks up from her knitting with a dreamy hopeful expression. "
        "2) Add a large soft-edged thought bubble in the upper middle, INSIDE THE "
        "BUBBLE: Brian and Julie together (same faces, hair and clothes as the "
        "couple below) standing at the railing of an ocean liner at sea, wind in "
        "their hair, distant tropical islands behind them — STRICTLY these 2 people "
        "only inside the bubble. 3) Brian looks toward Julie warmly."
    ),
    "dream_house": (
        "1) Brian spreads both arms wide with an excited smile, describing his "
        "dream (the pools paper rests on his lap). 2) Add a large soft-edged "
        "thought bubble in the upper middle, INSIDE THE BUBBLE: a big warm English "
        "country house with a beautiful flower garden, hedges and a winding path — "
        "NO people inside the bubble. 3) Julie watches him with a gentle amused smile."
    ),
    "poor_again": (
        "1) Julie raises one finger with a practical, doubtful expression. "
        "2) Brian scratches his head awkwardly with a sheepish smile. 3) Add a "
        "thought bubble in the upper middle that looks grey, sagging and deflating; "
        "INSIDE THE BUBBLE: Brian and Julie (same faces as the couple below) wearing "
        "shabby patched clothes, turning their empty pockets inside out — STRICTLY "
        "these 2 people only inside the bubble."
    ),
}


def generate(frame_id: str, edits: str) -> None:
    prompt = (
        "CRITICAL: image EDITING task. Pass scene1.webp (current directory) as an "
        "INPUT IMAGE to your image editing tool so the model sees the pixels. The "
        "output MUST keep the exact same wide landscape framing and aspect ratio as "
        "the input image (do not crop to square).\n\n"
        f"Edit instruction: {KEEP}Make ONLY these changes: {edits} "
        "NO text or letters anywhere.\n\n"
        f"Save as {frame_id}.png in the current directory."
    )
    subprocess.run(
        ["agy", "--add-dir", ".", "--dangerously-skip-permissions",
         "--print-timeout", "8m", "-p", prompt],
        cwd=OUT_DIR, check=False,
    )
    # agy 有时会把结果丢进自己的 scratch 目录
    local, scratch = OUT_DIR / f"{frame_id}.png", SCRATCH / f"{frame_id}.png"
    if not local.exists() and scratch.exists():
        local.write_bytes(scratch.read_bytes())
    print(f"{frame_id}: {'OK' if local.exists() else 'MISSING'}")


if __name__ == "__main__":
    only = sys.argv[1:]
    for fid, edits in STORYBOARD.items():
        if only and fid not in only:
            continue
        generate(fid, edits)
