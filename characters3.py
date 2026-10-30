# -*- coding: utf-8 -*-
"""老芭 v6：素描版 —— 芭芭拉的头部特征

造型要点（头部按参考图重做，服装沿用 v5）：
    灰金棕短发，高位扎短双马尾（蓬、带卷，只到下颌），发根白色荷叶边缎带
    头顶右侧斜戴白色小护士帽，蓝帽带 + 侧面小蓝结
    中分钝刘海 + 两缕垂到下颌的鬓发
    细长上挑的蓝杏眼，重上睑线，下睑只留外侧一段
    白色水手领 + 深蓝领巾，白色上衣，胸口黄色大蝴蝶结
    蓝色短裙 + 白色荷叶边，蓝色袖口（喇叭袖）
    白色过膝袜 / 蓝色系带短靴，小腿挂一只小黄鸭
    额头保持干净：不戴任何坠饰；眼神圆一点、软一点

几何契约不变（stage.py 依赖）：
    hb = R*s*head_k
    发冠顶 y-1.50hb / 下巴 y+0.95hb / 鞋底 y+3.16hb / 全身 4.64hb
"""
import math
from art import *
from art import _hatch_fill
from characters import R

TOTAL_H = 4.64
Y_SOLE = 3.16

# ---------------- 彩铅调色 ----------------
SKIN     = (0.985, 0.930, 0.906)
SKIN_SH  = (0.905, 0.795, 0.780)
HAIR     = (0.828, 0.790, 0.742)      # 芭芭拉的灰金棕
HAIR_SH  = (0.664, 0.626, 0.582)
HAIR_HL  = (0.952, 0.930, 0.898)
WHITE_D  = (0.905, 0.905, 0.900)
SAILOR   = (0.420, 0.540, 0.705)      # 水手蓝（压一点饱和）
SAILOR_SH= (0.295, 0.390, 0.545)
SAILOR_HL= (0.560, 0.665, 0.810)
YELLOW   = (0.905, 0.752, 0.380)      # 黄蝴蝶结 / 小鸭
YELLOW_D = (0.748, 0.585, 0.262)
BLUSH    = (0.930, 0.720, 0.720)
MOUTH    = (0.520, 0.320, 0.340)
EYE      = (0.300, 0.442, 0.718)      # 参考图是蓝眼
EYE_D    = (0.120, 0.196, 0.386)
GOLD     = (0.870, 0.720, 0.420)
GOLD_D   = (0.690, 0.540, 0.270)


# ================= 眼 / 眉 / 嘴 =================
def _eye(ctx, ex, ey, w, h, look, expr="normal", blink=0.0, flip=1.0):
    """圆一点的蓝眼睛：上睑一条厚线，外眼角只轻轻抬起一点

    不画额外的睫毛——那两根短线在动起来时最扎眼。
    上睑本身就是一个两头细、中间粗的柳叶形，收在外眼角就够了。
    flip = -1 时整只眼左右镜像，外眼角永远朝外。
    """
    def X(u):
        return ex + u * flip

    if expr == "happy" or blink > 0.82:
        ctx.new_path()
        ctx.move_to(X(-w * 1.00), ey + h * 0.24)
        ctx.curve_to(X(-w * 0.34), ey - h * 0.74, X(w * 0.34), ey - h * 0.74,
                     X(w * 1.00), ey + h * 0.18)
        ctx.set_line_width(w * 0.30); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
        return

    def almond(k=1.0):
        ctx.new_path()
        ctx.move_to(X(-w * 1.00), ey + h * 0.10)          # 内眼角
        ctx.curve_to(X(-w * 0.62), ey - h * 0.80 * k, X(w * 0.36), ey - h * 0.92 * k,
                     X(w * 1.02), ey - h * 0.10)          # 上睑：外眼角只抬一点点
        ctx.curve_to(X(w * 0.58), ey + h * 0.82 * k, X(-w * 0.38), ey + h * 0.84 * k,
                     X(-w * 1.00), ey + h * 0.10)         # 下睑
        ctx.close_path()

    hh = h * max(0.14, 1.0 - blink * 0.94)
    almond(1.0)
    ctx.set_source_rgba(*PAPER, 0.95); ctx.fill()
    ctx.save()
    almond(1.0); ctx.clip()
    ix, iy = X(look[0] * w * 0.16), ey + look[1] * hh * 0.16
    # 虹膜：上深下浅，竖长椭圆，贴住上下睑
    g = cairo.LinearGradient(ix, iy - hh * 0.82, ix, iy + hh * 0.86)
    g.add_color_stop_rgba(0.0, *EYE_D, 0.97)
    g.add_color_stop_rgba(0.46, *EYE, 0.95)
    g.add_color_stop_rgba(1.0, *mix(EYE, WHITE, 0.52), 0.93)
    ctx.set_source(g)
    ellipse_path(ctx, ix, iy, w * 0.76, hh * 1.00, 0, 0, 2 * math.pi); ctx.fill()
    # 瞳孔
    ctx.set_source_rgba(*mix(EYE_D, INK, 0.40), 0.95)
    ellipse_path(ctx, ix, iy + hh * 0.10, w * 0.38, hh * 0.54, 0, 0, 2 * math.pi); ctx.fill()
    # 下缘反光：一条薄月牙
    ctx.set_source_rgba(1, 1, 1, 0.30)
    ellipse_path(ctx, ix, iy + hh * 0.64, w * 0.50, hh * 0.19, 0, 0, 2 * math.pi); ctx.fill()
    # 高光：一大一小
    ctx.set_source_rgba(1, 1, 1, 0.97)
    ellipse_path(ctx, X(look[0] * w * 0.16 - w * 0.28), iy - hh * 0.40,
                 w * 0.24, w * 0.29, 0, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.62)
    ctx.arc(X(look[0] * w * 0.16 + w * 0.32), iy + hh * 0.36, w * 0.09, 0, 2 * math.pi); ctx.fill()
    ctx.restore()

    almond(1.0)
    ctx.set_line_width(w * 0.10); ctx.set_source_rgba(*INK, 0.32); ctx.stroke()

    # 上睑：一片柳叶形的厚线，内细外粗再收尖
    ctx.new_path()
    ctx.move_to(X(-w * 1.00), ey + h * 0.06)
    ctx.curve_to(X(-w * 0.66), ey - h * 0.86, X(w * 0.30), ey - h * 0.98,
                 X(w * 0.92), ey - h * 0.20)
    ctx.curve_to(X(w * 1.10), ey - h * 0.04, X(w * 1.10), ey + h * 0.10,
                 X(w * 0.88), ey + h * 0.04)
    ctx.curve_to(X(w * 0.30), ey - h * 0.56, X(-w * 0.60), ey - h * 0.52,
                 X(-w * 0.96), ey + h * 0.12)
    ctx.close_path()
    ctx.set_source_rgba(*INK, 0.90); ctx.fill()

    # 下睑：只画外侧一段，很弱
    ctx.new_path()
    ctx.move_to(X(w * 0.12), ey + h * 0.86)
    ctx.curve_to(X(w * 0.56), ey + h * 0.78, X(w * 0.86), ey + h * 0.44,
                 X(w * 0.96), ey + h * 0.02)
    ctx.set_line_width(w * 0.08); ctx.set_source_rgba(*INK, 0.30); ctx.stroke()


