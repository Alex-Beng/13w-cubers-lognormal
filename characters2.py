# -*- coding: utf-8 -*-
"""角色 v4：老芭（Q 版古风）+ 小方（圆角拟人魔方）

尺寸约定（hb = R*s）：
    头顶(发冠)  y - 1.50 hb
    头顶(脸)    y - 0.98 hb
    下巴        y + 0.95 hb
    肩          y + 1.22 hb
    腰          y + 1.74 hb
    裙摆        y + 2.52 hb
    脚踝        y + 3.00 hb
    鞋底        y + 3.14 hb
    全身高      = 4.64 hb
"""
import math
from art import *
from art import _hatch_fill
from characters import R

# ---------------- 调色 ----------------
SKIN     = (0.996, 0.930, 0.895)
SKIN_SH  = (0.960, 0.795, 0.790)
HAIR     = (0.290, 0.232, 0.240)      # 深栗
HAIR_SH  = (0.196, 0.150, 0.168)
HAIR_HL  = (0.520, 0.430, 0.440)
ROBE     = (0.660, 0.790, 0.640)      # 竹青外袍
ROBE_SH  = (0.500, 0.640, 0.505)
ROBE_HL  = (0.815, 0.885, 0.780)
ROBE_ED  = (0.925, 0.945, 0.900)      # 袍缘浅色
INNER    = (0.196, 0.300, 0.545)      # 内层深蓝
INNER_SH = (0.140, 0.215, 0.415)
INNER_HL = (0.320, 0.450, 0.690)
LILAC    = (0.720, 0.640, 0.870)      # 紫蝶 / 花
LILAC_D  = (0.535, 0.450, 0.720)
LILAC_L  = (0.845, 0.795, 0.930)
GOLD     = (0.900, 0.760, 0.430)
GOLD_D   = (0.740, 0.585, 0.290)
SHOE     = (0.420, 0.640, 0.610)
BLUSH    = (0.960, 0.700, 0.700)
MOUTH    = (0.545, 0.265, 0.320)
TONGUE   = (0.930, 0.600, 0.580)
WHITEB   = (0.995, 0.995, 0.990)
EYE_TOP  = (0.300, 0.245, 0.330)
EYE_BOT  = (0.560, 0.470, 0.640)

# 全身相对头心的高度（hb 倍数），stage.sole_y 会引用
TOTAL_H = 4.64


# ================= 脸 =================
def _eye(ctx, ex, ey, w, h, look, expr="normal", blink=0.0):
    """大眼：厚上睑 + 渐变虹膜 + 双高光 + 下明亮弧"""
    if expr == "happy" or blink > 0.82:
        # 闭眼笑：上弧 + 下弯，像月牙，不带睫毛
        ctx.new_path()
        ctx.move_to(ex - w * 0.98, ey + h * 0.10)
        ctx.curve_to(ex - w * 0.40, ey - h * 0.92, ex + w * 0.40, ey - h * 0.92, ex + w * 0.98, ey + h * 0.10)
        ctx.set_line_width(w * 0.40); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
        return
    hh = h * max(0.10, 1.0 - blink)
    # 眼白
    ctx.new_path(); ellipse_path(ctx, ex, ey, w * 1.02, hh * 1.04, 0, 0, 2 * math.pi)
    ctx.set_source_rgb(*WHITEB); ctx.fill()
    ctx.save()
    ctx.new_path(); ellipse_path(ctx, ex, ey, w * 1.02, hh * 1.04, 0, 0, 2 * math.pi); ctx.clip()
    ix, iy = ex + look[0] * w * 0.20, ey + look[1] * h * 0.14 + hh * 0.04
    iw, ih = w * 0.90, hh * 0.94
    # 虹膜：上深下浅
    for i in range(16):
        u = i / 15.0
        ctx.set_source_rgb(*mix(EYE_TOP, EYE_BOT, u))
        ellipse_path(ctx, ix, iy - ih + ih * 2.02 * u + ih * 0.10, iw, ih * 0.30, 0, 0, 2 * math.pi)
        ctx.fill()
    # 上半部压暗（上睑投影）
    ctx.set_source_rgba(*EYE_TOP, 0.55)
    ellipse_path(ctx, ix, iy - ih * 0.52, iw * 1.05, ih * 0.52, 0, 0, 2 * math.pi); ctx.fill()
    # 瞳孔
    ctx.set_source_rgb(*mix(EYE_TOP, INK, 0.45))
    ellipse_path(ctx, ix, iy + ih * 0.20, iw * 0.48, ih * 0.58, 0, 0, 2 * math.pi); ctx.fill()
    # 下缘反光
    ctx.set_source_rgba(*mix(EYE_BOT, WHITE, 0.55), 0.9)
    ellipse_path(ctx, ix, iy + ih * 0.68, iw * 0.66, ih * 0.24, 0, 0, 2 * math.pi); ctx.fill()
    # 高光：大 + 小
    ctx.set_source_rgba(1, 1, 1, 0.97)
    ellipse_path(ctx, ix - iw * 0.34, iy - ih * 0.48, w * 0.33, w * 0.42, 0, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.80)
    ctx.arc(ix + iw * 0.42, iy + ih * 0.30, w * 0.155, 0, 2 * math.pi); ctx.fill()
    if expr == "shock":
        ctx.set_source_rgba(1, 1, 1, 0.92)
        ellipse_path(ctx, ix, iy + ih * 0.06, iw * 0.18, ih * 0.24, 0, 0, 2 * math.pi); ctx.fill()
    ctx.restore()
    # 上睑：粗+外眼角上挑
    ctx.new_path()
    ctx.move_to(ex - w * 1.12, ey - hh * 0.22)
    ctx.curve_to(ex - w * 0.66, ey - hh * 1.34, ex + w * 0.64, ey - hh * 1.34, ex + w * 1.16, ey - hh * 0.16)
    ctx.set_line_width(w * 0.46); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*INK); ctx.stroke()
    # 外眼角睫毛（两根）
    for k, (dx, dy) in enumerate(((0.36, 0.44), (0.62, 0.20))):
        ctx.new_path()
        ctx.move_to(ex + w * 1.02, ey - hh * (0.34 + k * 0.16))
        ctx.line_to(ex + w * (1.28 + k * 0.16), ey - hh * (0.78 + dy))
        ctx.set_line_width(w * 0.20); ctx.set_source_rgb(*INK); ctx.stroke()
    # 下眼睑：亮线（二次元常用）
    ctx.new_path()
    ctx.move_to(ex - w * 0.78, ey + hh * 0.98)
    ctx.curve_to(ex - w * 0.22, ey + hh * 1.24, ex + w * 0.34, ey + hh * 1.18, ex + w * 0.80, ey + hh * 0.86)
    ctx.set_line_width(w * 0.20); ctx.set_source_rgba(*mix(SKIN_SH, INK, 0.25), 0.85)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def _brow(ctx, ex, ey, w, expr):
    if expr in ("normal", "think", "smug"):
        return
    ctx.new_path()
    if expr == "shock":
        ctx.move_to(ex - w * 0.7, ey - w * 0.30)
        ctx.curve_to(ex - w * 0.2, ey - w * 0.78, ex + w * 0.3, ey - w * 0.78, ex + w * 0.7, ey - w * 0.26)
    else:
        ctx.move_to(ex - w * 0.7, ey - w * 0.10)
        ctx.curve_to(ex - w * 0.2, ey - w * 0.58, ex + w * 0.3, ey - w * 0.52, ex + w * 0.8, ey - w * 0.18)
    ctx.set_line_width(w * 0.26); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*mix(HAIR_SH, INK, 0.25)); ctx.stroke()


