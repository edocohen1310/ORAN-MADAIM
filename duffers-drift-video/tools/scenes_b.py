"""Dreams one to four."""
import math

import blocks as B
import geo
import kit
from kit import SKIES

DX, DY = geo.DRIFT
CAMP = [(905, 322), (948, 334), (990, 324), (1032, 336), (925, 368), (968, 378), (1010, 368)]
MEN = [(880, 350), (1060, 350), (900, 405), (1040, 410), (960, 420), (1000, 300), (920, 300), (1080, 385)]
TINT_DAY = ("#F2B867", 0.22)
TINT_DAWN = ("#E7907E", 0.38)
TINT_NIGHT = ("#4D5A9C", 0.55)


def card(c, n):
    first = c.ch["segments"][0]["id"]
    end = c.end(first) + 0.65
    B.dream_card(c, n, end)
    return end


def mini_tablets(c, sid, count, t):
    """A row of small tablets in the corner: the lessons he remembers."""
    html = []
    for k in range(count):
        x = 1800 - 96 - k * 92
        html.append(
            f'<div class="abs" style="left:{x}px; top:40px; width:84px; height:46px;"><img id="{sid}-mt{k}" src="assets/art/slate.png" style="width:84px; height:46px; opacity:0" alt=""></div>'
            f'<div id="{sid}-mn{k}" class="abs k-title" style="left:{x}px; width:84px; top:44px; text-align:center; font-size:40px; color:#E3A33B; opacity:0">{k + 1}</div>'
        )
    for k in range(count):
        c.fromTo(f"#{sid}-mt{k}", {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0, "duration": 0.3, "ease": "power3.out"}, round(t + k * 0.06, 3))
        c.fromTo(f"#{sid}-mn{k}", {"opacity": 0, "y": -20}, {"opacity": 1, "y": 0, "duration": 0.3, "ease": "power3.out"}, round(t + k * 0.06, 3))
    return "".join(html)


def arrivals(c, prefix, pts, t, frm=(0, 620), dur=2.4):
    for k in range(len(pts)):
        c.fromTo(f"#{prefix}{k}", {"x": frm[0], "y": frm[1], "opacity": 0}, {"x": 0, "y": 0, "opacity": 1, "duration": dur, "ease": "power2.out"}, round(t + k * 0.08, 3))


def icon_row(c, sid, groups, y, t, size=1.0, panel_y=740):
    """groups: list of (label, kind, count). Person icons in a row inside the panel, each group labelled."""
    html, svg = [], []
    x = 1760
    k = 0
    step = 46 * size
    for label, kind, cnt in groups:
        x0 = x
        for j in range(cnt):
            svg.append(kit.person_icon(x - j * step, y, kind, 2.3 * size, "#1E1812", f'id="{sid}-i{k}"'))
            c.pop(f"#{sid}-i{k}", round(t + k * 0.04, 3), 0.25)
            k += 1
        width = cnt * step
        # label centred under its group, in panel coordinates (panel starts at x=60, y=panel_y)
        cx = x0 - width / 2 + step / 2 - 60
        html.append(
            f'<div id="{sid}-lb{len(html)}" class="abs label" style="left:{cx - 200:.0f}px; width:400px; text-align:center; top:{y - panel_y + 22}px; '
            f'font-size:34px; color:#1E1812; opacity:0">{label}</div>'
        )
        x -= width + 90
    for j in range(len(html)):
        c.fade(f"#{sid}-lb{j}", t + 0.3 + j * 0.3, 0.3)
    return "".join(svg), "".join(html)


def panel(inner_svg, inner_html, sid, y=60, h=230):
    return (
        f'<div id="{sid}" class="abs" style="left:60px; top:{y}px; width:1800px; height:{h}px; background:rgba(246,236,214,.94); border:4px solid #1E1812; '
        f'border-radius:18px; box-shadow:8px 10px 0 rgba(30,24,18,.3); opacity:0"><svg class="stage" viewBox="0 0 1800 {h}" style="width:1800px; height:{h}px">'
        f'<g transform="translate(-60 {-y})">{inner_svg}</g></svg>{inner_html}</div>'
    )


