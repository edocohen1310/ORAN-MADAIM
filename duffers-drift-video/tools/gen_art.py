"""Write the static art as HTML pages under tools/art/; render_art.cjs turns them into images.

- sand-base: the bare sand table (ground, hills, contours, rocks)
- sand-full: the same with the river, road, drift, gully, kraal and farm baked in
- slate: the lesson tablet
- stamp-fail / stamp-ok: rubber stamps
"""
import math
from pathlib import Path

import geo

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools/art"
OUT.mkdir(parents=True, exist_ok=True)

SAND = "#D8B47A"
SAND_HI = "#E6C793"
SAND_LO = "#C49A5F"
CONTOUR = "#8E6B3C"
BED = "#BE9862"
BANK = "#7B5A33"
WATER = "#4C8C86"
BUSH = ("#6F7A36", "#5E6A2C", "#7F8A40")
ROAD = "#8A693E"


def page(body, w, h, bg="transparent"):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{w}px;height:{h}px;background:{bg};overflow:hidden}}
svg{{display:block}}
</style></head><body>{body}</body></html>"""


def defs():
    return f"""<defs>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.25  0 0 0 0 0.12  0 0 0 0.55 -0.12"/>
</filter>
<filter id="swell" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.0035" numOctaves="3" seed="11"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.32  0 0 0 0 0.16  0 0 0 0.9 -0.32"/>
</filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="2.2"/><feOffset dx="3" dy="4"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.45"/></feComponentTransfer>
  <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<radialGradient id="vig" cx="50%" cy="50%" r="75%">
  <stop offset="62%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#3a2410" stop-opacity="0.38"/>
</radialGradient>
</defs>"""


def hill(cx, cy, rx, ry, rings, seed):
    """Stacked contour plates, lighter as they climb, each with a printed contour line."""
    out = []
    for k in range(rings):
        f = 1 - k / rings
        fill = mix(SAND, SAND_HI, k / max(1, rings - 1))
        d = geo.blob(cx, cy, rx * f, ry * f, seed=seed + k * 0.9, wob=0.08)
        out.append(f'<path d="{d}" fill="{fill}" opacity="0.9"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{CONTOUR}" stroke-width="2.2" opacity="0.5"/>')
    return "\n".join(out)


def mix(a, b, t):
    pa = [int(a[i : i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


def rocks(cx, cy, r, n, seed):
    g = geo.rng(seed)
    out = []
    for _ in range(n):
        a, d = next(g) * 6.283, math.sqrt(next(g)) * r
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.75
        s = 4 + next(g) * 9
        pts = " ".join(
            f"{x + math.cos(t) * s * (0.7 + 0.5 * next(g)):.1f},{y + math.sin(t) * s * 0.7 * (0.7 + 0.5 * next(g)):.1f}"
            for t in [i * 1.2566 for i in range(5)]
        )
        out.append(f'<polygon points="{pts}" fill="#8F7F69" stroke="#5f523f" stroke-width="1.2"/>')
    return "\n".join(out)


def bushes(points, seed, scale=1.0, skip=lambda x, y: False):
    g = geo.rng(seed)
    out = []
    for x, y in points:
        if skip(x, y) or next(g) < 0.18:
            continue
        x += (next(g) - 0.5) * 14
        y += (next(g) - 0.5) * 14
        s = (9 + next(g) * 7) * scale
        c = BUSH[int(next(g) * 3)]
        out.append(
            f'<g filter="url(#shadow)"><circle cx="{x:.1f}" cy="{y:.1f}" r="{s:.1f}" fill="{c}"/>'
            f'<circle cx="{x + s * 0.55:.1f}" cy="{y - s * 0.25:.1f}" r="{s * 0.7:.1f}" fill="{c}"/>'
            f'<circle cx="{x - s * 0.3:.1f}" cy="{y - s * 0.45:.1f}" r="{s * 0.38:.1f}" fill="#93A050" opacity="0.8"/></g>'
        )
    return "\n".join(out)


def near_drift(x, y, r=46):
    return math.hypot(x - geo.DRIFT[0], y - geo.DRIFT[1]) < r


def ground():
    parts = [f'<rect width="1920" height="1080" fill="{SAND}"/>', '<rect width="1920" height="1080" filter="url(#swell)"/>']
    parts.append(hill(*geo.REGRETS, 420, 150, 5, 2.0))
    parts.append(hill(*geo.TELPEGA, 190, 120, 4, 4.1))
    parts.append(hill(*geo.RISE, 260, 130, 3, 6.3))
    parts.append(hill(*geo.KOPJE, 360, 270, 6, 1.4))
    parts.append(rocks(geo.KOPJE[0] + 30, geo.KOPJE[1] + 40, 230, 46, 7))
    parts.append(rocks(geo.TELPEGA[0], geo.TELPEGA[1], 120, 14, 9))
    parts.append(rocks(geo.REGRETS[0] + 80, geo.REGRETS[1] + 40, 260, 22, 13))
    # scattered veld scrub on the open ground
    g = geo.rng(21)
    pts = []
    for _ in range(140):
        x, y = next(g) * 1920, next(g) * 1080
        if math.hypot(x - geo.KOPJE[0], y - geo.KOPJE[1]) < 200:
            continue
        pts.append((x, y))
    parts.append(bushes(pts, 22, 0.55))
    return "\n".join(parts)


def river():
    d = geo.RIVER
    return f"""