def _brow(ctx, ex, ey, w, expr):
    ctx.new_path()
    if expr == "shock":
        ctx.move_to(ex - w * 0.66, ey - w * 0.34)
        ctx.curve_to(ex - w * 0.18, ey - w * 0.82, ex + w * 0.26, ey - w * 0.80, ex + w * 0.66, ey - w * 0.30)
    elif expr == "sad":
        ctx.move_to(ex - w * 0.66, ey - w * 0.10)
        ctx.curve_to(ex - w * 0.20, ey - w * 0.42, ex + w * 0.24, ey - w * 0.44, ex + w * 0.68, ey - w * 0.16)
    else:
        ctx.move_to(ex - w * 0.64, ey - w * 0.16)
        ctx.curve_to(ex - w * 0.18, ey - w * 0.50, ex + w * 0.26, ey - w * 0.48, ex + w * 0.68, ey - w * 0.22)
    ctx.set_line_width(w * 0.145); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*mix(HAIR_SH, INK, 0.46), 0.72); ctx.stroke()


def _mouth(ctx, x, y, expr, open_k=0.0, u=1.0):
    w = 9.5 * u
    if expr == "shock":
        ctx.new_path(); ellipse_path(ctx, x, y + 2 * u, 6.4 * u, 9.4 * u, 0, 0, 2 * math.pi)
        ctx.set_source_rgba(*MOUTH, 0.75); ctx.fill_preserve()
        ctx.set_line_width(2.6 * u); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
    elif expr == "happy" or open_k > 0.35:
        o = max(open_k, 0.60)
        ctx.new_path()
        ctx.move_to(x - w, y - 1.4 * u)
        ctx.curve_to(x - w * 0.72, y + 16 * o * u, x + w * 0.72, y + 16 * o * u, x + w, y - 1.4 * u)
        ctx.curve_to(x + w * 0.40, y + 4.6 * o * u, x - w * 0.40, y + 4.6 * o * u, x - w, y - 1.4 * u)
        ctx.close_path(); ctx.set_source_rgba(*MOUTH, 0.85); ctx.fill_preserve()
        ctx.set_line_width(2.6 * u); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
    elif expr == "smug":
        ctx.new_path(); ctx.move_to(x - 8 * u, y - u)
        ctx.curve_to(x - 2 * u, y + 4.6 * u, x + 6 * u, y + 3 * u, x + 10 * u, y - 4 * u)
        ctx.set_line_width(2.9 * u); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
    elif expr == "sad":
        ctx.new_path(); ctx.move_to(x - 7 * u, y + 4 * u)
        ctx.curve_to(x - 2.2 * u, y - 2 * u, x + 2.2 * u, y - 2 * u, x + 7 * u, y + 4 * u)
        ctx.set_line_width(2.9 * u); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
    else:
        ctx.new_path(); ctx.move_to(x - 6.2 * u, y)
        ctx.curve_to(x - 2.4 * u, y + 4.6 * u, x + 2.4 * u, y + 4.6 * u, x + 6.2 * u, y)
        ctx.set_line_width(3.0 * u); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*INK, 0.9); ctx.stroke()


def draw_face(ctx, x, y, s=1.0, t=0.0, expr="normal", look=(0, 0),
              open_k=0.0, blink=0.0, mouth=True):
    rr = R * s

    def face_path():
        ctx.new_path()
        ctx.move_to(x - rr * 0.96, y - rr * 0.28)
        ctx.curve_to(x - rr * 1.00, y - rr * 1.00, x + rr * 1.00, y - rr * 1.00,
                     x + rr * 0.96, y - rr * 0.28)
        ctx.curve_to(x + rr * 0.98, y + rr * 0.36, x + rr * 0.76, y + rr * 0.84,
                     x + rr * 0.38, y + rr * 0.94)
        ctx.curve_to(x + rr * 0.13, y + rr * 1.00, x - rr * 0.13, y + rr * 1.00,
                     x - rr * 0.38, y + rr * 0.94)
        ctx.curve_to(x - rr * 0.76, y + rr * 0.84, x - rr * 0.98, y + rr * 0.36,
                     x - rr * 0.96, y - rr * 0.28)
        ctx.close_path()

    face_path()
    ctx.set_source_rgba(*SKIN, 0.97); ctx.fill()
    # 面部暗部：下巴与颈侧，用排线而不是实色
    ctx.save(); face_path(); ctx.clip()
    _hatch_fill(ctx, [(x - rr, y + rr * 0.30), (x + rr, y + rr * 0.30),
                      (x + rr, y + rr * 1.1), (x - rr, y + rr * 1.1)],
                amp=0.4, seed=3, closed=True, a=0.055, gap=7.5)
    ctx.set_source_rgba(*SKIN_SH, 0.30)
    ctx.new_path()
    ctx.move_to(x - rr * 0.78, y + rr * 0.72)
    ctx.curve_to(x - rr * 0.38, y + rr * 1.10, x + rr * 0.38, y + rr * 1.10,
                 x + rr * 0.78, y + rr * 0.72)
    ctx.line_to(x + rr * 0.88, y + rr * 1.12); ctx.line_to(x - rr * 0.88, y + rr * 1.12)
    ctx.close_path(); ctx.fill()
    # 腮红：三茬短斜线，彩铅的手感
    for sx in (-1, 1):
        ctx.set_line_width(rr * 0.022); ctx.set_source_rgba(*BLUSH, 0.75)
        for j in range(3):
            for i in range(4):
                px = x + sx * rr * (0.44 + i * 0.058)
                py = y + rr * (0.36 + j * 0.052)
                ctx.move_to(px - rr * 0.018, py + rr * 0.020)
                ctx.line_to(px + rr * 0.018, py - rr * 0.020)
        ctx.stroke()
    ctx.restore()

    face_path()
    ctx.set_line_width(rr * 0.062); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*INK, 0.92); ctx.stroke()
    # 下颚复线
    ctx.new_path()
    ctx.move_to(x - rr * 0.40, y + rr * 0.96)
    ctx.curve_to(x - rr * 0.14, y + rr * 1.02, x + rr * 0.14, y + rr * 1.02, x + rr * 0.40, y + rr * 0.96)
    ctx.set_line_width(rr * 0.024); ctx.set_source_rgba(*INK, 0.35); ctx.stroke()

    ex = rr * 0.42; ey = y + rr * 0.16
    ew, eh = rr * 0.250, rr * 0.262
    for sx in (-1, 1):
        _brow(ctx, x + sx * ex, ey - rr * 0.56, ew, expr)
    for sx in (-1, 1):
        _eye(ctx, x + sx * ex, ey, ew, eh, (look[0] * sx * 0.55 + look[0] * 0.45, look[1]),
             expr, blink, flip=sx)
    # 鼻：只一笔
    ctx.new_path()
    ctx.move_to(x + rr * 0.02 + look[0] * rr * 0.02, y + rr * 0.44)
    ctx.line_to(x + rr * 0.045 + look[0] * rr * 0.02, y + rr * 0.50)
    ctx.set_line_width(rr * 0.018); ctx.set_source_rgba(*SKIN_SH, 0.9)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if mouth:
        _mouth(ctx, x, y + rr * 0.66, expr, open_k, u=rr / 80.0)


