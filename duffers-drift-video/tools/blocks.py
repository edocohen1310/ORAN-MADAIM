"""Reusable shots: sand table, shadow theatre, dream card, lesson tablets, waking up."""
import math

import geo
import kit
from kit import NAVY, RUST, SKIES

LT_W, LT_H = 597, 724  # lieutenant cut-out (from the book's cover)

ORDINAL = ["", "הראשון", "השני", "השלישי", "הרביעי", "החמישי", "השישי"]


# ---------------------------------------------------------------- sand table
def sand_shot(c, sid, t0, t1, svg="", pins="", over="", cam=(960, 540, 1.0), base="sand-full", tint=None, fade=0.45, fade_in="fade"):
    tint_html = ""
    if tint:
        tint_html = f'<div id="{sid}-tint" class="full" style="background:{tint[0]}; mix-blend-mode:multiply; opacity:{tint[1]};"></div>'
    inner = (
        f'<div id="{sid}-cam" class="cam"><img class="map" src="assets/art/{base}.jpg" alt="">'
        f'<svg class="stage" viewBox="0 0 1920 1080">{svg}</svg>{pins}</div>{tint_html}{over}'
    )
    c.shot(sid, t0, t1, inner, fade=fade, fade_in=fade_in)
    c.cam(f"#{sid}-cam", t0, *cam, first=True)
    return sid


def tents_at(c, pts, prefix, s=1.0):
    out = []
    for k, (x, y) in enumerate(pts):
        out.append(kit.token_tent(x, y, s, f'id="{prefix}{k}"'))
    return "".join(out)


def tokens_at(c, pts, prefix, kind="brit", s=1.0, rot=0):
    out = []
    for k, (x, y) in enumerate(pts):
        if kind == "brit":
            out.append(kit.token_brit(x, y, s, f'id="{prefix}{k}"'))
        else:
            out.append(kit.token_boer(x, y, s, f'id="{prefix}{k}"', rot))
    return "".join(out)


def pop_group(c, prefix, n, t, stagger=0.06, dur=0.35, origin="50% 50%"):
    for k in range(n):
        c.pop(f"#{prefix}{k}", round(t + k * stagger, 3), dur, origin=origin)


def fire_volley(c, lines, t0, t1, seed=1, sound="rifles", vol=0.45):
    """lines: list of (uid, x1, y1, x2, y2) already in the svg."""
    for k, (uid, *_r) in enumerate(lines):
        c.flicker(f"#{uid}", round(t0 + 0.05 * k, 3), t1, rate=0.11, seed=seed + k, p=0.5)
        c.fromTo(f"#{uid}-l", {"strokeDashoffset": 0}, {"strokeDashoffset": -44 * max(1, int((t1 - t0) / 0.25)), "duration": t1 - t0, "ease": "none"}, t0)
    if sound:
        c.sfx(sound, t0, vol, dur=t1 - t0 + 0.3, fade_out=0.4)


def fire_svg(lines, color=kit.FIRE, width=4):
    return "".join(kit.fire_line(x1, y1, x2, y2, uid, color, width) for uid, x1, y1, x2, y2 in lines)


def move_tokens(c, ids, t, dx, dy, dur=1.4, stagger=0.05, ease="power2.inOut"):
    for k, i in enumerate(ids):
        c.to(f"#{i}", {"x": dx, "y": dy, "duration": dur, "ease": ease}, round(t + k * stagger, 3))


def white_flag(x, y, uid):
    return (
        f'<g transform="translate({x} {y})"><g id="{uid}" opacity="0">'
        f'<rect x="-2" y="-70" width="5" height="74" fill="#3b2a1c"/>'
        f'<path d="M 3 -70 C 20 -76, 34 -62, 52 -68 L 52 -40 C 34 -34, 20 -48, 3 -42 Z" fill="#FBF7EE" stroke="#6a5b45" stroke-width="2"/></g></g>'
    )


