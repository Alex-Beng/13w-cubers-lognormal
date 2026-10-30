# -*- coding: utf-8 -*-
"""场景 5-8（新）：机制 → 假设 → 取对数 → 大数定律

这一段是整片的主干，顺序不能乱：
    why   为什么会有长尾：一局是"乘"出来的，不是"加"出来的
    model 多阶段假设：把一局拆成若干步，每步乘一个系数，乘积就是成绩
    log   取对数：乘法变加法
    law   大数定律：很多小项相加，堆成中间高两头低的钟形
"""
import math
from art import *
from stage import *
from scenes1 import _D, _BINS, _PK, blink_at

_LOGMAX = max(_D["hist"]["log"]["counts"])
_MU = _D["trimmed"]["mu"]
_SG = _D["trimmed"]["sigma"]

# 一局的五个阶段（示意，不是真实测量值）
_STEPS = [("看", "看清整个面", 3.1, SKY_D),
          ("判", "判断下一步", 2.4, LILAC_D),
          ("找", "找到要转的块", 6.8, MINT_D),
          ("转", "实际动手转", 14.2, BUTTER_D),
          ("收", "停手、确认", 1.9, CORAL)]


# ================= 场景 5：为什么会有长尾 =================
def s_why(ctx, t, d):
    title_block(ctx, "04 / 原因", "一局是乘出来的", "不是加出来的", seg(t, 0.1, 0.9),
                size=56, c2=LILAC_D)
    foot(ctx, "示意：每一步的耗时 = 平均耗时 × 一个随机系数，整局是这五步相乘",
         x=M, y=H - 62, align="left", a=0.55)

    a0 = seg(t, 0.45, 1.25)
    if a0 > 0:
        draw_text(ctx, "普通一局 40 秒。拆成五步，每步都快两成，或者都慢两成。",
                  M, 376, 30, INK, alpha=a0)

    x0, x1, yax = 300.0, 1480.0, 660.0
    vmax = 110.0

    def X(v):
        return x0 + (x1 - x0) * v / vmax

    # ---- 时间轴 ----
    ax_a = seg(t, 0.8, 1.7)
    if ax_a > 0:
        ctx.new_path(); ctx.set_line_width(4.5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*INK, 0.85 * ax_a)
        ctx.move_to(x0, yax)
        ctx.line_to(x0 + (x1 - x0) * ease_out(ax_a), yax)
        ctx.stroke()

    # ---- 三个落点 ----
    pts = [(40.0, "40 秒", "不快不慢", INK, 1.7),
           (13.1, "13 秒", "都快两成", MINT_D, 2.5),
           (99.5, "100 秒", "都慢两成", CORAL, 3.3)]
    for v, big, small, col, t0 in pts:
        a = seg(t, t0, t0 + 0.6)
        if a <= 0: continue
        xx = X(v)
        yy = yax - 110 * (1 - ease_out_back(a))
        r = 13 * ease_out(min(1.0, a * 1.6), 2.0)
        if r > 0.6:
            ctx.new_path(); ctx.arc(xx, yy, r, 0, 2 * math.pi)
            ctx.set_source_rgba(*col, a); ctx.fill_preserve()
            ctx.set_line_width(3.0); ctx.set_source_rgba(*INK, 0.75 * a); ctx.stroke()
        draw_text(ctx, big, xx, yax + 62, 38, col, align="center", alpha=a)
        draw_text(ctx, small, xx, yax + 102, 21, INK_SOFT, align="center",
                  bold=False, alpha=a)

    # ---- 同样两成，差出来的长度差一倍 ----
    yb = yax - 56
    b1 = seg(t, 3.9, 4.6)
    if b1 > 0:
        ctx.new_path(); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*MINT_D, 0.72 * b1)
        ctx.move_to(X(13.1), yb)
        ctx.line_to(lerp(X(13.1), X(40.0) - 10, ease_out(b1)), yb)
        ctx.stroke()
        draw_text(ctx, "−27 秒", (X(13.1) + X(40.0) - 10) / 2, yb - 24, 26, MINT_D,
                  align="center", alpha=b1)
    b2 = seg(t, 4.3, 5.1)
    if b2 > 0:
        ctx.new_path(); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*CORAL, 0.72 * b2)
        ctx.move_to(X(40.0) + 10, yb)
        ctx.line_to(lerp(X(40.0) + 10, X(99.5), ease_out(b2)), yb)
        ctx.stroke()
        draw_text(ctx, "+60 秒", (X(40.0) + 10 + X(99.5)) / 2, yb - 24, 26, CORAL,
                  align="center", alpha=b2)

    # ---- 两头：快的到底了，慢的没有底 ----
    wa = seg(t, 4.9, 5.6)
    if wa > 0:
        ctx.new_path(); ctx.set_line_width(9.0); ctx.set_line_cap(cairo.LINE_CAP_BUTT)
        ctx.set_source_rgba(*INK, 0.78 * wa)
        ctx.move_to(x0, yax - 58); ctx.line_to(x0, yax + 58); ctx.stroke()
        draw_text(ctx, "0 秒", x0 - 20, yax + 12, 24, INK, align="right", alpha=wa)
        rough_arrow(ctx, x1 - 8, yax, x1 + 62, yax, 4.0, CORAL, 18, 0, 6, alpha=wa)
        draw_text(ctx, "没有上限", x1 + 58, yax - 12, 24, CORAL, align="right", alpha=wa)

    # ---- 结论 ----
    rows = [("每一步偏一点，整局就被放大一点", INK),
            ("快的这头有底：一局不可能小于 0 秒", MINT_D),
            ("慢的那头没有底，所以尾巴只往右长", CORAL)]
    for i, (s, col) in enumerate(rows):
        aa = seg(t, 5.6 + i * 0.22, 6.3 + i * 0.22)
        if aa <= 0: continue
        y = 832 + i * 52
        ctx.new_path(); ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*col, 0.80 * aa)
        ctx.move_to(M, y - 11); ctx.line_to(M + 28, y - 11); ctx.stroke()
        draw_text(ctx, s, M + 44, y, 27, col, alpha=aa)

    # 小方：被"乘"的那一下
    ka = seg(t, 3.4, 4.2)
    if ka > 0:
        sc = 1.0 + 0.10 * math.sin(t * 3.0)
        draw_cube(ctx, 1700, 520, 66 * ease_out_back(ka) * sc, t,
                  rot=math.sin(t * 1.8) * 0.08, expr="shock" if t > 4.6 else "normal",
                  look=(-0.9, 0.2), arms=(2.1, 0.45, 2.3, 0.40))

    # 老芭：右下讲解
    s = stand_s(330)
    laoba_at(ctx, 1660, 1046, s, t, expr="think" if t < 4.6 else "normal",
             look=(-0.9, -0.3), pose=((0.55, 0.60), (0.55, 0.20)),
             blink=blink_at(t + 1.1), bob=math.sin(t * 2.1) * 2.2)


