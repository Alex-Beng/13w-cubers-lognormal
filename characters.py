# -*- coding: utf-8 -*-
"""角色 v3：老芭（金发双马尾偶像）+ 小方（拟人魔方），日系赛璐璐平涂 + 粗马克笔线"""
import math
from art import *

SKIN    = (0.996, 0.914, 0.867)
SKIN_SH = (0.968, 0.812, 0.784)
# 奶油金发
HAIR    = (0.949, 0.898, 0.780)
HAIR_SH = (0.855, 0.778, 0.635)
HAIR_HL = (0.998, 0.972, 0.885)
# 白裙 / 藏青 / 蓝绿缎带 / 金饰
DRESS   = (0.992, 0.986, 0.972)
DRESS_SH= (0.902, 0.900, 0.918)
DRESS_D = (0.822, 0.822, 0.856)
NAVY    = (0.242, 0.298, 0.462)
NAVY_D  = (0.168, 0.208, 0.338)
BOW     = (0.268, 0.548, 0.706)
BOW_D   = (0.172, 0.382, 0.532)
GOLD    = (0.902, 0.762, 0.430)
GOLD_D  = (0.760, 0.598, 0.286)
LACE    = (0.998, 0.992, 0.975)
SKIRT   = (0.986, 0.980, 0.966)
SKIRT_SH= (0.868, 0.872, 0.898)
EYE     = (0.205, 0.180, 0.255)
IRIS_T  = (0.215, 0.462, 0.630)
IRIS_B  = (0.470, 0.762, 0.800)
BLUSH   = (0.960, 0.690, 0.690)
MOUTH   = (0.545, 0.265, 0.320)
TONGUE  = (0.930, 0.560, 0.545)
SOCK    = (0.995, 0.985, 0.965)
SHOE    = (0.246, 0.286, 0.412)

R = 86.0   # 头半径（单位坐标）

def _eye(ctx, ex, ey, w, h, look, expr="normal", blink=0.0):
    if blink > 0.80 or expr == "happy":
        ctx.new_path()
        ctx.move_to(ex - w, ey + h * 0.10)
        ctx.curve_to(ex - w * 0.45, ey - h * 0.75, ex + w * 0.45, ey - h * 0.75, ex + w, ey + h * 0.10)
        ctx.set_line_width(w * 0.42); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
        # 睫毛小勾
        ctx.new_path()
        ctx.move_to(ex + w * 0.80, ey - h * 0.18)
        ctx.line_to(ex + w * 1.16, ey - h * 0.52)
        ctx.set_line_width(w * 0.26); ctx.set_source_rgb(*INK); ctx.stroke()
        return
    hh = h * max(0.12, 1.0 - blink)
    # 眼白
    ctx.new_path(); ellipse_path(ctx, ex, ey, w, hh, 0, 0, 2 * math.pi)
    ctx.set_source_rgb(0.999, 0.995, 0.985); ctx.fill()
    # 虹膜（裁剪在眼白内）
    ctx.save()
    ctx.new_path(); ellipse_path(ctx, ex, ey, w, hh, 0, 0, 2 * math.pi); ctx.clip()
    ix, iy = ex + look[0] * w * 0.22, ey + look[1] * h * 0.16 + hh * 0.06
    iw, ih = w * 0.80, hh * 0.92
    for i in range(14):
        t = i / 13.0
        ctx.set_source_rgb(*mix(IRIS_T, IRIS_B, t))
        ellipse_path(ctx, ix, iy - ih + ih * 2 * t + ih * 0.14, iw, ih * 0.30, 0, 0, 2 * math.pi)
        ctx.fill()
    # 瞳孔
    ctx.set_source_rgb(*EYE)
    ellipse_path(ctx, ix, iy + ih * 0.16, iw * 0.46, ih * 0.60, 0, 0, 2 * math.pi); ctx.fill()
    # 下缘反光
    ctx.set_source_rgba(*mix(IRIS_B, WHITE, 0.5), 0.85)
    ellipse_path(ctx, ix, iy + ih * 0.52, iw * 0.62, ih * 0.22, 0, 0, 2 * math.pi); ctx.fill()
    # 高光
    ctx.set_source_rgba(1, 1, 1, 0.96)
    ctx.arc(ix - iw * 0.36, iy - ih * 0.40, w * 0.30, 0, 2 * math.pi); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.72)
    ctx.arc(ix + iw * 0.40, iy + ih * 0.34, w * 0.14, 0, 2 * math.pi); ctx.fill()
    if expr == "shock":
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ellipse_path(ctx, ix, iy + ih * 0.10, iw * 0.20, ih * 0.26, 0, 0, 2 * math.pi); ctx.fill()
    ctx.restore()
    # 上眼睑粗线
    ctx.new_path()
    ctx.move_to(ex - w * 1.04, ey - hh * 0.30)
    ctx.curve_to(ex - w * 0.62, ey - hh * 1.22, ex + w * 0.62, ey - hh * 1.22, ex + w * 1.04, ey - hh * 0.26)
    ctx.set_line_width(w * 0.40); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*INK); ctx.stroke()
    # 下眼睑细线
    ctx.new_path()
    ctx.move_to(ex - w * 0.72, ey + hh * 0.94)
    ctx.curve_to(ex - w * 0.2, ey + hh * 1.18, ex + w * 0.3, ey + hh * 1.14, ex + w * 0.74, ey + hh * 0.88)
    ctx.set_line_width(w * 0.16); ctx.set_source_rgba(*INK, 0.55)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # 外眼角睫毛
    ctx.new_path()
    ctx.move_to(ex + w * 0.92, ey - hh * 0.44)
    ctx.line_to(ex + w * 1.28, ey - hh * 0.76)
    ctx.set_line_width(w * 0.26); ctx.set_source_rgb(*INK); ctx.stroke()

