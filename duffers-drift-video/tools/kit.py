"""Drawing kit and timeline helpers shared by every scene of the film.

Two worlds are drawn here:
  * the sand table (top-down): tokens, trenches, fire lines, map pins
  * the shadow theatre (side view): skies, hills, silhouettes of people and things
Everything is plain SVG/HTML strings; the GSAP calls are written as JS text.
"""
import json
import math
from pathlib import Path

import geo

ROOT = Path(__file__).resolve().parent.parent
FONTS_CSS = (ROOT / "assets/fonts/fonts.css").read_text()

# ---------------------------------------------------------------- palette
INK = "#1E1812"
PAPER = "#F4E9D2"
SAND = "#D8B47A"
NAVY = "#203A5E"
NAVY_HI = "#5576A3"
RUST = "#B3452A"
RUST_HI = "#E07A52"
FIRE = "#F6B33C"
RED = "#B3261E"
GREEN = "#1F7A45"
SLATE_INK = "#E9E1CF"
ACCENT = "#E3A33B"

SKIES = {
    "day": ("#8FBCD2", "#F1DDAE", "#B98B5A", "#3A2A1C"),
    "gold": ("#E9A957", "#F8DFA2", "#B9784A", "#33210F"),
    "dusk": ("#5B3B66", "#F0A26A", "#6F4157", "#22141E"),
    "night": ("#0B1029", "#2B3561", "#1A2044", "#070914"),
    "dawn": ("#4E4C78", "#F2A57C", "#5A4A6E", "#1C1524"),
    "dream": ("#1A1F45", "#4A3D72", "#2A2552", "#0E1028"),
}


def js(v):
    return json.dumps(v, ensure_ascii=False)