# ================= 场景 6：多阶段假设 =================
def s_model(ctx, t, d):
    title_block(ctx, "05 / 假设", "把它写成一道乘法", "每步乘一个系数", seg(t, 0.1, 0.9),
                size=56, c2=SKY_D)
    foot(ctx, "每一步的实际耗时 = 平均耗时 × 一个随机系数（大多接近 1）",
         x=M, y=H - 62, align="left", a=0.55)

    # 五个系数芯片
    coef = [1.06, 0.94, 1.22, 0.88, 1.11]
    x0, y0 = M, 400
    for i, (ch, lab, v, col) in enumerate(_STEPS):
        a = seg(t, 0.8 + i * 0.30, 1.35 + i * 0.30)
        if a <= 0: continue
        sc = ease_out_back(a)
        x = x0 + i * 180
        if sc > 1e-3:
            ctx.save(); zoom(ctx, x + 75, y0 + 70, sc)
            card(ctx, x, y0, 150, 140, 1.0, mix(WHITE, col, 0.16), seed=740 + i)
            draw_text(ctx, ch, x + 75, y0 + 62, 44, INK, align="center")
            draw_text(ctx, lab, x + 75, y0 + 104, 18, INK_SOFT, align="center", bold=False)
            ctx.restore()
        ca = seg(t, 1.1 + i * 0.30, 1.7 + i * 0.30)
        draw_text(ctx, f"×{coef[i]:.2f}", x + 75, y0 + 186, 30,
                  SKY_D if coef[i] > 1 else MINT_D, align="center", alpha=ca)
        if i < 4:
            draw_text(ctx, "×", x + 165, y0 + 88, 26, INK_SOFT, align="center",
                      bold=False, alpha=ca * 0.8)

    # 结果
    ra = seg(t, 3.2, 4.1)
    if ra > 0:
        prod = 1.0
        for c in coef:
            prod *= c
        ribbon(ctx, f"成绩 = 平均 × 平均 × … × {prod:.2f}", 1080, 690, 32, INK, BUTTER, ra, pad=24)

    # 两种结果的对比：系数都接近 1 / 有一个偏大
    ba = seg(t, 4.8, 5.6)
    if ba > 0:
        draw_text(ctx, "大部分时候", M, 812, 24, INK_SOFT, bold=False, alpha=ba)
        draw_text(ctx, "系数在 1 附近打转 → 成绩在 40 秒上下轻轻晃", M, 850, 27, MINT_D,
                  alpha=ba)
        ba2 = seg(t, 6.4, 7.2)
        draw_text(ctx, "偶尔", M, 906, 24, INK_SOFT, bold=False, alpha=ba2)
        draw_text(ctx, "两三个系数同时偏大 → 一局就被推到几分钟", M, 944, 27, CORAL,
                  alpha=ba2)

    # 右偏提示
    ha = seg(t, 8.2, 9.2)
    if ha > 0:
        x, y, w, h = 1100, 400, 560, 210
        card(ctx, x, y, w, h, ha, PAPER2, seed=760)
        draw_text(ctx, "乘积的结果不是对称的", x + 26, y + 50, 25, INK, alpha=ha)
        draw_text(ctx, "多数挤在左边（快），少数被拉到很右边（慢）", x + 26, y + 92, 21,
                  INK_SOFT, bold=False, alpha=ha)
        # 右偏小曲线
        cx0, cy0 = x + 34, y + 186
        ctx.new_path()
        for i in range(101):
            u = i / 100.0
            px = cx0 + (w - 80) * u
            py = cy0 - 86 * math.exp(-0.5 * ((u - 0.16) / 0.13) ** 2) * ease_out(ha)
            if i == 0: ctx.move_to(px, py)
            else: ctx.line_to(px, py)
        ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*CORAL, 0.86 * ha); ctx.stroke()
        ctx.new_path(); ctx.set_line_width(3); ctx.set_source_rgba(*INK, 0.35 * ha)
        ctx.move_to(cx0, cy0); ctx.line_to(cx0 + (w - 80), cy0); ctx.stroke()

    # 老芭
    s = stand_s(350)
    laoba_at(ctx, 1680, 1046, s, t, expr="smug" if t > 8.2 else "normal",
             look=(-0.85, -0.35), pose=((0.42, 0.45), (1.30, 0.55)),
             blink=blink_at(t + 0.5), bob=math.sin(t * 2.3) * 2.4)

    # 小方
    ka = seg(t, 6.4, 7.2)
    if ka > 0:
        draw_cube(ctx, 1700, 250, 56 * ease_out_back(ka), t, rot=-0.10,
                  expr="happy", look=(-0.6, 0.4), arms=(2.0, 0.35, 2.2, 0.30))