def _mouth(ctx, x, y, expr, open_k=0.0, u=1.0):
    """u = 嘴的尺度（= rr），所有尺寸随脸缩放"""
    w = 11 * u
    if expr == "shock":
        ctx.new_path(); ellipse_path(ctx, x, y + 3 * u, 7 * u, 10.5 * u, 0, 0, 2 * math.pi)
        ctx.set_source_rgb(*MOUTH); ctx.fill_preserve()
        ctx.set_line_width(3.4 * u); ctx.set_source_rgb(*INK); ctx.stroke()
    elif expr == "happy" or open_k > 0.35:
        o = max(open_k, 0.62)
        ctx.new_path()
        ctx.move_to(x - w, y - 1.5 * u)
        ctx.curve_to(x - w * 0.76, y + 19 * o * u, x + w * 0.76, y + 19 * o * u, x + w, y - 1.5 * u)
        ctx.curve_to(x + w * 0.42, y + 5.5 * o * u, x - w * 0.42, y + 5.5 * o * u, x - w, y - 1.5 * u)
        ctx.close_path(); ctx.set_source_rgb(*MOUTH); ctx.fill_preserve()
        ctx.set_line_width(3.2 * u); ctx.set_source_rgb(*INK); ctx.stroke()
        ctx.save(); ctx.clip()
        ctx.set_source_rgb(*TONGUE)
        ellipse_path(ctx, x, y + 19 * o * u + u, 7 * u, 6 * o * u, 0, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    elif expr == "smug":
        ctx.new_path(); ctx.move_to(x - 9 * u, y - u)
        ctx.curve_to(x - 2 * u, y + 5.5 * u, x + 7 * u, y + 3.5 * u, x + 11 * u, y - 4.5 * u)
        ctx.set_line_width(3.4 * u); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
    elif expr == "sad":
        ctx.new_path(); ctx.move_to(x - 8 * u, y + 4.5 * u)
        ctx.curve_to(x - 2.5 * u, y - 2 * u, x + 2.5 * u, y - 2 * u, x + 8 * u, y + 4.5 * u)
        ctx.set_line_width(3.4 * u); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
    else:
        ctx.new_path(); ctx.move_to(x - 7 * u, y)
        ctx.curve_to(x - 2.6 * u, y + 5.5 * u, x + 2.6 * u, y + 5.5 * u, x + 7 * u, y)
        ctx.set_line_width(3.6 * u); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()


def draw_face(ctx, x, y, s=1.0, t=0.0, expr="normal", look=(0, 0),
              open_k=0.0, blink=0.0, mouth=True):
    """Q 版大脸：宽度 ≈ 2.0，下巴圆钝"""
    rr = R * s
    def face_path():
        ctx.new_path()
        ctx.move_to(x - rr * 0.99, y - rr * 0.30)
        ctx.curve_to(x - rr * 1.04, y - rr * 1.04, x + rr * 1.04, y - rr * 1.04, x + rr * 0.99, y - rr * 0.30)
        ctx.curve_to(x + rr * 1.00, y + rr * 0.34, x + rr * 0.78, y + rr * 0.80, x + rr * 0.40, y + rr * 0.92)
        ctx.curve_to(x + rr * 0.14, y + rr * 0.99, x - rr * 0.14, y + rr * 0.99, x - rr * 0.40, y + rr * 0.92)
        ctx.curve_to(x - rr * 0.78, y + rr * 0.80, x - rr * 1.00, y + rr * 0.34, x - rr * 0.99, y - rr * 0.30)
        ctx.close_path()
    face_path()
    ctx.set_source_rgb(*SKIN); ctx.fill()
    # 下巴 + 颈部投影
    ctx.save(); face_path(); ctx.clip()
    ctx.set_source_rgba(*SKIN_SH, 0.42)
    ctx.new_path()
    ctx.move_to(x - rr * 0.80, y + rr * 0.70)
    ctx.curve_to(x - rr * 0.40, y + rr * 1.10, x + rr * 0.40, y + rr * 1.10, x + rr * 0.80, y + rr * 0.70)
    ctx.line_to(x + rr * 0.90, y + rr * 1.10); ctx.line_to(x - rr * 0.90, y + rr * 1.10)
    ctx.close_path(); ctx.fill()
    # 腮红：细网点
    for sx in (-1, 1):
        ctx.save()
        ctx.new_path()
        ellipse_path(ctx, x + sx * rr * 0.62, y + rr * 0.42, rr * 0.23, rr * 0.13, 0, 0, 2 * math.pi)
        ctx.clip()
        ctx.set_source_rgba(*BLUSH, 0.75)
        for j in range(4):
            for i in range(8):
                ctx.arc(x + sx * rr * 0.62 - rr * 0.20 + i * rr * 0.056,
                        y + rr * 0.34 + j * rr * 0.054, rr * 0.021, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    ctx.restore()
    face_path()
    ctx.set_line_width(rr * 0.075); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(*INK); ctx.stroke()

    ex = rr * 0.44; ey = y + rr * 0.16
    ew, eh = rr * 0.290, rr * 0.360
    for sx in (-1, 1):
        _brow(ctx, x + sx * ex, ey - rr * 0.52, ew, expr)
    for sx in (-1, 1):
        _eye(ctx, x + sx * ex, ey, ew, eh, (look[0] * sx * 0.6 + look[0] * 0.4, look[1]), expr, blink)
    # 小鼻子
    ctx.new_path(); ellipse_path(ctx, x + look[0] * rr * 0.02, y + rr * 0.46, rr * 0.026, rr * 0.02, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*SKIN_SH, 0.9); ctx.fill()
    if mouth:
        _mouth(ctx, x, y + rr * 0.68, expr, open_k, u=rr / 80.0)


# ================= 头发 =================
def _hair_back(ctx, x, y, hb, t, wind=0.0):
    """后发：整颗蓬松发量 + 垂到腰"""
    sw = math.sin(t * 1.7) * hb * 0.03 + wind
    pts = [(x - hb * 0.30, y - hb * 1.42),
           (x - hb * 1.16, y - hb * 0.86),
           (x - hb * 1.32 + sw, y + hb * 0.10),
           (x - hb * 1.24 + sw * 1.5, y + hb * 0.92),
           (x - hb * 0.92 + sw * 1.6, y + hb * 1.52),
           (x - hb * 0.30 + sw * 1.2, y + hb * 1.74),
           (x + hb * 0.34 + sw, y + hb * 1.74),
           (x + hb * 0.96 + sw * 1.3, y + hb * 1.50),
           (x + hb * 1.26 + sw * 1.4, y + hb * 0.88),
           (x + hb * 1.34 + sw * 0.8, y + hb * 0.06),
           (x + hb * 1.16, y - hb * 0.88),
           (x + hb * 0.30, y - hb * 1.42),
           (x, y - hb * 1.52)]
    fill_stroke(ctx, pts, HAIR, INK, hb * 0.072, seed=211, amp=1.1)
    # 内侧稍亮
    ctx.save()
    ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.6, seed=211); ctx.clip()
    ctx.set_source_rgba(*mix(HAIR, HAIR_HL, 0.35), 0.30)
    ctx.new_path()
    ctx.move_to(x - hb * 0.70, y + hb * 0.30)
    ctx.curve_to(x - hb * 0.30, y + hb * 1.40, x + hb * 0.30, y + hb * 1.40, x + hb * 0.70, y + hb * 0.30)
    ctx.line_to(x + hb * 0.70, y + hb * 1.80); ctx.line_to(x - hb * 0.70, y + hb * 1.80)
    ctx.close_path(); ctx.fill()
    ctx.restore()


def _bun(ctx, x, y, hb, t):
    """头顶双丸子 + 绕发圈的细编发"""
    sw = math.sin(t * 1.6) * hb * 0.012
    for sx in (-1, 1):
        bx = x + sx * hb * 0.52
        by = y - hb * 1.42 + sx * hb * 0.02 + sw
        br = hb * 0.36
        ctx.new_path(); ellipse_path(ctx, bx, by, br * 1.06, br, 0, 0, 2 * math.pi)
        ctx.set_source_rgb(*HAIR); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.062); ctx.set_source_rgb(*INK); ctx.stroke()
        # 发丝
        ctx.new_path()
        for i in range(5):
            u = i / 4.0
            a = -0.9 + u * 1.8
            ctx.move_to(bx + math.cos(a) * br * 0.56, by - br * 0.40)
            ctx.curve_to(bx + math.cos(a) * br * 0.44, by - br * 0.06,
                         bx + math.cos(a + 0.12) * br * 0.60, by + br * 0.28,
                         bx + math.cos(a + 0.26) * br * 0.74, by + br * 0.52)
        ctx.set_line_width(hb * 0.016); ctx.set_source_rgba(*HAIR_SH, 0.85)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        # 高光弧
        ctx.new_path()
        ctx.move_to(bx - br * 0.56, by - br * 0.42)
        ctx.curve_to(bx - br * 0.10, by - br * 0.86, bx + br * 0.44, by - br * 0.72, bx + br * 0.62, by - br * 0.30)
        ctx.set_line_width(hb * 0.052); ctx.set_source_rgba(*HAIR_HL, 0.55)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        # 发圈：金环 + 小蝶
        ctx.new_path(); ellipse_path(ctx, bx + sx * br * 0.10, by + br * 0.94, br * 0.56, br * 0.20, 0, 0, 2 * math.pi)
        ctx.set_line_width(hb * 0.048); ctx.set_source_rgb(*GOLD); ctx.stroke()
        _butterfly(ctx, bx + sx * br * 0.42, by + br * 0.92, br * 0.70, t + sx * 0.4, flip=sx)
        _flower(ctx, bx - sx * br * 0.34, by - br * 0.44, br * 0.26, t + sx, alpha=0.95)


