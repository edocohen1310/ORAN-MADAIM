"""Dream five, dream six (the one that works) and the closing summary."""
import math

import blocks as B
import geo
import kit
from kit import SKIES
from scenes_b import TINT_DAWN, TINT_DAY, TINT_NIGHT, card, icon_row, panel

DX, DY = geo.DRIFT
KX, KY = geo.KOPJE


def along_road(t0, t1, n=6):
    pts = geo.sample(geo.ROAD, 8)
    i0, i1 = int(len(pts) * t0), int(len(pts) * t1)
    seg = pts[i0:i1]
    step = max(1, len(seg) // n)
    return [(p[0], p[1]) for p in seg[::step]]


def road_keys(c, uid, start_xy, t, t0, t1, dur):
    """Move a token along the road between fractions t0..t1 of its length."""
    way = along_road(t0, t1, 10)
    sx, sy = start_xy
    keys = [{"x": round(x - sx, 1), "y": round(y - sy, 1), "duration": round(dur / len(way), 3), "ease": "none"} for x, y in way]
    c.to(f"#{uid}", {"keyframes": keys}, t)


def arc_path(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)) * 0.8
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)) * 0.8
    return f"M {x0:.1f} {y0:.1f} A {r} {r * 0.8:.1f} 0 0 1 {x1:.1f} {y1:.1f}"