# ================================================================ dream 1
def dream1(c):
    ce = card(c, 1)
    # S1: a comfortable camp by the water
    s1_end = c.t("d1-3") - 0.15
    svg = B.tokens_at(c, MEN, "d1m", "brit") + B.tents_at(c, CAMP, "d1t")
    smoke = "".join(kit.puff(x, y - 30, f"d1sm{k}", 16, "#F4F0E8") for k, (x, y) in enumerate([(930, 390), (1050, 400)]))
    pins = kit.pin(DX + 150, DY + 160, "מחנה נוח", "d1-pin1", "navy") + kit.pin(DX - 140, DY + 10, "קרוב למים", "d1-pin2")
    over = '<div id="d1-tomorrow" class="tag dark" style="left:200px; top:820px; font-size:52px; opacity:0">חפירות? מחר.</div>'
    B.sand_shot(c, "d1-s1", ce, s1_end, svg + smoke, pins, over, cam=(960, 420, 1.15), tint=TINT_DAY)
    c.cam("#d1-s1-cam", ce + 0.2, 965, 360, 1.55, dur=6.0, ease="power1.inOut")
    arrivals(c, "d1m", MEN, c.w("d1-1", "מגיע") - 0.3)
    c.pop("#d1-pin1", c.w("d1-1", "נוח"), 0.35)
    c.pop("#d1-pin2", c.w("d1-1", "למים"), 0.35)
    B.pop_group(c, "d1t", len(CAMP), c.w("d1-2", "אוהלים") - 0.2, 0.09)
    for k in range(2):
        c.fromTo(f"#d1sm{k}", {"opacity": 0, "y": 10, "scale": 0.6}, {"opacity": 0.8, "y": -30, "scale": 1.3, "duration": 2.5, "ease": "sine.out"}, c.w("d1-2", "מבשלים") + k * 0.4)
    c.blur_in("#d1-tomorrow", c.w("d1-2", "מחר") - 0.2, 0.3)

    # S2: Brink and his sons at dusk
    sil = SKIES["dusk"][3]
    tents = "".join(kit.tent(x, 800, s, sil) for x, s in [(240, 1.2), (420, 1.0), (580, 1.15)])
    brink = B.actor(kit.boer(sil, beard=True, rifle=False, arm_up=False), 1980, 805, "d1-bk", 1.25, face_left=True)
    sons = "".join(B.actor(kit.boer(sil, beard=False, rifle=False, young=True), 2120 + k * 110, 805, f"d1-sn{k}", 1.2, face_left=True) for k in range(2))
    soldiers = "".join(B.place(kit.soldier(sil, rifle=False), x, 805, f"d1-ss{k}", 1.1) for k, x in enumerate([700, 790]))
    html = (
        B.bubble("d1-b1", "חלב טרי! ביצים!", 1040, 360, "r")
        + B.bubble("d1-b2", "אנחנו רק מסתכלים...", 300, 330, "l", 36)
    )
    s2_end = c.t("d1-4") - 0.15
    B.side_shot(c, "d1-s2", s1_end, s2_end, "dusk", tents + soldiers + brink + sons, html, ground_y=810, fade_in="blur")
    tb = c.w("d1-3", "האיכר") - 0.6
    B.walk(c, "d1-bk", tb, -860, 3.0)
    for k in range(2):
        B.walk(c, f"d1-sn{k}", tb + 0.2 + k * 0.2, -860, 3.0)
    B.say(c, "d1-b1", c.w("d1-3", "חלב") - 0.2, c.w("d1-3", "ומסתובבים") - 0.2)
    for k in range(2):
        B.walk(c, f"d1-sn{k}", c.w("d1-3", "ומסתובבים") - 0.3, -1500 - k * 160, 2.4)
    B.say(c, "d1-b2", c.w("d1-3", "ומסתובבים") - 0.1)

    # S3: sentries by a big fire, shouting every half hour
    sil = SKIES["night"][3]
    tents = "".join(kit.tent(x, 800, s, sil) for x, s in [(200, 1.1), (380, 0.95)])
    fire = kit.campfire(820, 806, 1.3, "d1f")
    sentry = B.place(kit.soldier(sil), 960, 806, "d1-sentry", 1.35)
    eyes = "".join(
        f'<g transform="translate({x} {y})"><g id="d1-eye{k}" opacity="0"><ellipse cx="-9" cy="0" rx="6" ry="4" fill="#F7E07A"/><ellipse cx="9" cy="0" rx="6" ry="4" fill="#F7E07A"/></g></g>'
        for k, (x, y) in enumerate([(1350, 760), (1480, 740), (1610, 770), (1740, 750), (1420, 790), (1680, 795)])
    )
    bushes = "".join(kit.bush_side(x, 812, 1.4, sil) for x in (1340, 1470, 1600, 1730, 1860))
    html = B.bubble("d1-b3", "מספר אחת: הכול בסדר!", 820, 300, "r", 46) + B.bubble("d1-b4", "מספר שתיים: הכול בסדר!", 780, 190, "r", 40)
    s3_end = c.t("d1-6") - 0.15
    B.side_shot(c, "d1-s3", s2_end, s3_end, "night", tents + fire + sentry + bushes + eyes, html, ground_y=812, fade_in="blur")
    c.flicker("#d1f-flames", s2_end, s3_end, rate=0.1, seed=3, lo=0.75, hi=1.0, p=0.6)
    tm = c.w("d1-4", "מספר")
    B.say(c, "d1-b3", tm - 0.2, tm + 2.3)
    B.say(c, "d1-b4", tm + 2.4, s3_end - 0.3)
    c.sfx("fire", s2_end, 0.35, dur=s3_end - s2_end, fade_out=0.8)
    c.sfx("cricket", s2_end, 0.2, dur=s3_end - s2_end, fade_out=0.8)
    te = c.w("d1-5", "האויב") - 0.6
    for k in range(6):
        c.fromTo(f"#d1-eye{k}", {"opacity": 0, "scaleY": 0.1, "transformOrigin": "50% 50%"}, {"opacity": 1, "scaleY": 1, "duration": 0.18, "ease": "power2.out"}, round(te + k * 0.25, 3))
    for k in range(6):
        tt = round(te + 1.9 + k * 0.33, 3)
        c.to(f"#d1-eye{k}", {"scaleY": 0.1, "duration": 0.07, "yoyo": True, "repeat": 1, "transformOrigin": "50% 50%"}, tt)

    # S4: dawn, fire from the riverbed
    boers = [(840, 250), (890, 246), (1040, 258), (1100, 256), (1160, 266), (790, 262)]
    lines = []
    for k, (bx, by) in enumerate(boers):
        tx, ty = CAMP[k % len(CAMP)]
        lines.append((f"d1fl{k}", bx, by + 8, tx, ty))
    svg = B.tents_at(c, CAMP, "d1u") + B.tokens_at(c, MEN, "d1n", "brit") + B.tokens_at(c, boers, "d1b", "boer", 1.0, 180) + B.fire_svg(lines) + B.white_flag(985, 300, "d1-flag")
    s4_end = c.t("d1-8") + 0.4
    B.sand_shot(c, "d1-s4", s3_end, s4_end, svg, "", "", cam=(965, 300, 1.95), tint=TINT_DAWN, fade_in="blur")
    ta = c.w("d1-6", "יריות") - 0.1
    B.pop_group(c, "d1b", len(boers), c.w("d1-6", "אפיק") - 0.4, 0.07)
    B.fire_volley(c, lines, ta + 0.2, c.end("d1-7") - 0.4, seed=11)
    c.shake("#d1-s4-cam", ta + 0.25, 7)
    tb = c.w("d1-7", "בבהלה")
    for k in range(len(CAMP)):
        c.to(f"#d1u{k}", {"rotation": 35 - k * 9, "scale": 0.75, "opacity": 0.6, "duration": 0.35, "ease": "power2.in", "transformOrigin": "50% 50%"}, round(tb + k * 0.12, 3))
    for k in range(len(MEN)):
        c.to(f"#d1n{k}", {"x": (k % 3 - 1) * 14, "y": 10, "duration": 0.3, "ease": "power2.out"}, round(tb + 0.1 + k * 0.05, 3))
    c.pop("#d1-flag", c.w("d1-7", "דגל") - 0.1, 0.4)

    # S5: Brink's sons among the Boers
    sil = SKIES["dawn"][3]
    boers_side = "".join(B.place(kit.boer(sil, beard=k % 2 == 0, rifle=True), x, 812, f"d1-bs{k}", 1.25) for k, x in enumerate([1280, 1460, 1640]))
    sons = "".join(B.place(kit.boer(sil, beard=False, rifle=True, young=True), x, 812, f"d1-son{k}", 1.3, flip=True) for k, x in enumerate([820, 980]))
    html = (
        '<div id="d1-ex1" class="abs k-title" style="left:770px; top:300px; font-size:200px; color:#B3261E; opacity:0">!</div>'
        '<div id="d1-ex2" class="abs k-title" style="left:930px; top:300px; font-size:200px; color:#B3261E; opacity:0">!</div>'
        + kit.stamp_img("d1-stamp", "fail", 580, 440, -8)
    )
    s5_end = c.t("d1-9") - 0.15
    B.side_shot(c, "d1-s5", s4_end, s5_end, "dawn", boers_side + sons, html, ground_y=812, fade_in="wipe")
    tf = c.w("d1-8", "מוכרות")
    c.pop("#d1-ex1", tf, 0.3)
    c.pop("#d1-ex2", tf + 0.15, 0.3)
    kit.slam(c, "#d1-stamp", c.end("d1-8") + 0.25)

    # S6: he wakes
    B.wake_shot(c, "d1-wake", s5_end, c.t("L1") - 0.4, "dawn", c.w("d1-9", "בבהלה") - 0.2)
    B.lesson_block(c, ["L1", "L2", "L3", "L4"], c.t("L1") - 0.45, c.dur, prior=0)

    c.music("invest", ce - 0.5, c.t("d1-4") - 0.2)
    c.music("hidden", c.t("d1-4") - 0.2, c.end("d1-8") + 0.4)
    c.music("thinking", c.end("d1-8") + 0.4, c.dur)


