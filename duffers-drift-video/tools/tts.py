"""Generate Hebrew narration for every script segment with edge-tts.

Writes one MP3 per segment to assets/audio/seg/<id>.mp3 and its word timings to
script/tts/<id>.json. A segment is regenerated only when its text, voice or rate
changes (hash stored next to the timings).

Usage: python tools/tts.py [segment-id ...]
"""
import asyncio
import hashlib
import json
import ssl
import subprocess
import sys
from pathlib import Path

import edge_tts
import edge_tts.communicate as comm

# The session's HTTPS proxy re-signs TLS; edge-tts pins certifi's bundle, so point it
# at the proxy CA bundle instead (verification stays on).
CA = Path("/root/.ccr/ca-bundle.crt")
if CA.exists():
    comm._SSL_CTX = ssl.create_default_context(cafile=str(CA))

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = json.loads((ROOT / "script/script.json").read_text())
SEG_DIR = ROOT / "assets/audio/seg"
TTS_DIR = ROOT / "script/tts"
SEG_DIR.mkdir(parents=True, exist_ok=True)
TTS_DIR.mkdir(parents=True, exist_ok=True)


def duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    )
    return float(out.strip())


async def synth(seg: dict, voice: str, rate: str) -> None:
    key = hashlib.sha1(f"{voice}|{rate}|{seg['say']}".encode()).hexdigest()
    meta_path = TTS_DIR / f"{seg['id']}.json"
    mp3 = SEG_DIR / f"{seg['id']}.mp3"
    if meta_path.exists() and mp3.exists():
        if json.loads(meta_path.read_text()).get("hash") == key:
            return
    for attempt in range(4):
        try:
            c = edge_tts.Communicate(seg["say"], voice, rate=rate, boundary="WordBoundary")
            words = []
            with open(mp3, "wb") as f:
                async for ch in c.stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        words.append(
                            {
                                "text": ch["text"],
                                "start": round(ch["offset"] / 1e7, 3),
                                "end": round((ch["offset"] + ch["duration"]) / 1e7, 3),
                            }
                        )
            break
        except Exception as exc:  # network hiccup: retry with backoff
            if attempt == 3:
                raise
            print(f"  retry {seg['id']}: {exc}")
            await asyncio.sleep(2 ** (attempt + 1))
    meta = {"id": seg["id"], "hash": key, "duration": round(duration(mp3), 3), "words": words}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"  {seg['id']}: {meta['duration']:.2f}s, {len(words)} words")


async def main(only: list[str]) -> None:
    voice, rate = SCRIPT["voice"], SCRIPT["rate"]
    segs = [s for ch in SCRIPT["chapters"] for s in ch["segments"]]
    if only:
        segs = [s for s in segs if s["id"] in only]
    sem = asyncio.Semaphore(4)

    async def run(s):
        async with sem:
            await synth(s, voice, rate)

    await asyncio.gather(*(run(s) for s in segs))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