# ================= 头发 =================
def _tail(ctx, x, y, hb, sx, t, wind=0.0, alpha=1.0):
    """单侧短双马尾：高位扎起，蓬、带两三个卷，垂到下颌就收"""
    ph = t * 1.5 + (1.1 if sx > 0 else 0.0)
    sway = math.sin(ph) * hb * 0.045 + wind * sx * 0.7
    # 短、高、蓬：一个圆鼓鼓的团，底缘只有一个浅浅的内勾
    pts = [(x + sx * hb * 0.80, y - hb * 0.76),
           (x + sx * (hb * 1.10 + sway * 0.3), y - hb * 1.04),
           (x + sx * (hb * 1.42 + sway * 0.6), y - hb * 0.94),
           (x + sx * (hb * 1.58 + sway), y - hb * 0.56),
           (x + sx * (hb * 1.60 + sway * 1.1), y - hb * 0.10),
           (x + sx * (hb * 1.46 + sway * 1.3), y + hb * 0.26),
           (x + sx * (hb * 1.24 + sway * 1.2), y + hb * 0.36),
           (x + sx * (hb * 1.14 + sway * 0.8), y + hb * 0.06),
           (x + sx * (hb * 1.04 + sway * 0.4), y - hb * 0.36),
           (x + sx * hb * 0.92, y - hb * 0.64)]
    fill_stroke(ctx, pts, HAIR, INK, hb * 0.050, seed=530 + sx, amp=0.8,
                fill_alpha=alpha)
    if alpha < 0.99:
        return
    ctx.save()
    ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.4, seed=530 + sx); ctx.clip()
    # 发束走向：顺着圆弧的两根长线
    for k in range(2):
        u = -0.04 + k * 0.12
        ctx.new_path()
        ctx.move_to(x + sx * hb * (1.02 + u), y - hb * 0.88)
        ctx.curve_to(x + sx * hb * (1.36 + u), y - hb * 0.54,
                     x + sx * hb * (1.44 + u), y - hb * 0.06,
                     x + sx * hb * (1.24 + u), y + hb * 0.24)
        ctx.set_line_width(hb * 0.018); ctx.set_source_rgba(*HAIR_SH, 0.72)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # 一个内卷，只在发尾收一下
    ctx.new_path()
    ctx.move_to(x + sx * hb * 1.14, y + hb * 0.24)
    ctx.curve_to(x + sx * hb * 1.30, y + hb * 0.06,
                 x + sx * hb * 1.44, y + hb * 0.16,
                 x + sx * hb * 1.38, y + hb * 0.30)
    ctx.set_line_width(hb * 0.022); ctx.set_source_rgba(*HAIR_SH, 0.55)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # 高光：靠内侧的一道亮线
    ctx.new_path()
    ctx.move_to(x + sx * hb * 1.02, y - hb * 0.82)
    ctx.curve_to(x + sx * hb * 1.22, y - hb * 0.48, x + sx * hb * 1.24, y - hb * 0.10,
                 x + sx * hb * 1.12, y + hb * 0.16)
    ctx.set_line_width(hb * 0.046); ctx.set_source_rgba(*HAIR_HL, 0.55)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


def _hair_ribbon(ctx, x, y, hb, sx, t):
    """发根的白缎带：两片小褶 + 中心结"""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(sx * (0.70 + math.sin(t * 1.7) * 0.05))
    r = hb * 0.112
    for s in (-1, 1):
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.curve_to(sx * s * r * 0.60, -r * 0.92, sx * s * r * 1.70, -r * 1.02,
                     sx * s * r * 1.62, -r * 0.10)
        ctx.curve_to(sx * s * r * 1.58, r * 0.66, sx * s * r * 0.60, r * 0.60, 0, 0)
        ctx.close_path()
        ctx.set_source_rgba(*WHITE, 0.97); ctx.fill_preserve()
        ctx.set_line_width(max(1.5, hb * 0.022)); ctx.set_source_rgba(*INK, 0.85); ctx.stroke()
        # 褶线
        ctx.new_path()
        ctx.move_to(sx * s * r * 0.10, -r * 0.06)
        ctx.curve_to(sx * s * r * 0.70, -r * 0.36, sx * s * r * 1.10, -r * 0.40,
                     sx * s * r * 1.34, -r * 0.22)
        ctx.set_line_width(max(1.0, hb * 0.012)); ctx.set_source_rgba(*INK, 0.32); ctx.stroke()
    ctx.new_path(); ellipse_path(ctx, 0, 0, r * 0.30, r * 0.26, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*mix(SAILOR_HL, WHITE, 0.55), 0.98); ctx.fill_preserve()
    ctx.set_line_width(max(1.4, hb * 0.020)); ctx.set_source_rgba(*INK, 0.85); ctx.stroke()
    ctx.restore()