def _mouth(ctx, x, y, expr, open_k=0.0):
    if expr == "shock":
        ctx.new_path(); ellipse_path(ctx, x, y + 4, 10, 15, 0, 0, 2 * math.pi)
        ctx.set_source_rgb(*MOUTH); ctx.fill()
        ctx.set_line_width(4.5); ctx.set_source_rgb(*INK); ctx.stroke()
    elif expr == "happy" or open_k > 0.35:
        o = max(open_k, 0.55)
        ctx.new_path()
        ctx.move_to(x - 15, y - 3)
        ctx.curve_to(x - 12, y + 26 * o, x + 12, y + 26 * o, x + 15, y - 3)
        ctx.curve_to(x + 6, y + 8 * o, x - 6, y + 8 * o, x - 15, y - 3)
        ctx.close_path()
        ctx.set_source_rgb(*MOUTH); ctx.fill_preserve()
        ctx.set_line_width(4.5); ctx.set_source_rgb(*INK); ctx.stroke()
        ctx.save(); ctx.clip()
        ctx.set_source_rgb(*TONGUE)
        ellipse_path(ctx, x, y + 26 * o + 2, 11, 9 * o, 0, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
    elif expr == "smug":
        ctx.new_path()
        ctx.move_to(x - 12, y)
        ctx.curve_to(x - 2, y + 8, x + 10, y + 6, x + 15, y - 6)
        ctx.set_line_width(4.6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
    elif expr == "sad":
        ctx.new_path()
        ctx.move_to(x - 11, y + 6)
        ctx.curve_to(x - 4, y - 3, x + 4, y - 3, x + 11, y + 6)
        ctx.set_line_width(4.6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
    elif expr == "think":
        ctx.new_path()
        ctx.move_to(x - 8, y + 1)
        ctx.curve_to(x - 2, y + 4, x + 2, y + 4, x + 8, y - 1)
        ctx.set_line_width(4.6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
    else:
        ctx.new_path()
        ctx.move_to(x - 10, y)
        ctx.curve_to(x - 4, y + 7, x + 4, y + 7, x + 10, y)
        ctx.set_line_width(4.8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()

def _brow(ctx, ex, ey, w, expr):
    if expr in ("normal", "think"):
        return
    ctx.new_path()
    if expr == "shock":
        ctx.move_to(ex - w * 0.8, ey - w * 0.55)
        ctx.curve_to(ex - w * 0.3, ey - w * 0.95, ex + w * 0.3, ey - w * 0.95, ex + w * 0.8, ey - w * 0.55)
    elif expr == "sad":
        ctx.move_to(ex - w * 0.8, ey - w * 0.20)
        ctx.curve_to(ex - w * 0.2, ey - w * 0.78, ex + w * 0.4, ey - w * 0.70, ex + w * 0.9, ey - w * 0.30)
    else:  # smug
        ctx.move_to(ex - w * 0.8, ey - w * 0.40)
        ctx.curve_to(ex - w * 0.1, ey - w * 0.80, ex + w * 0.5, ey - w * 0.70, ex + w * 0.9, ey - w * 0.35)
    ctx.set_line_width(w * 0.30); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*mix(HAIR_SH, INK, 0.30)); ctx.stroke()

def draw_face(ctx, x, y, s=1.0, t=0.0, expr="normal", look=(0, 0),
              open_k=0.0, blink=0.0, mouth=True):
    rr = R * s
    # 脸
    ctx.new_path()
    ctx.move_to(x - rr * 0.96, y - rr * 0.18)
    ctx.curve_to(x - rr * 1.02, y - rr * 1.05, x + rr * 1.02, y - rr * 1.05, x + rr * 0.96, y - rr * 0.18)
    ctx.curve_to(x + rr * 0.90, y + rr * 0.62, x + rr * 0.42, y + rr * 0.96, x, y + rr * 0.98)
    ctx.curve_to(x - rr * 0.42, y + rr * 0.96, x - rr * 0.90, y + rr * 0.62, x - rr * 0.96, y - rr * 0.18)
    ctx.close_path()
    ctx.set_source_rgb(*SKIN); ctx.fill()
    # 下颌阴影（网点）
    ctx.save(); ctx.clip()
    ctx.set_source_rgba(*SKIN_SH, 0.55)
    for j in range(9):
        for i in range(24):
            px = x - rr * 1.0 + i * rr * 0.085
            py = y + rr * 0.55 + j * rr * 0.06
            if (py - y) > rr * 0.62 + 0.30 * abs(px - x):
                ctx.arc(px, py, rr * 0.022, 0, 2 * math.pi); ctx.fill()
    ctx.restore()
    ctx.new_path()
    ctx.move_to(x - rr * 0.96, y - rr * 0.18)
    ctx.curve_to(x - rr * 1.02, y - rr * 1.05, x + rr * 1.02, y - rr * 1.05, x + rr * 0.96, y - rr * 0.18)
    ctx.curve_to(x + rr * 0.90, y + rr * 0.62, x + rr * 0.42, y + rr * 0.96, x, y + rr * 0.98)
    ctx.curve_to(x - rr * 0.42, y + rr * 0.96, x - rr * 0.90, y + rr * 0.62, x - rr * 0.96, y - rr * 0.18)
    ctx.close_path()
    ctx.set_line_width(rr * 0.085); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(*INK); ctx.stroke()

    # 腮红（网点）
    for sx in (-1, 1):
        ctx.save()
        ctx.new_path()
        ellipse_path(ctx, x + sx * rr * 0.60, y + rr * 0.36, rr * 0.24, rr * 0.14, 0, 0, 2 * math.pi)
        ctx.clip()
        ctx.set_source_rgba(*BLUSH, 0.60)
        for j in range(4):
            for i in range(9):
                ctx.arc(x + sx * rr * 0.60 - rr * 0.22 + i * rr * 0.055,
                        y + rr * 0.28 + j * rr * 0.055, rr * 0.019, 0, 2 * math.pi); ctx.fill()
        ctx.restore()

    # 眼睛
    ex = rr * 0.40; ey = y + rr * 0.14
    ew, eh = rr * 0.215, rr * 0.285
    for sx in (-1, 1):
        _brow(ctx, x + sx * ex, ey - rr * 0.46, ew, expr)
    for sx in (-1, 1):
        _eye(ctx, x + sx * ex, ey, ew, eh, (look[0] * sx * 0.7 + look[0] * 0.3, look[1]), expr, blink)
    # 鼻
    ctx.new_path(); ctx.arc(x + look[0] * rr * 0.02, y + rr * 0.42, rr * 0.022, 0, 2 * math.pi)
    ctx.set_source_rgba(*SKIN_SH, 0.95); ctx.fill()
    if mouth:
        _mouth(ctx, x, y + rr * 0.68, expr, open_k)

def _hair_back(ctx, x, y, s, t, wind=0.0):
    rr = R * s
    sw = math.sin(t * 1.9) * rr * 0.035 + wind
    pts = [(x - rr * 1.08, y - rr * 0.12), (x - rr * 1.22 + sw, y + rr * 0.60),
           (x - rr * 1.06 + sw * 1.5, y + rr * 1.26), (x - rr * 0.70 + sw * 1.2, y + rr * 1.56),
           (x + rr * 0.70 + sw * 0.5, y + rr * 1.58), (x + rr * 1.06 + sw * 1.1, y + rr * 1.24),
           (x + rr * 1.22 + sw * 1.5, y + rr * 0.58), (x + rr * 1.08, y - rr * 0.12),
           (x, y - rr * 1.16)]
    fill_stroke(ctx, pts, HAIR, INK, rr * 0.095, seed=21, amp=0.9)
    # 网点暗部
    ctx.save()
    ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.5, seed=21); ctx.clip()
    ctx.set_source_rgba(*HAIR_SH, 0.5)
    step = rr * 0.075
    for j in range(int(2.8 * rr / step)):
        for i in range(int(2.6 * rr / step)):
            px = x - rr * 1.3 + i * step
            py = y + rr * 0.9 + j * step
            if (py - y) > rr * 1.5 + 0.30 * abs(px - x):
                ctx.arc(px + (step * 0.5 if j % 2 else 0), py, rr * 0.022, 0, 2 * math.pi); ctx.fill()
    ctx.restore()

def _hair_front(ctx, x, y, s, t):
    rr = R * s
    sway = math.sin(t * 2.2) * rr * 0.018
    # 两侧长鬓发（垂到胸前）
    for sx in (-1, 1):
        pts = [(x + sx * rr * 0.78, y - rr * 0.52),
               (x + sx * rr * 1.04, y + rr * 0.34),
               (x + sx * rr * 1.00 + sway * sx, y + rr * 1.02),
               (x + sx * rr * 0.74 + sway * sx, y + rr * 1.10),
               (x + sx * rr * 0.80, y + rr * 0.56),
               (x + sx * rr * 0.66, y - rr * 0.36)]
        fill_stroke(ctx, pts, HAIR, INK, rr * 0.085, seed=30 + sx, amp=0.7)
    # 刘海：中分 + 齐额碎发
    path = [
        ("m", x - rr * 0.98, y - rr * 0.14),
        ("c", x - rr * 1.06, y - rr * 1.14, x + rr * 0.88, y - rr * 1.20, x + rr * 1.00, y - rr * 0.18),
        # 右侧发梢：外长内短
        ("c", x + rr * 0.96, y + rr * 0.02, x + rr * 0.86, y - rr * 0.10, x + rr * 0.80, y - rr * 0.34),
        ("c", x + rr * 0.76, y - rr * 0.06, x + rr * 0.54, y - rr * 0.02, x + rr * 0.46, y - rr * 0.30),
        ("c", x + rr * 0.40, y - rr * 0.08, x + rr * 0.22, y - rr * 0.06, x + rr * 0.16, y - rr * 0.28),
        # 中分尖
        ("c", x + rr * 0.06, y - rr * 0.52, x - rr * 0.06, y - rr * 0.54, x - rr * 0.14, y - rr * 0.30),
        ("c", x - rr * 0.24, y - rr * 0.06, x - rr * 0.44, y - rr * 0.08, x - rr * 0.52, y - rr * 0.32),
        ("c", x - rr * 0.62, y - rr * 0.02, x - rr * 0.82, y - rr * 0.04, x - rr * 0.92, y - rr * 0.20),
        ("c", x - rr * 0.94, y - rr * 0.18, x - rr * 0.97, y - rr * 0.16, x - rr * 0.98, y - rr * 0.14),
    ]
    def build():
        ctx.new_path()
        ctx.move_to(path[0][1], path[0][2])
        for item in path[1:]:
            ctx.curve_to(item[1], item[2], item[3], item[4], item[5], item[6])
        ctx.close_path()
    build(); ctx.set_source_rgb(*HAIR); ctx.fill()
    # 高光带（沿头顶弧）
    ctx.save(); build(); ctx.clip()
    ctx.set_source_rgba(*HAIR_HL, 0.55)
    ctx.new_path()
    ctx.move_to(x - rr * 0.70, y - rr * 0.74)
    ctx.curve_to(x - rr * 0.28, y - rr * 1.00, x + rr * 0.32, y - rr * 0.96, x + rr * 0.72, y - rr * 0.66)
    ctx.set_line_width(rr * 0.115); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.set_source_rgba(*HAIR_HL, 0.32)
    ctx.new_path()
    ctx.move_to(x - rr * 0.34, y - rr * 0.92)
    ctx.curve_to(x - rr * 0.06, y - rr * 1.02, x + rr * 0.22, y - rr * 0.98, x + rr * 0.44, y - rr * 0.84)
    ctx.set_line_width(rr * 0.052); ctx.stroke()
    # 发梢阴影
    ctx.set_source_rgba(*HAIR_SH, 0.42)
    ctx.new_path()
    ctx.move_to(x - rr * 0.96, y - rr * 0.34)
    ctx.curve_to(x - rr * 0.40, y - rr * 0.10, x + rr * 0.30, y - rr * 0.10, x + rr * 0.96, y - rr * 0.32)
    ctx.line_to(x + rr * 0.96, y + rr * 0.10); ctx.line_to(x - rr * 0.96, y + rr * 0.10)
    ctx.close_path(); ctx.fill()
    ctx.restore()
    build()
    ctx.set_line_width(rr * 0.085); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(*INK); ctx.stroke()
    # 分缝线
    ctx.new_path()
    ctx.move_to(x + rr * 0.02, y - rr * 1.02)
    ctx.curve_to(x + rr * 0.04, y - rr * 0.80, x - rr * 0.02, y - rr * 0.60, x - rr * 0.08, y - rr * 0.42)
    ctx.set_line_width(rr * 0.026); ctx.set_source_rgba(*HAIR_SH, 0.85)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()

def _bow(ctx, x, y, w, h, c, cd, rot=0.0, tails=0.0, knot=True):
    """缎带蝴蝶结。w/h = 单侧半径"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    if tails > 0:
        for sx in (-1, 1):
            pts = [(sx * w * 0.18, h * 0.10), (sx * w * 0.62, h * 1.05),
                   (sx * w * 1.02, h * 1.70), (sx * w * 0.52, h * 1.52), (sx * w * 0.16, h * 0.62)]
            ctx.new_path(); ctx.move_to(*pts[0])
            for p in pts[1:]: ctx.line_to(*p)
            ctx.close_path(); ctx.set_source_rgb(*c); ctx.fill_preserve()
            ctx.set_line_width(max(1.4, w * 0.11)); ctx.set_source_rgb(*INK); ctx.stroke()
    for sx in (-1, 1):
        ctx.new_path()
        ctx.move_to(sx * w * 0.06, 0)
        ctx.curve_to(sx * w * 0.55, -h * 1.05, sx * w * 1.10, -h * 0.92, sx * w * 1.02, -h * 0.06)
        ctx.curve_to(sx * w * 1.12, h * 0.92, sx * w * 0.52, h * 1.02, sx * w * 0.06, h * 0.06)
        ctx.close_path()
        ctx.set_source_rgb(*mix(c, WHITE, 0.20)); ctx.fill_preserve()
        ctx.set_line_width(max(1.4, w * 0.13)); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
        # 折痕
        ctx.new_path()
        ctx.move_to(sx * w * 0.18, -h * 0.10)
        ctx.curve_to(sx * w * 0.58, -h * 0.42, sx * w * 0.86, -h * 0.30, sx * w * 0.94, -h * 0.02)
        ctx.set_line_width(max(1.0, w * 0.055)); ctx.set_source_rgba(*cd, 0.9); ctx.stroke()
    if knot:
        ctx.new_path(); ellipse_path(ctx, 0, 0, w * 0.20, h * 0.30, 0, 0, 2 * math.pi)
        ctx.set_source_rgb(*cd); ctx.fill_preserve()
        ctx.set_line_width(max(1.4, w * 0.11)); ctx.set_source_rgb(*INK); ctx.stroke()
    ctx.restore()

def _twin_curl(ctx, x, y, s, t, amp=1.0):
    """高位双马尾：外扬后垂落，末端卷成螺旋"""
    rr = R * s
    for sx in (-1, 1):
        ph = t * 2.4 + (0.9 if sx > 0 else 0)
        sw = math.sin(ph) * rr * 0.05 * amp
        bx, by = x + sx * rr * 0.90, y - rr * 0.58
        pts = [(bx, by),
               (bx + sx * rr * 0.46, by + rr * 0.12 + sw * 0.3),
               (bx + sx * rr * 0.70, by + rr * 0.76 + sw),
               (bx + sx * rr * 0.56, by + rr * 1.26 + sw * 1.3),
               (bx + sx * rr * 0.20, by + rr * 1.18 + sw * 1.1),
               (bx + sx * rr * 0.18, by + rr * 0.58 + sw * 0.4),
               (bx + sx * rr * 0.04, by + rr * 0.14)]
        fill_stroke(ctx, pts, HAIR, INK, rr * 0.082, seed=50 + sx, amp=0.8)
        ctx.save()
        ctx.new_path(); jitter_path(ctx, pts, closed=True, amp=0.4, seed=50 + sx); ctx.clip()
        ctx.set_source_rgba(*HAIR_HL, 0.45)
        ctx.new_path()
        ctx.move_to(bx + sx * rr * 0.22, by + rr * 0.26)
        ctx.curve_to(bx + sx * rr * 0.52, by + rr * 0.46, bx + sx * rr * 0.52, by + rr * 0.92,
                     bx + sx * rr * 0.28, by + rr * 1.10)
        ctx.set_line_width(rr * 0.062); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        ctx.restore()
        # 末端螺旋卷
        ccx = bx + sx * rr * 0.40
        ccy = by + rr * 1.50 + sw * 1.1
        rad = rr * 0.40
        ctx.new_path(); ellipse_path(ctx, ccx, ccy, rad, rad * 0.96, 0, 0, 2 * math.pi)
        ctx.set_source_rgb(*HAIR); ctx.fill_preserve()
        ctx.set_line_width(rr * 0.082); ctx.set_source_rgb(*INK); ctx.stroke()
        ctx.new_path()
        N = 46
        for i in range(N):
            u = i / (N - 1.0)
            a = u * 3.9 * math.pi * sx
            r = rad * (0.78 - 0.58 * u)
            px = ccx + math.cos(a) * r
            py = ccy + math.sin(a) * r
            if i == 0: ctx.move_to(px, py)
            else: ctx.line_to(px, py)
        ctx.set_line_width(rr * 0.058); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_source_rgb(*INK); ctx.stroke()
        ctx.new_path()
        for i in range(N):
            u = i / (N - 1.0)
            a = u * 3.9 * math.pi * sx
            r = rad * (0.78 - 0.58 * u)
            px = ccx + math.cos(a) * r
            py = ccy + math.sin(a) * r + rad * 0.08
            if i == 0: ctx.move_to(px, py)
            else: ctx.line_to(px, py)
        ctx.set_line_width(rr * 0.030); ctx.set_source_rgba(*HAIR_HL, 0.7); ctx.stroke()
        # 发饰：小号白蓝蝴蝶结
        _bow(ctx, bx + sx * rr * 0.06, by + rr * 0.02, rr * 0.24, rr * 0.17,
             LACE if sx < 0 else mix(LACE, BOW, 0.35), BOW, rot=sx * 0.26)
        sparkle(ctx, bx + sx * rr * 0.28, by - rr * 0.10, rr * 0.085, CREAM, rot=0.3, width=rr * 0.03)

def _gem(ctx, x, y, r, c=BOW, rot=0.0):
    """菱形宝石 + 高光"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.new_path()
    ctx.move_to(0, -r); ctx.line_to(r * 0.74, 0); ctx.line_to(0, r); ctx.line_to(-r * 0.74, 0)
    ctx.close_path()
    ctx.set_source_rgb(*c); ctx.fill_preserve()
    ctx.set_line_width(max(1.0, r * 0.30)); ctx.set_source_rgb(*INK); ctx.stroke()
    ctx.new_path()
    ctx.move_to(0, -r * 0.72); ctx.line_to(r * 0.34, -r * 0.06); ctx.line_to(0, r * 0.42); ctx.line_to(-r * 0.34, -r * 0.06)
    ctx.close_path()
    ctx.set_source_rgba(*mix(c, WHITE, 0.62), 0.80); ctx.fill()
    ctx.restore()

def _filigree(ctx, x, y, w, h, flip=1, lw=0.030, col=None):
    """金色卷草纹：S 形回旋 + 末端小圆"""
    c = col if col else GOLD_D
    ctx.new_path()
    ctx.move_to(x - w * 0.5, y)
    ctx.curve_to(x - w * 0.16, y - h * flip, x + w * 0.16, y + h * flip, x + w * 0.42, y - h * 0.10 * flip)
    ctx.curve_to(x + w * 0.56, y - h * 0.34 * flip, x + w * 0.40, y - h * 0.60 * flip, x + w * 0.26, y - h * 0.46 * flip)
    ctx.set_line_width(lw); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*c, 0.92); ctx.stroke()
    ctx.new_path()
    ctx.arc(x - w * 0.5, y, lw * 0.85, 0, 2 * math.pi)
    ctx.set_source_rgba(*c, 0.92); ctx.fill()

def _hat(ctx, x, y, s, t, tilt=-0.05):
    """白色小帽：白帽冠 + 藏青滚边 + 顶部金十字 + 两侧白羽"""
    rr = R * s
    ctx.save()
    ctx.translate(x, y); ctx.rotate(tilt)
    # 羽饰（从帽冠两侧张开）
    for sx in (-1, 1):
        for k in range(2):
            ctx.new_path()
            ctx.move_to(sx * rr * 0.26, rr * 0.10)
            ctx.curve_to(sx * rr * 0.66, -rr * (0.10 + k * 0.16),
                         sx * rr * 1.02, -rr * (0.34 + k * 0.20),
                         sx * rr * (1.20 + k * 0.04), -rr * (0.20 + k * 0.22))
            ctx.curve_to(sx * rr * 1.00, -rr * (0.02 + k * 0.10),
                         sx * rr * 0.64, rr * (0.16 + k * 0.02),
                         sx * rr * 0.30, rr * 0.26)
            ctx.close_path(); ctx.set_source_rgb(*LACE); ctx.fill_preserve()
            ctx.set_line_width(rr * 0.032); ctx.set_source_rgb(*INK); ctx.stroke()
    # 帽冠（扁圆顶）
    ctx.new_path()
    ctx.move_to(-rr * 0.62, rr * 0.14)
    ctx.curve_to(-rr * 0.66, -rr * 0.34, -rr * 0.36, -rr * 0.56, 0, -rr * 0.56)
    ctx.curve_to(rr * 0.36, -rr * 0.56, rr * 0.66, -rr * 0.34, rr * 0.62, rr * 0.14)
    ctx.close_path()
    ctx.set_source_rgb(*LACE); ctx.fill_preserve()
    ctx.set_line_width(rr * 0.046); ctx.set_source_rgb(*INK); ctx.stroke()
    # 藏青滚边（帽冠下沿）
    ctx.save()
    ctx.new_path()
    ctx.move_to(-rr * 0.62, rr * 0.14)
    ctx.curve_to(-rr * 0.66, -rr * 0.34, -rr * 0.36, -rr * 0.56, 0, -rr * 0.56)
    ctx.curve_to(rr * 0.36, -rr * 0.56, rr * 0.66, -rr * 0.34, rr * 0.62, rr * 0.14)
    ctx.close_path(); ctx.clip()
    ctx.new_path(); ctx.rectangle(-rr * 0.70, -rr * 0.10, rr * 1.40, rr * 0.30)
    ctx.set_source_rgb(*NAVY); ctx.fill()
    ctx.new_path(); ctx.rectangle(-rr * 0.70, -rr * 0.12, rr * 1.40, rr * 0.03)
    ctx.set_source_rgb(*GOLD); ctx.fill()
    ctx.restore()
    # 帽冠左侧阴影
    ctx.save()
    ctx.new_path()
    ctx.move_to(-rr * 0.62, rr * 0.14)
    ctx.curve_to(-rr * 0.66, -rr * 0.34, -rr * 0.36, -rr * 0.56, 0, -rr * 0.56)
    ctx.curve_to(rr * 0.36, -rr * 0.56, rr * 0.66, -rr * 0.34, rr * 0.62, rr * 0.14)
    ctx.close_path(); ctx.clip()
    ctx.set_source_rgba(*DRESS_SH, 0.9)
    ctx.new_path()
    ctx.move_to(-rr * 0.66, rr * 0.16); ctx.line_to(-rr * 0.66, -rr * 0.30)
    ctx.curve_to(-rr * 0.50, -rr * 0.10, -rr * 0.56, rr * 0.00, -rr * 0.58, rr * 0.16)
    ctx.close_path(); ctx.fill()
    ctx.restore()
    # 顶部金十字（小而立）
    cw = rr * 0.042
    ctx.new_path()
    ctx.move_to(-cw, -rr * 0.56); ctx.line_to(cw, -rr * 0.56)
    ctx.line_to(cw, -rr * 0.94); ctx.line_to(-cw, -rr * 0.94)
    ctx.close_path(); ctx.set_source_rgb(*GOLD); ctx.fill_preserve()
    ctx.set_line_width(rr * 0.020); ctx.set_source_rgb(*INK); ctx.stroke()
    ctx.new_path()
    ctx.move_to(-rr * 0.135, -rr * 0.80); ctx.line_to(rr * 0.135, -rr * 0.80)
    ctx.line_to(rr * 0.135, -rr * 0.70); ctx.line_to(-rr * 0.135, -rr * 0.70)
    ctx.close_path(); ctx.set_source_rgb(*GOLD); ctx.fill_preserve()
    ctx.set_line_width(rr * 0.018); ctx.set_source_rgb(*INK); ctx.stroke()
    # 十字中心宝石
    _gem(ctx, 0, -rr * 0.79, rr * 0.045, mix(BOW, WHITE, 0.25))
    ctx.restore()

def draw_laoba(ctx, x, y, s=1.0, t=0.0, expr="normal", look=(0, 0), open_k=0.0,
               blink=0.0, pose=None, wind=0.0, bob=0.0, body=True, hat=True, fs=0.92,
               head_k=0.90):
    """老芭（全身偶像装）。x,y = 头部中心；head_k 控制头身比（越小越修长）"""
    ctx.save()
    ctx.translate(0, bob)
    rr = R * s * fs            # 身体尺度
    hs = s * head_k            # 头部尺度
    if body:
        _hair_back(ctx, x, y, hs, t, wind)
    hb = R * hs                # 头部半径（脸/发/帽用）
    neck = y + hb * 0.92
    sh_y = neck + rr * 0.36    # 肩
    ch = neck + rr * 1.36      # 胸
    ws = neck + rr * 2.10      # 腰
    hp = neck + rr * 2.58      # 胯
    hem = neck + rr * 4.24     # 白裙摆
    nhem = hem + rr * 0.36     # 藏青衬裙摆
    knee = neck + rr * 5.42
    ak = neck + rr * 6.82      # 脚踝
    sl = neck + rr * 7.42      # 鞋底
    if body:
        # 脖子
        ctx.new_path(); ctx.rectangle(x - hb * 0.21, neck - hb * 0.10, hb * 0.42, hb * 0.48)
        ctx.set_source_rgb(*SKIN); ctx.fill()
        for sx in (-1, 1):
            ctx.new_path()
            ctx.move_to(x + sx * hb * 0.21, neck - hb * 0.04)
            ctx.line_to(x + sx * hb * 0.21, neck + hb * 0.34)
            ctx.set_line_width(hb * 0.044); ctx.set_source_rgb(*INK); ctx.stroke()
        ctx.new_path(); ctx.move_to(x - hb * 0.16, neck + hb * 0.32); ctx.line_to(x + hb * 0.16, neck + hb * 0.32)
        ctx.set_line_width(hb * 0.028); ctx.set_source_rgba(*SKIN_SH, 0.9); ctx.stroke()

        # ---- 腿（白丝袜）+ 短靴 ----
        leg_top = hp + rr * 0.26
        for sx in (-1, 1):
            lx = x + sx * rr * 0.25
            knx = lx - sx * rr * 0.014      # 膝略内收
            anx = lx + sx * rr * 0.022      # 踝略外撇
            ca = knee + rr * 0.92           # 小腿最粗处
            def leg_path(grow):
                w0 = rr * 0.232 + grow     # 大腿
                w1 = rr * 0.146 + grow     # 膝
                w2 = rr * 0.170 + grow     # 小腿肚
                w3 = rr * 0.098 + grow     # 踝
                ctx.new_path()
                ctx.move_to(lx - w0, leg_top)
                # 外侧：大腿 → 膝（内收）
                ctx.curve_to(lx - w0 * 1.10, leg_top + rr * 0.86,
                             knx - w1 * 1.16, knee - rr * 0.46,
                             knx - w1, knee)
                # 外侧：膝 → 小腿肚 → 踝（S 形，不加尖点）
                ctx.curve_to(knx - w1 * 1.10, knee + rr * 0.34,
                             anx - w2 * 1.10, ca - rr * 0.16,
                             anx - w2, ca)
                ctx.curve_to(anx - w2 * 0.96, ca + rr * 0.72,
                             anx - w3 * 1.02, ak - rr * 0.70,
                             anx - w3, ak - rr * 0.04)
                ctx.line_to(anx + w3, ak - rr * 0.04)
                # 内侧：踝 → 小腿肚 → 膝
                ctx.curve_to(anx + w3 * 1.02, ak - rr * 0.70,
                             anx + w2 * 0.94, ca + rr * 0.72,
                             anx + w2, ca)
                ctx.curve_to(anx + w2 * 1.08, ca - rr * 0.16,
                             knx + w1 * 1.12, knee + rr * 0.34,
                             knx + w1, knee)
                # 内侧：膝 → 大腿（大腿内侧比外侧直）
                ctx.curve_to(knx + w1 * 1.12, knee - rr * 0.52,
                             lx + w0 * 0.94, leg_top + rr * 0.92,
                             lx + w0, leg_top)
                ctx.line_to(lx - w0, leg_top)
                ctx.close_path()
            leg_path(rr * 0.020); ctx.set_source_rgb(*INK); ctx.fill()
            leg_path(0.0); ctx.set_source_rgb(*SOCK); ctx.fill()
            # 膝窝与小腿内侧阴影
            ctx.new_path()
            ctx.move_to(knx - sx * rr * 0.072, knee - rr * 0.10)
            ctx.curve_to(knx - sx * rr * 0.092, knee + rr * 0.56,
                         anx - sx * rr * 0.080, ak - rr * 1.10,
                         anx - sx * rr * 0.054, ak - rr * 0.60)
            ctx.set_line_width(rr * 0.058); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(*DRESS_SH, 0.85); ctx.stroke()
            ctx.new_path()
            ctx.move_to(knx + sx * rr * 0.070, knee + rr * 0.18)
            ctx.line_to(anx + sx * rr * 0.086, ak - rr * 0.96)
            ctx.set_line_width(rr * 0.030); ctx.set_source_rgba(*SKIN_SH, 0.55); ctx.stroke()
            # 膝头微高光
            ctx.new_path()
            ctx.move_to(knx - sx * rr * 0.010, knee - rr * 0.22)
            ctx.curve_to(knx + sx * rr * 0.048, knee - rr * 0.26,
                         knx + sx * rr * 0.054, knee + rr * 0.02,
                         knx + sx * rr * 0.022, knee + rr * 0.14)
            ctx.set_line_width(rr * 0.032); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.stroke()
            # 袜口
            ctx.new_path()
            ctx.move_to(lx - rr * 0.192, leg_top + rr * 0.10)
            ctx.line_to(lx + rr * 0.192, leg_top + rr * 0.07)
            ctx.set_line_width(rr * 0.042); ctx.set_source_rgba(*DRESS_D, 0.90); ctx.stroke()
            # ---- 靴：白色系带短靴 + 黑鞋头 + 藏青后跟 + 交叉白鞋带 + 蓝结 ----
            bt = ak - rr * 0.60      # 靴筒口
            bx = anx
            def boot():
                # 以 sx 镜像：+u 为身体外侧（脚尖方向）
                def B(u, v): return (bx + sx * u, v)
                ctx.new_path()
                ctx.move_to(*B(-rr * 0.132, bt))
                ctx.line_to(*B(rr * 0.132, bt))
                # 靴筒外侧，向下略收
                ctx.curve_to(*B(rr * 0.148, ak - rr * 0.34),
                             *B(rr * 0.148, ak - rr * 0.02),
                             *B(rr * 0.140, ak + rr * 0.10))
                # 脚背向前，圆弧到鞋尖
                ctx.curve_to(*B(rr * 0.186, ak + rr * 0.36),
                             *B(rr * 0.206, sl - rr * 0.10),
                             *B(rr * 0.168, sl - rr * 0.01))
                # 鞋尖底圆弧，回到内侧
                ctx.curve_to(*B(rr * 0.136, sl + rr * 0.02),
                             *B(rr * 0.004, sl + rr * 0.02),
                             *B(-rr * 0.124, sl))
                # 脚跟
                ctx.curve_to(*B(-rr * 0.146, ak + rr * 0.34),
                             *B(-rr * 0.150, ak + rr * 0.04),
                             *B(-rr * 0.132, bt))
                ctx.close_path()
            boot()
            ctx.set_source_rgb(*LACE); ctx.fill_preserve()
            ctx.set_line_width(rr * 0.046); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            ctx.save()
            boot(); ctx.clip()
            def B(u, v): return (bx + sx * u, v)
            # 藏青后跟片（靴筒内侧一段）
            ctx.new_path()
            ctx.move_to(*B(-rr * 0.170, bt - rr * 0.04))
            ctx.line_to(*B(-rr * 0.026, bt - rr * 0.04))
            ctx.line_to(*B(-rr * 0.044, ak + rr * 0.06))
            ctx.line_to(*B(-rr * 0.170, ak + rr * 0.16))
            ctx.close_path(); ctx.set_source_rgb(*NAVY); ctx.fill()
            # 黑漆鞋头（整个鞋头 + 鞋底包边，上沿接近水平）
            ctx.new_path()
            ctx.move_to(*B(-rr * 0.170, ak + rr * 0.26))
            ctx.curve_to(*B(-rr * 0.080, ak + rr * 0.23),
                         *B(rr * 0.060, ak + rr * 0.26),
                         *B(rr * 0.152, ak + rr * 0.30))
            ctx.curve_to(*B(rr * 0.196, sl - rr * 0.30),
                         *B(rr * 0.202, sl - rr * 0.06),
                         *B(rr * 0.150, sl + rr * 0.02))
            ctx.line_to(*B(-rr * 0.136, sl + rr * 0.02))
            ctx.curve_to(*B(-rr * 0.162, sl - rr * 0.10),
                         *B(-rr * 0.172, ak + rr * 0.44),
                         *B(-rr * 0.170, ak + rr * 0.26))
            ctx.close_path(); ctx.set_source_rgb(*INK); ctx.fill()
            # 鞋头白滚边（黑鞋头上沿的一道细白线）
            ctx.new_path()
            ctx.move_to(*B(-rr * 0.166, ak + rr * 0.255))
            ctx.curve_to(*B(-rr * 0.078, ak + rr * 0.228),
                         *B(rr * 0.058, ak + rr * 0.255),
                         *B(rr * 0.148, ak + rr * 0.295))
            ctx.set_line_width(rr * 0.018); ctx.set_source_rgba(*LACE, 0.95)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
            # 鞋尖高光
            ctx.new_path()
            ctx.move_to(*B(rr * 0.122, sl - rr * 0.24))
            ctx.curve_to(*B(rr * 0.158, sl - rr * 0.20),
                         *B(rr * 0.168, sl - rr * 0.13),
                         *B(rr * 0.156, sl - rr * 0.08))
            ctx.set_line_width(rr * 0.022); ctx.set_source_rgba(1, 1, 1, 0.22)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
            # 交叉鞋带（白绳压深线，形成 X）
            ctx.set_line_width(rr * 0.034); ctx.set_source_rgba(*DRESS_D, 0.9)
            for k in range(5):
                yy = bt + rr * 0.11 + k * rr * 0.102
                hw = rr * 0.136 - k * rr * 0.001
                ctx.new_path(); ctx.move_to(bx - hw, yy)
                ctx.line_to(bx + hw, yy + rr * 0.058); ctx.stroke()
                ctx.new_path(); ctx.move_to(bx + hw, yy)
                ctx.line_to(bx - hw, yy + rr * 0.058); ctx.stroke()
            ctx.set_line_width(rr * 0.018); ctx.set_source_rgba(*LACE, 0.98)
            for k in range(5):
                yy = bt + rr * 0.11 + k * rr * 0.102
                hw = rr * 0.136 - k * rr * 0.001
                ctx.new_path(); ctx.move_to(bx - hw, yy)
                ctx.line_to(bx + hw, yy + rr * 0.058); ctx.stroke()
                ctx.new_path(); ctx.move_to(bx + hw, yy)
                ctx.line_to(bx - hw, yy + rr * 0.058); ctx.stroke()
            ctx.restore()
            # 靴口藏青滚边 + 金线
            ctx.new_path(); ctx.move_to(bx - rr * 0.150, bt); ctx.line_to(bx + rr * 0.150, bt)
            ctx.set_line_width(rr * 0.052); ctx.set_source_rgb(*NAVY); ctx.stroke()
            ctx.new_path(); ctx.move_to(bx - rr * 0.150, bt); ctx.line_to(bx + rr * 0.150, bt)
            ctx.set_line_width(rr * 0.014); ctx.set_source_rgba(*GOLD, 0.95); ctx.stroke()
            # 靴口蓝结 + 垂带
            _bow(ctx, bx + sx * rr * 0.02, bt - rr * 0.06, rr * 0.150, rr * 0.110,
                 BOW, BOW_D, rot=sx * 0.22, tails=0.42)

        # ---- 衬裙（深藏青，白裙下露出一截）----
        nw1 = rr * 1.44
        nwt = rr * 0.64
        ctx.new_path()
        ctx.move_to(x - nwt * 0.94, hp - rr * 0.20)
        ctx.curve_to(x - nwt * 1.16, hp + rr * 0.52, x - nw1 * 0.88, nhem - rr * 0.66, x - nw1 * 0.92, nhem - rr * 0.08)
        ctx.curve_to(x - nw1 * 0.98, nhem + rr * 0.12, x - nw1 * 1.01, nhem + rr * 0.18, x - nw1 * 0.96, nhem + rr * 0.22)
        ctx.line_to(x + nw1 * 0.96, nhem + rr * 0.22)
        ctx.curve_to(x + nw1 * 1.01, nhem + rr * 0.18, x + nw1 * 0.98, nhem + rr * 0.12, x + nw1 * 0.92, nhem - rr * 0.08)
        ctx.curve_to(x + nw1 * 0.88, nhem - rr * 0.66, x + nwt * 1.16, hp + rr * 0.52, x + nwt * 0.94, hp - rr * 0.20)
        ctx.close_path()
        ctx.set_source_rgb(*NAVY); ctx.fill_preserve()
        ctx.set_line_width(rr * 0.052); ctx.set_source_rgb(*INK); ctx.stroke()
        for i in range(11):
            u = (i + 0.5) / 11.0
            ctx.new_path()
            ctx.move_to(x - nwt * 0.94 + nwt * 1.88 * u, hp + rr * 0.28)
            ctx.line_to(x - nw1 * 0.94 + nw1 * 1.88 * u, nhem + rr * 0.16)
            ctx.set_line_width(rr * 0.020); ctx.set_source_rgba(*NAVY_D, 0.9); ctx.stroke()
        # 衬裙荷叶边
        ctx.new_path()
        for i in range(19):
            u = i / 18.0
            px = x - nw1 * 0.94 + nw1 * 1.88 * u
            py = nhem + rr * 0.18 + math.sin(math.pi * (u * 18.0 % 1.0)) * rr * 0.09
            if i == 0: ctx.move_to(px, py)
            else: ctx.line_to(px, py)
        ctx.set_line_width(rr * 0.030); ctx.set_source_rgb(*INK); ctx.stroke()

        # ---- 白色外裙（A 字裙：腰部贴合、下摆张开 + 褶裥 + 荷叶边）----
        SW = 1.42                     # 下摆半宽
        def skirt_outline(g):
            """skirt 轮廓；g = 外扩量（用于墨线厚度）"""
            ctx.new_path()
            ctx.move_to(x - nwt * 0.90 - g, ws + rr * 0.04)
            ctx.curve_to(x - nwt * 1.20 - g, hp + rr * 0.34,
                         x - rr * 1.08 - g, hem - rr * 1.00,
                         x - rr * (SW * 0.94) - g, hem - rr * 0.20)
            ctx.curve_to(x - rr * (SW * 1.03) - g, hem + rr * 0.06,
                         x - rr * (SW * 1.02) - g, hem + rr * 0.12,
                         x - rr * (SW * 0.96) - g, hem + rr * 0.14)
            ctx.line_to(x + rr * (SW * 0.96) + g, hem + rr * 0.14)
            ctx.curve_to(x + rr * (SW * 1.02) + g, hem + rr * 0.12,
                         x + rr * (SW * 1.03) + g, hem + rr * 0.06,
                         x + rr * (SW * 0.94) + g, hem - rr * 0.20)
            ctx.curve_to(x + rr * 1.08 + g, hem - rr * 1.00,
                         x + nwt * 1.20 + g, hp + rr * 0.34,
                         x + nwt * 0.90 + g, ws + rr * 0.04)
            ctx.close_path()
        skirt_outline(0.0)
        ctx.set_source_rgb(*SKIRT); ctx.fill_preserve()
        ctx.set_line_width(rr * 0.052); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
        # 裙面褶裥：从腰省起，9 条放射硬褶
        for i in range(9):
            u = (i - 4) / 4.0
            ua = abs(u)
            top_w = nwt * (0.16 + 0.20 * ua)
            ctx.new_path()
            ctx.move_to(x + top_w * u, ws + rr * 0.12)
            ctx.curve_to(x + rr * 0.42 * u, hp + rr * 0.54,
                         x + rr * (0.72 + 0.34 * ua) * u, hem - rr * 0.90,
                         x + rr * (SW * 0.90) * u, hem + rr * 0.10)
            ctx.set_line_width(rr * (0.026 if i % 2 else 0.018))
            ctx.set_source_rgba(*(DRESS_D if i % 2 else SKIRT_SH), 0.85); ctx.stroke()
        # 裙侧暗部
        ctx.save(); skirt_outline(0.0); ctx.clip()
        ctx.new_path()
        ctx.move_to(x + rr * 0.78, hp + rr * 0.10)
        ctx.curve_to(x + rr * 0.98, hem - rr * 1.20, x + rr * 1.24, hem - rr * 0.40, x + rr * 1.42, hem + rr * 0.16)
        ctx.line_to(x + rr * 1.52, hem - rr * 1.40)
        ctx.close_path(); ctx.set_source_rgba(*SKIRT_SH, 0.55); ctx.fill()
        # 裙摆内侧暗部（下摆向下折进去一点）
        ctx.new_path()
        ctx.move_to(x - rr * 1.44, hem - rr * 0.06)
        ctx.curve_to(x - rr * 0.64, hem + rr * 0.20, x + rr * 0.64, hem + rr * 0.20, x + rr * 1.44, hem - rr * 0.06)
        ctx.line_to(x + rr * 1.44, hem + rr * 0.20); ctx.line_to(x - rr * 1.44, hem + rr * 0.20)
        ctx.close_path(); ctx.set_source_rgba(*SKIRT_SH, 0.75); ctx.fill()
        ctx.restore()
        # 下摆荷叶边（波浪剪影）
        nsc = 9
        ctx.new_path()
        for i in range(nsc * 6 + 1):
            u = i / float(nsc * 6)
            px = x - rr * (SW * 0.96) + rr * (SW * 1.92) * u
            py = hem + rr * 0.14 + math.sin(math.pi * (u * nsc % 1.0)) * rr * 0.085
            if i == 0: ctx.move_to(px, py)
            else: ctx.line_to(px, py)
        ctx.set_line_width(rr * 0.034); ctx.set_source_rgb(*INK); ctx.stroke()
        # 金边（贴着下摆内侧）
        ctx.new_path()
        ctx.move_to(x - rr * (SW * 0.99), hem + rr * 0.02)
        ctx.curve_to(x - rr * 0.62, hem + rr * 0.16, x + rr * 0.62, hem + rr * 0.16, x + rr * (SW * 0.99), hem + rr * 0.02)
        ctx.set_line_width(rr * 0.024); ctx.set_source_rgba(*GOLD_D, 0.95); ctx.stroke()

        # ---- 上身 ----
        torso = [(x - hb * 0.34, neck + rr * 0.04), (x - rr * 0.44, sh_y + rr * 0.02),
                 (x - rr * 0.62, sh_y + rr * 0.24), (x - rr * 0.60, ch), (x - rr * 0.44, ws),
                 (x - rr * 0.62, hp + rr * 0.02),
                 (x + rr * 0.62, hp + rr * 0.02), (x + rr * 0.44, ws), (x + rr * 0.60, ch),
                 (x + rr * 0.62, sh_y + rr * 0.24), (x + rr * 0.44, sh_y + rr * 0.02),
                 (x + hb * 0.34, neck + rr * 0.04)]
        fill_stroke(ctx, torso, DRESS, INK, rr * 0.055, seed=60, amp=0.9)
        # 裙腰封带（藏青 + 金线，顺着腰部曲线）
        ctx.new_path()
        ctx.move_to(x - rr * 0.560, ws + rr * 0.01)
        ctx.curve_to(x - rr * 0.30, ws - rr * 0.05, x + rr * 0.30, ws - rr * 0.05, x + rr * 0.560, ws + rr * 0.01)
        ctx.curve_to(x + rr * 0.578, ws + rr * 0.14, x + rr * 0.590, ws + rr * 0.16, x + rr * 0.598, ws + rr * 0.17)
        ctx.curve_to(x + rr * 0.30, ws + rr * 0.11, x - rr * 0.30, ws + rr * 0.11, x - rr * 0.598, ws + rr * 0.17)
        ctx.curve_to(x - rr * 0.590, ws + rr * 0.16, x - rr * 0.578, ws + rr * 0.14, x - rr * 0.560, ws + rr * 0.01)
        ctx.close_path()
        ctx.set_source_rgb(*NAVY); ctx.fill_preserve()
        ctx.set_line_width(rr * 0.028); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()
        ctx.new_path()
        ctx.move_to(x - rr * 0.578, ws + rr * 0.135)
        ctx.curve_to(x - rr * 0.28, ws + rr * 0.078, x + rr * 0.28, ws + rr * 0.078, x + rr * 0.578, ws + rr * 0.135)
        ctx.set_line_width(rr * 0.016); ctx.set_source_rgba(*GOLD, 0.95); ctx.stroke()
        for sx in (-1, 1):
            ctx.new_path()
            ctx.move_to(x + sx * rr * 0.15, sh_y + rr * 0.30)
            ctx.curve_to(x + sx * rr * 0.19, ch, x + sx * rr * 0.15, ws, x + sx * rr * 0.22, hp)
            ctx.set_line_width(rr * 0.020); ctx.set_source_rgba(*DRESS_D, 0.95); ctx.stroke()
        for sx in (-1, 1):
            ctx.new_path()
            ctx.move_to(x + sx * rr * 0.40, ch); ctx.line_to(x + sx * rr * 0.31, ws)
            ctx.line_to(x + sx * rr * 0.44, hp); ctx.line_to(x + sx * rr * 0.58, hp)
            ctx.close_path(); ctx.set_source_rgba(*DRESS_SH, 0.5); ctx.fill()

        # 高领（藏青立领 + 白蕾丝上沿，向上收成拱形）
        ctx.new_path()
        ctx.move_to(x - hb * 0.295, neck + hb * 0.40)
        ctx.curve_to(x - hb * 0.290, neck + hb * 0.10,
                     x - hb * 0.220, neck - hb * 0.10,
                     x - hb * 0.140, neck - hb * 0.18)
        ctx.curve_to(x - hb * 0.060, neck - hb * 0.26,
                     x + hb * 0.060, neck - hb * 0.26,
                     x + hb * 0.140, neck - hb * 0.18)
        ctx.curve_to(x + hb * 0.220, neck - hb * 0.10,
                     x + hb * 0.290, neck + hb * 0.10,
                     x + hb * 0.295, neck + hb * 0.40)
        ctx.close_path()
        ctx.set_source_rgb(*NAVY); ctx.fill_preserve()
        ctx.set_line_width(hb * 0.042); ctx.set_source_rgb(*INK); ctx.stroke()
        # 领口蕾丝扇形（白，贴在上沿弧上）
        for i in range(7):
            u = (i - 3) / 3.0
            lx = x + hb * 0.245 * u
            ly = neck - hb * (0.10 + 0.14 * (1 - u * u))
            ctx.new_path()
            ctx.arc(lx, ly, hb * 0.050, math.pi, 2 * math.pi)
            ctx.set_source_rgb(*LACE); ctx.fill_preserve()
            ctx.set_line_width(hb * 0.018); ctx.set_source_rgb(*INK); ctx.stroke()
        # 领上金线
        ctx.new_path()
        ctx.move_to(x - hb * 0.284, neck + hb * 0.235)
        ctx.curve_to(x - hb * 0.16, neck + hb * 0.295, x + hb * 0.16, neck + hb * 0.295, x + hb * 0.284, neck + hb * 0.235)
        ctx.set_line_width(hb * 0.016); ctx.set_source_rgba(*GOLD, 0.95); ctx.stroke()
        # 领前宝石 + 金色小坠
        ctx.new_path()
        ctx.move_to(x, neck + hb * 0.11); ctx.line_to(x + hb * 0.050, neck + hb * 0.21)
        ctx.line_to(x, neck + hb * 0.36); ctx.line_to(x - hb * 0.050, neck + hb * 0.21)
        ctx.close_path()
        ctx.set_line_width(hb * 0.014); ctx.set_source_rgb(*GOLD); ctx.stroke()
        _gem(ctx, x, neck + hb * 0.215, hb * 0.070, BOW)

        # 胸前蝴蝶结（白底大号 + 青蓝主结，双结错落）
        _bow(ctx, x, ch + rr * 0.00, rr * 0.375, rr * 0.175, LACE, DRESS_D, tails=0.0)
        _bow(ctx, x, ch + rr * 0.30, rr * 0.250, rr * 0.180, BOW, BOW_D, rot=0.0, tails=0.44)
        _gem(ctx, x, ch + rr * 0.30, rr * 0.064, mix(BOW, WHITE, 0.12))

        # 斜挂绶带 + 腰侧佩饰（挂在右胯，贴着裙侧）
        shh = rr * 0.255
        ox, oy = x + rr * 0.50, hp + rr * 0.30
        ctx.new_path()
        ctx.move_to(x - rr * 0.40, ws - rr * 0.16)
        ctx.line_to(ox - rr * 0.06, oy - shh * 0.55)
        ctx.set_line_width(rr * 0.066); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*NAVY_D); ctx.stroke()
        ctx.new_path()
        ctx.move_to(x - rr * 0.40, ws - rr * 0.16)
        ctx.line_to(ox - rr * 0.06, oy - shh * 0.55)
        ctx.set_line_width(rr * 0.022); ctx.set_source_rgba(*GOLD, 0.75); ctx.stroke()
        ctx.save(); ctx.translate(ox, oy); ctx.rotate(0.14)
        ctx.new_path(); ctx.rectangle(-shh * 0.84, -shh * 0.96, shh * 1.68, shh * 1.92)
        ctx.set_source_rgb(*NAVY); ctx.fill_preserve()
        ctx.set_line_width(rr * 0.028); ctx.set_source_rgb(*GOLD); ctx.stroke()
        ctx.new_path(); ctx.rectangle(-shh * 0.66, -shh * 0.78, shh * 1.32, shh * 1.56)
        ctx.set_line_width(rr * 0.014); ctx.set_source_rgba(*GOLD, 0.85); ctx.stroke()
        _gem(ctx, 0, -shh * 0.26, shh * 0.52, mix(BOW, WHITE, 0.06))
        ctx.new_path()
        ctx.arc(0, shh * 0.48, shh * 0.32, math.pi * 0.25, math.pi * 1.75)
        ctx.set_line_width(rr * 0.026); ctx.set_source_rgb(*GOLD); ctx.stroke()
        ctx.new_path()
        ctx.move_to(-rr * 0.020, shh * 0.86); ctx.line_to(rr * 0.020, shh * 0.86)
        ctx.line_to(rr * 0.020, shh * 1.20); ctx.line_to(-rr * 0.020, shh * 1.20)
        ctx.close_path(); ctx.set_source_rgb(*GOLD); ctx.fill()
        ctx.new_path()
        ctx.move_to(-rr * 0.070, shh * 0.98); ctx.line_to(rr * 0.070, shh * 0.98)
        ctx.line_to(rr * 0.070, shh * 1.05); ctx.line_to(-rr * 0.070, shh * 1.05)
        ctx.close_path(); ctx.set_source_rgb(*GOLD); ctx.fill()
        ctx.restore()

        for (fx, fy, fw, fh, fl) in ((x - rr * 0.32, hp + rr * 0.62, rr * 0.34, rr * 0.078, 1),
                                     (x - rr * 0.42, hp + rr * 1.18, rr * 0.30, rr * 0.072, -1),
                                     (x - rr * 0.14, hp + rr * 1.66, rr * 0.26, rr * 0.068, 1),
                                     (x + rr * 0.30, hp + rr * 0.86, rr * 0.28, rr * 0.066, -1)):
            _filigree(ctx, fx, fy, fw, fh, flip=fl, lw=rr * 0.022)

        # ---- 长袖（白，肩部泡泡袖 + 宽袖口 + 藏青腕带）----
        if pose is None:
            pose = ((0.16, 0.05), (0.16, 0.05))
        for i, sx in enumerate((-1, 1)):
            a1, a2 = pose[i]
            sh = (x + sx * rr * 0.62, sh_y + rr * 0.30)
            L1, L2 = rr * 0.98, rr * 0.92
            el = (sh[0] + sx * math.sin(a1) * L1, sh[1] + math.cos(a1) * L1)
            hd = (el[0] + sx * math.sin(a1 + a2) * L2, el[1] + math.cos(a1 + a2) * L2)
            ang1 = math.atan2(el[1] - sh[1], el[0] - sh[0])
            ang2 = math.atan2(hd[1] - el[1], hd[0] - el[0])
            def limb(p0, p1, w0, w1):
                """从 p0 到 p1 的锥形布料（p0 处半径 w0，p1 处 w1）"""
                a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                ux, uy = math.cos(a), math.sin(a)
                vx, vy = -uy, ux
                def Q(u, v): return (p0[0] + ux * u + vx * v, p0[1] + uy * u + vy * v)
                L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
                ctx.new_path()
                ctx.move_to(*Q(0, -w0))
                ctx.curve_to(*Q(L * 0.35, -w0 * 1.04), *Q(L * 0.70, -w1 * 0.92), *Q(L, -w1))
                ctx.curve_to(*Q(L * 1.04, -w1 * 0.60), *Q(L * 1.04, w1 * 0.60), *Q(L, w1))
                ctx.curve_to(*Q(L * 0.70, w1 * 0.92), *Q(L * 0.35, w0 * 1.04), *Q(0, w0))
                ctx.curve_to(*Q(-w0 * 0.20, w0 * 0.62), *Q(-w0 * 0.20, -w0 * 0.62), *Q(0, -w0))
                ctx.close_path()
            # 上臂：肩部略鼓，肘部收
            limb(sh, el, rr * 0.178, rr * 0.140)
            ctx.set_source_rgb(*DRESS); ctx.fill_preserve()
            ctx.set_line_width(rr * 0.044); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            # 前臂：肘部收窄，袖口张开（喇叭口）
            limb(el, hd, rr * 0.142, rr * 0.258)
            ctx.set_source_rgb(*DRESS); ctx.fill_preserve()
            ctx.set_line_width(rr * 0.044); ctx.set_source_rgb(*INK); ctx.stroke()
            # 袖内阴影
            for (p0, p1, w0, w1) in ((sh, el, 0.178, 0.140), (el, hd, 0.142, 0.258)):
                a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                ux, uy = math.cos(a), math.sin(a)
                ctx.new_path()
                ctx.move_to(p0[0] + (-uy) * rr * w0 * 0.56, p0[1] + ux * rr * w0 * 0.56)
                ctx.line_to(p1[0] + (-uy) * rr * w1 * 0.64, p1[1] + ux * rr * w1 * 0.64)
                ctx.set_line_width(rr * 0.040); ctx.set_source_rgba(*DRESS_SH, 0.85); ctx.stroke()
            # 上臂袖褶（沿袖轴的两道软褶）
            for k in (-1, 1):
                a = math.atan2(el[1] - sh[1], el[0] - sh[0])
                nxp, nyp = -math.sin(a), math.cos(a)
                ctx.new_path()
                ctx.move_to(sh[0] + nxp * rr * 0.070 * k + math.cos(a) * rr * 0.16,
                            sh[1] + nyp * rr * 0.070 * k + math.sin(a) * rr * 0.16)
                ctx.curve_to(sh[0] + nxp * rr * 0.095 * k + math.cos(a) * rr * 0.42,
                             sh[1] + nyp * rr * 0.095 * k + math.sin(a) * rr * 0.42,
                             sh[0] + nxp * rr * 0.085 * k + math.cos(a) * rr * 0.64,
                             sh[1] + nyp * rr * 0.085 * k + math.sin(a) * rr * 0.64,
                             sh[0] + nxp * rr * 0.062 * k + math.cos(a) * rr * 0.80,
                             sh[1] + nyp * rr * 0.062 * k + math.sin(a) * rr * 0.80)
                ctx.set_line_width(rr * 0.018); ctx.set_source_rgba(*DRESS_D, 0.75); ctx.stroke()
            # 肩部横向褶边（披肩式，坐落在肩线之上）
            ctx.new_path()
            ctx.move_to(x + sx * rr * 0.02, sh_y + rr * 0.02)
            ctx.curve_to(x + sx * rr * 0.26, sh_y - rr * 0.06,
                         x + sx * rr * 0.54, sh_y - rr * 0.04,
                         x + sx * rr * 0.655, sh_y + rr * 0.16)
            ctx.curve_to(x + sx * rr * 0.68, sh_y + rr * 0.34,
                         x + sx * rr * 0.60, sh_y + rr * 0.46,
                         x + sx * rr * 0.50, sh_y + rr * 0.44)
            ctx.curve_to(x + sx * rr * 0.46, sh_y + rr * 0.56,
                         x + sx * rr * 0.34, sh_y + rr * 0.52,
                         x + sx * rr * 0.29, sh_y + rr * 0.42)
            ctx.curve_to(x + sx * rr * 0.20, sh_y + rr * 0.50,
                         x + sx * rr * 0.06, sh_y + rr * 0.40,
                         x + sx * rr * 0.02, sh_y + rr * 0.26)
            ctx.close_path()
            ctx.set_source_rgb(*LACE); ctx.fill_preserve()
            ctx.set_line_width(rr * 0.040); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            for a0 in (0.16, 0.30, 0.44):
                ctx.new_path()
                ctx.move_to(x + sx * rr * (a0 + 0.02), sh_y + rr * 0.02)
                ctx.curve_to(x + sx * rr * (a0 + 0.06), sh_y + rr * 0.16,
                             x + sx * rr * (a0 + 0.07), sh_y + rr * 0.30,
                             x + sx * rr * (a0 + 0.05), sh_y + rr * 0.42)
                ctx.set_line_width(rr * 0.016); ctx.set_source_rgba(*DRESS_D, 0.70); ctx.stroke()
            # 腕带：藏青 + 金边（横跨袖口）
            ux2, uy2 = math.cos(ang2), math.sin(ang2)
            vx2, vy2 = -uy2, ux2
            bwc = rr * 0.214                  # 袖口半宽
            bdist = L2 - rr * 0.070
            bcx, bcy = el[0] + ux2 * bdist, el[1] + uy2 * bdist
            for (wide, col, lw, ln) in ((bwc, NAVY, 0.046, 0.0), (bwc + rr * 0.012, GOLD, 0.020, 0.0),
                                        (bwc - rr * 0.012, INK, 0.012, 0.0)):
                ctx.new_path()
                ctx.move_to(bcx + vx2 * wide, bcy + vy2 * wide)
                ctx.line_to(bcx - vx2 * wide, bcy - vy2 * wide)
                ctx.set_line_width(rr * lw); ctx.set_line_cap(cairo.LINE_CAP_BUTT)
                ctx.set_source_rgb(*col); ctx.stroke()
            # 腕带上的金线
            ctx.new_path()
            ctx.move_to(bcx + vx2 * bwc * 1.01 - ux2 * rr * 0.01, bcy + vy2 * bwc * 1.01 - uy2 * rr * 0.01)
            ctx.line_to(bcx - vx2 * bwc * 1.01 - ux2 * rr * 0.01, bcy - vy2 * bwc * 1.01 - uy2 * rr * 0.01)
            ctx.set_line_width(rr * 0.018); ctx.set_source_rgb(*GOLD); ctx.stroke()
            # 手：掌心 + 拇指（沿手臂方向，从袖口探出）
            hx = hd[0] + ux2 * rr * 0.055
            hy = hd[1] + uy2 * rr * 0.055
            ux, uy = ux2, uy2
            vx, vy = vx2, vy2
            def H(u, v): return (hx + ux * u + vx * v, hy + uy * u + vy * v)
            ctx.new_path()
            ctx.move_to(*H(-rr * 0.010, -rr * 0.104))
            ctx.curve_to(*H(rr * 0.140, -rr * 0.146), *H(rr * 0.268, -rr * 0.082), *H(rr * 0.264, rr * 0.014))
            ctx.curve_to(*H(rr * 0.256, rr * 0.098), *H(rr * 0.140, rr * 0.140), *H(-rr * 0.010, rr * 0.100))
            ctx.close_path()
            ctx.set_source_rgb(*SKIN); ctx.fill_preserve()
            ctx.set_line_width(rr * 0.038); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            # 拇指
            ctx.new_path()
            ctx.move_to(*H(rr * 0.066, -rr * 0.084))
            ctx.curve_to(*H(rr * 0.094, -rr * 0.186), *H(rr * 0.192, -rr * 0.172), *H(rr * 0.174, -rr * 0.084))
            ctx.set_line_width(rr * 0.050); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*SKIN); ctx.stroke()
            ctx.new_path()
            ctx.move_to(*H(rr * 0.094, -rr * 0.178))
            ctx.curve_to(*H(rr * 0.136, -rr * 0.186), *H(rr * 0.168, -rr * 0.152), *H(rr * 0.170, -rr * 0.108))
            ctx.set_line_width(rr * 0.022); ctx.set_source_rgb(*INK); ctx.stroke()
            # 指缝
            for k in range(3):
                ctx.new_path()
                ctx.move_to(*H(rr * 0.180, rr * (0.015 + k * 0.036)))
                ctx.line_to(*H(rr * 0.268, rr * (0.015 + k * 0.033)))
                ctx.set_line_width(rr * 0.013); ctx.set_source_rgba(*SKIN_SH, 0.95); ctx.stroke()
    draw_face(ctx, x, y, hs, t, expr, look, open_k, blink)
    _hair_front(ctx, x, y, hs, t)
    if hat:
        _hat(ctx, x - hb * 0.02, y - hb * 0.86, hs, t)
    _twin_curl(ctx, x, y, hs, t, amp=1.0 if body else 0.55)
    ctx.restore()


