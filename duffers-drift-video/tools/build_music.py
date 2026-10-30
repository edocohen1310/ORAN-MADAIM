"""Build the music bed: Kevin MacLeod tracks placed by script/music_cues.json, crossfaded,
levelled to one loudness and ducked under the narration. Writes assets/audio/music.mp3.

Tracks (CC BY 4.0, incompetech.com) live in assets/music/ as downloaded originals.
"""
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 44100
TRACKS = {
    "invest": ("Investigations.mp3", 0.0),
    "sneaky": ("Sneaky_Snitch.mp3", 0.0),
    "hidden": ("Hidden_Agenda.mp3", 0.0),
    "thinking": ("Thinking_Music.mp3", 0.0),
    "heroic": ("Heroic_Age.mp3", 55.0),
    "celtic": ("Achaidh_Cheide.mp3", 0.0),
}
FADE_IN, FADE_OUT = 0.9, 1.2
DUCK = 0.28  # music gain while the voice speaks


def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"])
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    # level each track to a common RMS over its louder half
    frame = SR // 2
    n = len(x) // frame
    rms = np.sqrt((x[: n * frame] ** 2).mean(axis=1).reshape(n, frame).mean(axis=1))
    ref = np.sqrt(np.mean(np.sort(rms)[n // 2 :] ** 2)) + 1e-9
    return x * (0.11 / ref)


def main():
    tl = json.loads((ROOT / "script/timeline.json").read_text())
    cues = json.loads((ROOT / "script/music_cues.json").read_text())
    total = tl["duration"]
    out = np.zeros((int((total + 2) * SR), 2), np.float32)
    cache, head = {}, {}
    cues.sort(key=lambda c: c["t0"])
    # merge back-to-back cues of the same track so the music does not restart
    merged = []
    for c in cues:
        if merged and merged[-1]["track"] == c["track"] and c["t0"] - merged[-1]["t1"] < 1.5:
            merged[-1]["t1"] = max(merged[-1]["t1"], c["t1"])
        else:
            merged.append(dict(c))
    for c in merged:
        name, start_at = TRACKS[c["track"]]
        if name not in cache:
            cache[name] = load(ROOT / "assets/music" / name)
        src = cache[name]
        pos = head.get(name, start_at)
        t0, t1 = max(0.0, c["t0"]), min(total + 1, c["t1"] + 0.6)
        n = int((t1 - t0) * SR)
        i = int(pos * SR) % len(src)
        idx = (np.arange(n) + i) % len(src)  # loop the track if the cue outlasts it
        seg = src[idx].copy()
        env = np.ones(n, np.float32)
        fi, fo = min(n, int(FADE_IN * SR)), min(n, int(FADE_OUT * SR))
        env[:fi] *= np.linspace(0, 1, fi)
        env[n - fo :] *= np.linspace(1, 0, fo)
        a = int(t0 * SR)
        out[a : a + n] += seg * env[:, None] * c.get("gain", 1.0)
        head[name] = pos + (t1 - t0)

    # duck under the narration
    gain = np.ones(len(out), np.float32)
    for ch in tl["chapters"]:
        for s in ch["segments"]:
            a, b = int((s["start"] - 0.15) * SR), int((s["end"] + 0.25) * SR)
            gain[max(0, a) : b] = DUCK
    k = int(0.25 * SR)
    kernel = np.ones(k, np.float32) / k
    gain = np.convolve(gain, kernel, mode="same")
    out *= gain[:, None]
    # end: fade the last 2.5 s
    e = int(total * SR)
    f = int(2.5 * SR)
    out[e - f : e] *= np.linspace(1, 0, f)[:, None]
    out[e:] = 0
    out = out[: int(total * SR)]
    peak = np.abs(out).max()
    if peak > 0.89:
        out *= 0.89 / peak
    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "libmp3lame", "-b:a", "128k", str(ROOT / "assets/audio/music.mp3")],
        input=pcm, check=True,
    )
    print(f"music: {len(merged)} cues over {total:.1f}s, peak {peak:.2f}")


if __name__ == "__main__":
    main()