def _hair_back(ctx, x, y, hb, t, wind=0.0):
    """后脑 + 短双马尾（高位、蓬、末端内勾）"""
    # 双马尾先画，发根压在头后
    for sx in (-1, 1):
        _tail(ctx, x, y, hb, sx, t, wind)

    sw = math.sin(t * 1.7) * hb * 0.03 + wind
    # 后脑整体：比 v5 更圆更饱满
    pts = [(x - hb * 1.04, y - hb * 0.60),
           (x - hb * 1.12, y + hb * 0.18),
           (x - hb * 0.94 + sw, y + hb * 0.86),
           (x - hb * 0.42 + sw, y + hb * 1.02),
           (x + hb * 0.46 + sw, y + hb * 1.02),
           (x + hb * 0.96 + sw, y + hb * 0.84),
           (x + hb * 1.14, y + hb * 0.16),
           (x + hb * 1.04, y - hb * 0.62),
           (x, y - hb * 1.18)]
    fill_stroke(ctx, pts, HAIR, INK, hb * 0.058, seed=511, amp=1.0)
    ctx.save()
    ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.5, seed=511); ctx.clip()
    _hatch_fill(ctx, pts, 0.5, 519, True, a=0.075, gap=7.0)
    ctx.set_source_rgba(*HAIR_HL, 0.32)
    ctx.new_path()
    ctx.move_to(x - hb * 0.60, y - hb * 0.30)
    ctx.curve_to(x - hb * 0.30, y + hb * 0.40, x + hb * 0.30, y + hb * 0.40, x + hb * 0.62, y - hb * 0.28)
    ctx.set_line_width(hb * 0.10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()

    # 发根缎带：画在马尾根部，压住与后脑的接缝
    for sx in (-1, 1):
        _hair_ribbon(ctx, x + sx * hb * 1.00, y - hb * 0.66, hb, sx, t)


def _cap(ctx, x, y, hb, t):
    """白色小护士帽：斜扣在头顶右侧，蓝帽带 + 侧面一个小蓝结

    这是芭芭拉最好认的一件头饰，所以画得比发箍更实。
    """
    wave = math.sin(t * 1.3) * 0.022
    ctx.save()
    ctx.translate(x + hb * 0.50, y - hb * 1.22)
    ctx.rotate(0.46 + wave)

    W2, H2 = hb * 0.40, hb * 0.29        # 半宽 / 高度
    pts = [(0, -H2 * 0.92),
           (W2 * 0.58, -H2 * 0.98),
           (W2 * 0.94, -H2 * 0.58),
           (W2 * 1.00, -H2 * 0.06),
           (W2 * 0.90, H2 * 0.44),
           (W2 * 0.44, H2 * 0.60),
           (0, H2 * 0.61),
           (-W2 * 0.46, H2 * 0.59),
           (-W2 * 0.92, H2 * 0.40),
           (-W2 * 1.00, -H2 * 0.10),
           (-W2 * 0.90, -H2 * 0.62),
           (-W2 * 0.46, -H2 * 0.96)]
    fill_stroke(ctx, pts, WHITE_D, INK, hb * 0.040, seed=580, amp=0.5, hatch=False)
    ctx.save()
    ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.4, seed=580); ctx.clip()
    _hatch_fill(ctx, pts, 0.4, 583, True, a=0.045, gap=8.0)
    # 帽顶一道浅影：低处的褶皱
    ctx.set_source_rgba(*mix(SAILOR_HL, INK, 0.18), 0.14)
    ctx.new_path()
    ctx.move_to(-W2 * 0.94, -H2 * 0.16)
    ctx.curve_to(-W2 * 0.44, -H2 * 0.66, W2 * 0.5, -H2 * 0.70, W2 * 0.94, -H2 * 0.22)
    ctx.line_to(W2 * 0.88, H2 * 0.10)
    ctx.curve_to(W2 * 0.4, -H2 * 0.36, -W2 * 0.4, -H2 * 0.40, -W2 * 0.88, H2 * 0.12)
    ctx.close_path(); ctx.fill()
    # 竖褶：几根很淡的线
    ctx.set_line_width(hb * 0.010); ctx.set_source_rgba(*INK, 0.16)
    for k in (-0.62, -0.26, 0.14, 0.52):
        ctx.new_path()
        ctx.move_to(W2 * k * 0.5, -H2 * 0.80)
        ctx.curve_to(W2 * k * 0.9, -H2 * 0.2, W2 * k, H2 * 0.3, W2 * k * 0.92, H2 * 0.56)
        ctx.stroke()
    ctx.restore()

    # 蓝帽带：顺着帽檐压出的圆弧
    ctx.new_path()
    ctx.move_to(-W2 * 1.01, H2 * 0.04)
    ctx.curve_to(-W2 * 0.44, H2 * 0.68, W2 * 0.46, H2 * 0.66, W2 * 0.98, H2 * 0.04)
    ctx.set_line_width(hb * 0.108); ctx.set_source_rgba(*SAILOR, 0.96)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.set_line_width(hb * 0.026); ctx.set_source_rgba(*SAILOR_SH, 0.90); ctx.stroke()

    # 侧面小蓝结
    bx = -W2 * 0.72
    by = H2 * 0.10
    for s in (-1, 1):
        ctx.new_path()
        ctx.move_to(bx, by)
        ctx.curve_to(bx + s * hb * 0.05, by - hb * 0.10, bx + s * hb * 0.15, by - hb * 0.08,
                     bx + s * hb * 0.14, by + hb * 0.01)
        ctx.curve_to(bx + s * hb * 0.13, by + hb * 0.08, bx + s * hb * 0.05, by + hb * 0.08,
                     bx, by)
        ctx.close_path()
        ctx.set_source_rgba(*SAILOR, 0.95); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.016); ctx.set_source_rgba(*INK, 0.80); ctx.stroke()
    ctx.new_path(); ellipse_path(ctx, bx, by, hb * 0.030, hb * 0.026, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*SAILOR_HL, 0.98); ctx.fill_preserve()
    ctx.set_line_width(hb * 0.013); ctx.set_source_rgba(*INK, 0.80); ctx.stroke()
    ctx.restore()