# 兼容旧调用
def draw_kaka(ctx, *a, **kw):
    """兼容旧调用：arms=(...) 更名为 pose=(...)"""
    if "arms" in kw:
        kw.setdefault("pose", kw.pop("arms"))
    return draw_laoba(ctx, *a, **kw)

# =============== 小方 ===============
FACE_TOP = (0.988, 0.985, 0.975)
FACE_L   = (0.960, 0.845, 0.620)
FACE_R   = (0.945, 0.700, 0.755)
STICKER  = (1.0, 0.995, 0.980)

def draw_cube(ctx, cx, cy, r, t=0.0, rot=0.0, expr="normal", look=(0, 0),
              arms=None, legs=True, squash=1.0, tilt=0.0, outline=1.0, alpha=1.0,
              face=True, seed=9, glow=None):
    """等距立方体。r = 立面横向半宽（px）"""
    k = r
    ctx.save()
    ctx.set_source_rgba(0, 0, 0, alpha)
    if not face:
        ctx.set_source_rgba(0, 0, 0, 0)

    s_ = k
    # 局部坐标：用 3 个四边形模拟
    # 顶点
    V = {
        "top":   (0, -0.72 * s_ * squash),
        "tl":    (-0.86 * s_, -0.14 * s_ * squash),
        "tr":    (0.86 * s_, -0.14 * s_ * squash),
        "bl":    (-0.86 * s_, 0.72 * s_ * squash),
        "br":    (0.86 * s_, 0.72 * s_ * squash),
        "bot":   (0, 1.30 * s_ * squash),
        "mid":   (0, 0.29 * s_ * squash),
    }
    cr, sr = math.cos(rot), math.sin(rot)
    def T(p):
        return (cx + p[0] * cr - (p[1] * squash) * sr, cy + p[0] * sr + (p[1] * squash) * cr)

    # 影子
    ctx.new_path()
    ellipse_path(ctx, cx, cy + 1.42 * s_ * squash, 0.90 * s_, 0.17 * s_, 0, 0, 2 * math.pi)
    ctx.set_source_rgba(*LILAC_D, 0.20); ctx.fill()

    # 腿
    if legs:
        for sx in (-1, 1):
            hip = T((sx * 0.32 * s_, 1.02 * s_ * squash))
            ft = (hip[0] + sx * 0.06 * s_, hip[1] + 0.34 * s_)
            ctx.new_path(); ctx.move_to(*hip); ctx.line_to(*ft)
            ctx.set_line_width(0.17 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            ctx.new_path(); ctx.move_to(*hip); ctx.line_to(*ft)
            ctx.set_line_width(0.095 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*WHITE); ctx.stroke()
            ctx.new_path()
            ellipse_path(ctx, ft[0] + sx * 0.05 * s_, ft[1] + 0.06 * s_, 0.15 * s_, 0.09 * s_, 0, 0, 2 * math.pi)
            ctx.set_source_rgb(*CORAL); ctx.fill_preserve()
            ctx.set_line_width(0.045 * s_); ctx.set_source_rgb(*INK); ctx.stroke()

    # 手臂（画在后面）
    if arms:
        for sx, ang, ln in ((-1, arms[0], arms[1]), (1, arms[2], arms[3])):
            ax, ay = T((sx * 0.80 * s_, 0.24 * s_ * squash))
            hx = ax + math.sin(ang) * ln * s_
            hy = ay + math.cos(ang) * ln * s_
            ctx.new_path(); ctx.move_to(ax, ay); ctx.line_to(hx, hy)
            ctx.set_line_width(0.135 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
            ctx.new_path(); ctx.move_to(ax, ay); ctx.line_to(hx, hy)
            ctx.set_line_width(0.075 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*WHITE); ctx.stroke()
            ctx.new_path(); ctx.arc(hx, hy, 0.072 * s_, 0, 2 * math.pi)
            ctx.set_source_rgb(*WHITE); ctx.fill_preserve()
            ctx.set_line_width(0.036 * s_); ctx.set_source_rgb(*INK); ctx.stroke()

    faces = [
        ([V["tl"], V["tr"], V["mid"], V["bl"]], FACE_TOP, 0.0),      # 上
        ([V["bl"], V["mid"], V["bot"], V["bl"]], FACE_L, 0.10),        # 左
        ([V["mid"], V["br"], V["tr"], V["mid"]], FACE_R, 0.06),        # 右
    ]
    # 正确三面
    top_poly = [V["top"], V["tr"], V["mid"], V["tl"]]
    left_poly = [V["tl"], V["mid"], V["bot"], V["bl"]]
    right_poly = [V["mid"], V["tr"], V["br"], V["bot"]]
    for poly, col in ((left_poly, FACE_L), (right_poly, FACE_R), (top_poly, FACE_TOP)):
        P = [T(p) for p in poly]
        ctx.new_path(); ctx.move_to(*P[0])
        for p in P[1:]: ctx.line_to(*p)
        ctx.close_path()
        ctx.set_source_rgb(*col); ctx.fill()
        # 网点暗部
        ctx.save(); ctx.clip()
        x0 = min(p[0] for p in P); x1 = max(p[0] for p in P)
        y0 = min(p[1] for p in P); y1 = max(p[1] for p in P)
        ctx.set_source_rgba(*mix(col, INK, 0.22), 0.45)
        st = 0.075 * s_
        jn = int((y1 - y0) / st) + 1
        inn = int((x1 - x0) / st) + 1
        for j in range(jn):
            for i in range(inn):
                px = x0 + i * st + (st / 2 if j % 2 else 0)
                py = y0 + j * st
                if (py - (y0 + (y1 - y0) * 0.45)) > 0:
                    ctx.arc(px, py, 0.021 * s_, 0, 2 * math.pi); ctx.fill()
        ctx.restore()
        # 贴纸分割 3x3
        def lerp2(a, b, u):
            return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
        for i in range(1, 3):
            u = i / 3
            a = lerp2(P[0], P[1], u); bb = lerp2(P[3], P[2], u)
            ctx.new_path(); ctx.move_to(*a); ctx.line_to(*bb)
            ctx.set_line_width(0.022 * s_); ctx.set_source_rgba(*INK, 0.55); ctx.stroke()
            a = lerp2(P[0], P[3], u); bb = lerp2(P[1], P[2], u)
            ctx.new_path(); ctx.move_to(*a); ctx.line_to(*bb)
            ctx.set_line_width(0.022 * s_); ctx.set_source_rgba(*INK, 0.55); ctx.stroke()
        # 轮廓
        ctx.new_path(); ctx.move_to(*P[0])
        for p in P[1:]: ctx.line_to(*p)
        ctx.close_path()
        ctx.set_line_width(0.052 * s_ * outline); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_source_rgb(*INK); ctx.stroke()

    # 贴纸高光
    ctx.save()
    P = [T(p) for p in top_poly]
    ctx.new_path(); ctx.move_to(*P[0])
    for p in P[1:]: ctx.line_to(*p)
    ctx.close_path(); ctx.clip()
    ctx.set_source_rgba(1, 1, 1, 0.55)
    ctx.move_to(cx - 0.55 * s_, cy - 0.95 * s_)
    ctx.line_to(cx - 0.18 * s_, cy - 1.05 * s_)
    ctx.line_to(cx + 0.10 * s_, cy - 0.62 * s_)
    ctx.line_to(cx - 0.28 * s_, cy - 0.50 * s_)
    ctx.close_path(); ctx.fill()
    ctx.restore()

    # 五官
    if face:
        fx, fy = cx, cy + 0.68 * s_ * squash
        lx, ly = look[0] * 0.03 * s_, look[1] * 0.03 * s_
        for sx in (-1, 1):
            ex = fx + sx * 0.30 * s_ + lx
            if expr == "happy":
                ctx.new_path()
                ctx.move_to(ex - 0.115 * s_, fy + 0.02 * s_)
                ctx.curve_to(ex - 0.06 * s_, fy - 0.10 * s_, ex + 0.06 * s_, fy - 0.10 * s_,
                             ex + 0.115 * s_, fy + 0.02 * s_)
                ctx.set_line_width(0.055 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.set_source_rgb(*INK); ctx.stroke()
            elif expr == "shock":
                ctx.new_path(); ctx.arc(ex, fy, 0.115 * s_, 0, 2 * math.pi)
                ctx.set_source_rgb(*WHITE); ctx.fill_preserve()
                ctx.set_line_width(0.045 * s_); ctx.set_source_rgb(*INK); ctx.stroke()
                ctx.new_path(); ctx.arc(ex + lx, fy + ly, 0.052 * s_, 0, 2 * math.pi)
                ctx.set_source_rgb(*INK); ctx.fill()
            else:
                ctx.new_path()
                ellipse_path(ctx, ex, fy, 0.075 * s_, 0.098 * s_, 0, 0, 2 * math.pi)
                ctx.set_source_rgb(*WHITE); ctx.fill()
                ctx.save(); ctx.clip()
                ctx.set_source_rgb(*EYE)
                ellipse_path(ctx, ex + lx * 1.5, fy + 0.012 * s_ + ly, 0.042 * s_, 0.062 * s_, 0, 0, 2 * math.pi); ctx.fill()
                ctx.set_source_rgba(1, 1, 1, 0.95)
                ctx.arc(ex - 0.028 * s_, fy - 0.045 * s_, 0.024 * s_, 0, 2 * math.pi); ctx.fill()
                ctx.restore()
                ctx.new_path()
                ellipse_path(ctx, ex, fy, 0.075 * s_, 0.098 * s_, 0, 0, 2 * math.pi)
                ctx.set_line_width(0.032 * s_); ctx.set_source_rgb(*INK); ctx.stroke()
        # 嘴
        if expr == "happy":
            ctx.new_path()
            ctx.move_to(fx - 0.12 * s_, fy + 0.17 * s_)
            ctx.curve_to(fx - 0.05 * s_, fy + 0.30 * s_, fx + 0.05 * s_, fy + 0.30 * s_, fx + 0.12 * s_, fy + 0.17 * s_)
            ctx.close_path(); ctx.set_source_rgb(*MOUTH); ctx.fill_preserve()
            ctx.set_line_width(0.035 * s_); ctx.set_source_rgb(*INK); ctx.stroke()
        elif expr == "shock":
            ctx.new_path(); ellipse_path(ctx, fx, fy + 0.22 * s_, 0.065 * s_, 0.085 * s_, 0, 0, 2 * math.pi)
            ctx.set_source_rgb(*MOUTH); ctx.fill_preserve()
            ctx.set_line_width(0.03 * s_); ctx.set_source_rgb(*INK); ctx.stroke()
        elif expr == "sad":
            ctx.new_path()
            ctx.move_to(fx - 0.10 * s_, fy + 0.24 * s_)
            ctx.curve_to(fx - 0.03 * s_, fy + 0.14 * s_, fx + 0.03 * s_, fy + 0.14 * s_, fx + 0.10 * s_, fy + 0.24 * s_)
            ctx.set_line_width(0.038 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
        else:
            ctx.new_path()
            ctx.move_to(fx - 0.09 * s_, fy + 0.20 * s_)
            ctx.curve_to(fx - 0.03 * s_, fy + 0.26 * s_, fx + 0.03 * s_, fy + 0.26 * s_, fx + 0.09 * s_, fy + 0.20 * s_)
            ctx.set_line_width(0.038 * s_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgb(*INK); ctx.stroke()
        # 腮红
        for sx in (-1, 1):
            ctx.set_source_rgba(*BLUSH, 0.60)
            ctx.new_path()
            ellipse_path(ctx, fx + sx * 0.47 * s_, fy + 0.10 * s_, 0.085 * s_, 0.05 * s_, 0, 0, 2 * math.pi); ctx.fill()
    ctx.restore()