# ================================================================ dream 2
def dream2(c):
    ce = card(c, 2)
    cx, cy, r = 965, 345, 86
    ring = f"M {cx - r} {cy} A {r} {r} 0 1 1 {cx + r} {cy} A {r} {r} 0 1 1 {cx - r} {cy}"
    rp = r + 13
    ring_p = f"M {cx - rp} {cy} A {rp} {rp} 0 1 1 {cx + rp} {cy} A {rp} {rp} 0 1 1 {cx - rp} {cy}"
    tents = [(940, 330), (990, 330), (965, 372)]
    men = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in [k * 2 * math.pi / 10 for k in range(10)]]
    # S1: same drift, other men, dig at once
    svg = kit.trench_path(ring, "d2-tr", 13, ring_p) + B.tents_at(c, tents, "d2t") + B.tokens_at(c, men, "d2m", "brit", 0.9)
    s1_end = c.t("d2-3") - 0.15
    over = mini_tablets(c, "d2", 4, c.w("d2-1", "זוכר"))
    B.sand_shot(c, "d2-s1", ce, s1_end, svg, "", over, cam=(965, 380, 1.5), tint=TINT_DAY)
    arrivals(c, "d2m", men, ce + 0.3, (0, 560), 2.2)
    B.pop_group(c, "d2t", 3, ce + 1.2, 0.1)
    td = c.w("d2-2", "לחפור") - 0.1
    c.draw("#d2-tr-cut", td, 2.2)
    c.draw("#d2-tr-par", td + 0.2, 2.2)
    c.sfx("dust", td, 0.25)

    # S2: Brink is politely sent home
    sil = SKIES["dusk"][3]
    brink = B.actor(kit.boer(sil, rifle=False), 1980, 805, "d2-bk", 1.25, face_left=True)
    html = B.lieutenant("d2-lt", 470, 900, 560) + B.bubble("d2-b1", "תודה, לא צריך. להתראות!", 520, 300, "l", 42)
    s2_end = c.t("d2-4") - 0.15
    B.side_shot(c, "d2-s2", s1_end, s2_end, "dusk", brink, html, ground_y=810, fade_in="blur")
    tb = s1_end + 0.2
    B.walk(c, "d2-bk", tb, -880, 2.6)
    B.say(c, "d2-b1", c.w("d2-3", "שולח") - 0.2, c.end("d2-3") - 0.2)
    B.turn(c, "d2-bk", c.w("d2-3", "הביתה"))
    B.walk(c, "d2-bk", c.w("d2-3", "הביתה") + 0.25, 300, 2.4)

    # S3: a quiet night, no fires
    sil = SKIES["night"][3]
    tents_s = "".join(kit.tent(x, 806, s, sil) for x, s in [(300, 1.2), (520, 1.0)])
    sentry = B.place(kit.soldier(sil), 1060, 806, "d2-sentry", 1.2)
    html = "".join(
        f'<div id="d2-z{k}" class="abs k-title" style="left:{560 + k * 50}px; top:{470 - k * 60}px; font-size:{60 + k * 24}px; color:#B9B3E6; opacity:0">z</div>' for k in range(3)
    )
    s3_end = c.t("d2-5") - 0.15
    B.side_shot(c, "d2-s3", s2_end, s3_end, "night", tents_s + sentry, html, ground_y=812, fade_in="blur")
    tz = c.w("d2-4", "לישון") - 0.3
    for k in range(3):
        c.fromTo(f"#d2-z{k}", {"opacity": 0, "y": 20}, {"opacity": 0.9, "y": -30, "duration": 1.4, "ease": "sine.out"}, round(tz + k * 0.35, 3))
    c.sfx("cricket", s2_end, 0.22, dur=s3_end - s2_end, fade_out=0.6)

    # S4: fire from everywhere
    boers = [(800, 270), (860, 250), (1060, 258), (1130, 262), (1200, 290), (1120, 470), (850, 500), (1080, 560), (760, 330)]
    lines = [(f"d2fl{k}", bx, by, cx + (cx - bx) * -0.15, cy + (cy - by) * -0.15) for k, (bx, by) in enumerate(boers)]
    svg = (
        kit.trench_path(ring, "d2-tr2", 13, ring_p) + B.tents_at(c, tents, "d2u") + B.tokens_at(c, men, "d2n", "brit", 0.9)
        + B.tokens_at(c, boers, "d2b", "boer", 1.0) + B.fire_svg(lines)
    )
    s4_end = c.t("d2-6") + 0.2
    B.sand_shot(c, "d2-s4", s3_end, s4_end, svg, "", "", cam=(965, 380, 1.35), tint=TINT_NIGHT, fade_in="blur")
    ta = c.w("d2-5", "יריות")
    B.pop_group(c, "d2b", len(boers), ta - 0.3, 0.06)
    B.fire_volley(c, lines, ta, s4_end + 0.1, seed=21)
    c.fromTo("#d2-s4-tint", {"opacity": 0.55}, {"opacity": 0.3, "duration": 4, "ease": "none"}, s3_end)

    # S5: cross-section: the high bank hides them, the thin wall lets bullets through
    gd = "M -20 760 L 520 760 L 540 700 L 620 700 L 640 760 L 1180 760 L 1240 770 Q 1290 920 1340 930 L 1700 930 L 1940 940 L 1940 1100 L -20 1100 Z"
    sil = "#2a1d12"
    content = (
        B.place(kit.soldier(sil, rifle=True), 580, 720, "d2-xs", 0.9)
        + "".join(B.place(kit.boer(sil, beard=k == 0), x, 930, f"d2-xb{k}", 0.9, flip=True) for k, x in enumerate([1390, 1520]))
        + "".join(kit.bush_side(x, 764, 1.1, "#5E6A2C") for x in (1150, 1230))
        + '<path id="d2-bul" d="M 1360 800 L 600 690" stroke="#F6B33C" stroke-width="6" stroke-dasharray="20 14" pathLength="100" fill="none" opacity="0"/>'
        + '<path id="d2-dist" d="M 640 600 L 1380 600" stroke="#1E1812" stroke-width="4" marker-end="url(#ar)" fill="none" opacity="0"/>'
    )
    labels = (
        '<div id="d2-l1" class="tag" style="left:1400px; top:620px; font-size:36px; opacity:0">הגדה מסתירה אותם</div>'
        '<div id="d2-l2" class="tag dark" style="left:840px; top:520px; font-size:38px; opacity:0">כמה עשרות מטרים</div>'
        '<div id="d2-l3" class="tag red" style="left:380px; top:560px; font-size:38px; opacity:0">סוללה דקה מדי</div>'
    )
    s5_end = c.t("d2-8") - 0.15
    c.shot("d2-s5", s4_end, s5_end, B.section(content, gd, water=False, label_html=labels), fade_in="wipe")
    c.pop("#d2-l1", c.w("d2-6", "הסתירה"), 0.35)
    c.fade("#d2-dist", c.w("d2-6", "מטווח") - 0.2, 0.3)
    c.pop("#d2-l2", c.w("d2-6", "עשרות") - 0.2, 0.35)
    tb = c.t("d2-7") + 0.2
    c.fromTo("#d2-bul", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 0.5, "ease": "power1.in"}, tb)
    c.pop("#d2-l3", c.w("d2-7", "הדקה"), 0.35)
    c.sfx("rifle", tb, 0.5)
    c.sfx("rifle", tb + 0.9, 0.4)

    # S6: white flag; he sat in the worst place
    danger = "".join(
        f'<g transform="translate({x} {y})"><g id="d2-dz{k}" opacity="0"><ellipse rx="{rx}" ry="{ry}" fill="#B3261E" opacity="0.28"/>'
        f'<ellipse rx="{rx}" ry="{ry}" fill="none" stroke="#B3261E" stroke-width="4" stroke-dasharray="10 8"/></g></g>'
        for k, (x, y, rx, ry) in enumerate([(960, 262, 330, 58), (1110, 500, 90, 60), (850, 520, 80, 55)])
    )
    svg = (
        kit.trench_path(ring, "d2-tr3", 13, ring_p) + B.tents_at(c, tents, "d2v") + B.tokens_at(c, men, "d2o", "brit", 0.9)
        + B.tokens_at(c, boers, "d2c", "boer", 1.0) + danger + B.white_flag(975, 320, "d2-flag")
    )
    over = kit.stamp_img("d2-stamp", "fail", 580, 700, 6)
    B.sand_shot(c, "d2-s6", s5_end, c.t("d2-9") - 0.2, svg, "", over, cam=(965, 400, 1.2), tint=TINT_DAWN, fade_in="blur")
    c.pop("#d2-flag", c.t("d2-8") + 0.1, 0.4)
    for k in range(3):
        c.fade(f"#d2-dz{k}", c.w("d2-8", "מוקף") - 0.2 + k * 0.25, 0.4)
    kit.slam(c, "#d2-stamp", c.end("d2-8") + 0.2)

    B.lesson_block(c, ["L5", "L6", "L7"], c.t("d2-9") - 0.3, c.dur, prior=4, title="3 שיעורים חדשים")
    c.music("invest", ce - 0.5, c.t("d2-5") - 0.3)
    c.music("hidden", c.t("d2-5") - 0.3, c.end("d2-8") + 0.3)
    c.music("thinking", c.end("d2-8") + 0.3, c.dur)