# ---------------------------------------------------------------- shadow theatre
def side_shot(c, sid, t0, t1, kind, content="", html="", hills=True, ground_y=780, extra_sky="", fade=0.45, fade_in="fade", bank=False):
    _, _, far, sil = SKIES[kind]
    bg = []
    if kind in ("night", "dream"):
        bg.append(kit.stars(110, seed=len(sid)))
        bg.append(kit.moon(1560, 190))
    elif kind in ("gold", "day"):
        bg.append(kit.sun(1500, 250, 80))
    elif kind == "dusk":
        bg.append(kit.sun(1320, 640, 110, "#FFD08A"))
    elif kind == "dawn":
        bg.append(kit.sun(380, 720, 120, "#FFC08A"))
    bg.append(extra_sky)
    if hills:
        bg.append(kit.far_hills(kind, ground_y - 110))
    bg.append(kit.ground(kind, ground_y))
    if bank:
        bg.append(kit.river_bank(sil, ground_y))
    inner = (
        f'{kit.sky(kind)}<div id="{sid}-cam" class="cam"><svg class="stage" viewBox="0 0 1920 1080">{"".join(bg)}{content}</svg>{html}</div>'
    )
    c.shot(sid, t0, t1, inner, fade=fade, fade_in=fade_in)
    return sid


def lieutenant(uid, x, y, h=560, extra_style="", shadow=True):
    """The officer from the book's cover; (x, y) = his feet, h = height in px."""
    if shadow:
        w, src, fx = h * LT_W / LT_H, "lieutenant.png", 0.36
    else:
        w, src, fx = h * 299 / 724, "lieutenant-noshadow.png", 0.5
    return (
        f'<div class="abs" style="left:{x - w * fx:.0f}px; top:{y - h:.0f}px; width:{w:.0f}px; height:{h:.0f}px;{extra_style}">'
        f'<img id="{uid}" src="assets/book/{src}" style="width:100%; height:100%; display:block;" alt=""></div>'
    )


def place(svg_inner, x, y, uid, s=1.0, flip=False):
    sx = -s if flip else s
    return f'<g transform="translate({x} {y}) scale({sx} {s})"><g id="{uid}">{svg_inner}</g></g>'


def bubble(uid, text, x, y, tail="r", size=40, extra=""):
    return f'<div id="{uid}" class="bubble tail-{tail}" style="left:{x}px; top:{y}px; font-size:{size}px; opacity:0;{extra}">{text}</div>'


def say(c, uid, t, t_out=None):
    c.fromTo(f"#{uid}", {"opacity": 0, "scale": 0.6, "transformOrigin": "50% 100%"}, {"opacity": 1, "scale": 1, "duration": 0.32, "ease": "back.out(2)"}, t)
    if t_out:
        c.to(f"#{uid}", {"opacity": 0, "scale": 0.9, "duration": 0.2, "ease": "power2.in"}, t_out)


def walk(c, uid, t, dx, dur, bob=6, step=0.28, dy=0):
    """Slide a silhouette across with a small step bob (deterministic)."""
    c.to(f"#{uid}", {"x": dx, "y": dy, "duration": dur, "ease": "none"}, t)
    n = int(dur / step)
    for k in range(n):
        c.to(f"#{uid}-b", {"y": -bob if k % 2 == 0 else 0, "duration": step, "ease": "sine.inOut"}, round(t + k * step, 3))


def gallop(c, uid, t, dx, dur, step=0.14):
    """Swap two leg poses while sliding: ids uid-a / uid-b hold the two poses."""
    c.to(f"#{uid}", {"x": dx, "duration": dur, "ease": "none"}, t)
    n = int(dur / step)
    for k in range(n):
        tt = round(t + k * step, 3)
        c.set(f"#{uid}-a", {"opacity": 1 if k % 2 == 0 else 0}, tt)
        c.set(f"#{uid}-b", {"opacity": 0 if k % 2 == 0 else 1}, tt)


def horse(x, y, uid, color, s=1.0, flip=False):
    """Moves in screen space (#uid); the mirror lives in a static inner group."""
    sx = -s if flip else s
    return (
        f'<g transform="translate({x} {y})"><g id="{uid}"><g transform="scale({sx} {s})">'
        f'<g id="{uid}-a">{kit.rider(color, 0)}</g><g id="{uid}-b" opacity="0">{kit.rider(color, 1)}</g></g></g></g>'
    )