def _hair_front(ctx, x, y, hb, t):
    """中分钝刘海 + 两缕垂到下颌的鬓发"""
    sway = math.sin(t * 2.0) * hb * 0.012
    for sx in (-1, 1):
        # 鬓发：一条细长的尖，垂到下颌，不挡住马尾
        pts = [(x + sx * hb * 0.88, y - hb * 0.56),
               (x + sx * hb * 0.99, y + hb * 0.06),
               (x + sx * (hb * 0.95 + sway * sx), y + hb * 0.54),
               (x + sx * (hb * 0.90 + sway * sx), y + hb * 0.98),
               (x + sx * (hb * 0.83 + sway * sx), y + hb * 0.80),
               (x + sx * hb * 0.82, y + hb * 0.10),
               (x + sx * hb * 0.72, y - hb * 0.44)]
        fill_stroke(ctx, pts, HAIR, INK, hb * 0.046, seed=560 + sx, amp=0.6)

    def bangs():
        ctx.new_path()
        ctx.move_to(x - hb * 0.94, y - hb * 0.46)
        # 头顶弧：低一点的圆顶，别做成方盒子
        ctx.curve_to(x - hb * 0.96, y - hb * 0.92, x - hb * 0.74, y - hb * 1.16,
                     x - hb * 0.46, y - hb * 1.24)
        ctx.curve_to(x - hb * 0.26, y - hb * 1.29, x - hb * 0.06, y - hb * 1.28,
                     x - hb * 0.02, y - hb * 1.22)
        # 中分：到中间收成一个窄口，再对称拉开
        ctx.curve_to(x - hb * 0.008, y - hb * 1.12, x + hb * 0.008, y - hb * 1.12,
                     x + hb * 0.02, y - hb * 1.22)
        ctx.curve_to(x + hb * 0.06, y - hb * 1.28, x + hb * 0.26, y - hb * 1.29,
                     x + hb * 0.46, y - hb * 1.24)
        ctx.curve_to(x + hb * 0.74, y - hb * 1.16, x + hb * 0.96, y - hb * 0.92,
                     x + hb * 0.94, y - hb * 0.46)
        # 下缘：一整条平缓的弧，只在正中下压一点点，露出干净的额头
        ctx.curve_to(x + hb * 0.93, y - hb * 0.40, x + hb * 0.86, y - hb * 0.50,
                     x + hb * 0.74, y - hb * 0.56)
        ctx.curve_to(x + hb * 0.60, y - hb * 0.64, x + hb * 0.40, y - hb * 0.70,
                     x + hb * 0.22, y - hb * 0.78)
        ctx.curve_to(x + hb * 0.11, y - hb * 0.85, x + hb * 0.05, y - hb * 0.91,
                     x + hb * 0.015, y - hb * 0.94)
        ctx.curve_to(x - hb * 0.05, y - hb * 0.91, x - hb * 0.11, y - hb * 0.85,
                     x - hb * 0.22, y - hb * 0.78)
        ctx.curve_to(x - hb * 0.40, y - hb * 0.70, x - hb * 0.60, y - hb * 0.64,
                     x - hb * 0.74, y - hb * 0.56)
        ctx.curve_to(x - hb * 0.86, y - hb * 0.50, x - hb * 0.93, y - hb * 0.40,
                     x - hb * 0.92, y - hb * 0.38)
        ctx.close_path()

    bangs()
    ctx.set_source_rgba(*HAIR, 0.98); ctx.fill()
    ctx.save(); bangs(); ctx.clip()
    _hatch_fill(ctx, [(x - hb, y - hb * 1.4), (x + hb, y - hb * 1.4),
                      (x + hb, y), (x - hb, y)], 0.4, 571, True, a=0.06, gap=7.0)
    # 刘海的发丝：从头顶往下梳
    for sx in (-1, 1):
        for k in range(2):
            u = 0.18 + k * 0.26
            ctx.new_path()
            ctx.move_to(x + sx * hb * u * 0.6, y - hb * 1.26)
            ctx.curve_to(x + sx * hb * (u + 0.10), y - hb * 1.02,
                         x + sx * hb * (u + 0.20), y - hb * 0.86,
                         x + sx * hb * (u + 0.24), y - hb * 0.64)
            ctx.set_line_width(hb * 0.018); ctx.set_source_rgba(*HAIR_SH, 0.80); ctx.stroke()
    # 两侧的高光
    for sx in (-1, 1):
        ctx.new_path()
        ctx.move_to(x + sx * hb * 0.20, y - hb * 1.20)
        ctx.curve_to(x + sx * hb * 0.46, y - hb * 1.04, x + sx * hb * 0.60, y - hb * 0.82,
                     x + sx * hb * 0.62, y - hb * 0.54)
        ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*HAIR_HL, 0.55); ctx.stroke()
    ctx.restore()

    bangs()
    ctx.set_line_width(hb * 0.052); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*INK, 0.92); ctx.stroke()
    # 中分线：从发冠一直下到缺口
    ctx.new_path()
    ctx.move_to(x, y - hb * 1.23)
    ctx.line_to(x, y - hb * 1.16)
    ctx.set_line_width(hb * 0.020); ctx.set_source_rgba(*INK, 0.55); ctx.stroke()


# ================= 身体（水手裙） =================
Y_NECK  = 1.10
Y_SHLD  = 1.26
Y_CHEST = 1.52
Y_WAIST = 1.78
Y_HIP   = 1.94
Y_HEM   = 2.46
Y_KNEE  = 2.82
Y_ANKLE = 3.02


def _limb(ctx, p0, p1, w0, w1, bend=0.0):
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


def _bow(ctx, cx, cy, r, t=0.0, col=YELLOW, col_d=YELLOW_D, rot=0.0, alpha=1.0):
    """双环蝴蝶结 + 两条飘带"""
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot + math.sin(t * 1.6) * 0.03)
    for sx in (-1, 1):
        ctx.new_path()
        ctx.move_to(0, 0)
        ctx.curve_to(sx * r * 0.62, -r * 0.82, sx * r * 1.55, -r * 0.68, sx * r * 1.48, r * 0.06)
        ctx.curve_to(sx * r * 1.42, r * 0.78, sx * r * 0.58, r * 0.72, 0, 0)
        ctx.close_path()
        ctx.set_source_rgba(*col, 0.92 * alpha); ctx.fill_preserve()
        ctx.set_line_width(max(1.6, r * 0.13)); ctx.set_source_rgba(*INK, 0.90 * alpha); ctx.stroke()
    # 两条尾带
    for sx in (-1, 1):
        ctx.new_path()
        ctx.move_to(sx * r * 0.16, r * 0.30)
        ctx.curve_to(sx * r * 0.50, r * 1.20, sx * r * 0.80, r * 1.86,
                     sx * r * 0.62, r * 2.30)
        ctx.curve_to(sx * r * 0.30, r * 2.16, sx * r * 0.10, r * 1.40, sx * r * 0.04, r * 0.52)
        ctx.close_path()
        ctx.set_source_rgba(*col, 0.85 * alpha); ctx.fill_preserve()
        ctx.set_line_width(max(1.4, r * 0.10)); ctx.set_source_rgba(*INK, 0.85 * alpha); ctx.stroke()
    ctx.new_path(); ellipse_path(ctx, 0, 0, r * 0.26, r * 0.22, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*col_d, 0.95 * alpha); ctx.fill_preserve()
    ctx.set_line_width(max(1.4, r * 0.10)); ctx.set_source_rgba(*INK, 0.9 * alpha); ctx.stroke()
    ctx.restore()


