"""Synthesise the sound effects no free library could supply here (deterministic, seeded).

rifle-shot.mp3  one distant rifle shot with its echo across open ground
rifles.mp3      a ragged volley / exchange of fire (12 s, loopable bed)
chisel.mp3      chisel taps on stone (lesson tablets)
campfire.mp3    a crackling fire (10 s)
whistle.mp3     a pea whistle blast (only written if no recorded whistle exists)
"""
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/sfx"
SR = 48000
rng = np.random.default_rng(1902)


def lowpass(x, fc):
    n = 255
    t = np.arange(n) - (n - 1) / 2
    h = np.sinc(2 * fc / SR * t) * np.hamming(n)
    h /= h.sum()
    return np.convolve(x, h, mode="same")


def highpass(x, fc):
    return x - lowpass(x, fc)


def env(n, tau, attack=0.0005):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1) if attack > 0 else 1
    return a * np.exp(-t / tau)


def shot(dist=1.0):
    """One rifle shot; dist 1 = near, 3 = far (duller and quieter)."""
    n = int(1.6 * SR)
    noise = rng.standard_normal(n)
    crack = highpass(noise, 1800) * env(n, 0.004) * 1.4
    body = lowpass(noise, 2600 / dist) * env(n, 0.03 * dist) * 1.0
    tail = lowpass(rng.standard_normal(n), 700 / dist) * env(n, 0.35 + 0.15 * dist, 0.02) * 0.22
    boom = np.sin(2 * np.pi * np.cumsum(np.linspace(120, 50, n)) / SR) * env(n, 0.05) * 0.35
    x = (crack / dist + body + tail + boom) / dist
    # a second, late echo off the hills
    d = int(0.42 * SR * dist)
    echo = np.zeros(n)
    echo[d:] = lowpass(x, 900)[: n - d] * 0.28
    return x + echo


def place(buf, x, at):
    i = int(at * SR)
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]


def write(name, x, peak=0.9):
    x = x / (np.abs(x).max() + 1e-9) * peak
    fade = int(0.03 * SR)
    x[-fade:] *= np.linspace(1, 0, fade)
    pcm = (x * 32767).astype(np.int16).tobytes()
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "libmp3lame", "-b:a", "160k", str(OUT / name)],
        input=pcm, check=True,
    )
    print("wrote", name, f"{len(x) / SR:.1f}s")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    write("rifle-shot.mp3", shot(1.2))

    dur = 12.0
    bed = np.zeros(int((dur + 1.6) * SR))
    t = 0.05
    while t < dur:
        place(bed, shot(1.3 + rng.random() * 1.8) * (0.5 + rng.random() * 0.6), t)
        t += rng.exponential(0.16)
    # loop seam: fold the tail back onto the head
    tail = bed[int(dur * SR):]
    bed = bed[: int(dur * SR)]
    bed[: len(tail)] += tail
    write("rifles.mp3", bed, 0.85)

    n = int(6.0 * SR)
    ch = np.zeros(n)
    t = 0.05
    while t < 5.8:
        k = int(0.06 * SR)
        tap = highpass(rng.standard_normal(k), 2500) * env(k, 0.006)
        ring = np.sin(2 * np.pi * (3100 + rng.random() * 600) * np.arange(k) / SR) * env(k, 0.012) * 0.6
        place(ch, (tap + ring) * (0.6 + 0.4 * rng.random()), t)
        t += 0.17 + rng.random() * 0.12
    scrape = highpass(rng.standard_normal(n), 4000) * 0.02
    write("chisel.mp3", ch + scrape, 0.7)

    n = int(10.0 * SR)
    fire = lowpass(rng.standard_normal(n), 400) * 0.25
    t = 0.0
    while t < 9.9:
        k = int(0.02 * SR)
        place(fire, highpass(rng.standard_normal(k), 1500) * env(k, 0.003) * (0.3 + rng.random()), t)
        t += rng.exponential(0.11)
    write("campfire.mp3", fire, 0.6)

    if not (OUT / "whistle.mp3").exists():
        n = int(1.1 * SR)
        tt = np.arange(n) / SR
        trem = 0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 38 * tt))
        tone = np.sin(2 * np.pi * 2950 * tt) + 0.4 * np.sin(2 * np.pi * 5900 * tt)
        a = np.clip(tt / 0.02, 0, 1) * np.clip((1.1 - tt) / 0.08, 0, 1)
        write("whistle.mp3", tone * trem * a + highpass(rng.standard_normal(n), 3000) * 0.05 * a, 0.6)


if __name__ == "__main__":
    main()