# ================= 场景 7：取对数 =================
def s_log(ctx, t, d):
    title_block(ctx, "06 / 变形", "乘法算不动", "那就取对数", seg(t, 0.1, 0.9),
                size=58, c2=MINT_D)
    foot(ctx, "对数的唯一作用：把乘法换成加法，别的什么都没变",
         x=M, y=H - 62, align="left", a=0.55)

    # 上：乘法式
    a0 = seg(t, 0.5, 1.4)
    if a0 > 0:
        draw_text(ctx, "1.06 × 0.94 × 1.22 × 0.88 × 1.11", M, 372, 44, INK, alpha=a0)

    # 中间：一根向下的箭头，右边写清楚这一步在干什么
    a1 = seg(t, 1.6, 2.4)
    if a1 > 0:
        mx = M + 470
        rough_arrow(ctx, mx, 404, mx, 502, 4.0, MINT_D, 16, 0, 6, alpha=a1)
        draw_text(ctx, "取对数", mx + 26, 442, 30, MINT_D, alpha=a1)
        draw_text(ctx, "乘法 → 加法", mx + 26, 486, 27, INK_SOFT, bold=False, alpha=a1)

    # 下：加法式
    a2 = seg(t, 2.6, 3.5)
    if a2 > 0:
        draw_text(ctx, "ln1.06 + ln0.94 + ln1.22 + ln0.88 + ln1.11", M, 560, 44, MINT_D,
                  alpha=a2)
        draw_text(ctx, "五条小加法：正负都有，大小都差不多", M, 618, 27, INK_SOFT,
                  bold=False, alpha=seg(t, 3.2, 4.0))

    # 右侧：为什么这样有用
    a3 = seg(t, 4.0, 4.9)
    if a3 > 0:
        x, y, w = 1120, 300, 660
        card(ctx, x, y, w, 360, a3, PAPER2, seed=780)
        draw_text(ctx, "为什么要绕这一下？", x + 28, y + 56, 27, INK, alpha=a3)
        rows = [("乘法不好描述「中间多、两头少」", INK_SOFT),
                ("加法可以", INK),
                ("加法还有一条现成的规律", MINT_D),
                ("——下一场就来用它", CORAL)]
        for i, (s, col) in enumerate(rows):
            draw_text(ctx, s, x + 28, y + 116 + i * 52, 24, col,
                      bold=(i >= 2), alpha=seg(t, 4.1 + i * 0.20, 4.8 + i * 0.20))

    # 小方：站在空着的中间
    ka = seg(t, 2.0, 2.8)
    if ka > 0:
        draw_cube(ctx, 1240, 800 + math.sin(t * 2.2) * 8, 62 * ease_out_back(ka), t,
                  rot=0.06, expr="happy", look=(-0.9, -0.2), arms=(1.9, 0.40, 2.1, 0.35))

    # 老芭
    s = stand_s(330)
    laoba_at(ctx, 1660, 1046, s, t, expr="happy" if t > 4.2 else "normal",
             look=(-0.8, -0.4), pose=((0.35, 0.20), (1.55, 0.50)),
             blink=blink_at(t + 1.7), bob=math.sin(t * 2.4) * 2.2)