def _duck(ctx, x, y, r, t=0.0):
    """挂在腿边的小黄鸭"""
    bob = math.sin(t * 2.4) * r * 0.10
    ctx.save(); ctx.translate(x, y + bob)
    ctx.new_path()
    ellipse_path(ctx, 0, 0, r * 0.86, r * 0.70, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*YELLOW, 0.95); ctx.fill_preserve()
    ctx.set_line_width(max(1.5, r * 0.12)); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
    # 头
    ctx.new_path(); ellipse_path(ctx, r * 0.40, -r * 0.62, r * 0.44, r * 0.42, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*YELLOW, 0.98); ctx.fill_preserve()
    ctx.set_line_width(max(1.4, r * 0.11)); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
    # 嘴
    ctx.new_path()
    ctx.move_to(r * 0.78, -r * 0.64); ctx.line_to(r * 1.14, -r * 0.52)
    ctx.line_to(r * 0.78, -r * 0.42); ctx.close_path()
    ctx.set_source_rgba(*YELLOW_D, 0.95); ctx.fill_preserve()
    ctx.set_line_width(max(1.2, r * 0.09)); ctx.set_source_rgba(*INK, 0.85); ctx.stroke()
    # 眼
    ctx.new_path(); ctx.arc(r * 0.50, -r * 0.74, r * 0.075, 0, 2 * math.pi)
    ctx.set_source_rgba(*INK, 0.95); ctx.fill()
    # 翅
    ctx.new_path()
    ctx.move_to(-r * 0.50, -r * 0.06)
    ctx.curve_to(-r * 0.16, -r * 0.24, r * 0.10, r * 0.02, -r * 0.22, r * 0.26)
    ctx.set_line_width(max(1.2, r * 0.09)); ctx.set_source_rgba(*INK, 0.45);
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