# ================================================================ dream 3
def dream3(c):
    ce = card(c, 3)
    (x0, y0), (x1, y1) = geo.TRENCH3
    tr = f"M {x0} {y0} L {x1} {y1}"
    par = f"M {x0} {y0 - 14} L {x1} {y1 - 14}"
    men = [(x0 + 18 + k * 20, y0 + 2) for k in range(9)]
    camp = [(870, 700), (930, 705), (990, 700)]
    # S1: two patrols go out and come back
    p1 = [(960, 330), (980, 345), (1000, 330)]
    p2 = [(940, 360), (960, 375), (980, 360)]
    svg = B.tokens_at(c, p1, "d3p", "brit", 0.9) + B.tokens_at(c, p2, "d3q", "brit", 0.9)
    over = ""
    s1_end = c.t("d3-3") - 0.15
    sv, hv = icon_row(c, "d3ic", [("3 איכרים", "man", 3), ("2 נערים", "child", 2), ("13 פועלים מקומיים", "man", 13)], 860, c.w("d3-2", "שלושה") - 0.2, 0.95)
    over = panel(sv, hv, "d3-panel", 740, 250)
    B.sand_shot(c, "d3-s1", ce, s1_end, svg, "", over, cam=(1150, 420, 0.95), tint=TINT_DAY)
    tp = c.w("d3-1", "סיורים") - 0.4
    B.move_tokens(c, [f"d3p{k}" for k in range(3)], tp, geo.FARM[0] - 990, geo.FARM[1] - 330 + 40, 2.6)
    B.move_tokens(c, [f"d3q{k}" for k in range(3)], tp + 0.3, geo.KOPJE[0] - 960, geo.KOPJE[1] - 370 - 40, 2.6)
    B.move_tokens(c, [f"d3p{k}" for k in range(3)], c.t("d3-2") - 0.3, 0, 0, 2.0)
    B.move_tokens(c, [f"d3q{k}" for k in range(3)], c.t("d3-2") - 0.2, 0, 0, 2.0)
    c.fade("#d3-panel", c.w("d3-2", "שלושה") - 0.4, 0.3)

    # S2: the farmers complain, then dig
    sil = SKIES["gold"][3]
    farmers = "".join(B.actor(kit.boer(sil, beard=True, rifle=False, arm_up=k == 1), x, 812, f"d3-f{k}", 1.25, face_left=True) for k, x in enumerate([1180, 1360, 1540]))
    diggers = "".join(
        f'<g transform="translate({x} 812) scale(1.15)"><g id="d3-dg{k}" opacity="0">{kit.boer(sil, beard=k != 1, rifle=False)}'
        f'<g id="d3-sh{k}"><rect x="20" y="-120" width="6" height="120" fill="{sil}" transform="rotate(30 23 -60)"/><path d="M 52 -22 L 74 -10 L 62 6 L 42 -6 Z" fill="{sil}"/></g></g></g>'
        for k, x in enumerate([1180, 1360, 1540])
    )
    mound = '<path id="d3-mound" d="M 1060 812 Q 1350 760 1660 812 Z" fill="#6b4a26" opacity="0"/>'
    html = B.bubble("d3-b1", "אני אתלונן בלונדון!", 1080, 280, "r", 44) + B.bubble("d3-b2", "בפרלמנט!", 1390, 170, "r", 40)
    s2_end = c.t("d3-4") - 0.15
    B.side_shot(c, "d3-s2", s1_end, s2_end, "gold", farmers + mound + diggers, html, ground_y=812, fade_in="blur")
    B.say(c, "d3-b1", c.w("d3-3", "ומאיימים") - 0.2, c.w("d3-3", "בסוף") - 0.2)
    B.say(c, "d3-b2", c.w("d3-3", "בלונדון") - 0.1, c.w("d3-3", "בסוף") - 0.2)
    for k in range(3):
        c.to(f"#d3-f{k}-b", {"y": -10, "duration": 0.12, "yoyo": True, "repeat": 3}, round(c.w("d3-3", "צועקים") + k * 0.1, 3))
    tdg = c.w("d3-3", "חופרים") - 0.3
    for k in range(3):
        c.to(f"#d3-f{k}", {"opacity": 0, "duration": 0.2}, tdg)
        c.fade(f"#d3-dg{k}", tdg, 0.2)
        for j in range(4):
            c.to(f"#d3-sh{k}", {"rotation": -25 if j % 2 == 0 else 0, "duration": 0.25, "transformOrigin": "23px -60px", "ease": "sine.inOut"}, round(tdg + 0.2 + j * 0.28 + k * 0.07, 3))
    c.fade("#d3-mound", tdg + 0.2, 0.8)
    c.sfx("dust", tdg + 0.3, 0.25)

    # S3: a straight trench 650 m south, the ambush plan
    svg = (
        kit.trench_path(tr, "d3-tr", 13, par) + B.tokens_at(c, men, "d3m", "brit", 0.85) + B.tents_at(c, camp, "d3t", 0.9)
        + f'<path id="d3-meas" d="M {DX + 60} {DY + 30} L {x1 + 40} {y0 - 30}" stroke="#1E1812" stroke-width="4" stroke-dasharray="12 8" fill="none" pathLength="100" opacity="0"/>'
        + "".join(
            f'<path id="d3-ff{k}" d="M {x0 + 30 + k * 60} {y0 - 24} L {x0 - 40 + k * 110} {DY + 40}" stroke="#203A5E" stroke-width="5" stroke-dasharray="14 10" fill="none" pathLength="100" opacity="0"/>'
            for k in range(3)
        )
    )
    pins = kit.pin(DX + 120, (DY + y0) / 2 + 30, "650 מ'", "d3-pin1", "dark") + kit.pin(x0 + 40, y0 + 150, "קו ישר, 50 מ'", "d3-pin2") + kit.pin(DX + 30, DY + 60, "מארב", "d3-pin3", "navy")
    s3_end = c.t("d3-6") - 0.15
    B.sand_shot(c, "d3-s3", s2_end, s3_end, svg, pins, "", cam=(910, 470, 1.35), tint=TINT_DAY, fade_in="blur")
    tt = c.w("d3-4", "רמה") - 0.2
    c.draw("#d3-tr-cut", tt, 1.6)
    c.draw("#d3-tr-par", tt + 0.2, 1.6)
    B.pop_group(c, "d3m", len(men), tt + 1.0, 0.05)
    B.pop_group(c, "d3t", len(camp), tt + 1.4, 0.08)
    c.fromTo("#d3-meas", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 1.0}, c.w("d3-4", "650") - 0.4)
    c.pop("#d3-pin1", c.w("d3-4", "650"), 0.35)
    c.pop("#d3-pin2", c.w("d3-4", "ישר"), 0.35)
    c.fromTo("#d3-tr-par", {"strokeWidth": 12}, {"strokeWidth": 22, "duration": 0.5, "ease": "back.out(2)"}, c.w("d3-4", "גבוהה") - 0.1)
    for k in range(3):
        c.fromTo(f"#d3-ff{k}", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 0.9}, round(c.w("d3-5", "לחכות") + k * 0.2, 3))
    c.pop("#d3-pin3", c.w("d3-5", "מפתיעה") - 0.2, 0.35)

    # S4: dust cloud, the column halts and splits; then the guns
    col = [(1004 - k * 2, -40 + k * 34) for k in range(7)]
    guns = [(1560, 150), (1640, 190)]
    puffs = [(860, 600), (920, 585), (980, 605), (900, 625)]
    dust = "".join(kit.puff(1000 + (k - 2) * 50, 40 + (k % 2) * 30, f"d3d{k}", 40, "#E7D2A6") for k in range(5))
    arcs = "".join(
        f'<path id="d3-arc{k}" d="M {gx} {gy} Q {(gx + px) / 2} {min(gy, py) - 260} {px} {py}" stroke="#1E1812" stroke-width="3" stroke-dasharray="8 8" fill="none" pathLength="100" opacity="0"/>'
        for k, ((gx, gy), (px, py)) in enumerate(zip(guns * 2, puffs))
    )
    svg = (
        kit.trench_path(tr, "d3-tr2", 13, par) + B.tokens_at(c, men, "d3n", "brit", 0.85) + B.tents_at(c, camp, "d3u", 0.9) + dust
        + B.tokens_at(c, col, "d3c", "boer", 1.0) + "".join(kit.token_gun(x, y, 1.3, f'id="d3g{k}"', -60) for k, (x, y) in enumerate(guns)) + arcs
        + "".join(kit.puff(x, y - 40, f"d3pf{k}", 30) for k, (x, y) in enumerate(puffs))
    )
    over = '<div id="d3-q" class="abs k-title" style="left:1080px; top:180px; font-size:200px; color:#B3261E; opacity:0">?</div>'
    s4_end = c.t("d3-9") - 0.15
    B.sand_shot(c, "d3-s4", s3_end, s4_end, svg, "", over, cam=(1000, 330, 1.05), tint=TINT_DAY, fade_in="blur")
    td = c.w("d3-6", "אבק") - 0.3
    for k in range(5):
        c.fromTo(f"#d3d{k}", {"opacity": 0, "scale": 0.5}, {"opacity": 0.85, "scale": 1.3, "y": 60, "duration": 3.0, "ease": "sine.out", "transformOrigin": "50% 50%"}, round(td + k * 0.15, 3))
    for k in range(len(col)):
        c.fromTo(f"#d3c{k}", {"opacity": 0, "y": -200}, {"opacity": 1, "y": 0, "duration": 3.5, "ease": "power1.out"}, round(td + 0.6 + k * 0.15, 3))
    ts = c.w("d3-7", "עוצרים") - 0.1
    for k in range(len(col)):
        dx = (-1 if k % 2 == 0 else 1) * (160 + k * 30)
        c.to(f"#d3c{k}", {"x": dx, "y": 40 + k * 6, "duration": 1.6, "ease": "power2.out"}, round(ts + 0.3 + k * 0.05, 3))
    c.pop("#d3-q", c.w("d3-7", "הזהיר") - 0.2, 0.35)
    tg = c.w("d3-8", "תותחים") - 0.3
    c.out("#d3-q", tg - 0.3)
    c.cam("#d3-s4-cam", tg - 0.6, 1230, 420, 0.95, dur=1.0)
    for k in range(2):
        c.pop(f"#d3g{k}", round(tg + k * 0.15, 3), 0.35, origin="50% 50%")
    tr_ = c.w("d3-8", "רסיסים") - 0.3
    for k in range(4):
        t_ = round(tr_ + k * 0.7, 3)
        c.fromTo(f"#d3-arc{k}", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 0.5, "ease": "power1.in"}, t_)
        c.fromTo(f"#d3pf{k}", {"opacity": 0, "scale": 0.3}, {"opacity": 0.95, "scale": 1.4, "duration": 0.35, "ease": "power3.out", "transformOrigin": "50% 50%"}, t_ + 0.5)
        c.to(f"#d3pf{k}", {"opacity": 0, "duration": 1.6}, t_ + 1.2)
        c.sfx("boom", t_ + 0.5, 0.4)
    c.sfx("cannon", tg + 0.1, 0.45)

    # S5: the parapet that says "here!"
    sil = SKIES["day"][3]
    gd = "M -20 800 L 640 800 Q 760 690 880 690 Q 1000 690 1120 800 L 1940 800 L 1940 1100 L -20 1100 Z"
    burst = "".join(
        f'<g transform="translate({x} {y})"><g id="d3-sb{k}" opacity="0"><circle r="54" fill="#EEE6D6"/><circle cx="40" cy="-20" r="38" fill="#E4DACA"/>'
        + "".join(f'<circle cx="{(j - 3) * 16}" cy="{60 + (j % 3) * 22}" r="4" fill="#3a2a1c"/>' for j in range(7))
        + "</g></g>"
        for k, (x, y) in enumerate([(760, 420), (980, 380), (880, 300)])
    )
    heads = "".join(B.place(kit.soldier(sil, rifle=False), x, 760, f"d3-hd{k}", 0.75) for k, x in enumerate([1000, 1060, 1120]))
    sign = (
        '<g transform="translate(880 690)"><g id="d3-sign" opacity="0"><rect x="-4" y="-260" width="9" height="260" fill="#3b2a1c"/>'
        '<rect x="-150" y="-380" width="300" height="140" rx="12" fill="#B3261E" stroke="#5d120e" stroke-width="6"/>'
        '<text x="0" y="-282" text-anchor="middle" font-family="Karantina" font-weight="700" font-size="110" fill="#FFF3E6">כאן!</text></g></g>'
    )
    content = f'<path d="{gd}" fill="{sil}"/>' + heads + sign + burst
    s5_end = c.t("d3-10") - 0.15
    B.side_shot(c, "d3-s5", s4_end, s5_end, "day", content, "", ground_y=820, fade_in="wipe", hills=True)
    c.fromTo("#d3-sign", {"opacity": 0, "y": 200}, {"opacity": 1, "y": 0, "duration": 0.45, "ease": "back.out(1.8)"}, c.w("d3-9", "כמו") - 0.1)
    for k in range(3):
        t_ = round(c.w("d3-9", "הרסיסים") - 0.6 + k * 0.45, 3)
        c.fromTo(f"#d3-sb{k}", {"opacity": 0, "scale": 0.3}, {"opacity": 1, "scale": 1.2, "duration": 0.3, "ease": "power3.out", "transformOrigin": "50% 50%"}, t_)
        c.sfx("boom", t_, 0.35)
    for k in range(3):
        c.to(f"#d3-hd{k}", {"y": 60, "duration": 0.25, "ease": "power2.in"}, round(c.w("d3-9", "הרסיסים") - 0.4 + k * 0.1, 3))

    # S6: the women at the farm
    sil = SKIES["gold"][3]
    house = B.place(kit.farmhouse_side(sil), 760, 812, "d3-house", 1.4)
    women = "".join(B.place(kit.woman(sil, arm_up=True), x, 812, f"d3-w{k}", 1.3) for k, x in enumerate([1100, 1220]))
    cloth = '<g transform="translate(1262 560)"><g id="d3-cloth"><path d="M 0 0 C 30 -10, 50 10, 80 0 L 80 40 C 50 50, 30 30, 0 40 Z" fill="#FBF7EE"/></g></g>'
    html = '<div id="d3-l1" class="tag rust" style="left:1300px; top:250px; font-size:44px; opacity:0">הנשים בחווה</div>' + kit.stamp_img("d3-stamp", "fail", 300, 120, -6)
    B.side_shot(c, "d3-s6", s5_end, c.t("d3-11") - 0.2, "gold", house + women + cloth, html, ground_y=812, fade_in="blur")
    for j in range(8):
        c.to("#d3-cloth", {"rotation": 14 if j % 2 == 0 else -10, "duration": 0.3, "ease": "sine.inOut", "transformOrigin": "0% 50%"}, round(s5_end + 0.4 + j * 0.3, 3))
    c.pop("#d3-l1", c.w("d3-10", "הנשים") - 0.1, 0.35, origin="50% 50%")
    kit.slam(c, "#d3-stamp", c.w("d3-10", "לאסוף") + 0.3)

    B.lesson_block(c, ["L8", "L9", "L10"], c.t("d3-11") - 0.3, c.dur, prior=7, title="3 שיעורים חדשים")
    c.music("invest", ce - 0.5, c.t("d3-6") - 0.3)
    c.music("hidden", c.t("d3-6") - 0.3, c.end("d3-10") + 0.3)
    c.music("thinking", c.end("d3-10") + 0.3, c.dur)


