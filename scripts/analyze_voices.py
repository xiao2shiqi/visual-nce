#!/usr/bin/env python3
"""声纹档案：按角色/逐段测基频 F0，判定说话人性别，供生图管线的
Master Specs 使用（CLAUDE.md §3 性别强锚的自动化实现）。

原理：课程 JSON 每句自带 speaker + startTime/endTime，无需说话人分离；
对每段音频测 F0 中位数（男 <155Hz，女 175–260Hz，儿童 >260Hz）。

关键处理：
- 排除 intro_* 段（报课名的播音员，与故事角色无关）；
- 叙述型课程（角色只有 Narrator）中，含引语的句子（'...' said/asked）
  混有其他角色的声音，判定叙述者性别时只用「纯叙述句」；
- 逐段分类后按角色聚合：多数票 + 中位数双重判定，分歧时标记 review。

用法：
    python3 scripts/analyze_voices.py nce1            # 整册
    python3 scripts/analyze_voices.py nce1 l141 l143  # 指定课
输出：src/data/voice-profiles/{book}.json + 终端摘要表
"""
import json
import pathlib
import re
import sys

import numpy as np
import parselmouth

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "src" / "data" / "voice-profiles"

QUOTE_RE = re.compile(r"['‘’“”].{3,}?['‘’“”]")


def classify(f0: float) -> str:
    if f0 < 155:
        return "male"
    if f0 < 175:
        return "ambiguous"
    if f0 < 260:
        return "female"
    return "child"


def seg_f0(snd, st: float, et: float):
    st, et = max(0.0, st), min(snd.get_total_duration(), et)
    if et - st < 0.3:
        return None
    part = snd.extract_part(from_time=st, to_time=et)
    pitch = part.to_pitch(time_step=0.01, pitch_floor=60, pitch_ceiling=450)
    f = pitch.selected_array["frequency"]
    f = f[f > 0]
    return float(np.median(f)) if len(f) >= 15 else None


def analyze_lesson(lesson_path: pathlib.Path) -> dict:
    data = json.loads(lesson_path.read_text())
    snd = parselmouth.Sound(str(ROOT / "public" / data["audio"].lstrip("/")))

    per_speaker: dict[str, dict] = {}
    for s in data["segments"]:
        if s["id"].startswith("intro") or s.get("startTime") is None:
            continue
        f0 = seg_f0(snd, s["startTime"], s["endTime"])
        if f0 is None:
            continue
        spk = s.get("speaker") or s.get("role") or "?"
        rec = per_speaker.setdefault(spk, {"f0s": [], "narration_f0s": []})
        rec["f0s"].append(f0)
        # 纯叙述句（不含引语）才能代表叙述者本人的声音
        if not QUOTE_RE.search(s["text"]):
            rec["narration_f0s"].append(f0)

    result = {}
    for spk, rec in per_speaker.items():
        # Narrator 用纯叙述句；对话角色用全部台词
        pool = rec["narration_f0s"] if spk == "Narrator" and len(rec["narration_f0s"]) >= 3 else rec["f0s"]
        if not pool:
            continue
        med = float(np.median(pool))
        votes = [classify(f) for f in pool]
        majority = max(set(votes), key=votes.count)
        by_median = classify(med)
        agree = majority == by_median and by_median != "ambiguous"
        result[spk] = {
            "gender": by_median if agree else f"REVIEW({by_median}/{majority})",
            "f0_median": round(med, 1),
            "segments": len(pool),
            "vote_ratio": round(votes.count(majority) / len(votes), 2),
        }
    return result


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: analyze_voices.py <book> [lN ...]")
    book = sys.argv[1]
    only = set(sys.argv[2:])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    profiles = {}
    lessons = sorted(
        (ROOT / "src/data/lessons").glob(f"{book}-l*.json"),
        key=lambda p: int(p.stem.split("-l")[1]),
    )
    for lp in lessons:
        ln = "l" + lp.stem.split("-l")[1]
        if only and ln not in only:
            continue
        try:
            res = analyze_lesson(lp)
        except Exception as e:
            print(f"{lp.stem}: ERROR {e}")
            continue
        profiles[lp.stem] = res
        summary = "  ".join(
            f"{spk}={v['gender']}({v['f0_median']}Hz)" for spk, v in res.items()
        )
        flag = " ⚠️" if any("REVIEW" in v["gender"] for v in res.values()) else ""
        print(f"{lp.stem:12s} {summary}{flag}")

    out = OUT_DIR / f"{book}.json"
    existing = json.loads(out.read_text()) if out.exists() else {}
    existing.update(profiles)
    out.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n")
    print(f"\nsaved -> {out.relative_to(ROOT)}  ({len(profiles)} lessons)")


if __name__ == "__main__":
    main()
