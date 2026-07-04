#!/usr/bin/env python3
"""L143 A Walk Through the Woods — 主角换人修正（女 → 男）。

背景（2026-07-04 声纹分析确认）：录音叙述者 10 段全部男声（F0 中位
120.5Hz，高置信），历史插图错画成女性。依据 voice-profiles/nce1.json。

策略：对 5 帧逐帧「换人编辑」——只替换主角，树林、垃圾场、构图
姿势全部保留。

额度重置后运行：
    python3 scripts/nce1/generate_l143_storyboard.py

收尾（全部帧合格后）：
1. PNG → WebP q82 覆盖同名旧图；scene1 重生成 thumb.webp（480px 宽）。
2. 逐帧 Read 验收（妈妈五帧同脸同衣；其余元素与原帧一致）。
3. JSON 映射不变（文件名沿用），校验引用 + commit。
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "public" / "images" / "nce1" / "l143"
SCRATCH = Path.home() / ".gemini" / "antigravity-cli" / "scratch"

NARRATOR = (
    "the NARRATOR: a man in his mid-40s, short neat dark hair with grey flecks, "
    "wearing an olive-green field jacket over a checked shirt, dark walking trousers "
    "and brown boots. CRITICAL: MALE. "
)

# 每帧要保留的姿势/表情来自原帧本身，编辑指令只描述"换人"
FRAMES = {
    "scene1": "walking along the same path in the same pose as the woman he replaces",
    "beautiful_woods": "standing in the same spot and pose, admiring the woods",
    "sad_walk": "standing still in the same spot, one hand raised to his mouth, shocked and saddened by the litter",
    "dumped_cars": "standing at the edge of the junk clearing in the same pose, dismayed, arms at his sides",
    "ironic_sign": "standing beside the blank sign in the same pose, looking at it with a wry, ironic half-smile",
}


def generate(frame_id: str, pose: str) -> bool:
    src = f"{frame_id}.webp"
    # scene1 先换人；其余帧把换好人的 scene1_new 一并传入作为妈妈的身份参考，
    # 防止五帧各自发明一张不同的妈妈脸
    if frame_id == "scene1":
        inputs = (
            f"Pass {src} (current directory) as an INPUT IMAGE to your image editing "
            "tool so the model sees the pixels."
        )
        identity = ""
    else:
        inputs = (
            f"Pass TWO files from the current directory to your image editing tool: "
            f"{src} as the BASE image to edit, and scene1_new.png as the IDENTITY "
            "REFERENCE for the man's exact face, hair and clothing."
        )
        identity = (
            "The man's face, hair and clothing must be IDENTICAL to the man in "
            "scene1_new.png. "
        )
    prompt = (
        f"CRITICAL: image EDITING task. {inputs} Output MUST keep the exact same "
        "wide landscape framing as the base input.\n\n"
        "Edit instruction: keep the painting exactly as it is — same bluebell woods, "
        "same trees and light, same litter/junk/sign elements exactly where they are, "
        "same watercolor style. Make ONLY ONE change: "
        f"REPLACE the woman (green parka) with {NARRATOR}He is {pose}. {identity}"
        "NO text or letters anywhere.\n\n"
        f"Save as {frame_id}_new.png in the current directory."
    )
    subprocess.run(
        ["agy", "--add-dir", ".", "--dangerously-skip-permissions",
         "--print-timeout", "8m", "-p", prompt],
        cwd=OUT_DIR, check=False,
    )
    local = OUT_DIR / f"{frame_id}_new.png"
    scratch = SCRATCH / f"{frame_id}_new.png"
    if not local.exists() and scratch.exists():
        local.write_bytes(scratch.read_bytes())
    # 防假文件：与输入图字节数相同 = 额度耗尽时的复制品
    src_size = (OUT_DIR / src).stat().st_size
    if local.exists() and local.stat().st_size == src_size:
        local.unlink()
        print(f"{frame_id}: FAKE (quota exhausted?), removed")
        return False
    print(f"{frame_id}: {'OK' if local.exists() else 'MISSING'}")
    return local.exists()


if __name__ == "__main__":
    only = sys.argv[1:]
    for fid, pose in FRAMES.items():
        if only and fid not in only:
            continue
        if (OUT_DIR / f"{fid}_new.png").exists():
            print(f"{fid}: exists, skip")
            continue
        if not generate(fid, pose):
            print("停止：疑似额度锁，稍后重跑本脚本续传")
            break
