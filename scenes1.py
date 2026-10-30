# -*- coding: utf-8 -*-
"""场景 1：封面"""
import math
from art import *
from stage import *
from timeline import CUTS

CUT_B = [c / 0.5 for c in CUTS]     # 拍号

def blink_at(t):
    """周期性眨眼：[0,1] 闭眼程度"""
    ph = (t * 1.55 + 0.4) % 3.1
    if ph < 0.14:
        return math.sin(ph / 0.14 * math.pi)
    return 0.0

def s_title(ctx, t, d):
    # ---- 标题文字 ----
    a1 = seg(t, 0.25, 1.05)
    a2 = seg(t, 0.75, 1.60)
    a3 = seg(t, 1.20, 2.10)
    a4 = seg(t, 2.00, 2.80)

    draw_text(ctx, "CubeStation 数据小剧场 · 001", M, 138, 26, INK_SOFT,
              bold=True, alpha=a1 * 0.85)

    c = ease_out_back(a2)
    if c > 1e-3:
        ctx.save(); zoom(ctx, M, 0, c)
        title_block(ctx, None, "魔方玩家的成绩！", None, 1.0, y0=250, size=104)
        ctx.restore()

    c = ease_out_back(a3)
    if c > 1e-3:
        ctx.save(); zoom(ctx, M, 0, c)
        draw_text(ctx, "为什么不是正态分布？", M, 452, 86, CORAL)
        ctx.restore()

    # 分隔 + 副标题
    if a4 > 0:
        ctx.set_line_width(4)
        ctx.set_source_rgba(*INK, 0.55 * a4)
        ctx.move_to(M, 520); ctx.line_to(M + 300 * ease_out(a4), 520); ctx.stroke()
    draw_text(ctx, "130,104 位真实玩家的 SUB 成绩", M, 578, 31, INK,
              bold=True, alpha=seg(t, 2.25, 2.95) * 0.92)
    draw_text(ctx, "一次诚实的体检 · 无修图", M, 626, 27, INK_SOFT,
              bold=False, alpha=seg(t, 2.55, 3.25) * 0.8)

    # ---- 老芭 ----
    s = stand_s(770)
    rise = 1 - ease_out(seg(t, 0.10, 0.95), 3.2)
    wave = math.sin((t - 1.0) * 6.4) if t > 1.0 else 0.0
    amp = ease_out(seg(t, 1.0, 1.6)) * (1 - ease_in(seg(t, 6.6, 7.4)))
    pose = ((0.26, 0.10),
            (1.85 + 0.30 * wave * amp, 0.55 + 0.22 * wave * amp))
    laoba_at(ctx, 1516, 1036 + rise * 90, s, t,
             expr="happy" if (t % 4.2) < 0.35 else "normal",
             look=(-0.30, -0.06), pose=pose, blink=blink_at(t),
             bob=math.sin(t * 2.3) * 3.6 + rise * -14)

    # ---- 小方 ----
    if t > 2.9:
        ka = ease_out_back(seg(t, 2.9, 3.65))
        hop = abs(math.sin((t - 2.9) * 3.0)) * 40 * (1 - seg(t, 6.8, 7.6))
        draw_cube(ctx, 1232, 792 - hop - (1 - ka) * 140, 116 * ka,
                  t, rot=-0.06 + math.sin(t * 1.7) * 0.03,
                  expr="happy", look=(-0.5, -0.2),
                  arms=(0.9 + 0.5 * math.sin(t * 6), 0.62,
                        0.9 + 0.5 * math.sin(t * 6 + 1.2), 0.62))

    # ---- 点缀 ----
    for i, (sx, sy, ph) in enumerate(((1108, 742, 0.0), (1626, 596, 1.1), (1798, 856, 2.2))):
        a = seg(t, 3.1 + i * 0.25, 3.7 + i * 0.25) * (0.55 + 0.45 * math.sin(t * 3.1 + ph))
        sparkle(ctx, sx, sy, 19 + 5 * math.sin(t * 2.6 + ph), CREAM, rot=t * 0.6, width=4.6, alpha=a)
    foot(ctx, "数据来源：CubeStation 公开成绩样本", x=M, y=H - 62, align="left", a=0.6)


# ================= 场景 2：13 万条成绩 =================
import json as _json
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_D = _json.load(open(_os.path.join(_HERE, "stats.json"), encoding="utf-8"))
_BINS = list(zip(_D["hist"]["lin"]["counts"], _D["hist"]["lin"]["edges"][:-1]))
_N = _D["raw"]["linear"]["n"]
_MEAN = _D["trimmed"]["linear_mu"]
_MED = _D["trimmed"]["linear"]["median"]
_ROW = _D["meta"]["lines"]
_PK = max(c for c, _ in _BINS)