# ================================================================ dream 4
def dream4(c):
    ce = card(c, 4)
    (x0, y0), (x1, y1) = geo.TRENCH3
    tr = f"M {x0} {y0} L {x1} {y1}"
    par = f"M {x0} {y0 - 10} L {x1} {y1 - 10}"
    men = [(x0 + 18 + k * 20, y0 + 1) for k in range(9)]
    shelter = [(640, 800), (690, 795), (740, 790)]
    # S1: everyone, women and children too
    s1_end = c.t("d4-2") - 0.15
    sv, hv = icon_row(c, "d4ic", [("איכרים", "man", 4), ("נשים", "woman", 6), ("ילדים", "child", 5), ("פועלים מקומיים", "man", 10)], 860, c.w("d4-1", "כולם") - 0.2, 0.85)
    over = panel(sv, hv, "d4-panel", 740, 250)
    B.sand_shot(c, "d4-s1", ce, s1_end, "", "", over, cam=(1150, 420, 0.95), tint=TINT_DAY)
    c.fade("#d4-panel", c.w("d4-1", "כולם") - 0.4, 0.3)

    # S2-S3: the ladies, the sergeant's advice, the march
    sil = SKIES["gold"][3]
    ladies = "".join(
        f'<g transform="translate({x} 812) scale(-1.25 1.25)"><g id="d4-lw{k}"><g id="d4-l{k}"><g id="d4-la{k}">{kit.woman(sil, arm_up=False)}</g>'
        f'<g id="d4-lu{k}" opacity="0">{kit.woman(sil, arm_up=True)}</g></g></g></g>'
        for k, x in enumerate([1180, 1330, 1480, 1630])
    )
    sgt = B.place(kit.soldier(sil, rifle=False, extra='<path d="M -10 -142 Q 1 -136 12 -142 L 12 -138 Q 1 -132 -10 -138 Z" fill="#000"/>'), 760, 812, "d4-sgt", 1.3)
    can = (
        '<g transform="translate(840 700)"><g id="d4-can" opacity="0"><rect x="-34" y="-50" width="68" height="64" rx="6" fill="#B3452A" stroke="#5b1f10" stroke-width="4"/>'
        '<rect x="-8" y="-66" width="16" height="18" fill="#5b1f10"/><text x="0" y="-6" text-anchor="middle" font-family="Rubik" font-weight="700" font-size="28" fill="#FFF0E2">נפט</text></g></g>'
    )
    html = (
        B.lieutenant("d4-lt", 330, 905, 560)
        + B.bubble("d4-b0", "!!!", 1240, 300, "r", 64)
        + B.bubble("d4-b00", "לא זזות!", 1500, 220, "r", 52)
        + B.bubble("d4-b1", "מה הדרך הכי טובה לפנות בית?", 330, 210, "l", 44)
        + B.bubble("d4-b2", "כמה טיפות נפט בפינה...", 600, 330, "l", 44)
    )
    s3_end = c.t("d4-6") - 0.15
    B.side_shot(c, "d4-s2", s1_end, s3_end, "gold", ladies + sgt + can, html, ground_y=812, fade_in="blur")
    c.set("#d4-lt", {"opacity": 0}, s1_end)
    c.set("#d4-sgt", {"opacity": 0}, s1_end)
    ta = c.t("d4-2")
    for k in range(4):
        for j in range(6):
            tt = round(ta + 0.3 + j * 0.45 + k * 0.11, 3)
            c.set(f"#d4-la{k}", {"opacity": 0 if j % 2 == 0 else 1}, tt)
            c.set(f"#d4-lu{k}", {"opacity": 1 if j % 2 == 0 else 0}, tt)
    B.say(c, "d4-b0", c.w("d4-2", "צועקות") - 0.1, c.end("d4-2"))
    B.say(c, "d4-b00", c.w("d4-2", "ומסרבות") - 0.1, c.end("d4-2"))
    c.fade("#d4-lt", c.t("d4-3") - 0.3, 0.3)
    c.fade("#d4-sgt", c.t("d4-3") - 0.1, 0.3)
    B.say(c, "d4-b1", c.w("d4-3", "מה") - 0.2, c.t("d4-4") + 0.3)
    B.say(c, "d4-b2", c.w("d4-4", "טיפות") - 0.2, c.end("d4-4") + 0.4)
    c.pop("#d4-can", c.w("d4-4", "נפט"), 0.35)
    tm = c.t("d4-5") - 0.1
    for k in range(4):
        c.to(f"#d4-l{k}", {"x": 1500, "duration": 2.2, "ease": "power2.in"}, round(tm + 0.2 + k * 0.08, 3))

    # S4: a narrow hidden trench, women in the gully, then the flanking move and enfilade
    flank = [(700, 140), (660, 170), (620, 150), (680, 190)]
    route = "M 680 160 C 520 260, 470 420, 500 620 C 520 740, 560 790, 620 805 C 700 820, 780 790, 840 770"
    main_ = [(1004 - k * 2, -40 + k * 34) for k in range(5)]
    hill_boers = [(1090, 560), (1120, 600)]
    lines = [(f"d4fl{k}", 700 + k * 40, 780, 830 + k * 40, y0 + 6) for k in range(4)]
    lines += [(f"d4fl{k + 4}", hx, hy, x1 - 10, y0) for k, (hx, hy) in enumerate(hill_boers)]
    enf = f'<path id="d4-enf" d="M {x0 - 120} {y0} L {x1 + 40} {y1}" stroke="#F6B33C" stroke-width="8" stroke-dasharray="26 18" fill="none" pathLength="100" opacity="0"/>'
    front = (
        f'<g id="d4-front" opacity="0"><path d="M {x0} {y0 - 20} L {x0 - 60} {y0 - 260} L {x1 + 60} {y0 - 260} L {x1} {y0 - 20} Z" fill="#203A5E" opacity="0.18"/>'
        f'<path d="M {(x0 + x1) / 2} {y0 - 30} L {(x0 + x1) / 2} {y0 - 230}" stroke="#203A5E" stroke-width="10" marker-end="url(#arN)" fill="none"/></g>'
    )
    others = "".join(
        f'<path id="d4-oa{k}" d="{d}" stroke="#B3261E" stroke-width="10" fill="none" stroke-linecap="round" pathLength="100" opacity="0"/>'
        for k, d in enumerate([f"M {x0 - 260} {y0} L {x0 - 40} {y0}", f"M {x1 + 260} {y0 + 10} L {x1 + 40} {y0}", f"M {(x0 + x1) / 2} {y0 + 240} L {(x0 + x1) / 2} {y0 + 40}"])
    )
    defs = (
        '<defs><marker id="arN" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#203A5E"/></marker></defs>'
    )
    svg = (
        defs + kit.trench_path(tr, "d4-tr", 8, par, hidden=True) + B.tokens_at(c, men, "d4m", "brit", 0.8)
        + "".join(kit.person_icon(x, y, "woman", 1.0, "#1E1812", f'id="d4w{k}"') for k, (x, y) in enumerate(shelter))
        + B.tokens_at(c, main_, "d4c", "boer") + B.tokens_at(c, flank, "d4f", "boer") + B.tokens_at(c, hill_boers, "d4h", "boer")
        + f'<path id="d4-route" d="{route}" stroke="#B3452A" stroke-width="6" stroke-dasharray="14 10" fill="none" pathLength="100" opacity="0"/>'
        + B.fire_svg(lines) + enf + front + others + B.white_flag(905, 610, "d4-flag")
    )
    pins = kit.pin(x1 + 40, y0 - 60, "צרה, עמוקה, מוסתרת", "d4-pin1", "navy") + kit.pin(620, 880, "מחסה בערוץ", "d4-pin2")
    over = (
        '<div id="d4-enf-l" class="tag red" style="left:120px; top:120px; font-size:52px; opacity:0">אש אנפילדית = אש לאורך השורה</div>'
        '<div id="d4-front-l" class="tag navy" style="left:120px; top:120px; font-size:52px; opacity:0">חזית אחת בלבד</div>'
        '<div id="d4-nine" class="tag dark" style="left:120px; top:120px; font-size:52px; opacity:0">9 שיעורים חדשים</div>'
        + kit.stamp_img("d4-stamp", "fail", 1080, 700, 7)
    )
    B.sand_shot(c, "d4-s4", s3_end, c.t("L11") - 0.4, svg, pins, over, cam=(905, 620, 1.6), tint=TINT_DAY, fade_in="blur")
    cam = "#d4-s4-cam"
    tt = c.w("d4-6", "צרה") - 0.2
    c.draw("#d4-tr-cut", tt, 1.4)
    c.draw("#d4-tr-par", tt + 0.2, 1.4)
    B.pop_group(c, "d4m", len(men), tt + 0.8, 0.05)
    c.pop("#d4-pin1", c.w("d4-6", "מוסתרת"), 0.35)
    tg = c.w("d4-6", "ערוץ") - 0.4
    c.cam(cam, tg - 0.3, 760, 700, 1.6, dur=1.0)
    for k in range(3):
        c.pop(f"#d4w{k}", round(tg + k * 0.1, 3), 0.3)
    c.pop("#d4-pin2", tg + 0.3, 0.35)
    te = c.t("d4-7")
    c.cam(cam, te - 0.2, 900, 420, 0.95, dur=1.4)
    for k in range(len(main_)):
        c.fromTo(f"#d4c{k}", {"opacity": 0, "y": -200}, {"opacity": 1, "y": 120, "duration": 3.0, "ease": "power1.out"}, round(te + 0.3 + k * 0.15, 3))
    for k in range(len(flank)):
        c.fromTo(f"#d4f{k}", {"opacity": 0}, {"opacity": 1, "duration": 0.3}, round(te + 1.0 + k * 0.1, 3))
    tf = c.w("d4-8", "מקיפים") - 0.3
    c.fromTo("#d4-route", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 2.4, "ease": "power1.inOut"}, tf)
    for k in range(len(flank)):
        c.to(f"#d4f{k}", {"x": 700 + k * 40 - flank[k][0], "y": 780 - flank[k][1], "duration": 3.2, "ease": "power1.inOut"}, round(tf + 0.2 + k * 0.15, 3))
    for k in range(len(hill_boers)):
        c.pop(f"#d4h{k}", round(tf + 1.5 + k * 0.2, 3), 0.3, origin="50% 50%")
    tb = c.w("d4-9", "מהגב") - 0.3
    c.cam(cam, tb - 0.4, 880, 690, 1.45, dur=1.0)
    B.fire_volley(c, lines, tb, c.end("d4-9") - 0.2, seed=41)
    tx = c.w("d4-9", "כדור") - 0.2
    c.cam(cam, tx - 0.3, 905, 640, 2.3, dur=0.9)
    c.fromTo("#d4-enf", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 1.6, "ease": "none"}, tx + 0.4)
    for k in range(len(men)):
        c.to(f"#d4m{k}", {"scale": 0.6, "opacity": 0.45, "duration": 0.15, "transformOrigin": "50% 50%"}, round(tx + 0.5 + k * 0.17, 3))
    c.blur_in("#d4-enf-l", c.w("d4-9", "אנפילדית") - 0.4)
    tfr = c.t("d4-10")
    c.out("#d4-enf-l", tfr - 0.1)
    c.cam(cam, tfr, 905, 560, 1.15, dur=1.0)
    c.fade("#d4-front", c.w("d4-10", "לכיוון") - 0.3, 0.4)
    c.blur_in("#d4-front-l", c.w("d4-10", "צפונה") - 0.2)
    for k in range(3):
        c.fromTo(f"#d4-oa{k}", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 0.5}, round(c.w("d4-10", "צד") - 0.3 + k * 0.2, 3))
    t11 = c.t("d4-11")
    c.out("#d4-front-l", t11 - 0.1)
    c.pop("#d4-flag", t11 + 0.1, 0.4)
    kit.slam(c, "#d4-stamp", c.w("d4-11", "תבוסה"))
    c.blur_in("#d4-nine", c.w("d4-11", "תשעה") - 0.1)

    B.lesson_block(c, ["L11", "L12", "L13", "L14", "L15", "L16", "L17", "L18", "L19"], c.t("L11") - 0.45, c.dur, prior=10)
    c.music("sneaky", ce - 0.5, c.t("d4-6") - 0.3)
    c.music("invest", c.t("d4-6") - 0.3, c.t("d4-8") - 0.3)
    c.music("hidden", c.t("d4-8") - 0.3, c.end("d4-11") + 0.3)
    c.music("thinking", c.end("d4-11") + 0.3, c.dur)