<path d="{d}" fill="none" stroke="{BANK}" stroke-width="86" stroke-linecap="round" opacity="0.55"/>
<path d="{d}" fill="none" stroke="#5a4024" stroke-width="84" stroke-dasharray="2 7" opacity="0.55"/>
<path d="{d}" fill="none" stroke="{BED}" stroke-width="64" stroke-linecap="round"/>
<path d="{d}" fill="none" stroke="#d2b07a" stroke-width="40" stroke-linecap="round" opacity="0.55"/>
<path d="{d}" fill="none" stroke="{WATER}" stroke-width="9" stroke-linecap="round" opacity="0.9"/>
<path d="{d}" fill="none" stroke="#9fd0c4" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
"""


def river_bushes():
    pts = geo.bank_points(+1, 22, 50) + geo.bank_points(-1, 22, 50)
    return bushes(pts, 31, 1.0, skip=lambda x, y: near_drift(x, y, 60))


def road():
    d = geo.ROAD
    return f"""
<path d="{d}" fill="none" stroke="#cfae78" stroke-width="22" stroke-linecap="round" opacity="0.85"/>
<path d="{d}" fill="none" stroke="{ROAD}" stroke-width="2.6" stroke-dasharray="14 6" transform="translate(-6 0)" opacity="0.8"/>
<path d="{d}" fill="none" stroke="{ROAD}" stroke-width="2.6" stroke-dasharray="11 7" transform="translate(6 0)" opacity="0.8"/>
"""


def drift():
    x, y = geo.DRIFT
    g = geo.rng(5)
    stones = "".join(
        f'<ellipse cx="{x + (next(g) - 0.5) * 70:.1f}" cy="{y + (next(g) - 0.5) * 50:.1f}" rx="{4 + next(g) * 4:.1f}" ry="{3 + next(g) * 3:.1f}" fill="#9c8a72" stroke="#6d5e4b" stroke-width="1"/>'
        for _ in range(26)
    )
    return f'<ellipse cx="{x}" cy="{y}" rx="44" ry="38" fill="#d6bb88"/><path d="M {x - 8} {y - 40} L {x - 14} {y + 40} M {x + 6} {y - 40} L {x} {y + 40}" stroke="#8a693e" stroke-width="2.6" stroke-dasharray="9 6" fill="none" opacity="0.8"/>' + stones


def gully():
    d = geo.GULLY
    return f"""
<path d="{d}" fill="none" stroke="{BANK}" stroke-width="30" stroke-linecap="round" opacity="0.4"/>
<path d="{d}" fill="none" stroke="{BED}" stroke-width="18" stroke-linecap="round"/>
<path d="{d}" fill="none" stroke="#5a4024" stroke-width="30" stroke-dasharray="2 6" opacity="0.35"/>"""


def kraal():
    cx, cy = geo.KOPJE
    huts = []
    for k in range(7):
        a = k * 2 * math.pi / 7 + 0.3
        x, y = cx + math.cos(a) * 32, cy + math.sin(a) * 26
        huts.append(
            f'<g filter="url(#shadow)"><circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#9b7748"/>'
            f'<circle cx="{x - 3:.1f}" cy="{y - 3:.1f}" r="6" fill="#b58f5c"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#5d4426"/></g>'
        )
    fence = f'<ellipse cx="{cx}" cy="{cy}" rx="{geo.KRAAL_R + 8}" ry="{geo.KRAAL_R - 2}" fill="none" stroke="#5b4428" stroke-width="5" stroke-dasharray="3 5"/>'
    return fence + "".join(huts)


def farm():
    x, y = geo.FARM
    return f"""<g filter="url(#shadow)">