# ================= 场景 8：大数定律 =================
def s_law(ctx, t, d):
    title_block(ctx, "07 / 规律", "很多小项相加", "就会变成一口钟", seg(t, 0.1, 0.9),
                size=58, c2=SKY_D)
    foot(ctx, "掷骰子、量身高、扔球：只要是小项相加，都在往钟形靠",
         x=M, y=H - 62, align="left", a=0.55)

    # 三张直方图：1 项 / 3 项 / 8 项
    panels = [(1, "一个", SKY_D), (3, "三个", MINT_D), (8, "八个", LILAC_D)]
    for p, (n_dice, lab, col) in enumerate(panels):
        pa = seg(t, 0.8 + p * 1.4, 1.7 + p * 1.4)
        if pa <= 0: continue
        x = M + p * 420
        y, w, h = 372, 370, 250
        card(ctx, x, y, w, h + 90, pa, PAPER2, seed=800 + p)
        draw_text(ctx, f"{lab}骰子相加" if n_dice > 1 else "一个骰子",
                  x + 24, y + 44, 24, INK_SOFT, bold=False, alpha=pa)

        # 生成 n 个均匀整数的和的分布
        dist = [1.0]
        for _ in range(n_dice):
            nd = [0.0] * (len(dist) + 5)
            for i, v in enumerate(dist):
                for k in range(6):
                    nd[i + k] += v
            dist = nd
        mx = max(dist)
        n = len(dist)
        for i, v in enumerate(dist):
            ba = seg(t, 1.1 + p * 1.4 + i * 0.008, 1.6 + p * 1.4 + i * 0.008)
            if ba <= 0: continue
            bw = (w - 48) / n
            bh = (h - 30) * (v / mx) * ease_out(ba, 2.4)
            rrect(ctx, x + 24 + i * bw + 0.6, y + h + 70 - bh, max(1.6, bw - 1.4), bh, 3,
                  col, INK, 1.6, seed=810 + p * 50 + i, amp=0.35, hatch=False)
        # 钟形参考线
        ca = seg(t, 2.2 + p * 1.4, 3.0 + p * 1.4)
        if ca > 0:
            ctx.new_path()
            for i in range(81):
                u = i / 80.0
                px = x + 24 + (w - 48) * u
                py = (y + h + 70) - (h - 30) * math.exp(-0.5 * ((u - 0.5) / 0.19) ** 2) * ease_out(ca)
                if i == 0: ctx.move_to(px, py)
                else: ctx.line_to(px, py)
            ctx.set_line_width(4); ctx.set_dash([9, 7])
            ctx.set_source_rgba(*INK, 0.55 * ca); ctx.stroke()
            ctx.set_dash([])

    # 结论
    ca = seg(t, 5.2, 6.1)
    if ca > 0:
        ribbon(ctx, "项数越多，越接近一条钟形曲线", 1000, 884, 31, INK, BUTTER, ca, pad=22)

    # 落回本题
    ca2 = seg(t, 6.3, 7.2)
    if ca2 > 0:
        draw_text(ctx, "把「小项」换成 ln(每步的系数)", M, 806, 27, INK, alpha=ca2)
        draw_text(ctx, "→ ln(成绩) 就该是一条正态曲线", M, 856, 32, CORAL, alpha=seg(t, 6.8, 7.7))

    # 老芭
    s = stand_s(320)
    laoba_at(ctx, 1660, 1046, s, t, expr="normal", look=(-0.85, -0.35),
             pose=((0.50, 0.55), (0.85, 0.25)), blink=blink_at(t + 0.9),
             bob=math.sin(t * 2.2) * 2.2)

    # 小方
    ka = seg(t, 0.5, 1.3)
    if ka > 0:
        draw_cube(ctx, 1700, 300, 56 * ease_out_back(ka), t, rot=0.08,
                  expr="happy", look=(-0.5, 0.36), arms=(1.9, 0.4, 2.1, 0.35))