def s_data(ctx, t, d):
    title_block(ctx, "01 / 样本", "13 万条成绩", "长什么样？", seg(t, 0.1, 0.9), size=64)
    foot(ctx, "SUB 成绩 · 单位：秒 · 已剔除 >300s 的 7 条记录", a=0.55)

    # ---- 计数卡 ----
    cards = [("有效成绩", _N, "条", 1.0),
             ("原始行数", _ROW, "行", 1.45),
             ("平均值", _MEAN, "秒", 1.9)]
    for i, (lab, val, unit, t0) in enumerate(cards):
        a = seg(t, t0, t0 + 0.7)
        if a <= 0: continue
        x = 1170 + (i % 2) * 350
        y = 168 + (i // 2) * 172
        card(ctx, x, y, 330, 146, a, PAPER2, seed=30 + i)
        draw_text(ctx, lab, x + 26, y + 46, 24, INK_SOFT, bold=False, alpha=a)
        k = ease_out(seg(t, t0 + 0.15, t0 + 1.05), 2.4)
        v = f"{val * k:,.0f}"
        draw_text(ctx, v, x + 24, y + 120, 52, INK, alpha=a)
        draw_text(ctx, unit, x + 26 + text_width(ctx, v, 52) + 9, y + 118, 25, INK_SOFT, alpha=a)

    # ---- 直方图 ----
    bx0, bx1 = 150, 1180
    by0, by1 = 372, 884
    xmax = 300.0
    def X(v): return bx0 + (bx1 - bx0) * min(v, xmax) / xmax
    def Y(c): return by1 - (by1 - by0) * (c / _PK) ** 0.62

    # 柱
    for i, (c, lo) in enumerate(_BINS):
        a = seg(t, 0.9 + i * 0.014, 1.35 + i * 0.014)
        if a <= 0 or c == 0: continue
        h = (by1 - Y(c)) * ease_out_back(a, 1.4)
        col = mix(BUTTER, CORAL, clamp(lo / 150.0) ** 0.8)
        x = X(lo); w = X(lo + 5) - X(lo)
        rrect(ctx, x + 1.4, by1 - h, max(3.0, w - 2.8), h, min(8, w * 0.32),
              col, INK, 2.8, seed=200 + i, amp=0.5)

    # 轴
    ctx.set_line_width(4.5); ctx.set_source_rgb(*INK)
    ctx.move_to(bx0 - 16, by1); ctx.line_to(bx1 + 24, by1); ctx.stroke()
    ctx.set_line_width(3.2)
    for v in range(0, 301, 30):
        x = X(v)
        ctx.move_to(x, by1); ctx.line_to(x, by1 + 13); ctx.stroke()
        draw_text(ctx, str(v), x, by1 + 46, 22, INK_SOFT, align="center", bold=False,
                  alpha=seg(t, 1.6, 2.2))
    draw_text(ctx, "成绩 / 秒", bx1 + 36, by1 + 46, 22, INK_SOFT, bold=False,
              alpha=seg(t, 1.6, 2.2))

    # 峰值标注（上方留足空间）
    pa = seg(t, 2.6, 3.3)
    if pa > 0:
        px = X(32.5); py = Y(_PK)
        rough_arrow(ctx, px + 96, py - 96, px + 6, py - 20, 3.4, INK_SOFT, 13, 6, 3, alpha=pa)
        draw_text(ctx, "峰值在 30–35 秒", px + 104, py - 92, 25, INK, alpha=pa)
    # 均值 / 中位数：柱底虚线 + 卡片下方图例（水平引线）
    for (val, lab, col, t0, ly) in ((_MED, f"中位数 {_MED:.1f}s", MINT_D, 4.0, 640),
                                    (_MEAN, f"均值 {_MEAN:.1f}s", CORAL, 4.7, 700)):
        a = seg(t, t0, t0 + 0.6)
        if a <= 0: continue
        x = X(val)
        top = lerp(by1 - 4, Y(_PK) - 12, ease_out(a))
        ctx.save()
        ctx.set_dash([10, 8]); ctx.set_line_width(3.6)
        ctx.set_source_rgba(*col, 0.95 * a)
        ctx.move_to(x, by1 - 4); ctx.line_to(x, top); ctx.stroke()
        ctx.restore()
        # 从标签向左引一条折线到虚线顶端
        ctx.new_path()
        ctx.set_line_width(2.6); ctx.set_source_rgba(*col, 0.85 * a)
        ctx.move_to(1180, ly - 9); ctx.line_to(1108, ly - 9)
        ctx.line_to(x + 26, top + 6); ctx.line_to(x + 8, top + 6)
        ctx.stroke()
        ctx.new_path(); ctx.set_line_width(5); ctx.set_source_rgba(*col, a)
        ctx.arc(1168, ly - 9, 9, 0, 2 * math.pi); ctx.fill()
        draw_text(ctx, lab, 1192, ly, 27, INK, alpha=a, bold=True)


# ================= 场景 3：右偏长尾 =================
_SKEW = _D["raw"]["linear"]["skew"]
_KURT = _D["raw"]["linear"]["kurt"]
_MAXV = _D["raw"]["linear"]["max"]


def s_skew(ctx, t, d):
    title_block(ctx, "02 / 形状", "它其实是右偏的", "拖着一条长尾巴", seg(t, 0.1, 0.9),
                size=60, c2=CORAL)
    foot(ctx, "130,104 条原始成绩；横轴截到 300 秒，尾巴还在往右伸", a=0.55)

    # 左侧缩小版直方图
    bx0, bx1 = M, 900
    by1 = 926
    by0 = 566
    def X(v): return bx0 + (bx1 - bx0) * min(v, 300.0) / 300.0
    def Y(c): return by1 - (by1 - by0) * (c / _PK) ** 0.62
    appear = seg(t, 0.6, 1.5)
    for i, (c, lo) in enumerate(_BINS):
        a = seg(t, 0.6 + i * 0.008, 1.0 + i * 0.008)
        if a <= 0 or c == 0: continue
        h = (by1 - Y(c)) * ease_out_back(a, 1.3)
        col = mix(BUTTER, CORAL, clamp(lo / 150.0) ** 0.8)
        x = X(lo); w = X(lo + 5) - X(lo)
        if w < 2: continue
        rrect(ctx, x + 1, by1 - h, max(2.2, w - 2), h, min(6, w * 0.3),
              col, INK, 2.2, seed=300 + i, amp=0.4)
    ctx.set_line_width(4); ctx.set_source_rgb(*INK)
    ctx.move_to(bx0 - 12, by1); ctx.line_to(bx1 + 16, by1); ctx.stroke()
    draw_text(ctx, "0", bx0, by1 + 40, 20, INK_SOFT, align="center", bold=False, alpha=appear)
    draw_text(ctx, "300 秒", bx1, by1 + 40, 20, INK_SOFT, align="center", bold=False, alpha=appear)

    # 长尾箭头
    ta = seg(t, 2.4, 3.4)
    if ta > 0:
        rough_arrow(ctx, X(112), by1 - 74, X(290), by1 - 74, 3.2, CORAL, 15, 20, 7, alpha=ta)
        draw_text(ctx, "极少数人拖到几百秒", X(120), by1 - 92, 24, CORAL, alpha=ta, bold=True)

    # 右侧大字
    rows = [("中位数", "一半比它快", f"{_MED:.0f}", 1.5, MINT_D),
            ("平均数", "被尾巴拖高", f"{_MEAN:.0f}", 2.2, CORAL),
            ("最长一局", "秒", None, 2.9, INK)]
    for i, (lab, note, val, t0, col) in enumerate(rows):
        a = seg(t, t0, t0 + 0.6)
        if a <= 0: continue
        y = 480 + i * 150
        k = ease_out(seg(t, t0 + 0.1, t0 + 0.9), 2.6)
        draw_text(ctx, lab, 1002, y - 48, 26, INK_SOFT, bold=False, alpha=a)
        num = val if val else f"{_MAXV * k:,.0f}"
        draw_text(ctx, num, 1000, y + 34, 76, col, alpha=a)
        draw_text(ctx, note, 1004 + text_width(ctx, num, 76) + 14, y + 28, 26, INK_SOFT,
                  bold=False, alpha=a)

    # 结论条
    ribbon(ctx, "少数慢的，把平均数拉高了一截", 1180, 872, 32, INK, BUTTER, seg(t, 3.6, 4.4))

    # 小方
    ka = seg(t, 4.6, 5.4)
    if ka > 0:
        draw_cube(ctx, 1650, 790 + math.sin(t * 2.4) * 10, 74 * ease_out_back(ka), t,
                  rot=0.10 + math.sin(t * 1.4) * 0.06, expr="shock",
                  look=(-1.0, 0.2), arms=(2.3, 0.2, 2.5, 0.15))