# ---------------------------------------------------------------- composition builder
class Comp:
    """Collects markup, GSAP lines, sound cues and music cues for one chapter."""

    def __init__(self, chapter, film_start):
        self.ch = chapter
        self.id = chapter["id"]
        self.dur = chapter["duration"]
        self.start = chapter["start"]
        self.segs = {s["id"]: s for s in chapter["segments"]}
        self.html = []
        self.lines = []
        self.css = []
        self.sfx_cues = []
        self.music_cues = []
        self._z = 1
        self._n = 0
        self.shots = []
        self.extra = 0.0  # seconds this chapter stays on screen under the next one

    # time lookups (chapter-local seconds)
    def t(self, sid, frac=0.0):
        s = self.segs[sid]
        return round(s["local"] + (s["localEnd"] - s["local"]) * frac, 3)

    def end(self, sid):
        return self.segs[sid]["localEnd"]

    def w(self, sid, sub, nth=0, at="t"):
        """Local time of the nth spoken/displayed word containing `sub`."""
        hits = [w for w in self.segs[sid]["words"] if sub in w["w"]]
        if not hits:
            raise KeyError(f"{sid}: no word with {sub!r}: {[w['w'] for w in self.segs[sid]['words']]}")
        return hits[min(nth, len(hits) - 1)][at]

    def uid(self, p="e"):
        self._n += 1
        return f"{self.id}-{p}{self._n}"

    # markup
    def add(self, html):
        self.html.append(html)

    def style(self, css):
        self.css.append(css)

    def shot(self, sid, t0, t1, inner, bg=None, fade=0.45, cls="", fade_in="fade"):
        """A timed full-frame layer. Its inner wrapper is what animates."""
        z = self._z
        self._z += 1
        bg_css = f"background:{bg};" if bg else ""
        self.shots.append((sid, t0, t1))
        self.html.append(
            f'<div id="{sid}" class="clip shot {cls}" data-start="{t0:.3f}" data-duration="@@DUR:{sid}@@" '
            f'data-track-index="{z}" style="z-index:{z};{bg_css}"><div id="{sid}-in" class="shot-in">{inner}</div></div>'
        )
        if fade_in == "fade" and fade > 0:
            self.fromTo(f"#{sid}-in", {"opacity": 0}, {"opacity": 1, "duration": fade, "ease": "power2.out"}, t0)
        elif fade_in == "blur":
            self.fromTo(f"#{sid}-in", {"opacity": 0, "filter": "blur(14px)"}, {"opacity": 1, "filter": "blur(0px)", "duration": 0.5, "ease": "power3.out"}, t0)
        elif fade_in == "iris":
            self.fromTo(f"#{sid}-in", {"clipPath": "circle(0% at 50% 50%)"}, {"clipPath": "circle(75% at 50% 50%)", "duration": 0.9, "ease": "power2.inOut"}, t0)
        elif fade_in == "wipe":
            self.fromTo(f"#{sid}-in", {"clipPath": "inset(0 0 0 100%)"}, {"clipPath": "inset(0 0 0 0%)", "duration": 0.7, "ease": "power3.inOut"}, t0)
        return sid

    # tweens
    def fromTo(self, sel, a, b, t):
        # a hidden start must name its visible end too (cold-seek safety)
        if "opacity" in a and "opacity" not in b:
            b = dict(b, opacity=1)
        self.lines.append(("fromTo", sel, dict(a), dict(b), float(t)))

    def to(self, sel, b, t):
        self.lines.append(("to", sel, None, dict(b), float(t)))

    def set(self, sel, b, t):
        self.lines.append(("set", sel, None, dict(b), float(t)))

    def raw(self, line):
        self.lines.append(("raw", line, None, None, 0.0))

    def js_lines(self):
        first = {}
        for kind, sel, a, b, t in self.lines:
            if kind == "fromTo":
                first[sel] = min(first.get(sel, 1e9), t)
        out = []
        for kind, sel, a, b, t in self.lines:
            if kind == "raw":
                out.append(sel)
            elif kind == "fromTo":
                if t > first[sel] + 1e-6:
                    b = dict(b, immediateRender=False)
                out.append(f"tl.fromTo({js(sel)}, {js(a)}, {js(b)}, {t:.3f});")
            else:
                out.append(f"tl.{kind}({js(sel)}, {js(b)}, {t:.3f});")
        return out

    # common moves
    def pop(self, sel, t, dur=0.45, origin="50% 100%", ease="back.out(1.7)", s0=0.0):
        self.fromTo(sel, {"scale": s0, "opacity": 0, "transformOrigin": origin}, {"scale": 1, "opacity": 1, "duration": dur, "ease": ease}, t)

    def fade(self, sel, t, dur=0.4, to=1.0, frm=0.0):
        self.fromTo(sel, {"opacity": frm}, {"opacity": to, "duration": dur, "ease": "power2.out"}, t)

    def out(self, sel, t, dur=0.3):
        self.to(sel, {"opacity": 0, "duration": dur, "ease": "power2.in"}, t)

    def blur_in(self, sel, t, dur=0.25):
        self.fromTo(sel, {"opacity": 0, "filter": "blur(8px)"}, {"opacity": 1, "filter": "blur(0px)", "duration": dur, "ease": "power3.out"}, t)

    def words_in(self, sel, t, dur=0.18, stagger=0.08):
        self.raw(
            f"tl.fromTo({js(sel)}, {{opacity:0, filter:'blur(6px)'}}, {{opacity:1, filter:'blur(0px)', duration:{dur}, stagger:{stagger}, ease:'power3.out'}}, {t:.3f});"
        )

    def draw(self, sel, t, dur=1.0, ease="power2.inOut"):
        """Stroke draw-on for paths that carry pathLength=100."""
        self.fromTo(sel, {"strokeDasharray": "100 120", "strokeDashoffset": 110}, {"strokeDashoffset": 0, "duration": dur, "ease": ease}, t)

    def cam(self, sel, t, px, py, z, dur=1.6, ease="power2.inOut", first=False):
        """Frame map point (px, py) at zoom z on a 1920x1080 stage, never showing past the map's edge."""
        z = max(1.0, z)
        x = min(0.0, max(1920 - 1920 * z, 960 - z * px))
        y = min(0.0, max(1080 - 1080 * z, 540 - z * py))
        vals = {"x": x, "y": y, "scale": z, "transformOrigin": "0 0"}
        if first:
            self.set(sel, vals, t)
        else:
            vals.update({"duration": dur, "ease": ease})
            self.to(sel, vals, t)

    def shake(self, sel, t, amp=10, n=6, step=0.045):
        g = geo.rng(int(t * 1000) + 7)
        for k in range(n):
            a = amp * (1 - k / n)
            self.set(sel, {"x": round((next(g) - 0.5) * 2 * a, 1), "y": round((next(g) - 0.5) * 2 * a, 1)}, round(t + k * step, 3))
        self.set(sel, {"x": 0, "y": 0}, round(t + n * step, 3))

    def flicker(self, sel, t0, t1, rate=0.09, seed=1, lo=0.0, hi=1.0, p=0.45):
        """Deterministic on/off flashes (muzzle flashes, fire)."""
        g = geo.rng(seed)
        t = t0
        while t < t1:
            self.set(sel, {"opacity": hi if next(g) < p else lo}, round(t, 3))
            t += rate * (0.6 + next(g) * 0.8)
        self.set(sel, {"opacity": 0}, round(t1, 3))

    # sound
    def sfx(self, name, t, vol=0.4, dur=None, fade_out=0.0):
        self.sfx_cues.append({"name": name, "t": round(self.start + t, 3), "vol": vol, "dur": dur, "fade_out": fade_out})

    def music(self, track, t0, t1, gain=1.0):
        self.music_cues.append({"track": track, "t0": round(self.start + t0, 3), "t1": round(self.start + t1, 3), "gain": gain})

    # output
    def resolve_durations(self, body):
        """Each shot stays on screen under the shot that replaces it until that shot has
        finished entering, so transitions dissolve instead of dipping to black."""
        end_all = self.dur + self.extra
        for sid, t0, t1 in self.shots:
            nxt = any(abs(o0 - t1) < 0.08 and osid != sid for osid, o0, _ in self.shots)
            end = t1 + 1.0 if nxt else t1
            if t1 >= self.dur - 0.05:
                end = end_all
            end = min(end, end_all)
            body = body.replace(f"@@DUR:{sid}@@", f"{end - t0:.3f}")
        return body

    def render(self):
        body = self.resolve_durations("\n".join(self.html))
        css = "\n".join(self.css)
        lines = "\n".join("      " + l for l in self.js_lines())
        return f"""<template>
  <style>
{FONTS_CSS}
#root {{ position:absolute; inset:0; overflow:hidden; direction:rtl; }}
{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{self.id}" data-width="1920" data-height="1080" data-duration="{self.dur + self.extra:.3f}">
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{lines}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["{self.id}"] = tl;
    }})();
  </script>
</template>
"""