def draw_laoba(ctx, x, y, s=1.0, t=0.0, expr="normal", look=(0, 0), open_k=0.0,
               blink=0.0, pose=None, wind=0.0, bob=0.0, body=True, hat=True,
               fs=0.92, head_k=0.90):
    ctx.save()
    ctx.translate(0, bob)
    hb = R * s * head_k

    def Y(u):
        return y + hb * u

    if pose is None:
        pose = ((0.16, 0.06), (0.16, 0.06))

    if body:
        _hair_back(ctx, x, y, hb, t, wind)

        # ---- 脖子 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.19, Y(0.76))
        ctx.line_to(x + hb * 0.19, Y(0.76))
        ctx.line_to(x + hb * 0.21, Y(1.26))
        ctx.line_to(x - hb * 0.21, Y(1.26))
        ctx.close_path()
        ctx.set_source_rgba(*SKIN, 0.98); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
        ctx.new_path(); ellipse_path(ctx, x, Y(0.92), hb * 0.20, hb * 0.10, 0, 0, 2 * math.pi)
        ctx.set_source_rgba(*SKIN_SH, 0.55); ctx.fill()
        # ---- 颈饰：一条细蓝带 + 正中一颗蓝宝石（芭芭拉的第二个记号） ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.205, Y(1.11))
        ctx.curve_to(x - hb * 0.10, Y(1.16), x + hb * 0.10, Y(1.16), x + hb * 0.205, Y(1.11))
        ctx.set_line_width(hb * 0.042); ctx.set_source_rgba(*SAILOR, 0.92)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        r = hb * 0.048
        ctx.new_path()
        ctx.move_to(x, Y(1.22)); ctx.line_to(x + r, Y(1.16))
        ctx.line_to(x, Y(1.10)); ctx.line_to(x - r, Y(1.16))
        ctx.close_path()
        ctx.set_source_rgba(*mix(SAILOR_HL, WHITE, 0.30), 0.96); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.014); ctx.set_line_join(cairo.LINE_JOIN_MITER)
        ctx.set_source_rgba(*INK, 0.88); ctx.stroke()

        # ---- 腿：白色过膝袜 ----
        for sx in (-1, 1):
            lx = x + sx * hb * 0.29
            ctx.new_path()
            ctx.move_to(lx - hb * 0.145, Y(Y_HIP - 0.04))
            ctx.curve_to(lx - hb * 0.16, Y(Y_KNEE - 0.28), lx - hb * 0.10, Y(Y_KNEE),
                         lx - hb * 0.072, Y(Y_KNEE))
            ctx.curve_to(lx - hb * 0.082, Y(Y_KNEE + 0.16), lx - hb * 0.078, Y(Y_ANKLE - 0.12),
                         lx - hb * 0.070, Y(Y_ANKLE))
            ctx.line_to(lx + hb * 0.076, Y(Y_ANKLE))
            ctx.curve_to(lx + hb * 0.084, Y(Y_ANKLE - 0.12), lx + hb * 0.090, Y(Y_KNEE + 0.16),
                         lx + hb * 0.080, Y(Y_KNEE))
            ctx.curve_to(lx + hb * 0.102, Y(Y_KNEE), lx + hb * 0.170, Y(Y_KNEE - 0.28),
                         lx + hb * 0.150, Y(Y_HIP - 0.04))
            ctx.close_path()
            ctx.set_source_rgba(*SKIN, 0.98); ctx.fill()
            # 袜：从膝盖上一点到脚踝
            ctx.save(); ctx.clip()
            ctx.new_path()
            ctx.rectangle(lx - hb * 0.20, Y(Y_KNEE - 0.02), hb * 0.40, Y(Y_ANKLE) - Y(Y_KNEE - 0.02))
            ctx.set_source_rgba(*WHITE_D, 0.96); ctx.fill()
            ctx.new_path()
            ctx.move_to(lx - hb * 0.20, Y(Y_KNEE - 0.02)); ctx.line_to(lx + hb * 0.20, Y(Y_KNEE - 0.02))
            ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*SAILOR, 0.85); ctx.stroke()
            ctx.restore()
            ctx.new_path()
            ctx.move_to(lx - hb * 0.145, Y(Y_HIP - 0.04))
            ctx.curve_to(lx - hb * 0.16, Y(Y_KNEE - 0.28), lx - hb * 0.10, Y(Y_KNEE),
                         lx - hb * 0.072, Y(Y_KNEE))
            ctx.curve_to(lx - hb * 0.082, Y(Y_KNEE + 0.16), lx - hb * 0.078, Y(Y_ANKLE - 0.12),
                         lx - hb * 0.070, Y(Y_ANKLE))
            ctx.line_to(lx + hb * 0.076, Y(Y_ANKLE))
            ctx.curve_to(lx + hb * 0.084, Y(Y_ANKLE - 0.12), lx + hb * 0.090, Y(Y_KNEE + 0.16),
                         lx + hb * 0.080, Y(Y_KNEE))
            ctx.curve_to(lx + hb * 0.102, Y(Y_KNEE), lx + hb * 0.170, Y(Y_KNEE - 0.28),
                         lx + hb * 0.150, Y(Y_HIP - 0.04))
            ctx.close_path()
            ctx.set_line_width(hb * 0.032); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()

        # ---- 鞋：蓝色系带短靴 ----
        for sx in (-1, 1):
            bx = x + sx * hb * 0.29

            def shoe(u, v):
                return (bx + sx * u, v)
            ctx.new_path()
            ctx.move_to(*shoe(-hb * 0.100, Y(Y_ANKLE - 0.10)))
            ctx.line_to(*shoe(hb * 0.106, Y(Y_ANKLE - 0.10)))
            ctx.curve_to(*shoe(hb * 0.150, Y(Y_ANKLE + 0.06)),
                         *shoe(hb * 0.180, Y(Y_SOLE - 0.10)),
                         *shoe(hb * 0.140, Y(Y_SOLE)))
            ctx.curve_to(*shoe(hb * 0.06, Y(Y_SOLE + 0.030)),
                         *shoe(-hb * 0.10, Y(Y_SOLE + 0.030)),
                         *shoe(-hb * 0.140, Y(Y_SOLE - 0.02)))
            ctx.curve_to(*shoe(-hb * 0.168, Y(Y_ANKLE + 0.06)),
                         *shoe(-hb * 0.130, Y(Y_ANKLE - 0.10)),
                         *shoe(-hb * 0.100, Y(Y_ANKLE - 0.10)))
            ctx.close_path()
            ctx.set_source_rgba(*SAILOR, 0.92); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.034); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgba(*INK, 0.92); ctx.stroke()
            # 交叉系带
            for k in range(3):
                yy = Y(Y_ANKLE - 0.02 + k * 0.075)
                ctx.new_path()
                ctx.move_to(*shoe(-hb * 0.095, yy)); ctx.line_to(*shoe(hb * 0.100, yy + hb * 0.030))
                ctx.set_line_width(hb * 0.016); ctx.set_source_rgba(*WHITE_D, 0.95); ctx.stroke()
            # 鞋底
            ctx.new_path()
            ctx.move_to(*shoe(-hb * 0.135, Y(Y_SOLE - 0.012)))
            ctx.line_to(*shoe(hb * 0.138, Y(Y_SOLE - 0.012)))
            ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.55); ctx.stroke()

        # ---- 短裙：蓝色 + 白色荷叶边 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.52, Y(Y_WAIST - 0.02))
        ctx.curve_to(x - hb * 0.74, Y(Y_WAIST + 0.34), x - hb * 0.90, Y(Y_HEM - 0.10),
                     x - hb * 0.96, Y(Y_HEM))
        # 下摆：扇贝边
        n_sc = 7
        for i in range(1, n_sc + 1):
            u0 = -1 + 2 * (i - 0.5) / n_sc
            u1 = -1 + 2 * i / n_sc
            xm = lerp(x - hb * 0.96, x + hb * 0.96, (i - 0.5) / n_sc)
            ctx.curve_to(xm + hb * 0.02, Y(Y_HEM + 0.14), xm - hb * 0.02, Y(Y_HEM + 0.14),
                         lerp(x - hb * 0.96, x + hb * 0.96, i / n_sc), Y(Y_HEM))
        ctx.curve_to(x + hb * 0.90, Y(Y_HEM - 0.10), x + hb * 0.74, Y(Y_WAIST + 0.34),
                     x + hb * 0.52, Y(Y_WAIST - 0.02))
        ctx.close_path()
        ctx.set_source_rgba(*SAILOR, 0.92); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.046); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgba(*INK, 0.92); ctx.stroke()
        # 裙褶
        ctx.save()
        ctx.new_path()
        ctx.move_to(x - hb * 0.52, Y(Y_WAIST - 0.02))
        ctx.curve_to(x - hb * 0.74, Y(Y_WAIST + 0.34), x - hb * 0.90, Y(Y_HEM - 0.10),
                     x - hb * 0.96, Y(Y_HEM))
        for i in range(1, 8):
            ctx.line_to(lerp(x - hb * 0.96, x + hb * 0.96, i / 7.0), Y(Y_HEM))
        ctx.curve_to(x + hb * 0.90, Y(Y_HEM - 0.10), x + hb * 0.74, Y(Y_WAIST + 0.34),
                     x + hb * 0.52, Y(Y_WAIST - 0.02))
        ctx.close_path(); ctx.clip()
        for i in range(6):
            u = (i - 2.5) / 2.5
            ctx.new_path()
            ctx.move_to(x + u * hb * 0.34, Y(Y_WAIST + 0.04))
            ctx.curve_to(x + u * hb * 0.54, Y(Y_WAIST + 0.40), x + u * hb * 0.74, Y(Y_HEM - 0.24),
                         x + u * hb * 0.82, Y(Y_HEM + 0.06))
            ctx.set_line_width(hb * 0.020); ctx.set_source_rgba(*SAILOR_SH, 0.85); ctx.stroke()
        _hatch_fill(ctx, [(x - hb, Y(Y_WAIST)), (x + hb, Y(Y_WAIST)),
                          (x + hb, Y(Y_HEM + 0.2)), (x - hb, Y(Y_HEM + 0.2))],
                    0.3, 601, True, a=0.085, gap=7.2)
        ctx.restore()
        # 白色荷叶边（下摆外侧）
        ctx.new_path()
        for i in range(n_sc):
            xm = lerp(x - hb * 0.96, x + hb * 0.96, (i + 0.5) / n_sc)
            ctx.move_to(lerp(x - hb * 0.96, x + hb * 0.96, i / n_sc), Y(Y_HEM))
            ctx.curve_to(xm, Y(Y_HEM + 0.30), xm, Y(Y_HEM + 0.30),
                         lerp(x - hb * 0.96, x + hb * 0.96, (i + 1) / n_sc), Y(Y_HEM))
        ctx.set_line_width(hb * 0.026); ctx.set_source_rgba(*WHITE_D, 0.95); ctx.stroke()

        # ---- 白色上衣 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.46, Y(Y_SHLD - 0.06))
        ctx.curve_to(x - hb * 0.62, Y(Y_SHLD + 0.14), x - hb * 0.60, Y(Y_CHEST + 0.12),
                     x - hb * 0.52, Y(Y_WAIST - 0.02))
        ctx.line_to(x + hb * 0.52, Y(Y_WAIST - 0.02))
        ctx.curve_to(x + hb * 0.60, Y(Y_CHEST + 0.12), x + hb * 0.62, Y(Y_SHLD + 0.14),
                     x + hb * 0.46, Y(Y_SHLD - 0.06))
        ctx.close_path()
        ctx.set_source_rgba(*WHITE_D, 0.97); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.044); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgba(*INK, 0.92); ctx.stroke()
        ctx.save()
        ctx.clip()
        _hatch_fill(ctx, [(x - hb * 0.7, Y(Y_SHLD)), (x + hb * 0.7, Y(Y_SHLD)),
                          (x + hb * 0.7, Y(Y_WAIST)), (x - hb * 0.7, Y(Y_WAIST))],
                    0.3, 611, True, a=0.07, gap=7.0)
        ctx.restore()

        # ---- 水手领：后领一整条 + 两侧三角，压在白上衣上 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.50, Y(Y_SHLD + 0.14))
        ctx.curve_to(x - hb * 0.30, Y(Y_SHLD - 0.04), x + hb * 0.30, Y(Y_SHLD - 0.04),
                     x + hb * 0.50, Y(Y_SHLD + 0.14))
        ctx.curve_to(x + hb * 0.26, Y(Y_SHLD + 0.26), x - hb * 0.26, Y(Y_SHLD + 0.26),
                     x - hb * 0.50, Y(Y_SHLD + 0.14))
        ctx.close_path()
        ctx.set_source_rgba(*SAILOR, 0.94); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
        for sx in (-1, 1):
            ctx.new_path()
            ctx.move_to(x + sx * hb * 0.08, Y(Y_SHLD + 0.16))
            ctx.curve_to(x + sx * hb * 0.26, Y(Y_SHLD + 0.08), x + sx * hb * 0.44, Y(Y_SHLD + 0.16),
                         x + sx * hb * 0.46, Y(Y_SHLD + 0.30))
            ctx.curve_to(x + sx * hb * 0.38, Y(Y_SHLD + 0.60), x + sx * hb * 0.22, Y(Y_CHEST + 0.10),
                         x + sx * hb * 0.05, Y(Y_CHEST + 0.20))
            ctx.close_path()
            ctx.set_source_rgba(*SAILOR, 0.94); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
            # 白线边
            ctx.new_path()
            ctx.move_to(x + sx * hb * 0.12, Y(Y_SHLD + 0.20))
            ctx.curve_to(x + sx * hb * 0.30, Y(Y_SHLD + 0.13), x + sx * hb * 0.43, Y(Y_SHLD + 0.22),
                         x + sx * hb * 0.44, Y(Y_SHLD + 0.34))
            ctx.set_line_width(hb * 0.014); ctx.set_source_rgba(*WHITE_D, 0.95); ctx.stroke()

        # ---- 领巾：深蓝细长条 ----
        ctx.new_path()
        ctx.move_to(x - hb * 0.10, Y(Y_SHLD + 0.12))
        ctx.line_to(x + hb * 0.10, Y(Y_SHLD + 0.12))
        ctx.line_to(x + hb * 0.06, Y(Y_CHEST + 0.10))
        ctx.line_to(x - hb * 0.06, Y(Y_CHEST + 0.10))
        ctx.close_path()
        ctx.set_source_rgba(*SAILOR_SH, 0.95); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.022); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()

        # ---- 胸口黄蝴蝶结 ----
        _bow(ctx, x, Y(Y_CHEST - 0.02), hb * 0.20, t, YELLOW, YELLOW_D, rot=-0.04,
             alpha=0.96)

        # ---- 手臂 ----
        for i, sx in enumerate((-1, 1)):
            a1, a2 = pose[i]
            shx, shy = x + sx * hb * 0.46, Y(Y_SHLD + 0.06)
            L1, L2 = hb * 0.52, hb * 0.50
            a1w = a1 + 0.10 + 0.24 * math.sin(t * 2.0 + i * 1.4)
            el = (shx + sx * math.sin(a1w) * L1, shy + math.cos(a1w) * L1)
            a2w = a2 + 0.06 * math.sin(t * 1.7 + i)
            hd = (el[0] + sx * math.sin(a1w + a2w) * L2, el[1] + math.cos(a1w + a2w) * L2)

            # 小臂皮肤先铺底
            _limb(ctx, el, hd, hb * 0.098, hb * 0.082)
            ctx.set_source_rgba(*SKIN, 0.98); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()

            # 喇叭袖口：从肘部起向外张开，盖住小臂上段
            ang = math.atan2(hd[1] - el[1], hd[0] - el[0])
            ux, uy = math.cos(ang), math.sin(ang)
            vx, vy = -uy, ux
            c0 = (el[0] - ux * hb * 0.05, el[1] - uy * hb * 0.05)
            c1 = (el[0] + ux * hb * 0.26, el[1] + uy * hb * 0.26)
            w0, w1 = hb * 0.150, hb * 0.255
            ctx.new_path()
            ctx.move_to(c0[0] + vx * w0, c0[1] + vy * w0)
            ctx.curve_to(c0[0] + vx * w0 * 1.05 + ux * hb * 0.12, c0[1] + vy * w0 * 1.05 + uy * hb * 0.12,
                         c1[0] + vx * w1 * 0.94, c1[1] + vy * w1 * 0.94,
                         c1[0] + vx * w1, c1[1] + vy * w1)
            ctx.curve_to(c1[0] + ux * hb * 0.02, c1[1] + uy * hb * 0.02,
                         c1[0] - ux * hb * 0.02, c1[1] - uy * hb * 0.02,
                         c1[0] - vx * w1, c1[1] - vy * w1)
            ctx.curve_to(c1[0] - vx * w1 * 0.94, c1[1] - vy * w1 * 0.94,
                         c0[0] - vx * w0 * 1.05 + ux * hb * 0.12, c0[1] - vy * w0 * 1.05 + uy * hb * 0.12,
                         c0[0] - vx * w0, c0[1] - vy * w0)
            ctx.close_path()
            ctx.set_source_rgba(*SAILOR, 0.92); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.034); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgba(*INK, 0.9); ctx.stroke()
            # 袖口白边
            ctx.new_path()
            ctx.move_to(c1[0] + vx * w1, c1[1] + vy * w1)
            ctx.line_to(c1[0] - vx * w1, c1[1] - vy * w1)
            ctx.set_line_width(hb * 0.028); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(*WHITE_D, 0.95); ctx.stroke()

            # 肩头：一颗压在袖子底下的圆肩，只用它的外轮廓破开接缝
            ctx.new_path()
            ellipse_path(ctx, shx - sx * hb * 0.03, shy + hb * 0.01,
                        hb * 0.150, hb * 0.140, 0, 0, 2 * math.pi)
            ctx.set_source_rgba(*WHITE_D, 0.98); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.90); ctx.stroke()

            # 上臂白袖
            _limb(ctx, (shx, shy), el, hb * 0.170, hb * 0.140)
            ctx.set_source_rgba(*WHITE_D, 0.97); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.036); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgba(*INK, 0.92); ctx.stroke()

            # 手
            hx = hd[0] + ux * hb * 0.055
            hy = hd[1] + uy * hb * 0.055
            ctx.new_path()
            ellipse_path(ctx, hx, hy, hb * 0.112, hb * 0.094, ang, 0, 2 * math.pi)
            ctx.set_source_rgba(*SKIN, 0.98); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.030); ctx.set_source_rgba(*INK, 0.9); ctx.stroke()

        # ---- 腿边小黄鸭 ----
        _duck(ctx, x + hb * 0.86, Y(Y_KNEE + 0.28), hb * 0.19, t)

    # ---- 头 ----
    draw_face(ctx, x, y, s * head_k, t, expr, look, open_k, blink)
    _hair_front(ctx, x, y, hb, t)
    if hat:
        _cap(ctx, x, y, hb, t)

    ctx.restore()