# ================================================================ dream 5
def dream5(c):
    ce = card(c, 5)
    # S1: the books say "take the high ground"
    sil = SKIES["gold"][3]
    content = B.place(kit.books(sil), 640, 820, "d5-books", 1.7)
    html = (
        B.lieutenant("d5-lt", 1450, 960, 600)
        + '<div id="d5-19" class="tag dark" style="right:120px; top:110px; font-size:48px; opacity:0">19 שיעורים</div>'
        + '<div id="d5-rule" class="tag red" style="left:250px; top:260px; font-size:60px; opacity:0">תפוס את הגבעה השולטת!</div>'
    )
    s1_end = c.t("d5-2") - 0.15
    B.side_shot(c, "d5-s1", ce, s1_end, "gold", content, html, ground_y=820)
    c.pop("#d5-19", c.t("d5-1") + 0.1, 0.35, origin="50% 50%")
    c.fromTo("#d5-books", {"y": 60, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.5, "ease": "power3.out"}, c.w("d5-1", "הספרים") - 0.3)
    c.fromTo("#d5-rule", {"opacity": 0, "scale": 1.6, "rotation": -4}, {"opacity": 1, "scale": 1, "rotation": -2, "duration": 0.25, "ease": "power4.in"}, c.w("d5-1", "תפוס") - 0.1)
    c.sfx("stamp", c.w("d5-1", "תפוס") + 0.12, 0.45)

    # S2: up on the kopje
    sil = SKIES["day"][3]
    content = kit.kopje_side(960, 860, 1300, 420, sil, huts=True)
    html = B.lieutenant("d5-lt2", 1000, 452, 200)
    s2_end = c.t("d5-3") - 0.15
    B.side_shot(c, "d5-s2", s1_end, s2_end, "day", content, html, ground_y=860, fade_in="blur")
    c.fromTo("#d5-s2-cam", {"scale": 1.0, "y": 0, "transformOrigin": "52% 40%"}, {"scale": 1.25, "y": 120, "duration": s2_end - s1_end, "ease": "power1.inOut"}, s1_end)

    # S3: a ring of short trenches round the kraal; the Boers ring the hill and are held off
    arcs, comm = [], []
    for k in range(10):
        a = k * 36
        arcs.append(kit.trench_path(arc_path(KX, KY, 104, a - 12, a + 12), f"d5a{k}", 9, arc_path(KX, KY, 116, a - 12, a + 12)))
        x, y = KX + 104 * math.cos(math.radians(a)), KY + 104 * math.sin(math.radians(a)) * 0.8
        comm.append(f'<path id="d5c{k}" d="M {x:.1f} {y:.1f} L {KX + (x - KX) * 0.45:.1f} {KY + (y - KY) * 0.45:.1f}" stroke="#4A321C" stroke-width="5" pathLength="100" fill="none"/>')
    men = [(KX + 104 * math.cos(math.radians(k * 36)), KY + 104 * math.sin(math.radians(k * 36)) * 0.8) for k in range(10)]
    ring_boers = [(KX + 330 * math.cos(math.radians(k * 30 + 10)), KY + 270 * math.sin(math.radians(k * 30 + 10))) for k in range(12)]
    lines = [(f"d5fl{k}", bx, by, KX + (bx - KX) * 0.42, KY + (by - KY) * 0.42) for k, (bx, by) in enumerate(ring_boers)]
    locals_ = [(KX + 260, KY + 150 + k * 4) for k in range(6)]
    svg = (
        "".join(comm) + "".join(arcs) + B.tokens_at(c, men, "d5m", "brit", 0.75)
        + "".join(kit.person_icon(x - k * 20, y, "man" if k % 2 else "woman", 1.0, "#1E1812", f'id="d5l{k}"') for k, (x, y) in enumerate(locals_))
        + B.tokens_at(c, ring_boers, "d5b", "boer") + B.fire_svg(lines)
    )
    pins = kit.pin(KX + 160, KY - 120, "הגנה היקפית", "d5-pin1", "navy")
    over = '<div id="d5-good" class="tag navy" style="left:120px; top:110px; font-size:52px; opacity:0">עמדה מצוינת</div>'
    s3_end = c.t("d5-5") - 0.15
    B.sand_shot(c, "d5-s3", s2_end, s3_end, svg, pins, over, cam=(KX, KY, 1.7), tint=TINT_DAY, fade_in="blur")
    td = c.w("d5-3", "חופר") - 0.2
    for k in range(10):
        c.draw(f"#d5a{k}-cut", round(td + k * 0.18, 3), 0.5)
        c.draw(f"#d5a{k}-par", round(td + 0.1 + k * 0.18, 3), 0.5)
    B.pop_group(c, "d5m", 10, td + 1.8, 0.06)
    tc = c.w("d5-3", "קשר") - 0.3
    for k in range(10):
        c.draw(f"#d5c{k}", round(tc + k * 0.05, 3), 0.5)
    c.pop("#d5-pin1", c.w("d5-3", "היקפית") - 0.2, 0.35)
    tl_ = c.w("d5-3", "המקומיים") - 0.3
    for k in range(6):
        c.to(f"#d5l{k}", {"x": KX - locals_[k][0] + k * 3, "y": KY - locals_[k][1], "opacity": 0, "duration": 1.6, "ease": "power2.inOut"}, round(tl_ + k * 0.1, 3))
    tb = c.t("d5-4")
    c.cam("#d5-s3-cam", tb - 0.2, KX, KY - 20, 1.05, dur=1.2)
    B.pop_group(c, "d5b", len(ring_boers), tb + 0.6, 0.06)
    B.fire_volley(c, lines, c.w("d5-4", "יורים") - 0.1, c.end("d5-4") - 0.3, seed=51)
    c.blur_in("#d5-good", c.w("d5-4", "מצוינת") - 0.2)

    # S4: from up here you cannot see the drift
    sight = f'<path id="d5-sight" d="M {KX - 20} {KY - 40} L {DX + 10} {DY + 20}" stroke="#203A5E" stroke-width="7" stroke-dasharray="16 12" fill="none" pathLength="100" opacity="0"/>'
    block = f'<g transform="translate({(KX + DX) / 2 + 40} {(KY + DY) / 2 + 60})"><g id="d5-x" opacity="0"><path d="M -30 -30 L 30 30 M 30 -30 L -30 30" stroke="#B3261E" stroke-width="16" stroke-linecap="round"/></g></g>'
    svg = "".join(arcs).replace('id="d5a', 'id="d5e') + B.tokens_at(c, men, "d5n", "brit", 0.75) + sight + block
    over = f'<div id="d5-q" class="abs k-title" style="left:{DX - 40}px; top:{DY - 260}px; font-size:200px; color:#B3261E; opacity:0">?</div>'
    s4_end = c.t("d5-6") - 0.15
    B.sand_shot(c, "d5-s4", s3_end, s4_end, svg, "", over, cam=(1080, 500, 1.15), tint=TINT_DAY, fade_in="blur")
    c.fromTo("#d5-sight", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 1.0}, c.w("d5-5", "מהחפירות") - 0.2)
    c.pop("#d5-x", c.w("d5-5", "לראות") - 0.1, 0.3, origin="50% 50%")
    c.pop("#d5-q", c.w("d5-5", "המעבר") - 0.1, 0.35)

    # S5: cross-section of a convex slope and its dead ground
    gd = "M -20 870 L 900 860 C 980 850, 1020 800, 1050 760 C 1150 560, 1350 380, 1500 380 L 1940 380 L 1940 1100 L -20 1100 Z"
    dead = "M 1340 412 L 420 870 L 900 860 C 980 850, 1020 800, 1050 760 C 1150 560, 1300 440, 1340 418 Z"
    content = (
        f'<defs><pattern id="hatch" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="18" height="18" fill="#B3261E" opacity="0.18"/>'
        f'<line x1="0" y1="0" x2="0" y2="18" stroke="#B3261E" stroke-width="5" opacity="0.55"/></pattern></defs>'
        f'<path id="d5-dead" d="{dead}" fill="url(#hatch)" opacity="0"/>'
        + B.place(kit.soldier("#2a1d12"), 1580, 380, "d5-xs", 0.9)
        + '<path id="d5-los" d="M 1580 296 L 260 950" stroke="#203A5E" stroke-width="6" stroke-dasharray="18 12" fill="none" pathLength="100" opacity="0"/>'
        + '<path d="M 500 868 Q 560 885 620 866" stroke="#4C8C86" stroke-width="16" fill="none" stroke-linecap="round"/>'
    )
    labels = (
        '<div id="d5-l1" class="tag navy" style="left:760px; top:430px; font-size:40px; opacity:0">קו הראייה</div>'
        '<div id="d5-l2" class="tag red" style="left:820px; top:760px; font-size:46px; opacity:0">שטח מת</div>'
        '<div id="d5-l3" class="tag" style="left:440px; top:920px; font-size:38px; opacity:0">המעבר</div>'
    )
    s5_end = c.t("d5-7") - 0.15
    c.shot("d5-s5", s4_end, s5_end, B.section(content, gd, label_html=labels), fade_in="wipe")
    c.fromTo("#d5-los", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 1.4}, c.w("d5-6", "מעוגל") - 0.2)
    c.pop("#d5-l1", c.w("d5-6", "כדור") - 0.1, 0.35)
    c.fade("#d5-dead", c.w("d5-6", "העיקול") - 0.1, 0.6)
    c.pop("#d5-l2", c.w("d5-6", "מת") - 0.2, 0.35)
    c.pop("#d5-l3", c.w("d5-6", "לירות") + 0.2, 0.35)

    # S6: the drift lies in the dead ground; the convoy crosses and rides south
    poly = "M 750 190 L 1180 190 L 1215 330 L 1130 440 L 960 480 L 815 440 L 735 320 Z"
    deadmap = (
        f'<defs><pattern id="hatch2" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="18" height="18" fill="#B3261E" opacity="0.12"/>'
        f'<line x1="0" y1="0" x2="0" y2="18" stroke="#B3261E" stroke-width="4" opacity="0.4"/></pattern></defs>'
        f'<path id="d5-dm" d="{poly}" fill="url(#hatch2)" stroke="#B3261E" stroke-width="4" stroke-dasharray="12 8" opacity="0"/>'
    )
    convoy_start = along_road(0.0, 0.02, 1)[0]
    convoy = "".join(
        f'<g transform="translate({convoy_start[0]:.1f} {convoy_start[1]:.1f})"><g id="d5v{k}" opacity="0">'
        f'<ellipse cx="3" cy="7" rx="20" ry="12" fill="#000" opacity="0.3"/><path d="M 0 22 L 19 -14 L -19 -14 Z" fill="#7a2a18" stroke="#FFF3E6" stroke-width="4" stroke-linejoin="round"/></g></g>'
        for k in range(8)
    )
    svg = deadmap + "".join(arcs).replace('id="d5a', 'id="d5f') + B.tokens_at(c, men, "d5o", "brit", 0.75) + convoy
    over = (
        '<div id="d5-dl" class="tag red" style="left:120px; top:110px; font-size:52px; opacity:0">המעבר בתוך השטח המת</div>'
        '<div id="d5-safe" class="tag navy" style="left:120px; top:110px; font-size:52px; opacity:0">כמעט ללא נפגעים</div>'
        + kit.stamp_img("d5-stamp", "fail", 580, 720, -5)
    )
    s6_end = c.t("d5-10") - 0.15
    B.sand_shot(c, "d5-s6", s5_end, s6_end, svg, "", over, cam=(1040, 520, 1.0), tint=TINT_DAY, fade_in="blur")
    c.fade("#d5-dm", c.t("d5-7") + 0.1, 0.5)
    c.blur_in("#d5-dl", c.w("d5-7", "בדיוק") - 0.2)
    tv = c.t("d5-8") + 0.3
    c.out("#d5-dl", tv)
    for k in range(8):
        c.set(f"#d5v{k}", {"opacity": 1}, round(tv + k * 0.55, 3))
        road_keys(c, f"d5v{k}", convoy_start, round(tv + k * 0.55, 3), 0.0, 1.0, 8.5)
    c.blur_in("#d5-safe", c.t("d5-9") + 0.1)
    c.out("#d5-safe", c.w("d5-9", "המשימה") - 0.3)
    kit.slam(c, "#d5-stamp", c.w("d5-9", "נכשלה") - 0.1)

    # S7: the colonel
    inner = (
        '<div class="full" style="background:radial-gradient(ellipse at 50% 55%, #A2483A 0%, #6E2A20 60%, #3c140e 100%)"></div>'
        f'<svg class="stage" viewBox="0 0 1920 1080"><g transform="translate(960 640) scale(1.45)"><g id="d5-col">{kit.colonel()}</g></g></svg>'
        + B.bubble("d5-b1", "מה?!", 1260, 150, "l", 110)
    )
    c.shot("d5-s7", s6_end, c.t("L20") - 0.4, inner, fade_in="blur")
    tw = c.w("d5-10", "מה") - 0.1
    c.fromTo("#colonel-mouth", {"scaleY": 1, "transformOrigin": "50% 0%"}, {"scaleY": 2.2, "duration": 0.15, "ease": "power3.out"}, tw)
    B.say(c, "d5-b1", tw)
    c.shake("#d5-s7-in", tw + 0.05, 14, 8)
    c.to("#colonel-mouth", {"scaleY": 1.3, "duration": 0.4}, tw + 1.0)
    c.fromTo("#d5-col", {"scale": 1}, {"scale": 1.08, "duration": 0.25, "ease": "power2.out", "transformOrigin": "50% 50%"}, c.w("d5-10", "צלחו") - 0.1)

    B.lesson_block(c, ["L20", "L21", "L22"], c.t("L20") - 0.45, c.dur, prior=19)
    c.music("invest", ce - 0.5, c.t("d5-5") - 0.3)
    c.music("hidden", c.t("d5-5") - 0.3, c.end("d5-9") + 0.2)
    c.music("sneaky", c.end("d5-9") + 0.2, c.end("d5-10") + 0.6)
    c.music("thinking", c.end("d5-10") + 0.6, c.dur)


