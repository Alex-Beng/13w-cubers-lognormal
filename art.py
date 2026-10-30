# -*- coding: utf-8 -*-
"""手绘日系赛璐璐风格基元库（cairo + 程序化抖动）"""
import math, random
import cairo
import numpy as np

# ---------------- 素描 + 铅画调色 ----------------
# 纸：冷白速写纸；线：石墨灰；色：低饱和彩铅
PAPER   = (0.968, 0.960, 0.942)
PAPER2  = (0.944, 0.934, 0.912)
INK     = (0.185, 0.185, 0.200)
INK_SOFT= (0.400, 0.400, 0.425)
PINK    = (0.880, 0.700, 0.706)
PINK_D  = (0.775, 0.545, 0.575)
MINT    = (0.610, 0.775, 0.712)
MINT_D  = (0.430, 0.610, 0.560)
BUTTER  = (0.900, 0.800, 0.560)
BUTTER_D= (0.800, 0.672, 0.420)
SKY     = (0.590, 0.706, 0.822)
SKY_D   = (0.395, 0.518, 0.665)
LILAC   = (0.700, 0.660, 0.790)
LILAC_D = (0.505, 0.460, 0.600)
CORAL   = (0.815, 0.470, 0.430)
WHITE   = (1.0, 1.0, 1.0)
CREAM   = (0.980, 0.966, 0.928)

PALETTE = [PINK, MINT, BUTTER, SKY, LILAC, CORAL]

# 素描：排线与复线
HATCH_A = 0.075        # 排线浓度
HATCH_GAP = 8.5        # 排线间距
GHOST_A = 0.32         # 复线浓度

