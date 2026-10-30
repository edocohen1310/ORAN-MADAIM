"""Lay every narrated segment on the film's clock and build the narration track.

Reads script/script.json and the per-segment TTS output (tools/tts.py), trims each
clip to its speech, places it after the previous one (gap / pause_after / chapter
lead-in and tail), mixes one continuous narration file and groups the words into
caption lines.

Writes:
  script/timeline.json        chapters, segments (global + chapter-local times), captions
  assets/audio/narration.mp3  the mixed voice track
"""
import json
import re
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
FPS = 30
NIQQUD = re.compile(r"[֑-ׇ]")
END_PUNCT = tuple(".,?!:;…״\"”)")


def q(t: float) -> float:
    """Round to the nearest frame so every cue lands on a frame boundary."""
    return round(round(t * FPS) / FPS, 4)


def load(path: Path) -> np.ndarray:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    )
    return np.frombuffer(raw, np.float32).copy()


def speech_bounds(x: np.ndarray) -> tuple[int, int]:
    win = int(0.01 * SR)
    n = len(x) // win
    env = np.abs(x[: n * win]).reshape(n, win).max(axis=1)
    loud = np.where(env > 0.012)[0]
    if len(loud) == 0:
        return 0, len(x)
    a = max(0, loud[0] * win - int(0.04 * SR))
    b = min(len(x), (loud[-1] + 1) * win + int(0.14 * SR))
    return a, b


def strip(s: str) -> str:
    return NIQQUD.sub("", s)


def tokens(s: str) -> list[str]:
    return [t for t in s.split() if re.search(r"[\w֐-׿0-9]", t)]


def time_words(display: list[str], spoken: list[dict]) -> list[dict]:
    """Give each displayed word a start/end, from the spoken word timings."""
    if len(display) == len(spoken):
        return [{"text": d, "start": w["start"], "end": w["end"]} for d, w in zip(display, spoken)]
    # Different wording (numbers written as digits, quotes): spread by character share.
    s0, s1 = spoken[0]["start"], spoken[-1]["end"]
    sp_chars = [len(w["text"]) + 1 for w in spoken]
    sp_cum = np.concatenate([[0], np.cumsum(sp_chars)]) / sum(sp_chars)
    sp_t = [w["start"] for w in spoken] + [s1]

    def at(frac: float) -> float:
        return float(np.interp(frac, sp_cum, sp_t))

    d_chars = [len(d) + 1 for d in display]
    d_cum = np.concatenate([[0], np.cumsum(d_chars)]) / sum(d_chars)
    return [
        {"text": d, "start": at(d_cum[i]), "end": at(d_cum[i + 1]) - 0.02}
        for i, d in enumerate(display)
    ]


def group_words(words: list[dict]) -> list[list[dict]]:
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        chars = sum(len(x["text"]) + 1 for x in cur)
        punct = w["text"].endswith(END_PUNCT)
        pause = nxt is not None and nxt["start"] - w["end"] > 0.22
        if nxt is None or len(cur) >= 6 or chars > 34 or ((punct or pause) and len(cur) >= 2):
            # avoid a dangling single word at the end of a sentence
            if nxt is not None and not punct and len(cur) >= 6 and len(words) - i - 1 == 1:
                continue
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def main() -> None:
    script = json.loads((ROOT / "script/script.json").read_text())
    gap_default = script.get("gap", 0.32)
    t = 0.0
    chapters, captions, placed = [], [], []
    for ch in script["chapters"]:
        c_start = q(t)
        t += ch.get("lead_in", 0.6)
        segs = []
        for s in ch["segments"]:
            meta = json.loads((ROOT / f"script/tts/{s['id']}.json").read_text())
            x = load(ROOT / f"assets/audio/seg/{s['id']}.mp3")
            a, b = speech_bounds(x)
            clip = x[a:b]
            start = q(t)
            off = a / SR
            dur = len(clip) / SR
            words_spoken = [
                {"text": w["text"], "start": start + w["start"] - off, "end": start + w["end"] - off}
                for w in meta["words"]
            ]
            display = s.get("sub") or strip(s["say"])
            dwords = time_words(tokens(display), words_spoken)
            seg = {
                "id": s["id"],
                "kind": s.get("kind", "line"),
                "n": s.get("n"),
                "text": display,
                "short": s.get("short"),
                "start": start,
                "end": q(start + dur),
                "local": q(start - c_start),
                "localEnd": q(start + dur - c_start),
                "words": [
                    {"t": q(w["start"] - c_start), "e": q(w["end"] - c_start), "w": w["text"]}
                    for w in dwords
                ],
            }
            segs.append(seg)
            placed.append((start, clip))
            if not s.get("nocap") and seg["kind"] != "lesson":
                for g in group_words(dwords):
                    captions.append(
                        {
                            "start": g[0]["start"] - 0.06,
                            "end": g[-1]["end"] + 0.12,
                            "text": " ".join(w["text"] for w in g),
                            "seg": s["id"],
                        }
                    )
            pause = s.get("pause_after")
            if pause is None:
                pause = 0.9 if seg["kind"] == "lesson" else gap_default
            t = start + dur + pause
        t += ch.get("tail", 1.0)
        chapters.append(
            {
                "id": ch["id"],
                "label": ch["label"],
                "start": c_start,
                "duration": q(t - c_start),
                "segments": segs,
            }
        )
    total = q(t)

    # Captions: one at a time; each holds until the next one starts when they are close.
    captions.sort(key=lambda c: c["start"])
    for i, c in enumerate(captions):
        nxt = captions[i + 1] if i + 1 < len(captions) else None
        end = c["end"] + 0.25
        if nxt and nxt["start"] - c["end"] < 0.6:
            end = nxt["start"]
        if nxt:
            end = min(end, nxt["start"])
        c["start"], c["end"] = q(max(c["start"], 0.1)), q(end)

    # Mix the narration.
    mix = np.zeros(int((total + 1) * SR), np.float32)
    for start, clip in placed:
        i = int(round(start * SR))
        mix[i : i + len(clip)] += clip
    peak = float(np.abs(mix).max())
    mix *= min(1.0, 0.89 / peak)  # about -1 dBFS peak
    pcm = (mix * 32767).astype(np.int16).tobytes()
    out = ROOT / "assets/audio/narration.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
         "-c:a", "libmp3lame", "-b:a", "128k", str(out)],
        input=pcm, check=True,
    )

    timeline = {"fps": FPS, "duration": total, "chapters": chapters, "captions": captions}
    (ROOT / "script/timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1))
    for ch in chapters:
        print(f"{ch['id']:8s} start {ch['start']:7.2f}  dur {ch['duration']:6.2f}")
    print(f"total {total:.2f}s = {total/60:.2f} min, {len(captions)} captions")


if __name__ == "__main__":
    main()
