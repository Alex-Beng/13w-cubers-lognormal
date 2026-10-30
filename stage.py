# -*- coding: utf-8 -*-
"""画面公共件：纸张底、标题栏、进度条、转场、卡片"""
import math
import cairo
from art import *
from characters2 import draw_cube, R, Y_SOLE
from characters3 import draw_laoba
from timeline import SCENES, DUR

W, H = 1920, 1080
M = 120                      # 左右安全边

_BG = None
_GRAIN = None


def _grain_tile(n=192):
    """纸纹：细颗粒 + 少量纤维，做成可平铺的小块"""
    import random
    rnd = random.Random(4242)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, n, n)
    c = cairo.Context(s)
    for _ in range(n * n // 3):
        px, py = rnd.uniform(0, n), rnd.uniform(0, n)
        a = rnd.uniform(0.008, 0.030)
        c.set_source_rgba(*INK, a)
        c.arc(px, py, rnd.uniform(0.5, 1.15), 0, 2 * math.pi)
        c.fill()
    for _ in range(26):
        px, py = rnd.uniform(0, n), rnd.uniform(0, n)
        a = rnd.uniform(0.4, 1.4)
        L = rnd.uniform(6, 22)
        c.set_source_rgba(*INK, 0.020)
        c.set_line_width(0.7)
        c.move_to(px, py)
        c.curve_to(px + L * 0.3, py + math.sin(a) * 3, px + L * 0.7, py + math.cos(a) * 3,
                   px + L, py + math.sin(a) * 1.5)
        c.stroke()
    return s


def paper(ctx):
    """速写纸底：冷白 + 极淡横格 + 石墨边线 + 纸纹（首次构建后缓存）"""
    global _BG, _GRAIN
    if _BG is None:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = cairo.Context(s)
        c.set_source_rgb(*PAPER); c.paint()
        # 横格：铅笔划线，不是印刷线
        for y in range(84, H, 44):
            c.set_source_rgba(*INK, 0.030)
            c.set_line_width(1.0)
            c.move_to(0, y + 0.5); c.line_to(W, y + 0.5); c.stroke()
        # 左边距：石墨细线
        c.set_source_rgba(*INK, 0.075)
        c.set_line_width(1.3)
        c.move_to(M - 52, 0); c.line_to(M - 52, H); c.stroke()
        # 纸纹
        if _GRAIN is None:
            _GRAIN = _grain_tile()
        gp = cairo.SurfacePattern(_GRAIN)
        gp.set_extend(cairo.EXTEND_REPEAT)
        c.set_source(gp); c.paint()
        # 四角轻微压暗，像翻旧的本子
        vg = cairo.RadialGradient(W * 0.5, H * 0.48, H * 0.35, W * 0.5, H * 0.48, H * 1.05)
        vg.add_color_stop_rgba(0.0, *INK, 0.0)
        vg.add_color_stop_rgba(1.0, *INK, 0.035)
        c.set_source(vg); c.paint()
        _BG = s
    ctx.set_source_surface(_BG, 0, 0)
    ctx.paint()

def title_block(ctx, kicker, line1, line2=None, a=1.0, y0=118, size=70,
                c2=CORAL, accent=None):
    """左上标题区"""
    if a <= 0.001: return
    ctx.save()
    shift = (1 - ease_out(a, 3)) * -26
    if kicker:
        draw_text(ctx, kicker, M + shift, y0 - 44, 25, INK_SOFT, bold=True, alpha=a * 0.9)
    draw_text(ctx, line1, M + shift, y0 + 34, size, INK, alpha=a)
    if line2:
        draw_text(ctx, line2, M + shift * 1.4, y0 + 34 + size * 1.16, size, c2, alpha=a)
    if accent:
        w = text_width(ctx, line1, size)
        burst(ctx, M + shift + w + 34, y0 - 6, 46, BUTTER, INK, 5, 11, 5, alpha=a * 0.95)
        draw_text(ctx, "！", M + shift + w + 34, y0 + 12, 42, INK, align="center", alpha=a)
    ctx.restore()

def progress(ctx, t):
    y = H - 34
    ctx.new_path(); ctx.rectangle(M, y, W - 2 * M, 4)
    ctx.set_source_rgba(*INK, 0.10); ctx.fill()
    w = (W - 2 * M) * clamp(t / DUR)
    ctx.new_path(); ctx.rectangle(M, y, w, 4)
    ctx.set_source_rgba(*CORAL, 0.55); ctx.fill()
    ctx.new_path(); ctx.arc(M + w, y + 2, 6.5, 0, 2 * math.pi)
    ctx.set_source_rgba(*CORAL, 0.85); ctx.fill()

def card(ctx, x, y, w, h, a=1.0, fill=None, seed=4, shadow=True):
    if a <= 0.001: return
    ctx.save()
    ctx.translate(0, (1 - ease_out(a, 3)) * 16)
    if shadow:
        drop_shadow(ctx, x, y, w, h, INK_SOFT, 0.14 * a, (7, 9), 7.5, 3.0)
    rrect(ctx, x, y, w, h, 16, fill if fill else PAPER2, INK, 4.6, seed, 0.8)
    ctx.restore()

def foot(ctx, s, x=None, y=None, size=24, color=INK_SOFT, a=0.75, align="right"):
    draw_text(ctx, s, x if x is not None else W - M, y if y is not None else H - 62,
              size, color, bold=False, alpha=a, align=align)

# ---------------- 老芭：站姿基准 ----------------
# draw_laoba 内部：hb = R*s*head_k（默认 0.90）
#   头顶(发冠) = y - 1.50 hb，鞋底 = y + 3.16 hb，全身高 = 4.64 hb
_HEAD_K = 0.90
_HAT_TOP = 1.50                 # 发冠顶：头心以上
_TOTAL_H = 4.64

def sole_y(s):
    return R * s * _HEAD_K * Y_SOLE

def stand_s(px_height):
    """给定期望全身高度(px)，返回 draw_laoba 的 s"""
    return px_height / (R * _HEAD_K * _TOTAL_H)

def laoba_at(ctx, x, sole, s, t, **kw):
    """按“脚底 y”摆放老芭"""
    draw_laoba(ctx, x, sole - sole_y(s), s, t, **kw)

# ---------------- 文字条 ----------------
def pop_scale_safe(ctx, cx, cy, sc):
    """push 变换后以 (cx,cy) 为锚点缩放；sc 过小时不 push，返回 False（调用方直接 return）"""
    if sc < 1e-3:
        return False
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(sc, sc)
    ctx.translate(-cx, -cy)
    return True

def zoom(ctx, cx, cy, sc):
    """pop_scale_safe 的别名，给自己管的调用方用"""
    return pop_scale_safe(ctx, cx, cy, sc)

def ribbon(ctx, s, cx, y, size=40, color=INK, fill=BUTTER, a=1.0, pad=26):
    if a <= 0.001: return
    w = text_width(ctx, s, size) + pad * 2
    h = size * 1.62
    x = cx - w / 2
    sc = ease_out_back(a)
    if not pop_scale_safe(ctx, cx, y + h / 2, sc):
        return
    pts = [(x - w * 0.03, y), (x + w * 1.03, y - 6), (x + w, y + h), (x - w * 0.01, y + h + 5)]
    fill_stroke(ctx, pts, fill, INK, 5, seed=17, amp=1.2)
    draw_text(ctx, s, cx, y + h * 0.70, size, color, align="center")
    ctx.restore()


# ---------------- 解说字幕 ----------------
SUB_Y = H - 128          # 字幕基线
SUB_SIZE = 40


def subtitle(ctx, s, a=1.0):
    """底部解说字幕：半透明纸底 + 描边字，压在每个场景之上"""
    if not s or a <= 0.004:
        return
    ctx.save()
    sc = 0.82 + 0.18 * ease_out_back(a)
    w = text_width(ctx, s, SUB_SIZE)
    bw = w + 64
    bh = 74
    bx = W / 2 - bw / 2
    by = SUB_Y - 52
    if sc < 1e-3:
        ctx.restore()
        return
    ctx.translate(W / 2, by + bh / 2)
    ctx.scale(sc, sc)
    ctx.translate(-W / 2, -(by + bh / 2))
    # 底：纸色圆角 + 细边
    r = 18.0
    ctx.new_path()
    ctx.arc(bx + bw - r, by + r, r, -math.pi / 2, 0)
    ctx.arc(bx + bw - r, by + bh - r, r, 0, math.pi / 2)
    ctx.arc(bx + r, by + bh - r, r, math.pi / 2, math.pi)
    ctx.arc(bx + r, by + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()
    ctx.set_source_rgba(*PAPER, 0.92 * a); ctx.fill_preserve()
    ctx.set_line_width(2.6); ctx.set_source_rgba(*INK, 0.18 * a); ctx.stroke()
    # 字
    draw_text(ctx, s, W / 2, SUB_Y, SUB_SIZE, INK, align="center", alpha=a, bold=True)
    ctx.restore()