<rect x="{x - 46}" y="{y - 26}" width="92" height="52" fill="#e9dcc2" stroke="#6b5537" stroke-width="2"/>
<path d="M {x - 50} {y - 26} L {x} {y - 4} L {x + 50} {y - 26} L {x + 50} {y - 30} L {x - 50} {y - 30} Z" fill="#9a4630"/>
<rect x="{x - 50}" y="{y - 30}" width="100" height="30" fill="#a94e35"/>
<line x1="{x - 50}" y1="{y - 15}" x2="{x + 50}" y2="{y - 15}" stroke="#7e3725" stroke-width="2"/>
<rect x="{x + 60}" y="{y - 10}" width="40" height="28" fill="#d9c7a3" stroke="#6b5537" stroke-width="2"/>
</g>
<ellipse cx="{x + 10}" cy="{y + 10}" rx="120" ry="70" fill="none" stroke="#7a6446" stroke-width="3" stroke-dasharray="1 6"/>
{bushes([(x - 90, y - 30), (x - 100, y + 20), (x + 120, y + 40), (x - 60, y + 55)], 41, 1.6)}"""


def sand(full):
    body = [defs(), ground()]
    if full:
        body += [gully(), road(), river(), drift(), river_bushes(), kraal(), farm()]
    body += ['<rect width="1920" height="1080" filter="url(#grain)"/>', '<rect width="1920" height="1080" fill="url(#vig)"/>']
    return page(f'<svg width="1920" height="1080" viewBox="0 0 1920 1080">{"".join(body)}</svg>', 1920, 1080, SAND)


def overlay_parts():
    """The terrain pieces the terrain chapter draws in one by one (transparent layers)."""
    pieces = {
        "river": river() + river_bushes(),
        "road": road() + drift(),
        "kraal": kraal(),
        "farm": farm(),
        "gully": gully(),
    }
    out = {}
    for k, v in pieces.items():
        out[f"layer-{k}"] = page(f'<svg width="1920" height="1080" viewBox="0 0 1920 1080">{defs()}{v}</svg>', 1920, 1080)
    return out


def rrect(x0, y0, x1, y1, r, seed, jit=3.0):
    """A rounded rectangle whose edge wanders a little, like cut stone."""
    g = geo.rng(seed)
    pts = []
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    for (cx, cy, a0) in corners:
        for k in range(7):
            a = math.radians(a0 + k * 15)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        # straight run to the next corner, with chips
    out = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 40))
        for k in range(n):
            t = k / n
            out.append((a[0] + (b[0] - a[0]) * t + (next(g) - 0.5) * jit, a[1] + (b[1] - a[1]) * t + (next(g) - 0.5) * jit))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in out) + " Z"


def slate():
    w, h = 1480, 720
    edge = rrect(14, 14, w - 14, h - 22, 34, 3, 5.0)
    return page(f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<filter id="stone" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="4" seed="8" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.86 0 0 0 0 0.84 0 0 0 0 0.78 0 0 0 0.20 -0.04"/>
</filter>
<filter id="fine"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1" seed="2"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.35 -0.1"/></filter>
<filter id="drop" x="-10%" y="-10%" width="120%" height="130%"><feGaussianBlur in="SourceAlpha" stdDeviation="10"/><feOffset dy="16"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="c"><path d="{edge}"/></clipPath>
<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#46525a"/><stop offset="1" stop-color="#2c353b"/></linearGradient>
</defs>
<g filter="url(#drop)"><path d="{edge}" fill="url(#g)"/></g>
<g clip-path="url(#c)">
  <rect width="{w}" height="{h}" filter="url(#stone)"/>
  <rect width="{w}" height="{h}" filter="url(#fine)"/>
</g>
<path d="{edge}" fill="none" stroke="#7d8b91" stroke-width="5" opacity="0.6"/>
<path d="{rrect(46, 46, w - 46, h - 54, 18, 5, 1.2)}" fill="none" stroke="#1d2428" stroke-width="3" opacity="0.55"/>
<path d="{rrect(48, 49, w - 48, h - 51, 18, 5, 1.2)}" fill="none" stroke="#7b888d" stroke-width="2" opacity="0.35"/>
</svg>""", w, h)


def stamp(word, color, w=760, h=300):
    return page(f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<filter id="ink" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="6" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1.7 1.62" result="m"/>
  <feComposite in="SourceGraphic" in2="m" operator="in"/>
</filter>
</defs>
<style>@font-face{{font-family:K;src:url('../../assets/fonts/Karantina-700-hebrew.woff2')}}</style>
<g filter="url(#ink)" fill="none" stroke="{color}">
  <rect x="22" y="22" width="{w - 44}" height="{h - 44}" rx="26" stroke-width="16"/>
  <rect x="48" y="48" width="{w - 96}" height="{h - 96}" rx="14" stroke-width="5"/>
  <text x="{w / 2}" y="{h / 2 + 76}" text-anchor="middle" font-family="K" font-weight="700" font-size="230" fill="{color}" stroke="none" direction="rtl">{word}</text>
</g>
</svg>""", w, h)


def main():
    files = {
        "sand-base": sand(False),
        "sand-full": sand(True),
        "slate": slate(),
        "stamp-fail": stamp("נכשל", "#B3261E"),
        "stamp-ok": stamp("הצלחה", "#1F7A45", 860),
    }
    files.update(overlay_parts())
    for name, html in files.items():
        (OUT / f"{name}.html").write_text(html)
    print("wrote", len(files), "art pages")


if __name__ == "__main__":
    main()