BASE_CSS = """
.shot { position:absolute; inset:0; overflow:hidden; }
.shot-in { position:absolute; inset:0; }
.abs { position:absolute; }
.full { position:absolute; left:0; top:0; width:1920px; height:1080px; }
.sky { position:absolute; inset:0; }
svg.stage { position:absolute; left:0; top:0; width:1920px; height:1080px; overflow:visible; }
.cam { position:absolute; left:0; top:0; width:1920px; height:1080px; }
.cam > img.map { position:absolute; left:0; top:0; width:1920px; height:1080px; }
.k-title { font-family:'Karantina'; font-weight:700; color:#F4E7CB; line-height:0.95; letter-spacing:0.5px; }
.label { font-family:'Rubik'; font-weight:700; }
.bubble { position:absolute; font-family:'Rubik'; font-weight:700; font-size:40px; line-height:1.2; color:#1E1812;
  background:#FFF6E2; border:4px solid #1E1812; border-radius:28px; padding:16px 30px; white-space:nowrap; box-shadow:6px 8px 0 rgba(0,0,0,.28); }
.bubble.tail-r::after, .bubble.tail-l::after { content:''; position:absolute; bottom:-26px; width:34px; height:30px; background:#FFF6E2;
  border-right:4px solid #1E1812; border-bottom:4px solid #1E1812; }
.bubble.tail-r::after { right:58px; transform:skewX(35deg) rotate(8deg); }
.bubble.tail-l::after { left:58px; transform:skewX(-35deg) rotate(-8deg); }
.tag { position:absolute; font-family:'Rubik'; font-weight:700; font-size:32px; color:#1E1812; background:#F6ECD6;
  border:3px solid #1E1812; border-radius:10px; padding:6px 18px 8px; white-space:nowrap; box-shadow:4px 5px 0 rgba(30,24,18,.35); }
.tag.dark { background:#1E1812; color:#F6ECD6; border-color:#F6ECD6; }
.tag.red { background:#B3261E; color:#FFF3E6; border-color:#5d120e; }
.tag.navy { background:#203A5E; color:#F3ECDD; border-color:#0e1a2c; }
.tag.rust { background:#B3452A; color:#FFF0E2; border-color:#5b1f10; }
.stamp { position:absolute; width:760px; height:300px; }
.pin { position:absolute; width:0; height:0; }
.pin-post { position:absolute; left:-2px; top:-62px; width:5px; height:64px; background:#4a3520; border-radius:2px; }
.pin-post::after { content:''; position:absolute; left:-5px; top:58px; width:15px; height:7px; border-radius:50%; background:rgba(0,0,0,.3); }
.pin .tag { right:0; top:0; }
"""


# ---------------------------------------------------------------- side-view world
def sky(kind, extra=""):
    top, bottom, _, _ = SKIES[kind]
    return f'<div class="sky" style="background:linear-gradient(180deg,{top} 0%,{bottom} 78%);{extra}"></div>'


