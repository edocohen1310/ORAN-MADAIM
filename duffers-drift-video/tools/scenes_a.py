"""Opening, the book and its author, the ground."""
import blocks as B
import geo
import kit
from kit import SKIES


# ================================================================ intro
def intro(c):
    sil = SKIES["night"][3]
    # A: night by the river, the lieutenant and his fifty men
    soldiers = []
    for k in range(50):
        row, col = divmod(k, 25)
        x = col * 30 + row * 14
        y = row * 26
        soldiers.append(f'<g transform="translate({x} {y - 26 * row * 0 - row * 14}) scale(0.42)">{kit.soldier("#0a0d1e")}</g>')
    ridge = '<path d="M -20 712 C 300 690, 600 700, 900 708 C 1100 714, 1300 700, 1940 706 L 1940 800 L -20 800 Z" fill="#141a36"/>'
    col = ridge + f'<g transform="translate(-900 700)"><g id="intro-col"><g id="intro-col-b">{"".join(soldiers)}</g></g></g>'
    ring = (
        '<g transform="translate(760 812)"><g id="intro-ring" opacity="0"><ellipse rx="120" ry="34" fill="none" stroke="#F4E7CB" '
        'stroke-width="5" stroke-dasharray="14 10"/></g></g>'
    )
    html = (
        B.lieutenant("intro-lt", 1330, 960, 640)
        + '<div id="intro-tag1" class="tag" style="left:640px; top:640px; opacity:0">המעבר בנהר</div>'
        + '<div id="intro-tag2" class="tag red" style="left:600px; top:520px; font-size:54px; opacity:0">בכל מחיר</div>'
    )
    a_end = c.t("intro-3") - 0.1
    B.side_shot(c, "intro-a", 0, a_end, "night", col + ring, html, bank=True, fade=0, hills=False)
    c.fromTo("#intro-a-cam", {"scale": 1.0, "transformOrigin": "60% 60%"}, {"scale": 1.07, "duration": a_end, "ease": "none"}, 0)
    c.fromTo("#intro-lt", {"opacity": 0.0, "y": 14}, {"opacity": 1, "y": 0, "duration": 1.0, "ease": "power2.out"}, 0.0)
    tw = c.w("intro-2", "חמישים")
    B.walk(c, "intro-col", tw - 0.2, 980, 2.6, bob=5)
    c.fromTo("#intro-ring", {"opacity": 0, "scale": 0.6, "transformOrigin": "50% 50%"}, {"opacity": 1, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, c.w("intro-2", "מעבר"))
    c.pop("#intro-tag1", c.w("intro-2", "מעבר") + 0.1, 0.35)
    kit.slam(c, "#intro-tag2", c.w("intro-2", "מחיר") - 0.05)
    c.sfx("cricket", 0.0, 0.22, dur=a_end, fade_out=1.0)
    c.sfx("wind", 0.0, 0.15, dur=a_end, fade_out=1.0)

    # B: six tries, five failures
    rings, stamps, tabs = [], [], []
    for k in range(6):
        x = 1560 - k * 232
        rings.append(
            f'<g transform="translate({x} 520)"><g id="intro-r{k}" opacity="0"><circle r="92" fill="#232858" stroke="#F4E7CB" stroke-width="6"/>'
            f'<text y="34" text-anchor="middle" font-family="Karantina" font-weight="700" font-size="110" fill="#F4E7CB">{k + 1}</text></g></g>'
        )
        if k < 5:
            stamps.append(
                f'<div class="abs" style="left:{x - 115}px; top:{470}px; width:230px; height:91px; transform:rotate({-12 + k * 5}deg)">'
                f'<img id="intro-s{k}" src="assets/art/stamp-fail.png" style="width:230px; height:91px; opacity:0" alt=""></div>'
            )
            tabs.append(
                f'<div class="abs" style="left:{x - 46}px; top:690px; width:92px; height:46px;">'
                f'<img id="intro-tb{k}" src="assets/art/slate.png" style="width:92px; height:46px; opacity:0" alt=""></div>'
            )
    q = '<div id="intro-q" class="abs k-title" style="left:360px; top:420px; width:0; font-size:150px; color:#E3A33B; opacity:0">?</div>'
    inner = (
        '<div class="full" style="background:radial-gradient(ellipse at 50% 50%, #2E2B63 0%, #161A3C 70%)"></div>'
        f'<svg class="stage" viewBox="0 0 1920 1080">{kit.stars(70, 17)}{"".join(rings)}</svg>{"".join(stamps)}{"".join(tabs)}{q}'
    )
    b0, b1 = a_end, c.t("intro-5") - 0.1
    c.shot("intro-b", b0, b1, inner, fade_in="blur")
    t6 = c.w("intro-3", "שש")
    for k in range(6):
        c.pop(f"#intro-r{k}", round(b0 + 0.25 + k * 0.1, 3), 0.35, origin="50% 50%")
    for k in range(6):
        c.to(f"#intro-r{k}", {"scale": 1.12, "duration": 0.16, "yoyo": True, "repeat": 1, "transformOrigin": "50% 50%"}, round(t6 + k * 0.07, 3))
    tf = c.w("intro-4", "ייכשל")
    for k in range(5):
        kit.slam(c, f"#intro-s{k}", round(tf - 0.25 + k * 0.22, 3), sound=k % 2 == 0)
    c.fromTo("#intro-r5", {"scale": 1}, {"scale": 1.15, "duration": 0.3, "ease": "power2.out", "transformOrigin": "50% 50%"}, tf + 1.2)
    tl_ = c.w("intro-4", "ילמד")
    for k in range(5):
        c.fromTo(f"#intro-tb{k}", {"opacity": 0, "y": 30}, {"opacity": 1, "y": 0, "duration": 0.35, "ease": "power3.out"}, round(tl_ - 0.1 + k * 0.08, 3))

    # C: the book itself
    cover = (
        '<div class="full" style="background:radial-gradient(ellipse at 55% 45%, #4a3320 0%, #24180e 65%, #130c06 100%)"></div>'
        '<div class="abs" style="left:640px; top:70px; width:640px; height:910px;">'
        '<img id="intro-cover" src="assets/book/cover.jpg" style="width:640px; height:910px; box-shadow:0 30px 60px rgba(0,0,0,.6); display:block" alt=""></div>'
        '<div id="intro-n1" class="abs k-title" style="left:1340px; top:300px; font-size:140px; opacity:0">6 חלומות</div>'
        '<div id="intro-n2" class="abs k-title" style="left:1340px; top:470px; font-size:140px; color:#E3A33B; opacity:0">22 שיעורים</div>'
    )
    c0 = b1
    c.shot("intro-c", c0, c.dur, cover, fade_in="blur")
    c.fromTo("#intro-cover", {"scale": 0.9, "rotation": -5, "y": 40}, {"scale": 1, "rotation": -2, "y": 0, "duration": 1.4, "ease": "expo.out"}, c0)
    c.blur_in("#intro-n1", c.end("intro-5") + 0.1, 0.3)
    c.blur_in("#intro-n2", c.end("intro-5") + 0.8, 0.3)
    c.to("#intro-cover", {"x": -260, "duration": 1.0, "ease": "power3.inOut"}, c.end("intro-5") - 0.3)
    c.sfx("whoosh", c0 - 0.1, 0.3)
    c.sfx("page", c0 + 0.1, 0.4)

    c.music("hidden", 0, c.t("intro-5") - 0.6)
    c.music("heroic", c.t("intro-5") - 0.6, c.dur + 0.5, gain=1.0)


# ================================================================ about
def about(c):
    gold = SKIES["gold"][3]
    # A: author on the cover, then the war's dates
    a1 = c.t("about-3") - 0.2
    inner = (
        f'{kit.sky("gold")}<svg class="stage" viewBox="0 0 1920 1080">{kit.sun(1500, 260, 80)}{kit.far_hills("gold", 700)}{kit.ground("gold", 820)}</svg>'
        '<div class="abs" style="left:110px; top:90px; width:600px; height:854px;"><img id="ab-cover" src="assets/book/cover.jpg" '
        'style="width:600px; height:854px; box-shadow:0 26px 50px rgba(40,20,0,.45); display:block" alt=""></div>'
        '<div id="ab-name" class="abs k-title" style="right:150px; top:150px; font-size:150px; color:#33210F; opacity:0">סר ארנסט סווינטון</div>'
        '<div id="ab-role" class="abs label" style="right:156px; top:330px; font-size:46px; color:#33210F; opacity:0">קצין בריטי במלחמת הבורים</div>'
        '<div id="ab-y1" class="abs k-title" style="right:150px; top:520px; font-size:170px; color:#33210F; opacity:0">1899</div>'
        '<div id="ab-y2" class="abs k-title" style="right:800px; top:520px; font-size:170px; color:#33210F; opacity:0">1902</div>'
        '<svg class="stage" viewBox="0 0 1920 1080"><path id="ab-line" d="M 1500 640 L 1150 640" stroke="#33210F" stroke-width="8" stroke-linecap="round" pathLength="100" opacity="0"/></svg>'
        '<div id="ab-sa" class="abs label" style="right:150px; top:740px; font-size:46px; color:#33210F; opacity:0">דרום אפריקה</div>'
    )
    c.shot("ab-a", 0, a1, inner, fade_in="blur")
    c.fromTo("#ab-cover", {"scale": 1.0, "transformOrigin": "50% 28%"}, {"scale": 1.12, "duration": 6, "ease": "power1.inOut"}, 0)
    c.blur_in("#ab-name", c.w("about-1", "ארנסט") - 0.1)
    c.blur_in("#ab-role", c.w("about-1", "שלחם"), 0.3)
    c.to("#ab-cover", {"x": -760, "opacity": 0, "duration": 0.7, "ease": "power3.in"}, c.t("about-2") - 0.2)
    c.blur_in("#ab-y1", c.w("about-2", "1899") - 0.1)
    c.fromTo("#ab-line", {"opacity": 1, "strokeDasharray": "100 120", "strokeDashoffset": 110}, {"strokeDashoffset": 0, "duration": 1.1, "ease": "power2.inOut"}, c.w("about-2", "1899") + 0.3)
    c.blur_in("#ab-y2", c.w("about-2", "1902") - 0.1)
    c.blur_in("#ab-sa", c.w("about-2", "1902") + 0.5)

    # B: empire vs commando
    cols = "".join(B.bobber(f'<g transform="translate({k * 74} 0)">{kit.soldier(gold)}</g>', f"ab-s{k}") for k in range(9))
    brit = f'<g transform="translate(-740 840) scale(0.78)"><g id="ab-brit">{cols}</g></g>'
    riders = "".join(B.horse(1980 + k * 230, 840 + (k % 2) * 16, f"ab-h{k}", gold, 0.95, flip=True) for k in range(4))
    hill = f'<g id="ab-hill-g">{kit.kopje_side(1420, 845, 760, 210, gold, huts=False)}</g>'
    pop_riders = "".join(
        f'<g transform="translate({1240 + k * 120} 700)"><g id="ab-pr{k}" opacity="0">{kit.boer(gold, rifle=True, arm_up=k % 2 == 0)}</g></g>' for k in range(3)
    )
    html = (
        '<div id="ab-tb" class="tag navy" style="left:180px; top:240px; font-size:46px; opacity:0">האימפריה הבריטית</div>'
        '<div id="ab-tr" class="tag rust" style="right:180px; top:240px; font-size:46px; opacity:0">הבורים</div>'
        '<div id="ab-tk" class="tag dark" style="right:180px; top:340px; font-size:40px; opacity:0">קומנדו: קבוצות רכובות, קטנות וזריזות</div>'
    )
    b0, b1 = a1, c.t("about-6") - 0.2
    B.side_shot(c, "ab-b", b0, b1, "gold", brit + pop_riders + hill + riders, html, ground_y=840, fade_in="wipe")
    tb = c.w("about-3", "האימפריה")
    c.to("#ab-brit", {"x": 900, "duration": 3.2, "ease": "power1.out"}, b0 + 0.2)
    for k in range(9):
        for j in range(10):
            c.to(f"#ab-s{k}-b", {"y": -6 if j % 2 == 0 else 0, "duration": 0.16, "ease": "sine.inOut"}, round(b0 + 0.2 + j * 0.32 + k * 0.03, 3))
    c.pop("#ab-tb", tb, 0.35, origin="50% 50%")
    th = c.w("about-4", "הבורים")
    for k in range(4):
        B.gallop(c, f"ab-h{k}", round(th - 0.6 + k * 0.15, 3), -1150, 3.2)
    c.sfx("gallop", th - 0.6, 0.0)  # placeholder cue (skipped if no file)
    c.pop("#ab-tr", th, 0.35, origin="50% 50%")
    c.pop("#ab-tk", c.w("about-4", "קומנדו") - 0.3, 0.35, origin="50% 50%")
    c.out("#ab-tb", c.t("about-5") - 0.1)
    c.out("#ab-tr", c.t("about-5") - 0.1)
    c.out("#ab-tk", c.t("about-5") - 0.1)
    for k in range(4):
        c.to(f"#ab-h{k}", {"opacity": 0, "duration": 0.4}, c.t("about-5") - 0.3)
    tp = c.w("about-5", "והפתיעו")
    for k in range(3):
        c.fromTo(f"#ab-pr{k}", {"opacity": 0, "y": 90}, {"opacity": 1, "y": 0, "duration": 0.35, "ease": "back.out(2)"}, round(tp + k * 0.12, 3))
    c.to("#ab-brit", {"x": 760, "duration": 0.35, "ease": "power3.out"}, tp + 0.3)
    c.shake("#ab-b-cam", tp + 0.2, 8)
    c.sfx("rifle", tp + 0.25, 0.5)

    # C: the pen name
    c0, c1 = b1, c.t("about-7") - 0.2
    inner = (
        f'{kit.sky("gold")}<svg class="stage" viewBox="0 0 1920 1080">{kit.far_hills("gold", 720)}{kit.ground("gold", 860)}'
        + "".join(
            f'<g transform="translate({x} {y})"><g id="ab-x{k}" opacity="0"><path d="M -30 -30 L 30 30 M 30 -30 L -30 30" stroke="#B3261E" stroke-width="14" stroke-linecap="round"/></g></g>'
            for k, (x, y) in enumerate([(380, 300), (700, 420), (520, 600), (880, 250)])
        )
        + "</svg>"
        + B.lieutenant("ab-lt", 1450, 1000, 700)
        + '<div id="ab-pen" class="abs k-title" style="left:120px; top:330px; font-size:200px; color:#33210F; opacity:0">חכם־לאחר־מעשה</div>'
        + '<div id="ab-pen-en" class="abs label" style="left:130px; top:560px; font-size:44px; color:#5a3c22; opacity:0; direction:ltr">Backsight Forethought</div>'
    )
    c.shot("ab-c", c0, c1, inner, fade_in="blur")
    c.fromTo("#ab-lt", {"x": 120, "opacity": 0}, {"x": 0, "opacity": 1, "duration": 0.8, "ease": "expo.out"}, c0)
    tm = c.w("about-6", "טעויות")
    for k in range(4):
        c.pop(f"#ab-x{k}", round(tm - 0.2 + k * 0.15, 3), 0.3, origin="50% 50%")
    tpn = c.w("about-6", "משעשע")
    for k in range(4):
        c.out(f"#ab-x{k}", tpn - 0.3, 0.2)
    c.blur_in("#ab-pen", tpn + 0.35, 0.3)
    c.blur_in("#ab-pen-en", tpn + 1.1, 0.3)

    # D: the tank and Oxford
    d0, d1 = c1, c.t("about-8") - 0.2
    tank = f'<g transform="translate(2300 860)"><g id="ab-tank"><g transform="scale(-1.1 1.1)">{kit.tank(gold)}</g></g></g>'
    html = (
        '<div id="ab-t1" class="tag dark" style="right:200px; top:220px; font-size:48px; opacity:0">אחד מממציאי הטנק</div>'
        '<div id="ab-t2" class="tag" style="right:200px; top:330px; font-size:44px; opacity:0">פרופסור להיסטוריה צבאית, אוקספורד</div>'
    )
    B.side_shot(c, "ab-d", d0, d1, "day", tank, html, ground_y=860, fade_in="wipe")
    tt = c.w("about-7", "הטנק")
    c.to("#ab-tank", {"x": -1250, "duration": 3.0, "ease": "power2.out"}, tt - 1.0)
    c.pop("#ab-t1", tt, 0.35, origin="50% 50%")
    c.pop("#ab-t2", c.w("about-7", "פרופסור"), 0.35, origin="50% 50%")
    c.sfx("engine", tt - 1.0, 0.0)

    # E: the Hebrew edition
    e0, e1 = d1, c.t("about-9") - 0.2
    inner = (
        '<div class="full" style="background:radial-gradient(ellipse at 40% 45%, #4a3320 0%, #24180e 65%, #130c06 100%)"></div>'
        '<div class="abs" style="left:220px; top:150px; width:500px; height:712px;"><img id="ab-cov2" src="assets/book/cover.jpg" style="width:500px; height:712px; box-shadow:0 30px 60px rgba(0,0,0,.6); display:block; transform:rotate(-3deg)" alt=""></div>'
        '<div id="ab-1952" class="abs k-title" style="right:200px; top:220px; font-size:300px; color:#E3A33B; opacity:0">1952</div>'
        '<div id="ab-ed" class="abs label" style="right:210px; top:520px; font-size:48px; color:#F4E7CB; opacity:0">מהדורה עברית, הוצאת מערכות</div>'
        '<div id="ab-idf" class="abs label" style="right:210px; top:600px; font-size:48px; color:#F4E7CB; opacity:0">נלמד בצה״ל עד היום</div>'
    )
    c.shot("ab-e", e0, e1, inner, fade_in="blur")
    c.fromTo("#ab-cov2", {"y": 40, "opacity": 0}, {"y": 0, "opacity": 1, "duration": 0.9, "ease": "expo.out"}, e0)
    c.blur_in("#ab-1952", c.w("about-8", "1952") - 0.1, 0.3)
    c.blur_in("#ab-ed", c.w("about-8", "1952") + 0.5, 0.3)
    c.blur_in("#ab-idf", c.w("about-8", "ומפקדים"), 0.3)

    # F: everything happens in dreams
    f0 = e1
    pips = "".join(
        f'<g transform="translate({1460 - k * 150} 300)"><g id="ab-p{k}" opacity="0"><circle r="54" fill="#2c2a55" stroke="#F4E7CB" stroke-width="5"/>'
        f'<text y="22" text-anchor="middle" font-family="Karantina" font-weight="700" font-size="72" fill="#F4E7CB">{k + 1}</text></g></g>'
        for k in range(6)
    )
    html = (
        B.lieutenant("ab-sleep", 1020, 880, 470, shadow=False)
        + "".join(f'<div id="ab-z{k}" class="abs k-title" style="left:{980 + k * 60}px; top:{640 - k * 70}px; font-size:{80 + k * 30}px; color:#B9B3E6; opacity:0">z</div>' for k in range(3))
        + '<div class="abs" style="left:1240px; top:620px; width:440px; height:214px;"><img id="ab-slate" src="assets/art/slate.png" style="width:440px; height:214px; opacity:0" alt=""></div>'
        + '<div id="ab-022" class="abs k-title" style="left:1240px; width:440px; top:660px; text-align:center; font-size:120px; color:#E3A33B; opacity:0">0 / 22</div>'
    )
    B.side_shot(c, "ab-f", f0, c.dur, "dream", pips, html, ground_y=900, fade_in="iris")
    c.set("#ab-sleep", {"rotation": -84, "transformOrigin": "50% 90%", "y": 0}, f0)
    for k in range(3):
        c.fromTo(f"#ab-z{k}", {"opacity": 0, "y": 30}, {"opacity": 0.9, "y": -40, "duration": 1.8, "ease": "sine.out"}, round(f0 + 0.4 + k * 0.5, 3))
    t6 = c.w("about-10", "שש")
    for k in range(6):
        c.pop(f"#ab-p{k}", round(t6 - 0.3 + k * 0.1, 3), 0.35, origin="50% 50%")
    tz = c.w("about-10", "מאפס")
    for k in range(6):
        c.to(f"#ab-p{k}", {"scale": 0.85, "duration": 0.15, "yoyo": True, "repeat": 1, "transformOrigin": "50% 50%"}, round(tz + k * 0.05, 3))
    c.fade("#ab-slate", c.w("about-10", "השיעורים") - 0.3)
    c.blur_in("#ab-022", c.w("about-10", "השיעורים"), 0.3)
    c.sfx("whoosh", f0 - 0.1, 0.3)

    c.music("invest", 0, c.dur)


# ================================================================ terrain
def terrain(c):
    layers = "".join(
        f'<img id="tr-{k}" class="map" src="assets/art/layer-{k}.png" style="opacity:0" alt="">' for k in ("gully", "road", "river", "kraal", "farm")
    )
    pins = "".join(
        [
            kit.pin(452, 470, "נהר עיט-אויל", "tr-p-river", "navy"),
            kit.pin(geo.DRIFT[0] + 20, geo.DRIFT[1] + 30, "מעברות פתיים", "tr-p-drift", "red"),
            kit.pin(geo.KOPJE[0] + 120, geo.KOPJE[1] + 80, "גבעת המכשלה", "tr-p-kopje"),
            kit.pin(geo.KOPJE[0] - 10, geo.KOPJE[1] - 50, "כפר (קראל)", "tr-p-kraal", "dark"),
            kit.pin(geo.FARM[0] - 20, geo.FARM[1] + 30, "החווה של ברינק", "tr-p-farm", "rust"),
            kit.pin(geo.TELPEGA[0] + 60, geo.TELPEGA[1] + 40, "תל-פגע", "tr-p-tel"),
            kit.pin(330, 120, "הר החרטות", "tr-p-regrets"),
        ]
    )
    order = (
        '<div id="tr-order" class="abs" style="right:120px; top:170px; width:640px; padding:40px 48px; background:#F6ECD6; border:4px solid #1E1812; '
        'box-shadow:12px 14px 0 rgba(30,24,18,.35); opacity:0">'
        '<div class="k-title" style="color:#1E1812; font-size:96px">פקודה</div>'
        '<div class="label" style="font-size:44px; line-height:1.35; color:#1E1812; margin-top:14px">להחזיק את מעברות פתיים<br>בכל מחיר</div>'
        '<div class="label" style="font-size:36px; line-height:1.35; color:#5a4a36; margin-top:18px; font-weight:500">שיירת תגבורת תגיע<br>בעוד 3 עד 4 ימים</div></div>'
        '<div id="tr-enemy" class="tag red" style="left:820px; top:40px; font-size:44px; opacity:0">האויב: 100 מייל מכאן ⬆</div>'
        '<div id="tr-q" class="abs k-title" style="left:1010px; top:250px; font-size:220px; color:#B3261E; opacity:0">?</div>'
    )
    svg = (
        f'<g transform="translate({geo.DRIFT[0]} {geo.DRIFT[1]})"><g id="tr-ring" opacity="0"><circle r="70" fill="none" stroke="#B3261E" stroke-width="6" stroke-dasharray="12 9"/></g></g>'
    )
    sid = B.sand_shot(c, "tr", 0, c.dur, svg=svg, pins=layers + pins, over=order, cam=(960, 300, 1.9), base="sand-base", fade_in="blur")
    cam = "#tr-cam"
    c.cam(cam, 0.5, 960, 540, 1.0, dur=2.2, ease="power3.inOut")
    # river
    tr2 = c.t("terrain-2")
    c.fromTo("#tr-river", {"opacity": 1, "clipPath": "inset(0 100% 0 0)"}, {"opacity": 1, "clipPath": "inset(0 0% 0 0)", "duration": 2.0, "ease": "power2.inOut"}, tr2)
    c.pop("#tr-p-river", tr2 + 1.2, 0.35)
    tb = c.w("terrain-2", "הגדות")
    c.cam(cam, tb - 0.3, 760, 300, 1.8, dur=1.4)
    c.cam(cam, c.end("terrain-2") - 0.2, 960, 540, 1.0, dur=1.2)
    # road and drift
    t3 = c.t("terrain-3")
    c.fromTo("#tr-road", {"opacity": 1, "clipPath": "inset(0 0 100% 0)"}, {"opacity": 1, "clipPath": "inset(0 0 0% 0)", "duration": 1.6, "ease": "power2.inOut"}, t3)
    tm = c.w("terrain-3", "המעבר")
    c.cam(cam, tm - 0.4, geo.DRIFT[0], geo.DRIFT[1] + 40, 1.7, dur=1.3)
    c.fromTo("#tr-ring", {"opacity": 0, "scale": 0.5, "transformOrigin": "50% 50%"}, {"opacity": 1, "scale": 1, "duration": 0.4, "ease": "back.out(2)"}, tm)
    c.pop("#tr-p-drift", c.w("terrain-3", "מעברות"), 0.35)
    # kopje and kraal
    t4 = c.t("terrain-4")
    c.out("#tr-ring", t4)
    c.cam(cam, t4, geo.KOPJE[0], geo.KOPJE[1] - 40, 1.35, dur=1.6)
    c.fade("#tr-kraal", c.w("terrain-4", "כפר") - 0.2, 0.5)
    c.pop("#tr-p-kraal", c.w("terrain-4", "כפר"), 0.35)
    c.pop("#tr-p-kopje", c.w("terrain-4", "המכשלה") - 0.2, 0.35)
    # farm, Tel-Pega
    t5 = c.t("terrain-5")
    c.cam(cam, t5, geo.FARM[0] + 60, geo.FARM[1] + 120, 1.45, dur=1.6)
    c.fade("#tr-farm", c.w("terrain-5", "החווה") - 0.2, 0.5)
    c.pop("#tr-p-farm", c.w("terrain-5", "ברינק"), 0.35)
    c.pop("#tr-p-tel", c.w("terrain-5", "תל-פגע") - 0.2, 0.35)
    # Hill of Regrets
    t6 = c.t("terrain-6")
    c.cam(cam, t6, 520, 300, 1.25, dur=1.6)
    c.pop("#tr-p-regrets", c.w("terrain-6", "החרטות") - 0.3, 0.35)
    # the order
    t7 = c.t("terrain-7")
    c.cam(cam, t7, 960, 540, 1.0, dur=1.6)
    c.fade("#tr-gully", t7 + 0.4, 0.8)
    c.fromTo("#tr-order", {"opacity": 0, "x": 80, "rotation": 4}, {"opacity": 1, "x": 0, "rotation": 1.5, "duration": 0.7, "ease": "expo.out"}, c.w("terrain-7", "להחזיק") - 0.2)
    c.sfx("page", c.w("terrain-7", "להחזיק") - 0.2, 0.45)
    # 100 miles
    t8 = c.t("terrain-8")
    c.to("#tr-order", {"opacity": 0, "x": 60, "duration": 0.35, "ease": "power2.in"}, t8 - 0.1)
    c.pop("#tr-enemy", c.w("terrain-8", "מאה") - 0.2, 0.35, origin="50% 0%")
    c.fromTo("#tr-q", {"opacity": 0, "scale": 0.4, "transformOrigin": "50% 80%"}, {"opacity": 1, "scale": 1, "duration": 0.4, "ease": "back.out(2.4)"}, c.w("terrain-8", "לקרות") - 0.1)
    c.style(kit.PIN_CSS)
    c.music("invest", 0, c.dur)