def actor(inner, x, y, uid, s=1.0, face_left=False):
    """translate > #uid (slides, screen space) > #uid-b (bobs) > #uid-f (turns) > static scale > figure."""
    sx = -s if face_left else s
    return (
        f'<g transform="translate({x} {y})"><g id="{uid}"><g id="{uid}-b"><g id="{uid}-f">'
        f'<g transform="scale({sx} {s})">{inner}</g></g></g></g></g>'
    )


def turn(c, uid, t):
    c.to(f"#{uid}-f", {"scaleX": -1, "duration": 0.2, "ease": "power2.inOut"}, t)


def bobber(inner, uid):
    """Wrap a figure so it can slide (uid) and bob (uid-b) independently."""
    return f'<g id="{uid}"><g id="{uid}-b">{inner}</g></g>'


# ---------------------------------------------------------------- cross-sections
def section(content="", ground_d="", water=False, label_html=""):
    """A cut through the ground, drawn like a diagram on sand."""
    w = '<path d="M 690 905 Q 760 925 830 905 L 830 935 L 690 935 Z" fill="#4C8C86" opacity="0.9"/>' if water else ""
    return (
        '<div class="full" style="background:linear-gradient(180deg,#F6E7C6 0%,#EED7A6 100%)"></div>'
        f'<svg class="stage" viewBox="0 0 1920 1080"><defs><pattern id="strata" width="60" height="22" patternUnits="userSpaceOnUse">'
        f'<path d="M 0 11 Q 15 5 30 11 T 60 11" fill="none" stroke="#6b4a26" stroke-width="2" opacity="0.35"/></pattern></defs>'
        '<marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#1E1812"/></marker>'
        f'<path d="{ground_d}" fill="#B98A52"/><path d="{ground_d}" fill="url(#strata)"/>'
        f'<path d="{ground_d}" fill="none" stroke="#5b3d1d" stroke-width="5"/>{w}{content}</svg>{label_html}'
    )


# ---------------------------------------------------------------- dream card
def dream_card(c, n, card_end):
    sid = f"{c.id}-card"
    pips = []
    for k in range(1, 7):
        x = 960 + (3.5 - k) * 120  # right to left (rtl order)
        if k < n:
            pips.append(
                f'<g transform="translate({x} 760)"><g id="{sid}-p{k}"><circle r="36" fill="#2c2a55" stroke="#B3261E" stroke-width="6"/>'
                f'<path d="M -16 -16 L 16 16 M 16 -16 L -16 16" stroke="#E5534B" stroke-width="8" stroke-linecap="round"/></g></g>'
            )
        elif k == n:
            pips.append(
                f'<g transform="translate({x} 760)"><g id="{sid}-p{k}"><circle r="40" fill="#F4E7CB"/>'
                f'<text y="16" text-anchor="middle" font-family="Karantina" font-weight="700" font-size="54" fill="#1A1F45">{k}</text></g></g>'
            )
        else:
            pips.append(
                f'<g transform="translate({x} 760)"><g id="{sid}-p{k}"><circle r="34" fill="none" stroke="#6d6aa0" stroke-width="4" stroke-dasharray="6 7"/></g></g>'
            )
    z = "".join(
        f'<div id="{sid}-z{k}" class="abs k-title" style="left:{1180 + k * 70}px; top:{330 - k * 70}px; font-size:{70 + k * 26}px; color:#B9B3E6; opacity:0">z</div>'
        for k in range(3)
    )
    inner = (
        f'<div class="full" style="background:radial-gradient(ellipse at 50% 45%, #3B3470 0%, #1A1F45 55%, #0E1028 100%)"></div>'
        f'<svg class="stage" viewBox="0 0 1920 1080">{kit.stars(120, seed=40 + n, ymax=1080)}{"".join(pips)}</svg>{z}'
        f'<div id="{sid}-t" class="abs k-title" style="left:0; width:1920px; top:330px; text-align:center; font-size:250px; opacity:0">החלום {ORDINAL[n]}</div>'
    )
    c.shot(sid, 0, card_end, inner, fade_in="iris")
    for k in range(1, 7):
        c.pop(f"#{sid}-p{k}", round(0.5 + (k - 1) * 0.12, 3), 0.4, origin="50% 50%")
    c.fromTo(f"#{sid}-p{n}", {"scale": 1}, {"scale": 1.25, "duration": 0.35, "ease": "power2.out", "transformOrigin": "50% 50%"}, 1.6)
    c.to(f"#{sid}-p{n}", {"scale": 1, "duration": 0.5, "ease": "power2.inOut"}, 1.95)
    for k in range(3):
        c.fromTo(f"#{sid}-z{k}", {"opacity": 0, "y": 30}, {"opacity": 0.9, "y": -40, "duration": 1.6, "ease": "sine.out"}, round(0.3 + k * 0.45, 3))
        c.to(f"#{sid}-z{k}", {"opacity": 0, "duration": 0.5}, round(2.0 + k * 0.45, 3))
    c.blur_in(f"#{sid}-t", c.t(f"{c.ch['segments'][0]['id']}") - 0.15, 0.35)
    c.sfx("whoosh", 0.05, 0.45)
    c.sfx("wind", 0.2, 0.18, dur=3.2, fade_out=1.0)


