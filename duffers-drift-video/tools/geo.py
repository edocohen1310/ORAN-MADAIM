"""Shared geometry of the sand table (map space = 1920 x 1080 px, north up).

Laid out after the dream maps in the book (maps 2-7): the river bends around the
drift from the west and the north, the kopje with the kraal sits south-east of the
drift, the road runs north-south through the drift. Not to scale.
"""
import math

W, H = 1920, 1080

RIVER = (
    "M -60 1010 C 160 990, 360 930, 420 800 C 470 690, 440 520, 470 420 "
    "C 500 320, 600 262, 740 252 C 840 245, 900 252, 960 255 "
    "C 1050 259, 1130 250, 1220 272 C 1330 300, 1380 400, 1430 470 "
    "C 1480 540, 1560 575, 1680 578 C 1780 580, 1860 566, 1990 556"
)
ROAD = "M 1012 -40 C 1000 60, 990 170, 960 255 C 935 330, 925 470, 905 600 C 890 720, 870 850, 846 1120"
GULLY = "M 452 812 C 560 790, 660 812, 760 786 C 850 762, 930 770, 1000 742"

DRIFT = (960, 255)
KOPJE = (1200, 735)
KRAAL_R = 54
RISE = (905, 640)
TRENCH3 = ((815, 640), (995, 640))  # dreams 3 and 4: a straight line across the road
FARM = (1470, 150)
TELPEGA = (1660, 105)
REGRETS = (300, 30)


def _cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


def parse_path(d):
    toks = d.replace(",", " ").split()
    i, cur, segs = 0, None, []
    while i < len(toks):
        if toks[i] == "M":
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            i += 3
        elif toks[i] == "C":
            i += 1
            while i < len(toks) and toks[i] not in ("M", "C"):
                p1 = (float(toks[i]), float(toks[i + 1]))
                p2 = (float(toks[i + 2]), float(toks[i + 3]))
                p3 = (float(toks[i + 4]), float(toks[i + 5]))
                segs.append((cur, p1, p2, p3))
                cur = p3
                i += 6
        else:
            i += 1
    return segs


def sample(d, step=6.0):
    """Points (x, y, nx, ny) every ~step px along a path; n is the left-hand normal."""
    pts = []
    for seg in parse_path(d):
        n = 200
        prev = _cubic(*seg, 0)
        for k in range(1, n + 1):
            p = _cubic(*seg, k / n)
            pts.append((prev, p))
            prev = p
    out, acc = [], 0.0
    for a, b in pts:
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L == 0:
            continue
        acc += L
        if acc >= step:
            acc = 0.0
            out.append((b[0], b[1], -dy / L, dx / L))
    return out


def blob(cx, cy, rx, ry, seed=1, wob=0.07, n=72):
    """An irregular closed contour around (cx, cy)."""
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        r = 1 + wob * math.sin(3 * a + seed) + wob * 0.6 * math.sin(5 * a + seed * 2.3) + wob * 0.3 * math.sin(9 * a + seed * 0.7)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in pts[1:]) + " Z"
    return d


def rng(seed):
    """Deterministic pseudo-random numbers (no Math.random anywhere in the film)."""
    x = seed * 2654435761 % 2**32
    while True:
        x = (1103515245 * x + 12345) % 2**31
        yield x / 2**31


def bank_points(side=1, step=26, offset=40, xmin=-100, xmax=2100):
    """Points along one bank of the river (side=+1 south/inner, -1 north/outer)."""
    out = []
    for x, y, nx, ny in sample(RIVER, step):
        if xmin <= x <= xmax:
            out.append((x + nx * offset * side, y + ny * offset * side))
    return out