def stars(n=90, seed=3, ymax=640):
    g = geo.rng(seed)
    out = []
    for _ in range(n):
        x, y, r = next(g) * 1920, next(g) * ymax, 0.8 + next(g) * 1.8
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#FFF7DE" opacity="{0.35 + next(g) * 0.6:.2f}"/>')
    return "".join(out)


def moon(x, y, r=46):
    return (
        f'<circle cx="{x}" cy="{y}" r="{r * 2.2}" fill="#FFF5D6" opacity="0.08"/>'
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F7EBC8"/><circle cx="{x + r * 0.35}" cy="{y - r * 0.15}" r="{r * 0.9}" fill="#0B1029" opacity="0.0"/>'
        f'<circle cx="{x - r * 0.3}" cy="{y - r * 0.2}" r="{r * 0.16}" fill="#E5D5AC"/><circle cx="{x + r * 0.25}" cy="{y + r * 0.3}" r="{r * 0.11}" fill="#E5D5AC"/>'
    )


def sun(x, y, r=70, color="#FFF0C2"):
    return f'<circle cx="{x}" cy="{y}" r="{r * 1.9}" fill="{color}" opacity="0.18"/><circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def far_hills(kind, y=650, seed=2):
    """Flat-topped mesa (the Hill of Regrets) and soft far ridges."""
    _, _, far, _ = SKIES[kind]
    return (
        f'<path d="M -20 {y} L 160 {y - 60} L 330 {y - 150} L 760 {y - 158} L 900 {y - 70} L 1180 {y - 40} '
        f'L 1460 {y - 95} L 1620 {y - 110} L 1760 {y - 60} L 1940 {y - 20} L 1940 {y + 60} L -20 {y + 60} Z" fill="{far}" opacity="0.85"/>'
    )


def ground(kind, y=760, color=None):
    _, _, _, sil = SKIES[kind]
    c = color or sil
    return f'<path d="M -20 {y} C 300 {y - 18}, 700 {y + 14}, 1000 {y - 6} C 1300 {y - 20}, 1600 {y + 10}, 1940 {y - 4} L 1940 1100 L -20 1100 Z" fill="{c}"/>'


def kopje_side(x, y, w=620, h=230, color="#000", huts=True):
    hl = []
    if huts:
        for k in range(5):
            hx = x - 90 + k * 46
            hl.append(f'<path d="M {hx - 20} {y - h + 8} Q {hx} {y - h - 34} {hx + 20} {y - h + 8} Z" fill="{color}"/>')
    return (
        f'<path d="M {x - w / 2} {y} C {x - w * 0.36} {y - h * 0.4}, {x - w * 0.28} {y - h * 0.95}, {x - w * 0.1} {y - h} '
        f'L {x + w * 0.12} {y - h + 6} C {x + w * 0.3} {y - h * 0.9}, {x + w * 0.38} {y - h * 0.35}, {x + w / 2} {y} Z" fill="{color}"/>'
        + "".join(hl)
    )


def bush_side(x, y, s=1.0, color="#000"):
    return (
        f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-22" r="26" fill="{color}"/><circle cx="26" cy="-16" r="20" fill="{color}"/>'
        f'<circle cx="-24" cy="-14" r="18" fill="{color}"/><circle cx="8" cy="-40" r="16" fill="{color}"/><rect x="-40" y="-14" width="80" height="14" fill="{color}"/></g>'
    )


def river_bank(color, y=760, x0=-20, x1=1940):
    """A cut in the ground with bushes on both lips (side view)."""
    bushes = "".join(bush_side(x, y + 4, 0.9 + (i % 3) * 0.15, color) for i, x in enumerate(range(x0 + 40, x1, 120)))
    return bushes


def tent(x, y, s=1.0, color="#000", door=None):
    d = door or "rgba(255,255,255,0)"
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M -70 0 C -50 -40, -18 -96, 0 -112 C 18 -96, 50 -40, 70 0 Z" fill="{color}"/>'
        f'<path d="M -12 0 L 0 -60 L 12 0 Z" fill="{d}"/><rect x="-2" y="-126" width="4" height="16" fill="{color}"/></g>'
    )


