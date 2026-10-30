"""Build the HyperFrames project from script/timeline.json.

Writes compositions/<chapter>.html for every chapter, compositions/captions.html,
index.html (scene hosts + narration, music and sound-effect tracks) and
script/music_cues.json (read by build_music.py).

Usage: python tools/gen.py [chapter-id ...]   (default: every chapter)
"""
import json
import sys
from pathlib import Path

import kit
import scenes_a
import scenes_b
import scenes_c

ROOT = Path(__file__).resolve().parent.parent
TL = json.loads((ROOT / "script/timeline.json").read_text())

BUILDERS = {
    "intro": scenes_a.intro,
    "about": scenes_a.about,
    "terrain": scenes_a.terrain,
    "dream1": scenes_b.dream1,
    "dream2": scenes_b.dream2,
    "dream3": scenes_b.dream3,
    "dream4": scenes_b.dream4,
    "dream5": scenes_c.dream5,
    "dream6": scenes_c.dream6,
    "recap": scenes_c.recap,
}

# sound name -> (file in assets/sfx, gain multiplier)
SFX = {
    "whoosh": ("whoosh-deep.mp3", 1.0),
    "swoosh": ("whoosh-deep.mp3", 0.8),
    "stamp": ("thud.mp3", 1.0),
    "thud": ("thud.mp3", 0.5),
    "page": ("page-turn.mp3", 1.0),
    "cricket": ("cricket.mp3", 1.0),
    "wind": ("wind.mp3", 1.0),
    "rifles": ("rifles.mp3", 0.8),
    "rifle": ("rifle-shot.mp3", 0.9),
    "boom": ("boom.mp3", 0.9),
    "cannon": ("cannon.mp3", 1.0),
    "chisel": ("chisel.mp3", 0.9),
    "whistle": ("whistle.mp3", 0.9),
    "cheer": ("cheer.mp3", 0.9),
    "fire": ("campfire.mp3", 1.0),
    "dust": ("dust-hit.mp3", 1.0),
}
LOOPS = {"cricket.mp3", "campfire.mp3", "rifles.mp3", "wind.mp3", "chisel.mp3"}


_LEN = {}


def file_len(path):
    if path not in _LEN:
        import subprocess

        out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
        _LEN[path] = float(out.strip())
    return _LEN[path]


def build_captions(total):
    caps = TL["captions"]
    items, lines = [], []
    for i, c in enumerate(caps):
        d = round(c["end"] - c["start"], 3)
        if d <= 0.05:
            continue
        items.append(
            f'<div id="cap{i}" class="clip cap" data-start="{c["start"]:.3f}" data-duration="{d:.3f}" data-track-index="1">'
            f'<span id="cap{i}-t" class="cap-t">{c["text"]}</span></div>'
        )
        lines.append(f'tl.fromTo("#cap{i}-t", {{opacity:0}}, {{opacity:1, duration:0.12, ease:"power2.out"}}, {c["start"]:.3f});')
    body = "\n".join(items)
    js = "\n      ".join(lines)
    return f"""<template>
  <style>
{kit.FONTS_CSS}
#root {{ position:absolute; inset:0; pointer-events:none; }}
.cap {{ position:absolute; left:0; right:0; bottom:58px; height:96px; display:flex; align-items:center; justify-content:center; direction:rtl; }}
.cap-t {{ font-family:'Rubik'; font-weight:700; font-size:48px; line-height:1.1; color:#FFF8EC; background:rgba(22,16,10,.78);
  padding:12px 30px 16px; border-radius:16px; white-space:nowrap; box-shadow:0 6px 18px rgba(0,0,0,.25); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-duration="{total:.3f}">
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      {js}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""


def main(only):
    total = TL["duration"]
    comps_dir = ROOT / "compositions"
    comps_dir.mkdir(exist_ok=True)
    all_sfx, all_music = [], []
    HOLD = 1.2  # each chapter's last frame stays under the next chapter's entrance
    last_id = TL["chapters"][-1]["id"]
    for ch in TL["chapters"]:
        c = kit.Comp(ch, ch["start"])
        c.extra = 0.0 if ch["id"] == last_id else HOLD
        BUILDERS[ch["id"]](c)
        all_sfx += c.sfx_cues
        all_music += c.music_cues
        if not only or ch["id"] in only:
            (comps_dir / f"{ch['id']}.html").write_text(c.render())
            print(f"  {ch['id']}: {len(c.html)} layers, {len(c.lines)} tweens, {len(c.sfx_cues)} sfx")
    (comps_dir / "captions.html").write_text(build_captions(total))
    (ROOT / "script/music_cues.json").write_text(json.dumps(all_music, ensure_ascii=False, indent=1))

    hosts = []
    for k, ch in enumerate(TL["chapters"]):
        hosts.append(
            f'      <div id="{ch["id"]}" data-composition-id="{ch["id"]}" data-composition-src="compositions/{ch["id"]}.html" '
            f'data-start="{ch["start"]:.3f}" data-duration="{ch["duration"] + (0 if k == len(TL["chapters"]) - 1 else 1.2):.3f}" data-track-index="1" data-track-kind="graphics" '
            f'data-width="1920" data-height="1080" style="z-index:{k + 1}"></div>'
        )
    hosts.append(
        f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
        f'data-duration="{total:.3f}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:50"></div>'
    )
    audio = [
        f'      <audio id="narration" class="clip" src="assets/audio/narration.mp3" data-start="0" data-duration="{total:.3f}" data-track-index="10" data-volume="1"></audio>',
        f'      <audio id="music" class="clip" src="assets/audio/music.mp3" data-start="0" data-duration="{total:.3f}" data-track-index="11" data-volume="1"></audio>',
    ]
    n = 0
    used = set()
    track_free = []  # end time per sfx track
    for cue in sorted(all_sfx, key=lambda x: x["t"]):
        if cue["name"] not in SFX or cue["vol"] <= 0:
            continue
        fn, gain = SFX[cue["name"]]
        path = ROOT / "assets/sfx" / fn
        if not path.exists():
            continue
        used.add(fn)
        n += 1
        start = max(0.0, cue["t"])
        flen = file_len(path)
        loop = bool(fn in LOOPS and cue.get("dur"))
        d = cue["dur"] if loop else (min(cue["dur"], flen - 0.06) if cue.get("dur") else flen - 0.06)
        d = min(d, total - start)
        tr = next((i for i, e in enumerate(track_free) if e <= start), None)
        if tr is None:
            track_free.append(0)
            tr = len(track_free) - 1
        track_free[tr] = start + d + 0.05
        fo = f' data-fade-out="{cue["fade_out"]:.2f}"' if cue.get("fade_out") else ""
        audio.append(
            f'      <audio id="sfx{n}" class="clip" src="assets/sfx/{fn}" data-start="{start:.3f}" data-duration="{d:.3f}" '
            f'data-track-index="{20 + tr}" data-volume="{cue["vol"] * gain:.3f}"{fo}{" loop" if loop else ""}></audio>'
        )
    html = f"""<!doctype html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>הגנת מעברות פתיים</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #140f0a; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="1920" data-height="1080" data-fps="30">
{chr(10).join(hosts)}
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    print(f"index.html: {len(TL['chapters'])} scenes, {n} sound cues ({len(used)} files), total {total:.1f}s")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main(sys.argv[1:])