def _butterfly(ctx, x, y, r, t=0.0, flip=1, alpha=1.0):
    """紫蝶：四片翅 + 触角；flip=-1 镜像"""
    ctx.save()
    ctx.translate(x, y); ctx.scale(flip, 1); ctx.rotate(-0.16 + math.sin(t * 2.2) * 0.05)
    for k, (ang, ln, wd, col) in enumerate(((-0.75, 1.02, 0.62, LILAC),
                                            (-2.30, 0.86, 0.50, LILAC_D),
                                            (0.55, 0.72, 0.44, LILAC_L),
                                            (-2.90, 0.60, 0.34, LILAC_D))):
        ctx.save(); ctx.rotate(ang)
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.curve_to(ln * r * 0.30, -wd * r, ln * r * 0.96, -wd * r * 0.62, ln * r, 0)
        ctx.curve_to(ln * r * 0.86, wd * r * 0.66, ln * r * 0.28, wd * r * 0.70, 0, 0)
        ctx.close_path()
        ctx.set_source_rgba(*col, alpha); ctx.fill_preserve()
        ctx.set_line_width(r * 0.075); ctx.set_source_rgba(*mix(LILAC_D, INK, 0.45), alpha); ctx.stroke()
        ctx.set_source_rgba(*mix(col, WHITE, 0.55), 0.55 * alpha)
        ctx.arc(ln * r * 0.52, -wd * r * 0.12, r * 0.10, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    # 触角
    for sy in (-1, 1):
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.curve_to(r * 0.10, sy * r * 0.30, r * 0.42, sy * r * 0.40, r * 0.52, sy * r * 0.18)
        ctx.set_line_width(r * 0.056); ctx.set_source_rgba(*ink(0.55), alpha)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.new_path(); ellipse_path(ctx, 0, 0, r * 0.13, r * 0.34, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*mix(LILAC_D, INK, 0.30), alpha); ctx.fill()
    ctx.restore()


def ink(a=1.0):
    return INK


def _flower(ctx, x, y, r, t=0.0, alpha=1.0):
    """五瓣紫花 + 金心"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.sin(t * 1.4) * 0.08)
    for i in range(5):
        a = i / 5.0 * 2 * math.pi - math.pi / 2
        ctx.save(); ctx.rotate(a)
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.curve_to(r * 0.44, -r * 0.30, r * 0.40, -r * 1.02, 0, -r * 1.06)
        ctx.curve_to(-r * 0.40, -r * 1.02, -r * 0.44, -r * 0.30, 0, 0)
        ctx.close_path()
        ctx.set_source_rgba(*LILAC, alpha); ctx.fill_preserve()
        ctx.set_line_width(r * 0.10); ctx.set_source_rgba(*mix(LILAC_D, INK, 0.35), alpha); ctx.stroke()
        ctx.restore()
    ctx.new_path(); ctx.arc(0, 0, r * 0.26, 0, 2 * math.pi)
    ctx.set_source_rgba(*GOLD, alpha); ctx.fill()
    ctx.restore()


def _hair_front(ctx, x, y, hb, t):
    """齐刘海 + 两侧鬓发"""
    sway = math.sin(t * 2.0) * hb * 0.016
    # 侧发（窄，露出脸颊）
    for sx in (-1, 1):
        pts = [(x + sx * hb * 0.92, y - hb * 0.50),
               (x + sx * hb * 1.08, y + hb * 0.06),
               (x + sx * hb * 1.02 + sway * sx, y + hb * 0.92),
               (x + sx * hb * 0.86 + sway * sx, y + hb * 0.86),
               (x + sx * hb * 0.84, y + hb * 0.12),
               (x + sx * hb * 0.76, y - hb * 0.44)]
        fill_stroke(ctx, pts, HAIR, INK, hb * 0.056, seed=230 + sx, amp=0.7)
        ctx.new_path()
        ctx.move_to(x + sx * hb * 0.96, y + hb * 0.08)
        ctx.curve_to(x + sx * hb * 1.00, y + hb * 0.40, x + sx * hb * 0.98, y + hb * 0.66,
                     x + sx * hb * 0.92, y + hb * 0.84)
        ctx.set_line_width(hb * 0.026); ctx.set_source_rgba(*HAIR_HL, 0.42)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # 刘海：一片式，下缘几缕尖
    def bangs():
        ctx.new_path()
        ctx.move_to(x - hb * 0.98, y - hb * 0.52)
        ctx.curve_to(x - hb * 1.10, y - hb * 1.14, x - hb * 0.30, y - hb * 1.38, x, y - hb * 1.40)
        ctx.curve_to(x + hb * 0.30, y - hb * 1.38, x + hb * 1.10, y - hb * 1.14, x + hb * 0.98, y - hb * 0.52)
        # 右侧发尾
        ctx.curve_to(x + hb * 0.94, y - hb * 0.36, x + hb * 0.86, y - hb * 0.44, x + hb * 0.78, y - hb * 0.62)
        ctx.curve_to(x + hb * 0.68, y - hb * 0.36, x + hb * 0.52, y - hb * 0.44, x + hb * 0.44, y - hb * 0.66)
        ctx.curve_to(x + hb * 0.34, y - hb * 0.42, x + hb * 0.16, y - hb * 0.46, x + hb * 0.04, y - hb * 0.68)
        ctx.curve_to(x - hb * 0.08, y - hb * 0.44, x - hb * 0.24, y - hb * 0.40, x - hb * 0.34, y - hb * 0.64)
        ctx.curve_to(x - hb * 0.46, y - hb * 0.38, x - hb * 0.62, y - hb * 0.40, x - hb * 0.72, y - hb * 0.60)
        ctx.curve_to(x - hb * 0.82, y - hb * 0.40, x - hb * 0.92, y - hb * 0.40, x - hb * 0.98, y - hb * 0.52)
        ctx.close_path()
    bangs(); ctx.set_source_rgb(*HAIR); ctx.fill()
    ctx.save(); bangs(); ctx.clip()
    ctx.set_source_rgba(*HAIR_HL, 0.42)
    ctx.new_path()
    ctx.move_to(x - hb * 0.74, y - hb * 0.86)
    ctx.curve_to(x - hb * 0.24, y - hb * 1.16, x + hb * 0.30, y - hb * 1.14, x + hb * 0.76, y - hb * 0.80)
    ctx.set_line_width(hb * 0.085); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.set_source_rgba(*HAIR_HL, 0.20)
    ctx.new_path()
    ctx.move_to(x - hb * 0.40, y - hb * 1.04)
    ctx.curve_to(x - hb * 0.10, y - hb * 1.18, x + hb * 0.20, y - hb * 1.16, x + hb * 0.44, y - hb * 1.00)
    ctx.set_line_width(hb * 0.040); ctx.stroke()
    ctx.restore()
    bangs()
    ctx.set_line_width(hb * 0.062); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(*INK); ctx.stroke()
    # 额前碎发（细）
    for k, sx in enumerate((-1, 1)):
        ctx.new_path()
        ctx.move_to(x + sx * hb * 0.10, y - hb * 1.28)
        ctx.curve_to(x + sx * hb * 0.20, y - hb * 1.04, x + sx * hb * 0.26, y - hb * 0.72,
                     x + sx * hb * 0.30, y - hb * 0.50)
        ctx.set_line_width(hb * 0.018); ctx.set_source_rgba(*HAIR_SH, 0.85); ctx.stroke()


def _pendant(ctx, x, y, hb, t):
    """额前金坠 —— 原十字纹章的形制：竖杆 + 横臂 + 中心宝石，仅重绘"""
    sw = math.sin(t * 1.3) * hb * 0.008
    ctx.save(); ctx.translate(x, y + sw)
    U = hb * 0.042                       # 杆宽的一半
    Lv, Aw = hb * 0.185, hb * 0.070      # 竖长 / 横臂长
    ctx.new_path()
    ctx.move_to(-U, -Lv * 0.62); ctx.line_to(U, -Lv * 0.62)
    ctx.line_to(U, Lv * 0.38); ctx.line_to(-U, Lv * 0.38)
    ctx.close_path(); ctx.set_source_rgb(*GOLD); ctx.fill_preserve()
    ctx.set_line_width(hb * 0.014); ctx.set_source_rgb(*GOLD_D); ctx.stroke()
    ctx.new_path()
    ctx.move_to(-Aw, -Lv * 0.30); ctx.line_to(Aw, -Lv * 0.30)
    ctx.line_to(Aw, -Lv * 0.16); ctx.line_to(-Aw, -Lv * 0.16)
    ctx.close_path(); ctx.set_source_rgb(*GOLD); ctx.fill_preserve()
    ctx.set_line_width(hb * 0.013); ctx.set_source_rgb(*GOLD_D); ctx.stroke()
    # 中心宝石
    r = hb * 0.032
    ctx.new_path()
    ctx.move_to(0, -r); ctx.line_to(r * 0.74, 0); ctx.line_to(0, r); ctx.line_to(-r * 0.74, 0)
    ctx.close_path(); ctx.set_source_rgb(*mix(LILAC, WHITE, 0.18)); ctx.fill_preserve()
    ctx.set_line_width(hb * 0.010); ctx.set_source_rgb(*INK); ctx.stroke()
    ctx.new_path()
    ctx.move_to(0, -r * 0.66); ctx.line_to(r * 0.30, 0); ctx.line_to(0, r * 0.30); ctx.line_to(-r * 0.30, 0)
    ctx.close_path(); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.fill()
    # 垂珠
    for i, (dy, rr) in enumerate(((0.46, 0.026), (0.58, 0.020))):
        ctx.new_path(); ctx.arc(0, hb * dy + Lv * 0.10, hb * rr, 0, 2 * math.pi)
        ctx.set_source_rgb(*GOLD); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.009); ctx.set_source_rgb(*GOLD_D); ctx.stroke()
    ctx.restore()


def _tassel_ear(ctx, x, y, hb, t, sx):
    """长耳坠：金环 + 流苏串珠"""
    sw = math.sin(t * 1.9 + sx) * hb * 0.012
    ctx.new_path(); ctx.arc(x, y, hb * 0.045, 0, 2 * math.pi)
    ctx.set_line_width(hb * 0.018); ctx.set_source_rgb(*GOLD); ctx.stroke()
    ctx.new_path()
    ctx.move_to(x, y + hb * 0.04)
    ctx.line_to(x + sw, y + hb * 0.50)
    ctx.set_line_width(hb * 0.014); ctx.set_source_rgba(*GOLD_D, 0.95); ctx.stroke()
    for i in range(3):
        cy = y + hb * (0.16 + i * 0.11)
        ctx.new_path(); ctx.arc(x + sw * (i + 1) / 3.0, cy, hb * 0.026, 0, 2 * math.pi)
        ctx.set_source_rgb(*(GOLD if i % 2 == 0 else LILAC)); ctx.fill()
    for i in range(3):
        ctx.new_path()
        ctx.move_to(x + sw + hb * (-0.035 + i * 0.035), y + hb * 0.50)
        ctx.line_to(x + sw + hb * (-0.055 + i * 0.045), y + hb * 0.78)
        ctx.set_line_width(hb * 0.014); ctx.set_source_rgba(*LILAC_D, 0.95)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
# ================= 身体 =================
# 相对头心 y 的倍数（hb 单位）
Y_NECK  = 1.10
Y_SHLD  = 1.26
Y_CHEST = 1.52
Y_WAIST = 1.78
Y_HIP   = 1.94
Y_HEM   = 2.56
Y_KNEE  = 2.82
Y_ANKLE = 3.02
Y_SOLE  = 3.16


def _limb(ctx, p0, p1, w0, w1, bend=0.0):
    """从 p0 到 p1 的锥形布料，w0/w1 为两端半宽"""
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    def Q(u, v):
        b = math.sin(u / max(L, 1e-6) * math.pi) * bend
        return (p0[0] + ux * u + vx * (v + b), p0[1] + uy * u + vy * (v + b))
    ctx.new_path()
    ctx.move_to(*Q(0, -w0))
    ctx.curve_to(*Q(L * 0.34, -w0 * 1.06), *Q(L * 0.70, -w1 * 0.94), *Q(L, -w1))
    ctx.curve_to(*Q(L * 1.05, -w1 * 0.55), *Q(L * 1.05, w1 * 0.55), *Q(L, w1))
    ctx.curve_to(*Q(L * 0.70, w1 * 0.94), *Q(L * 0.34, w0 * 1.06), *Q(0, w0))
    ctx.curve_to(*Q(-w0 * 0.18, w0 * 0.60), *Q(-w0 * 0.18, -w0 * 0.60), *Q(0, -w0))
    ctx.close_path()
    return (ux, uy, vx, vy)


def _hair_ribbon(ctx, x, y, hb, t, sway=0.0):
    """脑后垂下的两束长发"""
    for sx in (-1, 1):
        ph = t * 1.8 + (1.1 if sx > 0 else 0)
        sw = math.sin(ph) * hb * 0.05 + sway * sx * 0.5
        pts = [(x + sx * hb * 0.86, y + hb * 0.62),
               (x + sx * (hb * 1.20 + sw), y + hb * 1.20),
               (x + sx * (hb * 1.34 + sw * 1.4), y + hb * 1.86),
               (x + sx * (hb * 1.16 + sw * 1.8), y + hb * 2.28),
               (x + sx * (hb * 0.92 + sw * 1.4), y + hb * 2.02),
               (x + sx * (hb * 0.80 + sw * 0.7), y + hb * 1.24)]
        fill_stroke(ctx, pts, HAIR, INK, hb * 0.062, seed=270 + sx, amp=0.9)
        ctx.save()
        ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.5, seed=270 + sx); ctx.clip()
        ctx.set_source_rgba(*HAIR_HL, 0.35)
        ctx.new_path()
        ctx.move_to(x + sx * hb * 0.92, y + hb * 0.80)
        ctx.curve_to(x + sx * hb * 1.10, y + hb * 1.40, x + sx * hb * 1.16, y + hb * 1.90,
                     x + sx * hb * 1.06, y + hb * 2.14)
        ctx.set_line_width(hb * 0.040); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        ctx.restore()


def draw_laoba(ctx, x, y, s=1.0, t=0.0, expr="normal", look=(0, 0), open_k=0.0,
               blink=0.0, pose=None, wind=0.0, bob=0.0, body=True, hat=True,
               fs=0.92, head_k=0.90):
    """老芭 v4：Q 版古风。x,y = 头部中心；head_k 保留兼容，头部半径 = R*s*head_k"""
    ctx.save()
    ctx.translate(0, bob)
    hb = R * s * head_k

    def Y(u):
        return y + hb * u

    if pose is None:
        pose = ((0.16, 0.06), (0.16, 0.06))

    if body:
        _hair_back(ctx, x, y, hb, t, wind)
        _hair_ribbon(ctx, x, y, hb, t, wind * 2.0)

        # ---- 脖子 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.20, Y(0.78))
        ctx.line_to(x + hb * 0.20, Y(0.78))
        ctx.line_to(x + hb * 0.22, Y(1.28))
        ctx.line_to(x - hb * 0.22, Y(1.28))
        ctx.close_path()
        ctx.set_source_rgb(*SKIN); ctx.fill()
        ctx.set_source_rgba(*SKIN_SH, 0.55)
        ctx.new_path(); ellipse_path(ctx, x, Y(0.92), hb * 0.21, hb * 0.11, 0, 0, 2 * math.pi); ctx.fill()

        # ---- 腿 ----
        for sx in (-1, 1):
            lx = x + sx * hb * 0.30
            ctx.new_path()
            ctx.move_to(lx - hb * 0.15, Y(Y_HIP - 0.06))
            ctx.curve_to(lx - hb * 0.17, Y(Y_KNEE - 0.30), lx - hb * 0.10, Y(Y_KNEE),
                         lx - hb * 0.075, Y(Y_KNEE))
            ctx.curve_to(lx - hb * 0.085, Y(Y_KNEE + 0.16), lx - hb * 0.080, Y(Y_ANKLE - 0.12),
                         lx - hb * 0.072, Y(Y_ANKLE))
            ctx.line_to(lx + hb * 0.078, Y(Y_ANKLE))
            ctx.curve_to(lx + hb * 0.086, Y(Y_ANKLE - 0.12), lx + hb * 0.092, Y(Y_KNEE + 0.16),
                         lx + hb * 0.082, Y(Y_KNEE))
            ctx.curve_to(lx + hb * 0.105, Y(Y_KNEE), lx + hb * 0.175, Y(Y_KNEE - 0.30),
                         lx + hb * 0.155, Y(Y_HIP - 0.06))
            ctx.close_path()
            ctx.set_source_rgb(*SKIN); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.036); ctx.set_source_rgb(*INK); ctx.stroke()
            ctx.new_path()
            ctx.move_to(lx - sx * hb * 0.052, Y(Y_KNEE + 0.04))
            ctx.curve_to(lx - sx * hb * 0.060, Y(Y_KNEE + 0.30), lx - sx * hb * 0.056, Y(Y_ANKLE - 0.20),
                         lx - sx * hb * 0.050, Y(Y_ANKLE - 0.04))
            ctx.set_line_width(hb * 0.026); ctx.set_source_rgba(*SKIN_SH, 0.9)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

        # ---- 鞋：青绿绣鞋 ----
        for sx in (-1, 1):
            bx = x + sx * hb * 0.30
            def shoe(u, v):
                return (bx + sx * u, v)
            ctx.new_path()
            ctx.move_to(*shoe(-hb * 0.115, Y(Y_ANKLE - 0.10)))
            ctx.line_to(*shoe(hb * 0.115, Y(Y_ANKLE - 0.10)))
            ctx.curve_to(*shoe(hb * 0.150, Y(Y_ANKLE + 0.04)),
                         *shoe(hb * 0.185, Y(Y_SOLE - 0.10)),
                         *shoe(hb * 0.150, Y(Y_SOLE)))
            ctx.curve_to(*shoe(hb * 0.06, Y(Y_SOLE + 0.035)),
                         *shoe(-hb * 0.10, Y(Y_SOLE + 0.035)),
                         *shoe(-hb * 0.150, Y(Y_SOLE - 0.02)))
            ctx.curve_to(*shoe(-hb * 0.175, Y(Y_ANKLE + 0.06)),
                         *shoe(-hb * 0.145, Y(Y_ANKLE - 0.10)),
                         *shoe(-hb * 0.115, Y(Y_ANKLE - 0.10)))
            ctx.close_path()
            ctx.set_source_rgb(*SHOE); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.040); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            # 鞋口 + 珠花
            ctx.new_path()
            ctx.move_to(*shoe(-hb * 0.118, Y(Y_ANKLE - 0.075)))
            ctx.line_to(*shoe(hb * 0.118, Y(Y_ANKLE - 0.075)))
            ctx.set_line_width(hb * 0.020); ctx.set_source_rgba(*mix(SHOE, WHITE, 0.55), 0.95); ctx.stroke()
            _flower(ctx, bx + sx * hb * 0.02, Y(Y_ANKLE + 0.20), hb * 0.070, t)

        # ---- 内层深蓝长裙 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.62, Y(Y_WAIST - 0.10))
        ctx.curve_to(x - hb * 0.72, Y(Y_WAIST + 0.40), x - hb * 0.86, Y(Y_KNEE - 0.20),
                     x - hb * 0.84, Y(Y_ANKLE - 0.10))
        ctx.line_to(x + hb * 0.84, Y(Y_ANKLE - 0.10))
        ctx.curve_to(x + hb * 0.86, Y(Y_KNEE - 0.20), x + hb * 0.72, Y(Y_WAIST + 0.40),
                     x + hb * 0.62, Y(Y_WAIST - 0.10))
        ctx.close_path()
        ctx.set_source_rgb(*INNER); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.048); ctx.set_source_rgb(*INK); ctx.stroke()
        # 裙褶
        for i in range(5):
            u = (i - 2) / 2.0
            ctx.new_path()
            ctx.move_to(x + u * hb * 0.36, Y(Y_WAIST + 0.02))
            ctx.curve_to(x + u * hb * 0.56, Y(Y_KNEE - 0.30), x + u * hb * 0.74, Y(Y_ANKLE - 0.40),
                         x + u * hb * 0.80, Y(Y_ANKLE - 0.14))
            ctx.set_line_width(hb * 0.022); ctx.set_source_rgba(*INNER_SH, 0.85); ctx.stroke()
        ctx.new_path()
        ctx.move_to(x - hb * 0.80, Y(Y_ANKLE - 0.22))
        ctx.curve_to(x - hb * 0.30, Y(Y_ANKLE - 0.12), x + hb * 0.30, Y(Y_ANKLE - 0.12),
                     x + hb * 0.80, Y(Y_ANKLE - 0.22))
        ctx.set_line_width(hb * 0.028); ctx.set_source_rgba(*INNER_HL, 0.65); ctx.stroke()

        # ---- 外袍：竹青，开襟，长及小腿 ----
        def robe_outline(g=0.0):
            ctx.new_path()
            ctx.move_to(x - hb * 0.44 - g, Y(Y_SHLD - 0.06))
            ctx.curve_to(x - hb * 0.70 - g, Y(Y_SHLD + 0.10), x - hb * 0.70 - g, Y(Y_CHEST + 0.10),
                         x - hb * 0.60 - g, Y(Y_WAIST))
            ctx.curve_to(x - hb * 0.74 - g, Y(Y_WAIST + 0.60), x - hb * 0.90 - g, Y(Y_HEM - 0.30),
                         x - hb * 0.98 - g, Y(Y_HEM))
            ctx.curve_to(x - hb * 0.60 - g, Y(Y_HEM + 0.10), x - hb * 0.20 - g, Y(Y_HEM + 0.12),
                         x - hb * 0.02 - g, Y(Y_HEM + 0.10))
            ctx.line_to(x + hb * 0.02 + g, Y(Y_HEM + 0.10))
            ctx.curve_to(x + hb * 0.20 + g, Y(Y_HEM + 0.12), x + hb * 0.60 + g, Y(Y_HEM + 0.10),
                         x + hb * 0.98 + g, Y(Y_HEM))
            ctx.curve_to(x + hb * 0.90 + g, Y(Y_HEM - 0.30), x + hb * 0.74 + g, Y(Y_WAIST + 0.60),
                         x + hb * 0.60 + g, Y(Y_WAIST))
            ctx.curve_to(x + hb * 0.70 + g, Y(Y_CHEST + 0.10), x + hb * 0.70 + g, Y(Y_SHLD + 0.10),
                         x + hb * 0.44 + g, Y(Y_SHLD - 0.06))
            ctx.close_path()
        robe_outline(0)
        ctx.set_source_rgb(*ROBE); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.050); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
        # 袍身明暗
        ctx.save(); robe_outline(0); ctx.clip()
        ctx.set_source_rgba(*ROBE_SH, 0.55)
        ctx.new_path()
        ctx.move_to(x + hb * 0.36, Y(Y_CHEST))
        ctx.curve_to(x + hb * 0.62, Y(Y_WAIST + 0.30), x + hb * 0.80, Y(Y_HEM - 0.40),
                     x + hb * 0.86, Y(Y_HEM + 0.16))
        ctx.line_to(x + hb * 1.10, Y(Y_HEM + 0.16)); ctx.line_to(x + hb * 1.10, Y(Y_CHEST))
        ctx.close_path(); ctx.fill()
        ctx.set_source_rgba(*ROBE_HL, 0.45)
        ctx.new_path()
        ctx.move_to(x - hb * 0.52, Y(Y_CHEST))
        ctx.curve_to(x - hb * 0.44, Y(Y_WAIST + 0.40), x - hb * 0.40, Y(Y_HEM - 0.50),
                     x - hb * 0.36, Y(Y_HEM + 0.14))
        ctx.line_to(x - hb * 0.54, Y(Y_HEM + 0.14)); ctx.line_to(x - hb * 0.64, Y(Y_CHEST))
        ctx.close_path(); ctx.fill()
        # 下摆褶
        for i in range(7):
            u = (i - 3) / 3.0
            ctx.new_path()
            ctx.move_to(x + u * hb * 0.30, Y(Y_WAIST + 0.16))
            ctx.curve_to(x + u * hb * 0.66, Y(Y_WAIST + 0.72), x + u * hb * 0.90, Y(Y_HEM - 0.40),
                         x + u * hb * 0.94, Y(Y_HEM + 0.06))
            ctx.set_line_width(hb * 0.020); ctx.set_source_rgba(*ROBE_SH, 0.70); ctx.stroke()
        ctx.restore()

        # 开襟：露出内层深蓝 + 浅色袍缘
        ctx.new_path()
        ctx.move_to(x - hb * 0.30, Y(Y_SHLD - 0.02))
        ctx.curve_to(x - hb * 0.16, Y(Y_CHEST + 0.06), x - hb * 0.04, Y(Y_WAIST - 0.14),
                     x + hb * 0.02, Y(Y_WAIST + 0.10))
        ctx.line_to(x + hb * 0.30, Y(Y_WAIST + 0.02))
        ctx.curve_to(x + hb * 0.20, Y(Y_WAIST - 0.24), x + hb * 0.12, Y(Y_CHEST + 0.02),
                     x + hb * 0.10, Y(Y_SHLD - 0.02))
        ctx.close_path()
        ctx.set_source_rgb(*INNER); ctx.fill()
        for sx in (-1, 1):
            ctx.new_path()
            ctx.move_to(x + sx * hb * 0.30, Y(Y_SHLD - 0.02))
            ctx.curve_to(x + sx * hb * 0.16, Y(Y_CHEST + 0.06), x + sx * hb * 0.04, Y(Y_WAIST - 0.16),
                         x + sx * hb * 0.03, Y(Y_WAIST + 0.08))
            ctx.set_line_width(hb * 0.048); ctx.set_source_rgb(*ROBE_ED); ctx.stroke()
            ctx.new_path()
            ctx.move_to(x + sx * hb * 0.30, Y(Y_SHLD - 0.02))
            ctx.curve_to(x + sx * hb * 0.16, Y(Y_CHEST + 0.06), x + sx * hb * 0.04, Y(Y_WAIST - 0.16),
                         x + sx * hb * 0.03, Y(Y_WAIST + 0.08))
            ctx.set_line_width(hb * 0.018); ctx.set_source_rgba(*GOLD, 0.95); ctx.stroke()

        # 腰封：金链 + 玉坠
        ctx.new_path()
        ctx.move_to(x - hb * 0.58, Y(Y_WAIST + 0.02))
        ctx.curve_to(x - hb * 0.24, Y(Y_WAIST - 0.06), x + hb * 0.24, Y(Y_WAIST - 0.06),
                     x + hb * 0.58, Y(Y_WAIST + 0.02))
        ctx.set_line_width(hb * 0.060); ctx.set_source_rgb(*GOLD); ctx.stroke()
        ctx.new_path()
        ctx.move_to(x - hb * 0.58, Y(Y_WAIST + 0.02))
        ctx.curve_to(x - hb * 0.24, Y(Y_WAIST - 0.06), x + hb * 0.24, Y(Y_WAIST - 0.06),
                     x + hb * 0.58, Y(Y_WAIST + 0.02))
        ctx.set_line_width(hb * 0.022); ctx.set_source_rgba(*GOLD_D, 0.95); ctx.stroke()
        for i in range(5):
            u = (i - 2) / 2.0
            ctx.new_path(); ctx.arc(x + u * hb * 0.30, Y(Y_WAIST - 0.02), hb * 0.030, 0, 2 * math.pi)
            ctx.set_source_rgb(*GOLD_D); ctx.fill()
        # 垂下的玉珠链
        ctx.new_path()
        ctx.move_to(x - hb * 0.10, Y(Y_WAIST + 0.04))
        ctx.curve_to(x - hb * 0.16, Y(Y_WAIST + 0.30), x - hb * 0.10, Y(Y_WAIST + 0.52),
                     x - hb * 0.02, Y(Y_WAIST + 0.56))
        ctx.set_line_width(hb * 0.020); ctx.set_source_rgba(*GOLD_D, 0.9); ctx.stroke()
        for i, (u, r) in enumerate(((0.24, 0.028), (0.40, 0.026), (0.54, 0.032))):
            ctx.new_path(); ctx.arc(x - hb * (0.12 - i * 0.03), Y(Y_WAIST + u + 0.02), hb * r, 0, 2 * math.pi)
            ctx.set_source_rgb(*(LILAC if i % 2 else GOLD)); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.010); ctx.set_source_rgb(*INK); ctx.stroke()
        # 袍上散花
        for (fx, fy, fr) in ((-0.40, Y_HEM - 0.48, 0.085), (0.34, Y_HEM - 0.20, 0.070),
                             (0.46, Y_WAIST + 0.46, 0.062), (-0.26, Y_WAIST + 0.30, 0.050)):
            _flower(ctx, x + hb * fx, Y(fy), hb * fr, t + fx * 3.0, alpha=0.85)

        # ---- 手臂 + 大袖 ----
        for i, sx in enumerate((-1, 1)):
            a1, a2 = pose[i]
            shx, shy = x + sx * hb * 0.56, Y(Y_SHLD + 0.02)
            L1, L2 = hb * 0.74, hb * 0.66
            a1w = a1 + 0.10 + 0.30 * sw_arm(t, i)
            el = (shx + sx * math.sin(a1w) * L1, shy + math.cos(a1w) * L1)
            hd = (el[0] + sx * math.sin(a1w + a2) * L2, el[1] + math.cos(a1w + a2) * L2)
            geo1 = _limb(ctx, (shx, shy), el, hb * 0.215, hb * 0.185)
            ctx.set_source_rgb(*ROBE); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.046); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            # 前臂大袖：喇叭口
            geo2 = _limb(ctx, el, hd, hb * 0.185, hb * 0.400, bend=hb * 0.03)
            ctx.set_source_rgb(*ROBE); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.046); ctx.set_source_rgb(*INK); ctx.stroke()
            # 袖内阴影
            for (p0, p1, w0, w1) in (((shx, shy), el, 0.20, 0.17), (el, hd, 0.17, 0.34)):
                a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                ux, uy = math.cos(a), math.sin(a)
                ctx.new_path()
                ctx.move_to(p0[0] + (-uy) * hb * w0 * 0.55, p0[1] + ux * hb * w0 * 0.55)
                ctx.line_to(p1[0] + (-uy) * hb * w1 * 0.66, p1[1] + ux * hb * w1 * 0.66)
                ctx.set_line_width(hb * 0.040); ctx.set_source_rgba(*ROBE_SH, 0.80); ctx.stroke()
            # 袖口浅色镶边
            ux2, uy2, vx2, vy2 = geo2
            for (wide, col, lw) in ((hb * 0.395, ROBE_ED, 0.048), (hb * 0.395, GOLD, 0.016)):
                ctx.new_path()
                ctx.move_to(hd[0] + vx2 * wide, hd[1] + vy2 * wide)
                ctx.line_to(hd[0] - vx2 * wide, hd[1] - vy2 * wide)
                ctx.set_line_width(hb * lw); ctx.set_line_cap(cairo.LINE_CAP_BUTT)
                ctx.set_source_rgb(*col); ctx.stroke()
            # 手
            hx = hd[0] + ux2 * hb * 0.050
            hy = hd[1] + uy2 * hb * 0.050
            def H(u, v):
                return (hx + ux2 * u + vx2 * v, hy + uy2 * u + vy2 * v)
            ctx.new_path()
            ctx.move_to(*H(-hb * 0.010, -hb * 0.098))
            ctx.curve_to(*H(hb * 0.130, -hb * 0.140), *H(hb * 0.250, -hb * 0.078),
                         *H(hb * 0.246, hb * 0.012))
            ctx.curve_to(*H(hb * 0.238, hb * 0.092), *H(hb * 0.130, hb * 0.132),
                         *H(-hb * 0.010, hb * 0.094))
            ctx.close_path()
            ctx.set_source_rgb(*SKIN); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.036); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            ctx.new_path()
            ctx.move_to(*H(hb * 0.062, -hb * 0.078))
            ctx.curve_to(*H(hb * 0.090, -hb * 0.176), *H(hb * 0.182, -hb * 0.162),
                         *H(hb * 0.164, -hb * 0.078))
            ctx.set_line_width(hb * 0.046); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*SKIN); ctx.stroke()
            for k in range(3):
                ctx.new_path()
                ctx.move_to(*H(hb * 0.172, hb * (0.012 + k * 0.034)))
                ctx.line_to(*H(hb * 0.250, hb * (0.012 + k * 0.031)))
                ctx.set_line_width(hb * 0.012); ctx.set_source_rgba(*SKIN_SH, 0.95); ctx.stroke()

    # ---- 头 ----
    draw_face(ctx, x, y, s * head_k, t, expr, look, open_k, blink)
    _hair_front(ctx, x, y, hb, t)
    if hat:
        _pendant(ctx, x, y - hb * 0.36, hb, t)
    _bun(ctx, x, y, hb, t)
    # 两侧耳坠
    for sx in (-1, 1):
        _tassel_ear(ctx, x + sx * hb * 0.96, y + hb * 0.30, hb, t, sx)
    # 侧发上的大蝶
    for sx in (-1, 1):
        _butterfly(ctx, x + sx * hb * 1.02, y - hb * 0.34, hb * 0.42, t + sx * 0.7, flip=sx)
    ctx.restore()


def sw_arm(t, i):
    return math.sin(t * 2.0 + i * 1.4)


# ================= 小方 =================
# ================= 小方 v4（扁平的铅笔方块） =================
CUBE_FACE  = (0.992, 0.984, 0.962)
CUBE_BODY  = (0.944, 0.918, 0.872)
CUBE_EDGE  = (0.185, 0.185, 0.200)

# 六个面的贴纸色（按面循环取用）—— 彩铅的六支
_STK = [(0.822, 0.505, 0.462), (0.858, 0.742, 0.432), (0.552, 0.718, 0.622),
        (0.470, 0.612, 0.772), (0.688, 0.618, 0.792), (0.905, 0.878, 0.822)]

# 贴纸排布：左右对称，中间一格被脸挡住
_GRID = [[0, 3, 1],
         [2, 5, 4],
         [1, 3, 0]]


def _rounded_poly(ctx, pts, rad):
    """多边形顶点圆角化"""
    n = len(pts)
    ctx.new_path()
    for i in range(n):
        p0 = pts[i - 1]; p1 = pts[i]; p2 = pts[(i + 1) % n]
        v1 = (p0[0] - p1[0], p0[1] - p1[1])
        v2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1 = math.hypot(*v1) or 1; l2 = math.hypot(*v2) or 1
        r1 = min(rad, l1 * 0.45); r2 = min(rad, l2 * 0.45)
        a = (p1[0] + v1[0] / l1 * r1, p1[1] + v1[1] / l1 * r1)
        c = (p1[0] + v2[0] / l2 * r2, p1[1] + v2[1] / l2 * r2)
        if i == 0:
            ctx.move_to(*a)
        else:
            ctx.line_to(*a)
        ctx.curve_to(p1[0], p1[1], p1[0], p1[1], *c)
    ctx.close_path()


def _quad(ctx, p00, p10, p11, p01, rad):
    _rounded_poly(ctx, [p00, p10, p11, p01], rad)


def draw_cube(ctx, cx, cy, r, t=0.0, rot=0.0, expr="normal", look=(0, 0),
              arms=None, legs=True, squash=1.0, tilt=0.0, outline=1.0, alpha=1.0,
              face=True, seed=9, glow=None):
    """小方 v4：扁平的铅笔方块

    只画一个正面：正方形 + 3×3 贴纸 + 奶油脸盘。没有顶面、没有侧面、
    没有透视和渐变——和人物同一支铅笔，排线 + 石墨轮廓。
    r = 正面半宽（方块总宽 2r）
    """
    if alpha <= 0.001 or r <= 0.5:
        return
    k = r
    sq = squash
    cr, sr = math.cos(rot), math.sin(rot)

    def T(p):
        x, y = p
        return (cx + x * cr - (y * sq) * sr, cy + x * sr + (y * sq) * cr)

    HH = 0.94 * k                       # 半高
    F = [(-k, -HH), (k, -HH), (k, HH), (-k, HH)]
    edge_lw = 0.050 * k * outline

    # ---- 影子 ----
    ctx.new_path()
    ellipse_path(ctx, cx, cy + HH * sq + 0.22 * k, 0.80 * k, 0.145 * k, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*LILAC_D, 0.18 * alpha); ctx.fill()

    # ---- 腿（在方块后面）----
    if legs:
        for sx in (-1, 1):
            hip = T((sx * 0.34 * k, HH * 0.94))
            ft = (hip[0] + sx * 0.05 * k, hip[1] + 0.28 * k)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.new_path(); ctx.move_to(*hip); ctx.line_to(*ft)
            ctx.set_line_width(0.150 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
            ctx.new_path(); ctx.move_to(*hip); ctx.line_to(*ft)
            ctx.set_line_width(0.080 * k); ctx.set_source_rgba(*WHITE, alpha); ctx.stroke()
            ctx.new_path()
            ellipse_path(ctx, ft[0] + sx * 0.04 * k, ft[1] + 0.01 * k,
                         0.112 * k, 0.070 * k, 0, 0, 2 * math.pi)
            ctx.set_source_rgba(*CORAL, alpha); ctx.fill_preserve()
            ctx.set_line_width(0.036 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()

    # ---- 手臂（在方块后面）----
    if arms:
        for sx, ang, ln in ((-1, arms[0], arms[1]), (1, arms[2], arms[3])):
            ax, ay = T((sx * 0.98 * k, 0.02 * k * sq))
            hx = ax + sx * math.sin(ang) * ln * k
            hy = ay + math.cos(ang) * ln * k
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.new_path(); ctx.move_to(ax, ay); ctx.line_to(hx, hy)
            ctx.set_line_width(0.115 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
            ctx.new_path(); ctx.move_to(ax, ay); ctx.line_to(hx, hy)
            ctx.set_line_width(0.062 * k); ctx.set_source_rgba(*CUBE_FACE, alpha); ctx.stroke()
            ctx.new_path(); ctx.arc(hx, hy, 0.080 * k, 0, 2 * math.pi)
            ctx.set_source_rgba(*CUBE_FACE, alpha); ctx.fill_preserve()
            ctx.set_line_width(0.032 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
            ctx.new_path(); ctx.arc(hx - 0.028 * k, hy - 0.030 * k, 0.021 * k, 0, 2 * math.pi)
            ctx.set_source_rgba(1, 1, 1, 0.85 * alpha); ctx.fill()

    # ---- 方块本体：一个正面 ----
    body = [T(p) for p in F]
    _rounded_poly(ctx, body, 0.16 * k)
    ctx.set_source_rgba(*CUBE_BODY, alpha); ctx.fill()

    ctx.save()
    _rounded_poly(ctx, body, 0.16 * k); ctx.clip()
    _hatch_fill(ctx, body, 0.6, seed + 40, True, a=0.055 * alpha, gap=8.0)
    # 底边一带压深一点，代替立体阴影
    ctx.set_source_rgba(*mix(CUBE_EDGE, CUBE_BODY, 0.80), 0.16 * alpha)
    ctx.new_path()
    ctx.move_to(*T((-k, HH * 0.72)))
    ctx.line_to(*T((k, HH * 0.72)))
    ctx.line_to(*T((k, HH)))
    ctx.line_to(*T((-k, HH)))
    ctx.close_path(); ctx.fill()
    ctx.restore()

    _rounded_poly(ctx, body, 0.16 * k)
    ctx.set_line_width(edge_lw); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
    _rounded_poly(ctx, [(x + 0.012 * k, y + 0.014 * k) for x, y in body], 0.16 * k)
    ctx.set_line_width(edge_lw * 0.42)
    ctx.set_source_rgba(*CUBE_EDGE, 0.32 * alpha); ctx.stroke()

    # ---- 3×3 贴纸 ----
    cell, gap = 0.53 * k, 0.055 * k
    step = cell + gap
    gx0, gy0 = -1.5 * cell - gap, -1.5 * cell - gap
    for iu in range(3):
        for iv in range(3):
            x0 = gx0 + iu * step
            y0 = gy0 + iv * step
            pts = [T((x0, y0)), T((x0 + cell, y0)),
                   T((x0 + cell, y0 + cell)), T((x0, y0 + cell))]
            _rounded_poly(ctx, pts, 0.055 * k)
            col = _STK[_GRID[iv][iu] % 6]
            ctx.set_source_rgba(*col, 0.94 * alpha); ctx.fill()
            _hatch_fill(ctx, pts, 0.5, seed + 60 + iu * 3 + iv, True,
                        a=0.075 * alpha, gap=6.0)
            _rounded_poly(ctx, pts, 0.055 * k)
            ctx.set_line_width(0.018 * k)
            ctx.set_source_rgba(*CUBE_EDGE, 0.62 * alpha); ctx.stroke()

    # ---- 脸盘 ----
    fx, fy = T((0.0, 0.02 * k * sq))
    ctx.new_path()
    ellipse_path(ctx, fx, fy, 0.78 * k, 0.63 * k * sq, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*CUBE_FACE, 0.98 * alpha); ctx.fill_preserve()
    ctx.set_source_rgba(*CUBE_EDGE, 0.85 * alpha)
    ctx.set_line_width(0.032 * k); ctx.stroke()

    # ---- 五官 ----
    if face:
        lx, ly = look[0] * 0.040 * k, look[1] * 0.036 * k
        # 腮红：一小丛斜线
        for sx in (-1, 1):
            ctx.save()
            ctx.set_line_width(0.016 * k); ctx.set_source_rgba(*BLUSH, 0.80 * alpha)
            for j in range(3):
                for i in range(4):
                    px = fx + sx * (0.44 + i * 0.030) * k
                    py = fy + (0.16 + j * 0.030) * k
                    ctx.move_to(px - 0.014 * k, py + 0.014 * k)
                    ctx.line_to(px + 0.014 * k, py - 0.014 * k)
            ctx.stroke()
            ctx.restore()
        for sx in (-1, 1):
            ex = fx + sx * 0.285 * k + lx
            ey = fy - 0.03 * k + ly
            if expr == "happy":
                ctx.new_path()
                ctx.move_to(ex - 0.125 * k, ey + 0.02 * k)
                ctx.curve_to(ex - 0.065 * k, ey - 0.11 * k, ex + 0.065 * k, ey - 0.11 * k,
                             ex + 0.125 * k, ey + 0.02 * k)
                ctx.set_line_width(0.055 * k); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
            elif expr == "shock":
                ctx.new_path(); ellipse_path(ctx, ex, ey, 0.135 * k, 0.158 * k, 0, 0, 2 * math.pi)
                ctx.set_source_rgba(*WHITE, alpha); ctx.fill_preserve()
                ctx.set_line_width(0.038 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
                ctx.new_path(); ctx.arc(ex + lx * 1.4, ey + ly, 0.058 * k, 0, 2 * math.pi)
                ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.fill()
            else:
                ctx.new_path()
                ellipse_path(ctx, ex, ey, 0.125 * k, 0.152 * k, 0, 0, 2 * math.pi)
                ctx.set_source_rgba(*WHITE, alpha); ctx.fill()
                ctx.save()
                ctx.new_path(); ellipse_path(ctx, ex, ey, 0.125 * k, 0.152 * k, 0, 0, 2 * math.pi)
                ctx.clip()
                for i in range(6):
                    u = i / 5.0
                    ctx.set_source_rgba(*mix((0.20, 0.22, 0.34), (0.46, 0.56, 0.78), u), alpha)
                    ellipse_path(ctx, ex + lx * 0.6, ey - 0.14 * k + 0.28 * k * u,
                                 0.108 * k, 0.058 * k, 0, 0, 2 * math.pi); ctx.fill()
                ctx.new_path()
                ellipse_path(ctx, ex + lx, ey + 0.04 * k + ly, 0.054 * k, 0.076 * k, 0, 0, 2 * math.pi)
                ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.fill()
                ctx.new_path(); ctx.arc(ex - 0.040 * k, ey - 0.058 * k, 0.045 * k, 0, 2 * math.pi)
                ctx.set_source_rgba(1, 1, 1, 0.96 * alpha); ctx.fill()
                ctx.new_path(); ctx.arc(ex + 0.042 * k, ey + 0.052 * k, 0.020 * k, 0, 2 * math.pi)
                ctx.set_source_rgba(1, 1, 1, 0.72 * alpha); ctx.fill()
                ctx.restore()
                ctx.new_path()
                ellipse_path(ctx, ex, ey, 0.125 * k, 0.152 * k, 0, 0, 2 * math.pi)
                ctx.set_line_width(0.028 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
        # 嘴
        if expr == "happy":
            ctx.new_path()
            ctx.move_to(fx - 0.12 * k, fy + 0.22 * k)
            ctx.curve_to(fx - 0.05 * k, fy + 0.35 * k, fx + 0.05 * k, fy + 0.35 * k,
                         fx + 0.12 * k, fy + 0.22 * k)
            ctx.close_path(); ctx.set_source_rgba(*MOUTH, alpha); ctx.fill_preserve()
            ctx.set_line_width(0.030 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
        elif expr == "shock":
            ctx.new_path(); ellipse_path(ctx, fx, fy + 0.28 * k, 0.066 * k, 0.086 * k, 0, 0, 2 * math.pi)
            ctx.set_source_rgba(*MOUTH, alpha); ctx.fill_preserve()
            ctx.set_line_width(0.028 * k); ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
        elif expr == "sad":
            ctx.new_path()
            ctx.move_to(fx - 0.095 * k, fy + 0.30 * k)
            ctx.curve_to(fx - 0.03 * k, fy + 0.20 * k, fx + 0.03 * k, fy + 0.20 * k,
                         fx + 0.095 * k, fy + 0.30 * k)
            ctx.set_line_width(0.036 * k); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
        else:
            ctx.new_path()
            ctx.move_to(fx - 0.082 * k, fy + 0.24 * k)
            ctx.curve_to(fx - 0.026 * k, fy + 0.31 * k, fx + 0.026 * k, fy + 0.31 * k,
                         fx + 0.082 * k, fy + 0.24 * k)
            ctx.set_line_width(0.036 * k); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(*CUBE_EDGE, alpha); ctx.stroke()