def campfire(x, y, s=1.0, uid="fire"):
    return f"""<g transform="translate({x} {y}) scale({s})">
  <circle id="{uid}-glow" cx="0" cy="-30" r="170" fill="url(#{uid}-g)"/>
  <defs><radialGradient id="{uid}-g"><stop offset="0" stop-color="#FFB347" stop-opacity="0.55"/><stop offset="1" stop-color="#FF8A2A" stop-opacity="0"/></radialGradient></defs>
  <g id="{uid}-flames">
    <path d="M -34 0 C -40 -40, -12 -54, -16 -96 C 8 -66, 24 -60, 18 -18 C 30 -36, 34 -52, 30 -70 C 50 -40, 46 -12, 34 0 Z" fill="#F08A24"/>
    <path d="M -18 0 C -20 -26, -2 -36, -4 -64 C 12 -42, 18 -30, 14 0 Z" fill="#FFD25A"/>
  </g>
  <rect x="-44" y="-8" width="88" height="12" rx="6" fill="#3a2414" transform="rotate(-8)"/>
  <rect x="-44" y="-8" width="88" height="12" rx="6" fill="#4a2e18" transform="rotate(10)"/>
</g>"""


# people: origin at the feet, ~190 px tall at scale 1, facing right
def soldier(color="#000", rifle=True, extra=""):
    r = '<rect x="14" y="-182" width="4.5" height="150" rx="2" transform="rotate(8 16 -110)" fill="%s"/>' % color if rifle else ""
    return f"""<g fill="{color}">
  <path d="M -18 -166 Q -16 -194 0 -196 Q 16 -194 18 -166 Z"/><path d="M -25 -165 Q 0 -158 25 -165 L 23 -159 Q 0 -153 -23 -159 Z"/>
  <path d="M -2 -196 L 0 -204 L 2 -196 Z"/><circle cx="1" cy="-150" r="11"/>
  <path d="M -18 -140 L 18 -140 L 21 -88 L -21 -88 Z"/>
  <path d="M -18 -138 L -27 -134 L -30 -92 L -22 -92 Z"/><path d="M 18 -138 L 27 -134 L 31 -94 L 23 -92 Z"/>
  <path d="M -17 -90 L -2 -90 L -5 -2 L -16 -2 Z"/><path d="M 2 -90 L 17 -90 L 16 -2 L 5 -2 Z"/>
  <path d="M -18 -4 L -2 -4 L 0 0 L -20 0 Z"/><path d="M 4 -4 L 20 -4 L 24 0 L 4 0 Z"/>
  {r}{extra}
</g>"""


def boer(color="#000", beard=True, rifle=True, young=False, arm_up=False):
    s = 0.88 if young else 1.0
    beard_p = '<path d="M -9 -146 Q 2 -116 12 -146 Z"/>' if beard else ""
    rifle_p = f'<rect x="-30" y="-150" width="5" height="140" rx="2" transform="rotate(-24 -28 -80)"/>' if rifle else ""
    arm = (
        '<path d="M 18 -134 L 26 -140 L 44 -184 L 36 -188 L 20 -146 Z"/>' if arm_up else '<path d="M 18 -134 L 28 -130 L 32 -84 L 24 -82 Z"/>'
    )
    return f"""<g fill="{color}" transform="scale({s})">
  <path d="M -34 -160 Q 0 -170 34 -160 L 32 -154 Q 0 -161 -32 -154 Z"/><path d="M -15 -160 Q -14 -184 0 -186 Q 14 -184 15 -160 Z"/>
  <circle cx="1" cy="-148" r="11"/>{beard_p}
  <path d="M -19 -136 L 19 -136 L 27 -58 L -27 -58 Z"/>
  <path d="M -18 -134 L -28 -130 L -32 -84 L -24 -82 Z"/>{arm}
  <path d="M -15 -60 L -2 -60 L -4 -2 L -14 -2 Z"/><path d="M 2 -60 L 15 -60 L 14 -2 L 4 -2 Z"/>
  <path d="M -16 -4 L -2 -4 L 0 0 L -18 0 Z"/><path d="M 4 -4 L 18 -4 L 22 0 L 4 0 Z"/>
  {rifle_p}
</g>"""


def woman(color="#000", arm_up=False, s=1.0):
    arm = (
        '<path d="M 14 -128 L 22 -134 L 40 -176 L 32 -180 L 16 -140 Z"/>' if arm_up else '<path d="M 14 -126 L 24 -122 L 26 -80 L 18 -80 Z"/>'
    )
    return f"""<g fill="{color}" transform="scale({s})">
  <path d="M -16 -146 Q -20 -178 2 -180 Q 24 -178 22 -150 L 30 -140 L 10 -138 L -12 -138 Z"/>
  <circle cx="2" cy="-146" r="10"/>
  <path d="M -14 -134 L 16 -134 L 20 -96 L 40 0 L -38 0 L -18 -96 Z"/>
  <path d="M -14 -130 L -24 -124 L -26 -80 L -18 -80 Z"/>{arm}
</g>"""