def ellipse_path(ctx, x, y, rx, ry, rot=0.0, a0=0.0, a1=2 * math.pi):
    """兼容 ctx.ellipse(x,y,rx,ry,rot,a0,a1) 的参数顺序"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, a0, a1)
    ctx.restore()


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def shade(c, k=0.86):
    return tuple(max(0, v * k) for v in c)

def tint(c, k=0.35):
    return mix(c, (1, 1, 1), k)

# ---------------- 缓动 ----------------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)

def lerp(a, b, t):
    return a + (b - a) * t


def pop_scale(ctx, cx, cy, sc):
    """以 (cx,cy) 为锚点缩放；sc≈0 时直接返回 False，避免退化矩阵"""
    if sc < 1e-3:
        return False
    ctx.translate(cx, cy)
    ctx.scale(sc, sc)
    ctx.translate(-cx, -cy)
    return True

def ease_io(t):
    t = clamp(t); return t * t * (3 - 2 * t)

def ease_out(t, p=3.0):
    t = clamp(t); return 1 - (1 - t) ** p

def ease_in(t, p=3.0):
    t = clamp(t); return t ** p

def ease_out_back(t, s=1.9):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1

def ease_out_elastic(t):
    t = clamp(t)
    if t in (0.0, 1.0): return t
    p = 0.36
    return 2 ** (-11 * t) * math.sin((t - p / 4) * (2 * math.pi) / p) + 1

def seg(t, a, b):
    """归一化到 [a,b] 区间的 0..1"""
    if b <= a: return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))

def pop(t, a, b, dur=0.18):
    """在 a 时刻弹出，b 时刻收回"""
    return ease_out_back(seg(t, a, a + dur)) * (1 - ease_in(seg(t, b - 0.12, b)))

# ---------------- 屏幕字体 ----------------
FONT_CJK = "Noto Sans SC"
FONT_JP  = "Yu Gothic"

def set_font(ctx, size, bold=True, jp=False):
    ctx.select_font_face(FONT_JP if jp else FONT_CJK,
                         cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text_width(ctx, s, size, bold=True, jp=False, spacing=0.0):
    set_font(ctx, size, bold, jp)
    return ctx.text_extents(s)[4] + spacing * max(0, len(s) - 1)

def draw_text(ctx, s, x, y, size, color=INK, bold=True, jp=False,
              align="left", outline=0, outline_color=WHITE, alpha=1.0, spacing=0.0):
    """带描边的手写感文字；align: left/center/right

    素描版：大字加一层错位副本，做出铅笔复写的手感。
    """
    set_font(ctx, size, bold, jp)
    w = ctx.text_extents(s)[4] + spacing * max(0, len(s) - 1)
    if align == "center": x -= w / 2
    elif align == "right": x -= w

    def _path(dx, dy):
        ctx.new_path()
        if spacing == 0.0:
            ctx.move_to(x + dx, y + dy)
            ctx.text_path(s)
        else:
            cx = x + dx
            for ch in s:
                ctx.move_to(cx, y + dy)
                ctx.text_path(ch)
                cx += ctx.text_extents(ch)[4] + spacing

    if size >= 24:
        u = max(0.9, size * 0.011)
        _path(u, -u * 0.78)
        ctx.set_source_rgba(*color, alpha * GHOST_A)
        ctx.fill()
    _path(0, 0)
    ctx.set_line_width(outline * 2)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*outline_color, alpha)
    ctx.stroke_preserve()
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()
    return w

# ---------------- 手绘抖动路径 ----------------
def jitter_path(ctx, pts, closed=False, amp=1.6, seed=0, smooth=True, step_scale=1.0):
    """把折线点列转成带手抖平滑的三次贝塞尔路径"""
    rnd = random.Random(seed)
    n = len(pts)
    P = [(p[0] + rnd.uniform(-amp, amp), p[1] + rnd.uniform(-amp, amp)) for p in pts]
    if smooth and n > 2:
        ctx.move_to(*P[0])
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p0 = P[(i - 1) % n]; p1 = P[i]; p2 = P[(i + 1) % n]; p3 = P[(i + 2) % n]
            if not closed:
                p0 = P[max(i - 1, 0)]; p3 = P[min(i + 2, n - 1)]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6.0 * step_scale, p1[1] + (p2[1] - p0[1]) / 6.0 * step_scale)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6.0 * step_scale, p2[1] - (p3[1] - p1[1]) / 6.0 * step_scale)
            ctx.curve_to(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
        if closed: ctx.close_path()
    else:
        ctx.move_to(*P[0])
        for p in P[1:]: ctx.line_to(*p)
        if closed: ctx.close_path()

def blot(ctx, x, y, r, color, alpha=1.0, seed=0, amp=0.10, wobble=7):
    """手绘色块：不规则圆形"""
    rnd = random.Random(seed)
    ctx.new_path()
    for i in range(wobble):
        a = i / wobble * 2 * math.pi
        rr = r * (1 + rnd.uniform(-amp, amp))
        px, py = x + math.cos(a) * rr, y + math.sin(a) * rr
        if i == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.close_path()
    ctx.set_source_rgba(*color, alpha)
    ctx.fill()

def marker_line(ctx, pts, width=7, color=INK, alpha=1.0, seed=0, closed=False,
                aa=True, amp=1.8):
    """粗黑马克笔描边"""
    ctx.new_path()
    jitter_path(ctx, pts, closed=closed, amp=amp, seed=seed)
    ctx.set_line_width(width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*color, alpha)
    ctx.stroke()

_HATCH_CACHE = {}


def _hatch_pattern(a=HATCH_A, gap=HATCH_GAP, angle=0.75, lw=1.15, color=INK):
    """斜排线的平铺图案：比逐帧画线快一个量级，且线距天然均匀"""
    key = (round(a, 3), round(gap, 2), round(angle, 3), round(lw, 2), color)
    pat = _HATCH_CACHE.get(key)
    if pat is not None:
        return pat
    S = max(6, int(round(gap)))
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
    c = cairo.Context(s)
    c.set_source_rgba(*color, a)
    c.set_line_width(lw)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(-S * 0.4, S * 0.5)
    c.line_to(S * 1.4, S * 0.5)
    c.stroke()
    pat = cairo.SurfacePattern(s)
    pat.set_extend(cairo.EXTEND_REPEAT)
    m = cairo.Matrix()
    m.rotate(angle)
    pat.set_matrix(m)
    _HATCH_CACHE[key] = pat
    return pat


def _hatch_fill(ctx, pts, amp, seed, closed, a=HATCH_A, gap=HATCH_GAP, angle=0.75):
    """在裁剪区内铺斜排线，给色块加铅笔影调"""
    if a <= 0:
        return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    if (x1 - x0) * (y1 - y0) < 240:
        return
    ctx.save()
    ctx.new_path()
    jitter_path(ctx, pts, closed=closed, amp=amp, seed=seed)
    ctx.clip()
    ctx.set_source(_hatch_pattern(a, gap, angle))
    ctx.paint()
    ctx.restore()


def fill_stroke(ctx, pts, fill, stroke=INK, width=6, seed=0, closed=True,
                amp=1.8, fill_alpha=1.0, hatch=True):
    ctx.new_path()
    jitter_path(ctx, pts, closed=closed, amp=amp, seed=seed)
    ctx.set_source_rgba(*fill, fill_alpha)
    ctx.fill()
    # 排线叠在色块上，再压主线：色块有了铅笔的颗粒感
    if hatch:
        _hatch_fill(ctx, pts, amp, seed + 7, closed)
    ctx.new_path()
    jitter_path(ctx, pts, closed=closed, amp=amp, seed=seed)
    ctx.set_line_width(width)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*stroke, 1.0)
    ctx.stroke()
    # 复线：略微偏一点的第二道，像反复描过的轮廓
    if width >= 3.2:
        ctx.new_path()
        jitter_path(ctx, pts, closed=closed, amp=amp * 1.15, seed=seed + 31)
        ctx.set_line_width(width * 0.45)
        ctx.set_source_rgba(*stroke, GHOST_A)
        ctx.stroke()

def _rrect_path(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def rrect(ctx, x, y, w, h, r, fill=None, stroke=INK, width=6, seed=0, amp=1.2,
          hatch=True):
    """圆角矩形：直接用圆弧画，不做抖动拟合

    卡片/标签这类规整块，抖动会把四角拉成伸出边框的横线，
    所以这里只留很轻的手感：排线 + 一道复线。
    """
    if fill is not None:
        _rrect_path(ctx, x, y, w, h, r)
        ctx.set_source_rgba(*fill, 1.0); ctx.fill()
        if hatch:
            _hatch_fill(ctx, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                        0.0, seed + 7, True)
    _rrect_path(ctx, x, y, w, h, r)
    ctx.set_line_width(width); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*stroke, 1.0); ctx.stroke()
    if width >= 3.2:
        _rrect_path(ctx, x + 0.9, y - 0.7, w, h, r)
        ctx.set_line_width(width * 0.40)
        ctx.set_source_rgba(*stroke, GHOST_A * 0.7); ctx.stroke()

def scalene_quad(ctx, x, y, w, h, fill, stroke=INK, width=6, seed=0, sl=0.12, amp=1.0):
    pts = [(x + w * sl, y), (x + w, y), (x + w * (1 - sl), y + h), (x, y + h)]
    fill_stroke(ctx, pts, fill, stroke, width, seed, True, amp)

# ---------------- 网点纸 ----------------
_tone_cache = {}
def screentone(ctx, x, y, w, h, color=INK, spacing=9, r=2.6, angle=0.6,
               alpha=1.0, clip_pts=None, phase=(0, 0)):
    """旋转点阵网屏；clip_pts 给定时只用其裁剪"""
    sa, ca = math.sin(angle), math.cos(angle)
    ctx.save()
    if clip_pts is not None:
        ctx.new_path()
        jitter_path(ctx, clip_pts, closed=True, amp=0.6, seed=7)
        ctx.clip()
    else:
        ctx.rectangle(x, y, w, h); ctx.clip()
    ctx.set_source_rgba(*color, alpha)
    diag = math.hypot(w, h) + spacing * 2
    cx0, cy0 = x + w / 2 + phase[0], y + h / 2 + phase[1]
    n = int(diag / spacing) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            u, v = i * spacing, j * spacing
            px = cx0 + u * ca - v * sa
            py = cy0 + u * sa + v * ca
            if x - 10 <= px <= x + w + 10 and y - 10 <= py <= y + h + 10:
                ctx.arc(px, py, r, 0, 2 * math.pi)
                ctx.fill()
    ctx.restore()

def halftone_grad(ctx, x, y, w, h, dirn="down", c1=PINK, c2=WHITE,
                  spacing=10, rmax=3.4, alpha=0.55):
    """网点渐变阴影（漫画式）"""
    n = int(h / spacing) + 1 if dirn == "down" else int(w / spacing) + 1
    ctx.set_source_rgba(*mix(c1, c2, 0.15), alpha)
    total = n
    for j in range(total):
        for i in range(int(w / spacing) + 1):
            t = (j / max(1, total - 1)) if dirn == "down" else (i / max(1, total - 1))
            r = rmax * (1 - t)
            if r < 0.4: continue
            ctx.arc(x + i * spacing + (spacing / 2 if j % 2 else 0), y + j * spacing, r, 0, 2 * math.pi)
            ctx.fill()

# ---------------- 气泡 / 拟声词 ----------------
def burst_points(x, y, r_out, r_in, spikes=11, seed=3, rot=0.0):
    rnd = random.Random(seed)
    pts = []
    for i in range(spikes * 2):
        a = rot + i / (spikes * 2) * 2 * math.pi
        r = (r_out * rnd.uniform(0.88, 1.14)) if i % 2 == 0 else (r_in * rnd.uniform(0.92, 1.08))
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
    return pts

def burst(ctx, x, y, r, fill=BUTTER, stroke=INK, width=6, spikes=11, seed=3,
          rot=0.0, alpha=1.0):
    pts = burst_points(x, y, r, r * 0.72, spikes, seed, rot)
    ctx.new_path()
    for i, p in enumerate(pts):
        if i == 0: ctx.move_to(*p)
        else: ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source_rgba(*fill, alpha); ctx.fill_preserve()
    ctx.set_line_width(width); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*stroke, alpha); ctx.stroke()

def speech_bubble(ctx, x, y, w, h, tail=(0, 0), fill=WHITE, alpha=1.0,
                  stroke=INK, width=5.5, seed=11):
    """椭圆对话气泡 + 尖尾"""
    ctx.new_path()
    ctx.save()
    ctx.translate(x + w / 2, y + h / 2)
    ctx.scale(w / 2, h / 2)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source_rgba(*fill, alpha)
    ctx.fill_preserve()
    ctx.set_line_width(width); ctx.set_source_rgba(*stroke, alpha); ctx.stroke()
    # 尾巴
    bx, by = x + w / 2, y + h / 2
    ang = math.atan2(tail[1] - by, tail[0] - bx)
    p1 = (bx + math.cos(ang - 0.30) * w * 0.48, by + math.sin(ang - 0.30) * h * 0.48)
    p2 = (bx + math.cos(ang + 0.30) * w * 0.48, by + math.sin(ang + 0.30) * h * 0.48)
    tip = tail
    ctx.new_path()
    ctx.move_to(*p1); ctx.line_to(*tip); ctx.line_to(*p2)
    ctx.set_source_rgba(*fill, alpha); ctx.fill_preserve()
    ctx.set_line_width(width); ctx.set_source_rgba(*stroke, alpha); ctx.stroke()
    # 盖住割线
    ctx.new_path()
    ctx.move_to(p1[0] + (tip[0] - p1[0]) * 0.10, p1[1] + (tip[1] - p1[1]) * 0.10)
    ctx.line_to(p2[0] + (tip[0] - p2[0]) * 0.10, p2[1] + (tip[1] - p2[1]) * 0.10)
    ctx.set_source_rgba(*fill, alpha)
    ctx.set_line_width(width * 0.0)
    ctx.stroke()

def rough_arrow(ctx, x1, y1, x2, y2, width=7, color=INK, head=22, curve=0.0, seed=5, alpha=1.0):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    cx, cy = mx + nx * curve, my + ny * curve
    ctx.new_path()
    ctx.move_to(x1, y1)
    ctx.curve_to(x1 + (cx - x1) * 0.7, y1 + (cy - y1) * 0.7, cx, cy, x2, y2)
    ctx.set_line_width(width); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*color, alpha); ctx.stroke()
    # 箭头
    a = math.atan2(y2 - cy, x2 - cx)
    p1 = (x2 - math.cos(a - 0.45) * head, y2 - math.sin(a - 0.45) * head)
    p2 = (x2 - math.cos(a + 0.45) * head, y2 - math.sin(a + 0.45) * head)
    ctx.new_path(); ctx.move_to(*p1); ctx.line_to(x2, y2); ctx.line_to(*p2)
    ctx.set_line_width(width); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*color, alpha); ctx.stroke()

def speed_lines(ctx, cx, cy, r_in, r_out, n=28, color=INK, alpha=0.5, seed=1, width=5,
                spread=2 * math.pi, rot=0.0, gap=0.0):
    rnd = random.Random(seed)
    ctx.set_line_width(width); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        a = rot + (i / n) * spread + rnd.uniform(-0.03, 0.03) + gap
        r0 = r_in * rnd.uniform(0.95, 1.25)
        r1 = r_out * rnd.uniform(0.85, 1.15)
        ctx.move_to(cx + math.cos(a) * r0, cy + math.sin(a) * r0)
        ctx.line_to(cx + math.cos(a) * r1, cy + math.sin(a) * r1)
    ctx.set_source_rgba(*color, alpha); ctx.stroke()

def sparkle(ctx, x, y, r, color=BUTTER, rot=0.0, width=4, alpha=1.0, n=4):
    ctx.new_path()
    for i in range(n):
        a = rot + i * math.pi / n * 2
        ctx.move_to(x, y)
        ctx.line_to(x + math.cos(a) * r, y + math.sin(a) * r)
    ctx.set_line_width(width); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*color, alpha); ctx.stroke()

# ---------------- 铅笔阴影 ----------------
def drop_shadow(ctx, x, y, w, h, color=INK_SOFT, alpha=0.16, off=(10, 12), spacing=7.5, r=3.0):
    """卡片底下的铅笔投影：一层排线 + 外沿再压淡一圈，不用网点"""
    if alpha <= 0:
        return
    pts = []
    steps = 6
    x0, y0 = x + off[0], y + off[1]
    corners = [(x0 + w - r, y0 + r, -math.pi / 2, 0), (x0 + w - r, y0 + h - r, 0, math.pi / 2),
               (x0 + r, y0 + h - r, math.pi / 2, math.pi), (x0 + r, y0 + r, math.pi, 1.5 * math.pi)]
    for cx, cy, a0, a1 in corners:
        for i in range(steps + 1):
            a = lerp(a0, a1, i / steps)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    ctx.save()
    ctx.new_path()
    jitter_path(ctx, pts, closed=True, amp=0.6, seed=13)
    ctx.save()
    ctx.clip_preserve()
    ctx.set_source_rgba(*color, alpha * 0.42)
    ctx.fill()
    ctx.restore()
    ctx.clip()
    ctx.set_source(_hatch_pattern(alpha * 1.1, spacing, 0.75, 1.6, color))
    ctx.paint()
    ctx.restore()