# ---------------------------------------------------------------- lessons
def split_lines(text, maxc=27):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


LESSON_CSS = """
.tab-wrap { position:absolute; left:210px; top:150px; width:1500px; height:730px; }
.tablet { position:absolute; inset:0; background:url('assets/art/slate.png') center/100% 100% no-repeat; opacity:0; }
.tab-num { position:absolute; right:84px; top:70px; font-family:'Karantina'; font-weight:700; font-size:230px; line-height:0.8; color:#E3A33B;
  text-shadow: 0 3px 0 rgba(0,0,0,.55), 0 -2px 0 rgba(255,240,200,.18); }
.tab-kicker { position:absolute; right:92px; top:290px; font-family:'Rubik'; font-weight:700; font-size:34px; color:#B9C3C6; }
.tab-text { position:absolute; right:320px; left:90px; top:60px; bottom:70px; display:flex; flex-direction:column; justify-content:center;
  font-family:'Frank Ruhl Libre'; font-weight:900; font-size:72px; line-height:1.3;
  color:#EFE8D8; text-shadow: 0 3px 1px rgba(0,0,0,.65), 0 -1px 0 rgba(255,255,255,.12); }
.tab-line { display:block; white-space:nowrap; }
.notches { position:absolute; left:0; width:1920px; top:950px; display:flex; justify-content:center; gap:12px; direction:rtl; }
.notch { width:52px; height:16px; border-radius:4px; background:rgba(239,232,216,.16); border:2px solid rgba(239,232,216,.35); }
.notch-lbl { position:absolute; left:0; width:1920px; top:986px; text-align:center; font-family:'Rubik'; font-weight:700; font-size:30px; color:#EFE8D8; opacity:.85; }
"""