def rider(color="#000", legs=0):
    """Boer on a galloping horse, facing right; `legs` picks one of two gallop poses."""
    if legs == 0:
        lg = (
            '<path d="M 36 -82 L 46 -80 L 74 -42 L 84 -12 L 76 -10 L 62 -36 Z"/>'
            '<path d="M 22 -80 L 32 -80 L 44 -50 L 30 -28 L 24 -32 L 34 -52 Z"/>'
            '<path d="M -52 -86 L -40 -84 L -62 -42 L -80 -16 L -86 -20 L -72 -46 Z"/>'
            '<path d="M -36 -80 L -26 -80 L -30 -48 L -16 -24 L -22 -20 L -40 -46 Z"/>'
        )
    else:
        lg = (
            '<path d="M 36 -82 L 46 -80 L 50 -40 L 48 -4 L 40 -4 L 40 -40 Z"/>'
            '<path d="M 22 -80 L 32 -80 L 28 -44 L 18 -6 L 10 -8 L 20 -44 Z"/>'
            '<path d="M -52 -86 L -40 -84 L -44 -44 L -38 -6 L -46 -6 L -54 -44 Z"/>'
            '<path d="M -36 -80 L -26 -80 L -22 -44 L -30 -6 L -38 -8 L -32 -44 Z"/>'
        )
    return f"""<g fill="{color}">
  <path d="M -60 -100 C -62 -120, -40 -128, -10 -126 C 20 -124, 40 -128, 52 -138 C 62 -150, 70 -168, 82 -176 L 88 -186 L 92 -175
    C 102 -168, 110 -156, 113 -147 C 114 -141, 106 -137, 98 -141 C 88 -145, 80 -146, 74 -138 C 66 -126, 62 -112, 54 -100
    C 50 -88, 40 -80, 30 -78 L -30 -76 C -48 -78, -58 -86, -60 -100 Z"/>
  <path d="M -60 -104 C -82 -104, -94 -90, -102 -66 L -95 -64 C -88 -84, -77 -94, -60 -95 Z"/>
  {lg}
  <path d="M -16 -122 L 8 -122 L 8 -168 L -12 -168 Z"/><circle cx="-2" cy="-178" r="10"/>
  <path d="M -24 -186 Q -2 -194 20 -186 L 18 -182 Q -2 -188 -22 -182 Z"/><path d="M -12 -186 Q -11 -200 -2 -201 Q 7 -200 8 -186 Z"/>
  <path d="M -6 -128 L 10 -128 L 18 -96 L 10 -94 Z"/>
  <rect x="0" y="-206" width="4.5" height="90" rx="2" transform="rotate(38 2 -160)"/>
</g>"""


def cannon_side(color="#000"):
    return f"""<g fill="{color}">
  <rect x="-10" y="-62" width="120" height="20" rx="8" transform="rotate(-14 0 -52)"/>
  <circle cx="0" cy="-34" r="34" fill="none" stroke="{color}" stroke-width="8"/>
  {''.join(f'<rect x="-2" y="-66" width="4" height="64" transform="rotate({a} 0 -34)"/>' for a in (0, 45, 90, 135))}
  <path d="M -10 -40 L -120 -6 L -118 2 L -6 -28 Z"/>
</g>"""


def tank(color="#000"):
    return f"""<g fill="{color}">
  <path d="M -230 -20 L -170 -120 L 170 -120 L 240 -20 L 196 34 L -196 34 Z"/>
  <path d="M -200 -18 L -152 -100 L 152 -100 L 210 -18 L 172 22 L -172 22 Z" fill="#000" opacity="0.18"/>
  <rect x="-52" y="-92" width="104" height="70" rx="6"/><rect x="40" y="-70" width="70" height="12" rx="5"/>
  <circle cx="-268" cy="18" r="18"/><circle cx="-304" cy="18" r="18"/><rect x="-306" y="-2" width="80" height="10"/>
</g>"""


