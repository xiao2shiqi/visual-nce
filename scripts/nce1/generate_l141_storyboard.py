#!/usr/bin/env python3
"""L141 Sally's First Train Ride — 家长换人修正（爷爷 → 妈妈）。

背景（2026-07-04 领导确认）：课文录音的叙述者是女声，"I" 是 Sally 的
妈妈；历史图（包括本轮重绘）都错画成了老爷爷。按 CLAUDE.md §3
性别强锚规则，此类角色必须以录音音色为准。

策略：对已验收的 5 帧逐帧做「换人编辑」——只替换家长这一个人物，
车厢、Sally、蓝衣太太、构图姿势全部保留，比整课重画省一半额度。

额度重置后运行：
    python3 scripts/nce1/generate_l141_storyboard.py

收尾（全部帧合格后）：
1. PNG → WebP q82 覆盖同名旧图；scene1 重生成 thumb.webp（480px 宽）。
2. 逐帧 Read 验收（妈妈五帧同脸同衣；其余元素与原帧一致）。
3. JSON 映射不变（文件名沿用），校验引用 + commit。
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "public" / "images" / "nce1" / "l141"
SCRATCH = Path.home() / ".gemini" / "antigravity-cli" / "scratch"

MOTHER = (
    "Sally's MOTHER: a woman in her early 30s, shoulder-length wavy chestnut-brown "
    "hair, wearing a mustard-yellow cardigan over a cream blouse and a knee-length "
    "brown skirt, warm and gentle. CRITICAL: FEMALE, young mother, NOT elderly. "
)

# 每帧要保留的姿势/表情来自原帧本身，编辑指令只描述"换人"
FRAMES = {
    "scene1": "sitting calmly in the seat where the elderly man sat, hands folded, watching Sally fondly",
    "on_the_train": "sitting in the same seat, smiling as Sally kneels by the window asking questions",
    "lady_boards": "sitting in the same seat, glancing politely at the lady who has just sat down",
    "makeup_face": "sitting in the same seat, watching quietly while the lady powders her face",
    "still_ugly": "covering her face with one hand, deeply embarrassed, cheeks flushed",
}


def generate(frame_id: str, mother_pose: str) -> bool:
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
            "REFERENCE for the mother's exact face, hair and clothing."
        )
        identity = (
            "The mother's face, hair and clothing must be IDENTICAL to the woman in "
            "scene1_new.png. "
        )
    prompt = (
        f"CRITICAL: image EDITING task. {inputs} Output MUST keep the exact same "
        "wide landscape framing as the base input.\n\n"
        "Edit instruction: keep the painting exactly as it is — same vintage train "
        "compartment, same luggage rack with red suitcase, same window view, same "
        "little girl Sally (black pigtails, blue cardigan, yellow dress) in the same "
        "pose, and (if present) the same middle-aged lady in the BLUE coat and LARGE "
        "flowery hat in the same pose, same watercolor style. Make ONLY ONE change: "
        f"REPLACE the elderly gentleman with {MOTHER}She is {mother_pose}. {identity}"
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