def lesson_block(c, ids, t0, t1, prior, title=None):
    """Stone tablets for the given lesson segments. `prior` = lessons learnt before this dream."""
    sid = f"{c.id}-lessons"
    tabs = []
    for lid in ids:
        seg = c.segs[lid]
        lines = split_lines(seg["short"], 25)
        tabs.append(
            f'<div id="{sid}-{lid}" class="tablet"><div class="tab-num">{seg["n"]}</div><div class="tab-kicker">שיעור</div>'
            f'<div class="tab-text">{"".join(f"<span id={chr(34)}{sid}-{lid}-l{i}{chr(34)} class={chr(34)}tab-line{chr(34)}>{ln}</span>" for i, ln in enumerate(lines))}</div></div>'
        )
    notches = "".join(f'<div id="{sid}-n{k}" class="notch"></div>' for k in range(1, 23))
    inner = (
        '<img class="full" src="assets/art/sand-dim.jpg" alt="" style="object-fit:cover">'
        f'<div class="tab-wrap">{"".join(tabs)}</div><div class="notches">{notches}</div>'
        + "".join(
            f'<div id="{sid}-cnt{k}" class="notch-lbl" style="opacity:{1 if k == prior else 0}">שיעורים שנלמדו: {k} מתוך 22</div>'
            for k in range(prior, prior + len(ids) + 1)
        )
    )
    if title:
        inner += f'<div id="{sid}-title" class="abs k-title" style="left:0; width:1920px; top:400px; text-align:center; font-size:200px; color:#F4E7CB; opacity:0">{title}</div>'
    c.shot(sid, t0, t1, inner, fade=0.5)
    c.style(LESSON_CSS)
    if title:
        c.blur_in(f"#{sid}-title", t0 + 0.25, 0.3)
        c.out(f"#{sid}-title", c.t(ids[0]) - 0.6, 0.25)
    for k in range(1, prior + 1):
        c.set(f"#{sid}-n{k}", {"backgroundColor": "#C9B78F", "borderColor": "#E8DCBE"}, t0)
    for j, lid in enumerate(ids):
        seg = c.segs[lid]
        ts, te = c.t(lid), c.end(lid)
        nxt = c.t(ids[j + 1]) if j + 1 < len(ids) else None
        tab = f"#{sid}-{lid}"
        c.fromTo(tab, {"opacity": 0, "y": -70, "rotation": -1.5}, {"opacity": 1, "y": 0, "rotation": 0, "duration": 0.45, "ease": "power3.out"}, ts - 0.35)
        c.sfx("thud", ts - 0.05, 0.35)
        lines = split_lines(seg["short"], 25)
        span = max(0.8, (te - ts) - 0.6)
        for i in range(len(lines)):
            a = ts + 0.3 + span * i / len(lines)
            c.fromTo(f"{tab}-l{i}", {"clipPath": "inset(0 0 0 100%)"}, {"clipPath": "inset(0 0 0 0%)", "duration": span / len(lines) * 0.92, "ease": "none"}, round(a, 3))
        c.sfx("chisel", ts + 0.3, 0.16, dur=min(span, 4.0), fade_out=0.5)
        n = seg["n"]
        c.fromTo(f"#{sid}-n{n}", {"backgroundColor": "rgba(239,232,216,.16)"}, {"backgroundColor": "#E3A33B", "borderColor": "#FFE2A6", "duration": 0.3}, ts + 0.1)
        c.set(f"#{sid}-cnt{n - 1}", {"opacity": 0}, round(ts + 0.1, 3))
        c.set(f"#{sid}-cnt{n}", {"opacity": 1}, round(ts + 0.1, 3))
        if nxt is not None:
            c.to(tab, {"opacity": 0, "y": 60, "duration": 0.28, "ease": "power2.in"}, round(nxt - 0.45, 3))
            c.to(f"#{sid}-n{n}", {"backgroundColor": "#C9B78F", "borderColor": "#E8DCBE", "duration": 0.3}, round(nxt - 0.3, 3))
    return sid


# ---------------------------------------------------------------- waking up
def wake_shot(c, sid, t0, t1, kind="dawn", line_word_t=None):
    """The lieutenant jolts awake: lying down, then up with a start."""
    content = ""
    html = lieutenant(f"{sid}-lt", 960, 860, 560, shadow=False) + f'<div id="{sid}-ex" class="abs k-title" style="left:1150px; top:250px; font-size:260px; color:#B3261E; opacity:0">!</div>'
    side_shot(c, sid, t0, t1, kind, content, html, fade_in="blur")
    c.fromTo(f"#{sid}-lt", {"rotation": -82, "transformOrigin": "50% 90%", "y": 0}, {"rotation": -82, "y": 0, "duration": 0.01}, t0)
    tj = line_word_t if line_word_t is not None else t0 + 0.5
    c.to(f"#{sid}-lt", {"rotation": 0, "y": 0, "duration": 0.42, "ease": "back.out(2.2)"}, tj)
    c.pop(f"#{sid}-ex", tj + 0.15, 0.3)
    c.shake(f"#{sid}-cam", tj + 0.1, 12)
    c.sfx("swoosh", tj - 0.05, 0.35)