def colonel(angry=True):
    """Front view, in colour: the colonel's head and shoulders."""
    brow = "M -78 -40 L -22 -24 M 22 -24 L 78 -40" if angry else "M -78 -30 L -22 -34 M 22 -34 L 78 -30"
    return f"""<g>
  <path d="M -230 260 C -220 150, -150 110, 0 108 C 150 110, 220 150, 230 260 Z" fill="#B49A62"/>
  <path d="M -60 112 L 0 178 L 60 112 Z" fill="#8f7848"/><rect x="-140" y="128" width="40" height="16" rx="3" fill="#B3261E"/><rect x="100" y="128" width="40" height="16" rx="3" fill="#B3261E"/>
  <ellipse cx="0" cy="0" rx="120" ry="140" fill="#E58A6E"/>
  <ellipse cx="-122" cy="10" rx="18" ry="30" fill="#D9775C"/><ellipse cx="122" cy="10" rx="18" ry="30" fill="#D9775C"/>
  <path d="{brow}" stroke="#F4F1EA" stroke-width="16" stroke-linecap="round"/>
  <circle cx="-48" cy="-6" r="13" fill="#1E1812"/><circle cx="48" cy="-6" r="13" fill="#1E1812"/>
  <circle cx="48" cy="-6" r="30" fill="none" stroke="#C9A34A" stroke-width="5"/>
  <path d="M -14 0 Q 0 40 14 0" fill="#C96A52"/>
  <path d="M 0 58 C -40 40, -110 46, -150 84 C -100 80, -50 86, 0 72 C 50 86, 100 80, 150 84 C 110 46, 40 40, 0 58 Z" fill="#F4F1EA"/>
  <ellipse id="colonel-mouth" cx="0" cy="96" rx="26" ry="20" fill="#5a1d14"/>
  <path d="M -150 -96 Q -130 -230 0 -236 Q 130 -230 150 -96 Z" fill="#D8C48E"/>
  <path d="M -190 -92 Q 0 -60 190 -92 L 182 -76 Q 0 -44 -182 -76 Z" fill="#C8B278"/>
  <rect x="-150" y="-120" width="300" height="20" fill="#7d6a43"/>
</g>"""


def mug(color="#000"):
    return f'<g fill="{color}"><rect x="-22" y="-44" width="44" height="44" rx="6"/><path d="M 22 -36 C 44 -36, 44 -10, 22 -10 L 22 -16 C 34 -16, 34 -30, 22 -30 Z"/></g>'


def books(color="#000"):
    rows = [(-150, 150, 60), (-130, 130, 52), (-160, 140, 58), (-110, 120, 48)]
    y, out = 0, []
    for x0, x1, h in rows:
        y -= h
        out.append(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h - 6}" rx="6"/><rect x="{x0 + 14}" y="{y + 10}" width="{x1 - x0 - 28}" height="5" fill="#ffffff" opacity="0.18"/>')
    return f'<g fill="{color}">{"".join(out)}</g>'


def farmhouse_side(color="#000", lit=False):
    win = '<rect x="-60" y="-110" width="34" height="36" fill="#FFCF6B"/><rect x="40" y="-110" width="34" height="36" fill="#FFCF6B"/>' if lit else ""
    return f"""<g>
  <g fill="{color}"><rect x="-140" y="-150" width="280" height="150"/><path d="M -160 -150 L 0 -240 L 160 -150 Z"/><rect x="80" y="-250" width="26" height="70"/></g>
  {win}
</g>"""


# ---------------------------------------------------------------- sand-table pieces
def token_brit(x, y, s=1.0, i=""):
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({s})"><g {i}>'
        f'<ellipse cx="3" cy="5" rx="13" ry="9" fill="#000" opacity="0.28"/>'
        f'<circle r="12" fill="{NAVY}"/><circle r="12" fill="none" stroke="{NAVY_HI}" stroke-width="3"/><circle cx="-3" cy="-3" r="4" fill="#9fb7d6"/></g></g>'
    )


def token_boer(x, y, s=1.0, i="", rot=0):
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({s}) rotate({rot})"><g {i}>'
        f'<ellipse cx="3" cy="6" rx="14" ry="9" fill="#000" opacity="0.28"/>'
        f'<path d="M 0 -15 L 14 11 L -14 11 Z" fill="{RUST}" stroke="#5b1f10" stroke-width="2.5" stroke-linejoin="round"/>'
        f'<circle cx="0" cy="3" r="3.5" fill="#FFD9C2"/></g></g>'
    )


def token_tent(x, y, s=1.0, i=""):
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({s})"><g {i}>'
        f'<path d="M -16 -12 L 16 -12 L 20 14 L -20 14 Z" fill="#000" opacity="0.25" transform="translate(4 5)"/>'
        f'<path d="M -16 -12 L 16 -12 L 20 14 L -20 14 Z" fill="#F7F1E3" stroke="#6d5f48" stroke-width="2"/>'
        f'<line x1="0" y1="-12" x2="0" y2="14" stroke="#b4a688" stroke-width="2.5"/></g></g>'
    )


def token_gun(x, y, s=1.0, i="", rot=0):
    return (
        f'<g transform="translate({x:.1f} {y:.1f}) scale({s}) rotate({rot})"><g {i}>'
        f'<circle cx="-8" cy="8" r="7" fill="#3b2a1c"/><circle cx="8" cy="8" r="7" fill="#3b2a1c"/>'
        f'<rect x="-4" y="-28" width="8" height="32" rx="3" fill="#2a1d12"/><rect x="-10" y="0" width="20" height="10" fill="{RUST}"/></g></g>'
    )