# ================================================================ dream 6
def dream6(c):
    ce = card(c, 6)
    # S1: on the kopje again, an idea
    sil = SKIES["dawn"][3]
    content = kit.kopje_side(1180, 880, 1300, 400, sil, huts=True)
    html = (
        B.lieutenant("d6-lt", 1120, 490, 230)
        + B.bubble("d6-b1", "?", 1180, 120, "l", 90)
        + B.bubble("d6-b2", "לא למעלה. למטה!", 900, 110, "l", 56)
    )
    s1_end = c.w("d6-2", "להחזיק") - 0.3
    B.side_shot(c, "d6-s1", ce, s1_end, "dawn", content, html, ground_y=880)
    B.say(c, "d6-b1", c.w("d6-1", "ומחפש") - 0.2, c.w("d6-2", "רעיון") - 0.1)
    B.say(c, "d6-b2", c.w("d6-2", "לרדת") - 0.2)
    c.sfx("whoosh", c.w("d6-2", "לרדת") - 0.2, 0.3)

    # S2: the riverbed itself
    band = (
        f'<g transform="translate({DX} {DY})"><g id="d6-band" opacity="0"><ellipse rx="300" ry="78" fill="#E3A33B" opacity="0.22"/>'
        f'<ellipse rx="300" ry="78" fill="none" stroke="#E3A33B" stroke-width="7" stroke-dasharray="16 10"/></g></g>'
    )
    pins = kit.pin(DX + 210, DY + 90, "אפיק הנהר", "d6-pin0", "navy")
    s2_end = c.t("d6-3") - 0.15
    B.sand_shot(c, "d6-s2", s1_end, s2_end, band, pins, "", cam=(DX, DY + 60, 1.0), tint=TINT_DAY, fade_in="blur")
    c.cam("#d6-s2-cam", s1_end + 0.2, DX, DY + 30, 1.7, dur=1.6)
    c.fromTo("#d6-band", {"opacity": 0, "scale": 0.7, "transformOrigin": "50% 50%"}, {"opacity": 1, "scale": 1, "duration": 0.5, "ease": "back.out(1.8)"}, s1_end + 0.8)
    c.pop("#d6-pin0", s1_end + 1.1, 0.35)

    # S3: cross-section of the riverbed position
    gd = "M -20 760 L 1100 760 Q 1130 760 1150 940 L 1500 945 Q 1525 780 1560 780 L 1940 780 L 1940 1100 L -20 1100 Z"
    content = (
        '<path d="M 1220 940 Q 1320 955 1420 940 L 1420 944 L 1220 944 Z" fill="#4C8C86"/>'
        + "".join(B.place(kit.soldier("#203A5E"), x, 945, f"d6-xs{k}", 1.0, flip=True) for k, x in enumerate([1180, 1250]))
        + "".join(B.place(kit.boer("#7a2a18", beard=k % 2 == 0), x, 760, f"d6-xb{k}", 0.85) for k, x in enumerate([260, 420, 580]))
        + '<path id="d6-fire" d="M 1150 780 L 650 640" stroke="#F6B33C" stroke-width="6" stroke-dasharray="18 14" fill="none" pathLength="100" opacity="0"/>'
        + kit.bush_side(1090, 764, 1.0, "#5E6A2C")
    )
    labels = (
        '<div id="d6-l1" class="tag navy" style="left:1290px; top:600px; font-size:40px; opacity:0">מוסתרים מתחת לגדה</div>'
        '<div id="d6-l2" class="tag" style="left:1560px; top:840px; font-size:36px; opacity:0">מים קרובים</div>'
        '<div id="d6-l3" class="tag red" style="left:250px; top:460px; font-size:44px; opacity:0">שטח פתוח וחשוף</div>'
    )
    s3_end = c.t("d6-4") - 0.15
    c.shot("d6-s3", s2_end, s3_end, B.section(content, gd, label_html=labels), fade_in="wipe")
    c.pop("#d6-l1", c.w("d6-3", "יסתירו"), 0.35)
    c.pop("#d6-l2", c.w("d6-3", "המים") - 0.1, 0.35)
    for k in range(3):
        c.fromTo(f"#d6-xb{k}", {"opacity": 0, "x": -200}, {"opacity": 1, "x": 0, "duration": 1.2, "ease": "power2.out"}, round(c.w("d6-3", "לחצות") - 0.8 + k * 0.15, 3))
    c.pop("#d6-l3", c.w("d6-3", "וחשוף") - 0.2, 0.35)
    c.fromTo("#d6-fire", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 0.5}, c.w("d6-3", "הרובים") - 0.2)

    # S4: collect everyone, dig pits in the banks, clear a field of fire, a picket on the kopje, dummy trenches
    south = [p for p in geo.bank_points(+1, 46, 44) if 790 <= p[0] <= 1140 and p[1] < 360]
    north = [p for p in geo.bank_points(-1, 46, 44) if 820 <= p[0] <= 1110 and p[1] < 300]
    pits = south + north
    pit_svg, pit_men = [], []
    for k, (x, y) in enumerate(pits):
        pit_svg.append(f'<g transform="translate({x:.1f} {y:.1f})"><g id="d6p{k}" opacity="0"><ellipse rx="17" ry="9" fill="#3d2814"/><ellipse rx="17" ry="9" fill="none" stroke="#7b5a33" stroke-width="3"/></g></g>')
        pit_men.append((x - 6, y - 2))
        pit_men.append((x + 7, y + 1))
    fans = "".join(
        f'<path id="d6-fan{k}" d="M {DX + dx} {DY - 30} L {DX + dx - 170} {DY - 330} L {DX + dx + 170} {DY - 330} Z" fill="#FFF4D6" opacity="0"/>'
        for k, dx in enumerate((-110, 110))
    )
    picket = [(KX - 18, KY - 52), (KX + 2, KY - 58), (KX + 22, KY - 52)]
    dummy = [("M 830 642 L 990 642", "d6-dm0"), ("M 1040 520 L 1150 548", "d6-dm1"), ("M 700 470 L 800 455", "d6-dm2")]
    dummies = "".join(
        f'<g id="{u}" opacity="0"><path d="{d}" stroke="#1E1812" stroke-width="20" stroke-linecap="round" fill="none"/>'
        f'<path d="{d}" stroke="#FBF7EE" stroke-width="14" stroke-dasharray="20 5" fill="none"/></g>'
        for d, u in dummy
    )
    svg = fans + "".join(pit_svg) + B.tokens_at(c, pit_men, "d6m", "brit", 0.62) + B.tokens_at(c, picket, "d6k", "brit", 0.7) + dummies
    pins = (
        kit.pin(DX + 230, DY + 120, "שוחות קטנות בגדות", "d6-pin1", "navy")
        + kit.pin(DX - 60, DY - 240, "שדה אש", "d6-pin2")
        + kit.pin(KX + 60, KY - 90, "חוליה מוסתרת", "d6-pin3", "navy")
        + kit.pin(910, 700, "חפירות דמה", "d6-pin4", "red")
    )
    sv, hv = icon_row(c, "d6ic", [("גברים", "man", 5), ("נשים", "woman", 5), ("ילדים", "child", 4)], 860, c.t("d6-4") + 0.4, 0.95)
    over = (
        panel(sv, hv, "d6-panel", 740, 250)
        + '<div id="d6-wagons" class="tag dark" style="left:140px; top:830px; font-size:44px; opacity:0">ואפילו העגלות</div>'
        + '<div id="d6-wait" class="tag dark" style="left:120px; top:110px; font-size:52px; opacity:0">לא יורים עד השריקה</div>'
    )
    s4_end = c.t("d6-9") - 0.15
    B.sand_shot(c, "d6-s4", s3_end, s4_end, svg, pins, over, cam=(1100, 480, 0.95), tint=TINT_DAY, fade_in="blur")
    cam = "#d6-s4-cam"
    c.fade("#d6-panel", c.t("d6-4") + 0.1, 0.3)
    c.pop("#d6-wagons", c.w("d6-4", "העגלות") - 0.2, 0.35)
    t5 = c.t("d6-5")
    c.out("#d6-panel", t5 - 0.3)
    c.out("#d6-wagons", t5 - 0.3)
    c.cam(cam, t5 - 0.2, DX, DY + 20, 1.75, dur=1.4)
    tp = c.w("d6-5", "שוחות") - 0.2
    for k in range(len(pits)):
        c.pop(f"#d6p{k}", round(tp + k * 0.08, 3), 0.3, origin="50% 50%")
    B.pop_group(c, "d6m", len(pit_men), tp + 0.5, 0.03)
    c.pop("#d6-pin1", tp + 0.6, 0.35)
    tf = c.w("d6-5", "גוזמים") - 0.2
    c.cam(cam, tf - 0.2, DX, DY - 60, 1.3, dur=1.0)
    for k in range(2):
        c.fade(f"#d6-fan{k}", tf + 0.3 + k * 0.2, 0.6, to=0.35)
    c.pop("#d6-pin2", c.w("d6-5", "אש") - 0.2, 0.35)
    t6 = c.t("d6-6")
    c.cam(cam, t6 - 0.2, KX, KY - 40, 1.6, dur=1.4)
    B.pop_group(c, "d6k", 3, c.w("d6-6", "חוליה") - 0.1, 0.1)
    c.pop("#d6-pin3", c.w("d6-6", "ומוסתרת") - 0.2, 0.35)
    t7 = c.t("d6-7")
    c.cam(cam, t7 - 0.2, 960, 520, 1.05, dur=1.4)
    for k in range(3):
        c.fromTo(f"#d6-dm{k}", {"opacity": 0, "scale": 0.8, "transformOrigin": "50% 50%"}, {"opacity": 1, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, round(c.w("d6-7", "דמה") - 0.2 + k * 0.25, 3))
    c.pop("#d6-pin4", c.w("d6-7", "לבנים") - 0.1, 0.35)
    c.blur_in("#d6-wait", c.w("d6-8", "יורים") - 0.2)

    # S5: the scouts, the whistle, the volley; guns waste their shells on the dummies; a day and a night
    scouts = [(1004, -40), (996, -10), (1012, 20), (1000, 50)]
    north_pits = [p for p in pit_men if p[1] < 250]
    south_pits = [p for p in pit_men if p[1] >= 250]
    lines = [(f"d6fl{k}", x, y, 990 + (k % 3 - 1) * 30, 120 + (k % 2) * 30) for k, (x, y) in enumerate(south_pits[:7] + north_pits[:4])]
    guns = [(560, 110), (640, 150), (1560, 150)]
    targets = [(880, 630), (950, 640), (1090, 530), (1130, 540), (740, 465), (780, 460)]
    arcs = "".join(
        f'<path id="d6-arc{k}" d="M {gx} {gy} Q {(gx + tx) / 2} {min(gy, ty) - 300} {tx} {ty}" stroke="#1E1812" stroke-width="3" stroke-dasharray="8 8" fill="none" pathLength="100" opacity="0"/>'
        for k, ((gx, gy), (tx, ty)) in enumerate(zip(guns * 2, targets))
    )
    booms = "".join(kit.puff(x, y - 10, f"d6bm{k}", 30, "#6b5a45") for k, (x, y) in enumerate(targets))
    svg = (
        fans.replace('id="d6-fan', 'id="d6-gan') + "".join(pit_svg).replace('id="d6p', 'id="d6q').replace('opacity="0"', "")
        + B.tokens_at(c, pit_men, "d6n", "brit", 0.62) + B.tokens_at(c, picket, "d6j", "brit", 0.7)
        + dummies.replace('id="d6-dm', 'id="d6-em').replace('opacity="0"', "") + B.tokens_at(c, scouts, "d6s", "boer")
        + "".join(kit.token_gun(x, y, 1.3, f'id="d6g{k}"', 120 if x < 1000 else -120) for k, (x, y) in enumerate(guns))
        + B.fire_svg(lines) + arcs + booms
    )
    over = (
        '<div class="abs" style="left:1500px; top:60px; width:300px; height:300px;"><svg viewBox="-150 -150 300 300" style="width:300px; height:300px">'
        '<g id="d6-whistle" opacity="0"><circle r="120" fill="#F6ECD6" stroke="#1E1812" stroke-width="8"/>'
        '<path d="M -70 -10 L 30 -10 Q 60 -10 60 20 Q 60 50 30 50 L 0 50 L -10 20 L -70 20 Z" fill="#1E1812"/><circle cx="34" cy="18" r="10" fill="#F6ECD6"/>'
        '<path d="M 70 -40 L 100 -70 M 80 -10 L 120 -20 M 64 -64 L 76 -104" stroke="#1E1812" stroke-width="8" stroke-linecap="round"/></g></svg></div>'
        '<div id="d6-dlbl" class="tag red" style="left:120px; top:110px; font-size:52px; opacity:0">מפגיזים את הדמה</div>'
        '<div id="d6-sun" class="abs k-title" style="left:120px; top:90px; font-size:90px; color:#1E1812; opacity:0">יום</div>'
        '<div id="d6-moon" class="abs k-title" style="left:120px; top:90px; font-size:90px; color:#F4E7CB; opacity:0">לילה</div>'
    )
    s5_end = c.t("d6-13") - 0.15
    B.sand_shot(c, "d6-s5", s4_end, s5_end, svg, "", over, cam=(980, 330, 1.2), tint=TINT_NIGHT, fade_in="blur")
    c.set("#d6-s5-tint", {"opacity": 0}, s4_end)
    cam = "#d6-s5-cam"
    t9 = c.t("d6-9")
    for k in range(len(scouts)):
        c.fromTo(f"#d6s{k}", {"opacity": 0, "y": -100}, {"opacity": 1, "y": 70, "duration": 4.5, "ease": "power1.inOut"}, round(t9 + 0.2 + k * 0.3, 3))
    ta = c.w("d6-10", "אש") - 0.15
    c.pop("#d6-whistle", ta - 0.5, 0.25, origin="50% 50%")
    c.out("#d6-whistle", ta + 1.2)
    c.sfx("whistle", ta - 0.45, 0.55)
    B.fire_volley(c, lines, ta, c.end("d6-10") - 0.4, seed=61)
    c.shake(cam, ta + 0.05, 8)
    tr = c.w("d6-10", "ונסוגים") - 0.3
    for k in range(len(scouts)):
        c.to(f"#d6s{k}", {"y": -260, "opacity": 0, "duration": 1.4, "ease": "power2.in"}, round(tr + k * 0.08, 3))
    t11 = c.t("d6-11")
    c.cam(cam, t11 - 0.3, 960, 420, 0.95, dur=1.2)
    for k in range(3):
        c.pop(f"#d6g{k}", round(t11 + 0.2 + k * 0.15, 3), 0.35, origin="50% 50%")
    tb = c.w("d6-11", "הדמה") - 0.5
    c.blur_in("#d6-dlbl", tb + 0.3)
    for k in range(6):
        t_ = round(tb + k * 0.9, 3)
        c.fromTo(f"#d6-arc{k}", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"opacity": 1, "strokeDashoffset": 0, "duration": 0.55, "ease": "power1.in"}, t_)
        c.fromTo(f"#d6bm{k}", {"opacity": 0, "scale": 0.3}, {"opacity": 0.95, "scale": 1.5, "duration": 0.35, "ease": "power3.out", "transformOrigin": "50% 50%"}, t_ + 0.55)
        c.to(f"#d6bm{k}", {"opacity": 0, "duration": 1.4}, t_ + 1.3)
        c.sfx("boom", t_ + 0.55, 0.42)
    t12 = c.t("d6-12")
    c.out("#d6-dlbl", t12 - 0.2)
    c.fromTo("#d6-s5-tint", {"opacity": 0}, {"opacity": 0.6, "duration": 1.6, "ease": "power2.inOut"}, t12 + 0.6)
    c.fade("#d6-moon", t12 + 1.2, 0.4)
    c.out("#d6-moon", t12 + 4.0)
    c.to("#d6-s5-tint", {"opacity": 0.0, "duration": 1.6, "ease": "power2.inOut"}, t12 + 4.2)
    c.fade("#d6-sun", t12 + 4.6, 0.4)
    small = [(f"d6fl{k}", 0, 0, 0, 0) for k in range(3)]
    B.fire_volley(c, small, t12 + 1.8, t12 + 3.2, seed=71, vol=0.25)

    # S6: the relief column arrives; success
    col0 = along_road(0.98, 1.0, 1)[0]
    relief = "".join(kit.token_brit(col0[0], col0[1], 1.35, f'id="d6r{k}" opacity="0"') for k in range(9))
    smoke = "".join(kit.puff(820 + k * 40, 1040, f"d6rs{k}", 26, "#EDE4D3") for k in range(3))
    svg = (
        "".join(pit_svg).replace('id="d6p', 'id="d6t').replace('opacity="0"', "") + B.tokens_at(c, pit_men, "d6o", "brit", 0.62)
        + dummies.replace('id="d6-dm', 'id="d6-fm').replace('opacity="0"', "") + relief + smoke
    )
    over = kit.stamp_img("d6-stamp", "ok", 520, 640, -6)
    s6_end = c.t("d6-14") - 0.15
    B.sand_shot(c, "d6-s6", s5_end, s6_end, svg, "", over, cam=(930, 600, 0.95), tint=TINT_DAY, fade_in="blur")
    tc = c.w("d6-13", "רעם") - 0.4
    for k in range(3):
        c.fromTo(f"#d6rs{k}", {"opacity": 0, "scale": 0.4}, {"opacity": 0.9, "scale": 1.6, "duration": 0.8, "ease": "power2.out", "transformOrigin": "50% 50%"}, round(tc + k * 0.3, 3))
        c.sfx("cannon", round(tc + k * 0.3, 3), 0.3)
    tr = c.w("d6-13", "השיירה") - 0.4
    for k in range(9):
        c.set(f"#d6r{k}", {"opacity": 1}, round(tr + k * 0.3, 3))
        side = (k % 3 - 1) * 26
        way = list(reversed(along_road(0.62 + (k // 3) * 0.08, 1.0, 8)))
        c.to(f"#d6r{k}", {"keyframes": [{"x": round(x - col0[0] + side, 1), "y": round(y - col0[1], 1), "duration": 0.42, "ease": "none"} for x, y in way]}, round(tr + k * 0.3, 3))
    kit.slam(c, "#d6-stamp", c.w("d6-13", "הושלמה") - 0.1)

    # S7: the price
    inner = (
        '<img class="full" src="assets/art/sand-dim.jpg" alt="">'
        '<div id="d6-k" class="abs k-title" style="right:260px; top:300px; font-size:170px; color:#F4E7CB; opacity:0">11 הרוגים</div>'
        '<div id="d6-w" class="abs k-title" style="right:260px; top:480px; font-size:170px; color:#F4E7CB; opacity:0">15 פצועים</div>'
        '<div id="d6-held" class="abs k-title" style="right:260px; top:690px; font-size:120px; color:#E3A33B; opacity:0">המעבר נשאר בידינו</div>'
    )
    c.shot("d6-s7", s6_end, c.t("d6-15") - 0.3, inner, fade_in="blur")
    c.blur_in("#d6-k", c.w("d6-14", "אחד-עשר") - 0.2, 0.3)
    c.blur_in("#d6-w", c.w("d6-14", "חמישה-עשר") - 0.2, 0.3)
    c.blur_in("#d6-held", c.w("d6-14", "נשאר") - 0.2, 0.3)

    # S8: the ceremony ("Arise, Sir Forethought"), then the coffee
    sil = SKIES["gold"][3]
    flags = "".join(
        f'<path d="M {x} 120 L {x + 50} 120 L {x + 25} 170 Z" fill="{["#B3261E", "#F4E7CB", "#203A5E"][k % 3]}"/>' for k, x in enumerate(range(0, 1920, 64))
    )
    rope = '<path d="M 0 118 Q 960 150 1920 118" stroke="#3b2a1c" stroke-width="4" fill="none"/>'
    crowd = "".join(B.place(kit.soldier(sil), x, 860, f"d6-cr{k}", 1.0) for k, x in enumerate(list(range(60, 560, 70)) + list(range(1420, 1900, 70))))
    colonel = (
        '<g transform="translate(1180 860) scale(-1.45 1.45)"><g id="d6-colonel">' + kit.soldier(sil, rifle=False)
        + f'<g id="d6-sword"><rect x="20" y="-210" width="7" height="110" fill="{sil}" transform="rotate(-50 24 -110)"/></g></g></g>'
    )
    orderly = f'<g transform="translate(1180 860) scale(-1.45 1.45)"><g id="d6-ord" opacity="0">{kit.soldier(sil, rifle=False)}<g transform="translate(36 -100)">{kit.mug(sil)}</g></g></g>'
    html = (
        B.lieutenant("d6-hero", 820, 900, 560)
        + B.bubble("d6-b3", "קום על רגליך, האביר תכנוני!", 1060, 260, "r", 44)
        + B.bubble("d6-b4", "המפקד! הקפה מוכן.", 1080, 300, "r", 50)
    )
    s8_end = c.t("d6-17") - 0.15
    B.side_shot(c, "d6-s8", c.t("d6-15") - 0.3, s8_end, "gold", rope + flags + crowd + colonel + orderly, html, ground_y=860, fade_in="blur")
    tk = c.w("d6-15", "התזמורת") - 0.2
    for k in range(14):
        c.to(f"#d6-cr{k}", {"y": -14, "duration": 0.14, "yoyo": True, "repeat": 3, "ease": "sine.inOut"}, round(tk + 0.4 + (k % 5) * 0.07, 3))
    c.sfx("cheer", c.w("d6-15", "מחיאות") - 0.3, 0.45, dur=3.0, fade_out=1.0)
    ts = c.w("d6-15", "קום") - 0.3
    B.say(c, "d6-b3", ts, c.t("d6-16") + 0.2)
    c.fromTo("#d6-sword", {"rotation": 0}, {"rotation": 38, "duration": 0.35, "ease": "power2.inOut", "transformOrigin": "24px -110px"}, ts + 0.3)
    c.to("#d6-sword", {"rotation": 0, "duration": 0.35, "ease": "power2.inOut"}, ts + 0.9)
    tw = c.w("d6-16", "משתנה") - 0.4
    c.fromTo("#d6-s8-cam", {"filter": "blur(0px)", "skewX": 0}, {"filter": "blur(10px)", "skewX": 8, "duration": 0.45, "ease": "sine.inOut"}, tw)
    c.to("#d6-s8-cam", {"filter": "blur(0px)", "skewX": 0, "duration": 0.45, "ease": "sine.inOut"}, tw + 0.45)
    c.set("#d6-colonel", {"opacity": 0}, tw + 0.45)
    c.set("#d6-ord", {"opacity": 1}, tw + 0.45)
    for k in range(14):
        c.set(f"#d6-cr{k}", {"opacity": 0}, tw + 0.45)
    B.say(c, "d6-b4", c.w("d6-16", "המפקד") - 0.2)
    to_ = c.w("d6-16", "הקפה") - 0.3
    c.to("#d6-ord", {"x": -40, "duration": 0.5, "ease": "power2.out"}, to_)
    c.to("#d6-hero", {"rotation": -4, "duration": 0.6, "ease": "sine.inOut", "transformOrigin": "50% 100%"}, to_ + 0.6)
    c.to("#d6-hero", {"rotation": 0, "duration": 0.6, "ease": "sine.inOut"}, to_ + 1.3)

    # S9: awake in the dusty hole in the Dream Village
    wall = (
        '<path d="M -20 -20 L 520 -20 C 430 300, 470 700, 380 1100 L -20 1100 Z" fill="#4a3320"/>'
        '<path d="M 1940 -20 L 1400 -20 C 1490 300, 1450 700, 1540 1100 L 1940 1100 Z" fill="#4a3320"/>'
        '<path d="M -20 900 L 1940 900 L 1940 1100 L -20 1100 Z" fill="#3a2716"/>'
    )
    sign = (
        '<g transform="translate(960 560)"><g id="d6-sign" opacity="0"><rect x="-6" y="0" width="12" height="340" fill="#3b2a1c"/>'
        '<path d="M -230 -110 L 200 -110 L 250 -55 L 200 0 L -230 0 Z" fill="#D8B47A" stroke="#3b2a1c" stroke-width="8"/>'
        '<text x="-10" y="-30" text-anchor="middle" font-family="Karantina" font-weight="700" font-size="84" fill="#1E1812">כפר החלומות</text></g></g>'
    )
    html = (
        B.lieutenant("d6-lie", 1240, 905, 480, shadow=False)
        + '<div id="d6-lid1" class="full" style="background:#000; height:540px;"></div>'
        + '<div class="abs" style="left:0; top:540px; width:1920px; height:540px;"><div id="d6-lid2" class="full" style="background:#000; height:540px; top:0"></div></div>'
    )
    inner = f'{kit.sky("dawn")}<div id="d6-s9-cam" class="cam"><svg class="stage" viewBox="0 0 1920 1080">{wall}{sign}</svg>{html}</div>'
    c.shot("d6-s9", s8_end, c.dur, inner, fade=0)
    c.set("#d6-lie", {"rotation": -84, "transformOrigin": "50% 90%", "y": 0}, s8_end)
    c.fromTo("#d6-lid1", {"y": 0}, {"y": -560, "duration": 0.5, "ease": "power2.inOut"}, s8_end + 0.25)
    c.fromTo("#d6-lid2", {"y": 0}, {"y": 560, "duration": 0.5, "ease": "power2.inOut"}, s8_end + 0.25)
    c.to("#d6-lid1", {"y": -300, "duration": 0.15, "yoyo": True, "repeat": 1}, s8_end + 1.0)
    c.to("#d6-lid2", {"y": 300, "duration": 0.15, "yoyo": True, "repeat": 1}, s8_end + 1.0)
    c.fromTo("#d6-sign", {"opacity": 0, "y": 80, "rotation": -6}, {"opacity": 1, "y": 0, "rotation": -3, "duration": 0.5, "ease": "back.out(1.8)"}, c.w("d6-17", "החלומות") - 0.4)

    c.music("invest", ce - 0.5, c.t("d6-9") - 0.3)
    c.music("hidden", c.t("d6-9") - 0.3, c.t("d6-10") - 0.2)
    c.music("heroic", c.t("d6-10") - 0.2, c.end("d6-13") + 0.4)
    c.music("thinking", c.end("d6-13") + 0.4, c.t("d6-15") - 0.3)
    c.music("celtic", c.t("d6-15") - 0.3, c.t("d6-16") - 0.2)
    c.music("sneaky", c.t("d6-16") - 0.2, c.dur)


# ================================================================ recap
IDEAS = [
    ("r-2", "הגנה לפני נוחות", "חופרים היום, לא מחר"),
    ("r-3", "אוספים את כולם", "כל מי שראה אותך יכול לספר"),
    ("r-4", "להסתתר ולהטעות", "עמדות מוסתרות וחפירות דמה"),
    ("r-5", "קצר, צר, עמוק, מפוזר", "לא קו ישר אחד וארוך"),
    ("r-6", "אין עורף", "מגינים מכל הכיוונים"),
    ("r-7", "הקרקע לפי המשימה", "לא תמיד הגבעה. לפעמים האפיק"),
]


def idea_diagram(k, dark=False):
    """One small picture per big idea (drawn in a 700x520 box)."""
    ink, red, navy = ("#F4E7CB", "#F0605A", "#8FB0DA") if dark else ("#1E1812", "#B3261E", "#203A5E")
    cut = "#C9A46A" if dark else "#4A321C"
    if k == 0:
        return (
            f'<g transform="translate(200 300) scale(1.6)">{kit.tent(0, 0, 1, "#8a7a60")}</g>'
            f'<g id="rx-0a" opacity="0"><path d="M 110 120 L 290 320 M 290 120 L 110 320" stroke="{red}" stroke-width="18" stroke-linecap="round"/></g>'
            f'<path id="rx-0b" d="M 400 300 L 640 300" stroke="#4A321C" stroke-width="30" stroke-linecap="round" pathLength="100"/>'
            f'<path id="rx-0c" d="M 400 270 L 640 270" stroke="#E2C48E" stroke-width="18" stroke-linecap="round" pathLength="100"/>'
        )
    if k == 1:
        pts = [(80 + (j % 6) * 110, 120 + (j // 6) * 300) for j in range(12)]
        return "".join(
            f'<g transform="translate({x} {y})"><g id="rx-1p{j}">{kit.person_icon(0, 0, ["man", "woman", "child"][j % 3], 2.2, ink)}</g></g>' for j, (x, y) in enumerate(pts)
        ) + f'<ellipse id="rx-1c" cx="350" cy="280" rx="230" ry="150" fill="none" stroke="{navy}" stroke-width="8" stroke-dasharray="18 12" opacity="0"/>'
    if k == 2:
        return (
            f'<path d="M 40 360 L 660 360" stroke="#8a6a40" stroke-width="6"/>'
            f'<ellipse cx="170" cy="360" rx="80" ry="22" fill="#3d2814"/>{kit.bush_side(170, 362, 1.4, "#5E6A2C")}'
            f'<path d="M 420 352 L 620 352" stroke="{ink}" stroke-width="28" stroke-linecap="round"/><path d="M 420 352 L 620 352" stroke="#FBF7EE" stroke-width="20" stroke-dasharray="26 6"/>'
            f'<g id="rx-2b" opacity="0">{kit.puff(520, 300, "rx-2pf", 60, "#6b5a45").replace("opacity=\"0\"", "")}</g>'
            f'<text x="170" y="470" text-anchor="middle" font-family="Rubik" font-weight="700" font-size="40" fill="{navy}">אמיתי</text>'
            f'<text x="520" y="470" text-anchor="middle" font-family="Rubik" font-weight="700" font-size="40" fill="{red}">דמה</text>'
        )
    if k == 3:
        shorts = "".join(
            f'<path id="rx-3s{j}" d="M {x} {y} q 40 -18 80 0" stroke="{cut}" stroke-width="20" stroke-linecap="round" fill="none" opacity="0"/>'
            for j, (x, y) in enumerate([(90, 380), (260, 330), (430, 390), (560, 300), (200, 450)])
        )
        return (
            f'<path d="M 60 170 L 640 170" stroke="{cut}" stroke-width="22" stroke-linecap="round"/>'
            f'<g id="rx-3x" opacity="0"><path d="M 250 90 L 450 250 M 450 90 L 250 250" stroke="{red}" stroke-width="18" stroke-linecap="round"/></g>' + shorts
        )
    if k == 4:
        arrows = "".join(
            f'<path id="rx-4a{j}" d="M {350 + 300 * math.cos(a):.0f} {270 + 230 * math.sin(a):.0f} L {350 + 150 * math.cos(a):.0f} {270 + 115 * math.sin(a):.0f}" '
            f'stroke="{red}" stroke-width="14" stroke-linecap="round" marker-end="url(#rxa)" opacity="0"/>'
            for j, a in enumerate([i * math.pi / 4 for i in range(8)])
        )
        return (
            f'<defs><marker id="rxa" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3.5" markerHeight="3.5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="{red}"/></marker></defs>'
            f'<circle cx="350" cy="270" r="100" fill="{navy}" opacity="0.15"/><circle cx="350" cy="270" r="100" fill="none" stroke="{navy}" stroke-width="10"/>' + arrows
        )
    return (
        f'<path d="M 30 420 Q 170 120 310 420 Z" fill="{"#B8A27A" if dark else "#8a7a60"}"/>'
        f'<g id="rx-5x" opacity="0"><path d="M 110 200 L 230 320 M 230 200 L 110 320" stroke="{red}" stroke-width="18" stroke-linecap="round"/></g>'
        f'<path d="M 380 300 L 460 300 Q 480 420 540 420 L 600 420 Q 640 420 660 300 L 700 300" stroke="#5b3d1d" stroke-width="10" fill="#B98A52"/>'
        f'<path d="M 520 418 Q 560 428 600 418" stroke="#4C8C86" stroke-width="12"/>'
        f'<g id="rx-5v" opacity="0"><path d="M 470 230 L 520 280 L 620 160" stroke="#1F7A45" stroke-width="18" stroke-linecap="round" fill="none"/></g>'
    )


def recap(c):
    # S1: twenty-two tablets gather into six ideas
    chips = []
    for k in range(22):
        col, row = k % 11, k // 11
        x, y = 1660 - col * 140, 330 + row * 180
        chips.append(
            f'<div class="abs" style="left:{x}px; top:{y}px; width:120px; height:62px;"><div id="rc-c{k}" class="abs" style="left:0; top:0; width:120px; height:62px; opacity:0">'
            f'<img src="assets/art/slate.png" style="width:120px; height:62px; display:block" alt=""><div class="abs k-title" style="left:0; width:120px; top:6px; text-align:center; font-size:50px; color:#E3A33B">{k + 1}</div></div></div>'
        )
    six = "".join(
        f'<div id="rc-six{k}" class="abs k-title" style="left:{1580 - k * 260}px; top:420px; width:200px; height:200px; text-align:center; font-size:170px; '
        f'line-height:200px; color:#1E1812; background:#E3A33B; border-radius:24px; opacity:0">{k + 1}</div>'
        for k in range(6)
    )
    inner = '<img class="full" src="assets/art/sand-dim.jpg" alt="">' + "".join(chips) + six
    s1_end = c.t("r-2") - 0.2
    c.shot("rc-s1", 0, s1_end, inner, fade_in="blur")
    for k in range(22):
        c.fromTo(f"#rc-c{k}", {"opacity": 0, "y": -30}, {"opacity": 1, "y": 0, "duration": 0.3, "ease": "power3.out"}, round(0.3 + k * 0.05, 3))
    tg = c.w("r-1", "שישה") - 0.4
    for k in range(22):
        g = k * 6 // 22
        col, row = k % 11, k // 11
        x, y = 1660 - col * 140, 330 + row * 180
        tx, ty = 1580 - g * 260 + 40, 470
        c.to(f"#rc-c{k}", {"x": tx - x, "y": ty - y, "scale": 0.5, "opacity": 0, "duration": 0.8, "ease": "power3.in"}, round(tg + (k % 6) * 0.03, 3))
    for k in range(6):
        c.fromTo(f"#rc-six{k}", {"opacity": 0, "scale": 0.5}, {"opacity": 1, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, round(tg + 0.7 + k * 0.1, 3))
    c.sfx("whoosh", tg, 0.3)

    # S2..S7: one idea at a time
    grounds = ["#E9D3A3", "#2E3940", "#E9D3A3", "#2E3940", "#E9D3A3", "#2E3940"]
    entries = ["wipe", "blur", "iris", "wipe", "blur", "iris"]
    prev = s1_end
    for k, (sid, head, sub) in enumerate(IDEAS):
        dark = grounds[k] != "#E9D3A3"
        ink = "#F4E7CB" if dark else "#1E1812"
        end = c.t(IDEAS[k + 1][0]) - 0.2 if k + 1 < len(IDEAS) else c.t("r-8") - 0.3
        inner = (
            f'<div class="full" style="background:{grounds[k]}"></div>'
            f'<div id="ri{k}-n" class="abs k-title" style="right:140px; top:150px; font-size:420px; color:#E3A33B; opacity:0">{k + 1}</div>'
            f'<div id="ri{k}-h" class="abs k-title" style="right:140px; top:610px; font-size:140px; color:{ink}; opacity:0">{head}</div>'
            f'<div id="ri{k}-s" class="abs label" style="right:146px; top:780px; font-size:52px; color:{ink}; opacity:0">{sub}</div>'
            f'<svg class="stage" viewBox="0 0 1920 1080"><g transform="translate(120 230)"><g id="ri{k}-d" opacity="0">{idea_diagram(k, dark)}</g></g></svg>'
        )
        c.shot(f"rc-i{k}", prev, end, inner, fade_in=entries[k])
        t0 = c.t(sid)
        c.fromTo(f"#ri{k}-n", {"opacity": 0, "scale": 0.7, "transformOrigin": "100% 50%"}, {"opacity": 1, "scale": 1, "duration": 0.35, "ease": "expo.out"}, prev + 0.15)
        c.blur_in(f"#ri{k}-h", t0 + 0.4, 0.25)
        c.blur_in(f"#ri{k}-s", t0 + 1.4, 0.25)
        c.fade(f"#ri{k}-d", t0 + 0.2, 0.4)
        mid = t0 + (c.end(sid) - t0) * 0.45
        if k == 0:
            c.pop("#rx-0a", mid, 0.3, origin="50% 50%")
            c.draw("#rx-0b", mid + 0.4, 0.7)
            c.draw("#rx-0c", mid + 0.6, 0.7)
        elif k == 1:
            for j in range(12):
                x, y = 80 + (j % 6) * 110, 120 + (j // 6) * 300
                c.to(f"#rx-1p{j}", {"x": (350 - x) * 0.55, "y": (280 - y) * 0.55, "duration": 0.8, "ease": "power3.inOut"}, round(mid + j * 0.03, 3))
            c.fade("#rx-1c", mid + 0.7, 0.3)
        elif k == 2:
            c.fromTo("#rx-2b", {"opacity": 0, "scale": 0.4}, {"opacity": 1, "scale": 1.2, "duration": 0.35, "transformOrigin": "50% 50%"}, mid)
            c.sfx("boom", mid, 0.3)
        elif k == 3:
            c.pop("#rx-3x", mid - 0.4, 0.3, origin="50% 50%")
            for j in range(5):
                c.fade(f"#rx-3s{j}", round(mid + 0.2 + j * 0.15, 3), 0.25)
        elif k == 4:
            for j in range(8):
                c.fade(f"#rx-4a{j}", round(mid - 0.6 + j * 0.1, 3), 0.25)
        else:
            c.pop("#rx-5x", c.w(sid, "הגבוהה") - 0.1, 0.3, origin="50% 50%")
            c.pop("#rx-5v", c.w(sid, "אפיק") - 0.1, 0.3, origin="50% 50%")
        prev = end

    # S8: the question to ask
    inner = (
        '<div class="full" style="background:radial-gradient(ellipse at 50% 45%, #4a3320 0%, #24180e 65%, #130c06 100%)"></div>'
        '<div class="tab-wrap" style="position:absolute; left:210px; top:170px; width:1500px; height:730px;">'
        '<div id="rq-tab" class="tablet" style="opacity:0"><div class="tab-text" style="right:120px; left:120px; top:150px; text-align:center; font-size:78px">'
        '<span id="rq-l0" class="tab-line">שאל את עצמך תמיד:</span><span id="rq-l1" class="tab-line" style="color:#E3A33B">במה אני טועה?</span>'
        '<span id="rq-l2" class="tab-line" style="color:#E3A33B">היכן אכשל?</span></div></div></div>'
        '<div id="rq-src" class="abs label" style="left:0; width:1920px; top:80px; text-align:center; font-size:38px; color:#d8c8a8; opacity:0">מתוך ההקדמה לספר</div>'
    )
    s8_end = c.t("r-9") - 0.2
    c.shot("rc-q", prev, s8_end, inner, fade_in="blur")
    c.style(B.LESSON_CSS)
    c.fromTo("#rq-tab", {"opacity": 0, "y": -60}, {"opacity": 1, "y": 0, "duration": 0.5, "ease": "power3.out"}, prev + 0.2)
    c.sfx("thud", prev + 0.5, 0.35)
    for j, word in enumerate(["שאל", "במה", "היכן"]):
        c.fromTo(f"#rq-l{j}", {"clipPath": "inset(0 0 0 100%)"}, {"clipPath": "inset(0 0 0 0%)", "duration": 0.9, "ease": "power1.inOut"}, c.w("r-8", word) - 0.1)
    c.fade("#rq-src", c.w("r-8", "שאל") + 0.3, 0.4)

    # S9: wise before the deed
    html = (
        B.lieutenant("rc-lt", 1430, 1000, 680)
        + '<div id="rc-h" class="abs k-title" style="left:120px; top:250px; font-size:190px; color:#33210F; opacity:0">חכם לפני מעשה</div>'
        + '<div id="rc-g" class="abs k-title" style="left:120px; top:470px; font-size:160px; color:#B3261E; opacity:0">בהצלחה!</div>'
        + '<div id="rc-cr" class="abs label" style="left:110px; top:690px; width:1000px; padding:22px 30px; font-size:30px; line-height:1.55; color:#33210F; font-weight:500; background:rgba(248,232,196,.92); border:3px solid #33210F; border-radius:14px; opacity:0">'
        '<div>מבוסס על ״הגנת מעברות פתיים״ מאת סר א.ד. סווינטון, הוצאת מערכות</div>'
        '<div>קריינות: קול סינתטי <bdi>(Microsoft Avri)</bdi></div>'
        '<div dir="ltr" style="text-align:right">Music: Kevin MacLeod (incompetech.com), CC BY 4.0</div>'
        '<div dir="ltr" style="text-align:right">Sound effects: Freesound, Wikimedia Commons (CC0 / public domain)</div></div>'
    )
    B.side_shot(c, "rc-end", s8_end, c.dur, "gold", "", html, ground_y=900, fade_in="blur")
    c.fromTo("#rc-lt", {"x": 120, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.9, "ease": "expo.out"}, s8_end + 0.1)
    c.blur_in("#rc-h", c.w("r-9", "חכם") - 0.1, 0.3)
    c.blur_in("#rc-g", c.w("r-9", "בהצלחה") - 0.1, 0.3)
    c.fade("#rc-cr", c.end("r-9") + 0.4, 0.6)

    c.music("thinking", 0, c.t("r-9") - 0.4)
    c.music("celtic", c.t("r-9") - 0.4, c.dur + 1.0)
