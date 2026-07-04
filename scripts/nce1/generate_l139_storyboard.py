#!/usr/bin/env python3
"""L139 Is That You, John? — 整课重画（电话乌龙，双场景分屏）。

状态（2026-07-04）：scene1_new.png 已生成合格；其余 4 帧被 agy 额度锁
（约 4.5h）挡住，额度重置后运行本脚本补齐：

    python3 scripts/nce1/generate_l139_storyboard.py

全部帧合格后的收尾（手动或让 agent 做）：
1. PNG → WebP q82；scene1_new → scene1.webp（覆盖旧图）；重生成 thumb.webp
   （480px 宽缩略图，参照 scripts/compress_images.py 的 make_thumb）。
2. 删除旧故事图：phone_confusion / john_arrives / realisation /
   laughing_together（现有图画的是另一个故事，全部作废）。
3. 更新 src/data/lessons/nce1-l139.json 映射：
   s1-s2 scene1；s3 graham_message；s4 john_confused；
   s5-s10 graham_message；s11 john_confused；
   s12-s14 identity_check；s15-s18 punchline。
4. 校验引用完整 + 逐帧 Read 验收 + commit。
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "public" / "images" / "nce1" / "l139"
SCRATCH = Path.home() / ".gemini" / "antigravity-cli" / "scratch"
ANCHOR = "scene1_new.png"

KEEP = (
    "keep the painting exactly as it is — same split-screen telephone call: LEFT the "
    "1970s office at dusk with Graham (late 30s, dark hair, brown suit, loosened tie, "
    "black rotary phone), RIGHT the outdoor telephone pole with John (late 20s, tousled "
    "sandy hair, navy overalls, tool belt, test handset, junction box with colorful "
    "wires), same wavy divider, same connecting wire, same style. "
)

STORYBOARD = {
    "graham_message": (
        "1) LEFT: Graham leans back slightly, talking cheerfully and confidently into "
        "the handset, one hand gesturing as if giving instructions. 2) RIGHT: John "
        "listens politely with a mildly puzzled expression, eyebrows slightly raised."
    ),
    "john_confused": (
        "1) RIGHT: John scratches his head with his free hand, face deeply puzzled, "
        "mouth slightly open in confusion. 2) LEFT: Graham keeps talking, eyes closed "
        "contentedly, unaware of the confusion."
    ),
    "identity_check": (
        "1) Both men now frown with suspicion: LEFT Graham grips the handset tighter "
        "and leans forward over the desk, questioning carefully. 2) RIGHT: John frowns "
        "back, pressing the handset closer, cautious and serious."
    ),
    "punchline": (
        "1) RIGHT: John bursts out laughing, head tilted back, his free hand pointing "
        "at the open junction box with its colorful wires. 2) LEFT: Graham's jaw drops, "
        "eyes wide in embarrassed astonishment, a paper slipping from the desk."
    ),
}


def generate(frame_id: str, edits: str) -> bool:
    prompt = (
        f"CRITICAL: image EDITING task. Pass {ANCHOR} (current directory) as an INPUT "
        "IMAGE to your image editing tool so the model sees the pixels. Output MUST "
        "keep the exact same wide landscape framing and split-screen composition as "
        f"the input.\n\nEdit instruction: {KEEP}Make ONLY these changes: {edits} "
        "NO text or letters anywhere.\n\n"
        f"Save as {frame_id}.png in the current directory."
    )
    subprocess.run(
        ["agy", "--add-dir", ".", "--dangerously-skip-permissions",
         "--print-timeout", "8m", "-p", prompt],
        cwd=OUT_DIR, check=False,
    )
    local, scratch = OUT_DIR / f"{frame_id}.png", SCRATCH / f"{frame_id}.png"
    if not local.exists() and scratch.exists():
        local.write_bytes(scratch.read_bytes())
    # 防假文件：额度耗尽时 agy 会把输入图复制成输出名
    anchor_size = (OUT_DIR / ANCHOR).stat().st_size
    if local.exists() and local.stat().st_size == anchor_size:
        local.unlink()
        print(f"{frame_id}: FAKE (quota exhausted?), removed")
        return False
    print(f"{frame_id}: {'OK' if local.exists() else 'MISSING'}")
    return local.exists()


if __name__ == "__main__":
    only = sys.argv[1:]
    for fid, edits in STORYBOARD.items():
        if only and fid not in only:
            continue
        if (OUT_DIR / f"{fid}.png").exists():
            print(f"{fid}: exists, skip")
            continue
        if not generate(fid, edits):
            print("停止：疑似额度锁，稍后重跑本脚本续传")
            break