def person_icon(x, y, kind="man", s=1.0, color="#1E1812", i=""):
    if kind == "woman":
        body = '<circle cx="0" cy="-30" r="7"/><path d="M -6 -22 L 6 -22 L 13 0 L -13 0 Z"/><path d="M -9 -34 Q 0 -44 9 -34 L 10 -28 L -10 -28 Z"/>'
    elif kind == "child":
        body = '<circle cx="0" cy="-20" r="6"/><path d="M -6 -13 L 6 -13 L 7 0 L -7 0 Z"/>'
    else:
        body = '<circle cx="0" cy="-30" r="7"/><path d="M -7 -22 L 7 -22 L 8 0 L -8 0 Z"/><path d="M -12 -34 L 12 -34 L 10 -30 L -10 -30 Z"/>'
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({s})"><g fill="{color}" {i}>{body}</g></g>'


def trench_path(d, uid, width=12, parapet=None, hidden=False):
    """A trench: dark cut, a lighter spoil bank (parapet) on its front side."""
    par = ""
    if parapet:
        par = f'<path id="{uid}-par" d="{parapet}" fill="none" stroke="{"#c8a874" if hidden else "#EBD3A0"}" stroke-width="{width * 0.9:.0f}" stroke-linecap="round" pathLength="100"/>'
    return (
        f'<g id="{uid}">{par}'
        f'<path id="{uid}-cut" d="{d}" fill="none" stroke="#4A321C" stroke-width="{width}" stroke-linecap="round" pathLength="100"/>'
        f'<path d="{d}" fill="none" stroke="#2c1c0e" stroke-width="{max(2, width * 0.35):.0f}" stroke-linecap="round" opacity="0.7"/></g>'
    )


def fire_line(x1, y1, x2, y2, uid, color=FIRE, width=4):
    return (
        f'<g id="{uid}" opacity="0"><line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}" '
        f'stroke-dasharray="18 26" stroke-linecap="round" id="{uid}-l"/>'
        f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="9" fill="#FFE3A0" id="{uid}-f"/></g>'
    )


def puff(x, y, uid, r=34, color="#EDE4D3"):
    return (
        f'<g transform="translate({x:.1f} {y:.1f})"><g id="{uid}" opacity="0">'
        f'<circle r="{r}" fill="{color}" opacity="0.9"/><circle cx="{r * 0.6:.0f}" cy="{-r * 0.3:.0f}" r="{r * 0.7:.0f}" fill="{color}" opacity="0.85"/>'
        f'<circle cx="{-r * 0.55:.0f}" cy="{-r * 0.25:.0f}" r="{r * 0.6:.0f}" fill="{color}" opacity="0.85"/></g></g>'
    )


def pin(x, y, text, uid, cls="", dx=0, dy=-78):
    """A paper tag on a post, stuck into the sand at (x, y). HTML so Hebrew shapes well."""
    return (
        f'<div id="{uid}" class="pin" style="left:{x:.0f}px; top:{y:.0f}px;">'
        f'<div class="pin-post"></div><div class="tag {cls}" style="transform:translate(calc(50% + {dx}px), {dy}px)">{text}</div></div>'
    )


PIN_CSS = """
.pin { position:absolute; width:0; height:0; }
.pin-post { position:absolute; left:-2px; top:-62px; width:5px; height:64px; background:#4a3520; border-radius:2px; }
.pin-post::after { content:''; position:absolute; left:-5px; top:58px; width:15px; height:7px; border-radius:50%; background:rgba(0,0,0,.3); }
.pin .tag { right:0; top:0; }
"""


def stamp_img(uid, kind="fail", x=580, y=390, rot=-8):
    src = "assets/art/stamp-fail.png" if kind == "fail" else "assets/art/stamp-ok.png"
    w = 760 if kind == "fail" else 860
    return (
        f'<div class="abs" style="left:{x}px; top:{y}px; width:{w}px; height:300px; transform:rotate({rot}deg);">'
        f'<img id="{uid}" class="stamp" src="{src}" style="left:0; top:0; width:{w}px; height:300px; opacity:0" alt=""></div>'
    )


def slam(c, sel, t, sound=True):
    c.fromTo(sel, {"opacity": 0, "scale": 2.6}, {"opacity": 1, "scale": 1, "duration": 0.2, "ease": "power4.in"}, t)
    if sound:
        c.sfx("stamp", t + 0.17, 0.75)
