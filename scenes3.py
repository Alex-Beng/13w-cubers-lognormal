# -*- coding: utf-8 -*-
"""场景 9-12：玩家画像、分段排名、结论、片尾"""
import math
from art import *
from stage import *
from scenes1 import _D, blink_at

_O = _D["other"]
_N = _D["raw"]["linear"]["n"]


# ================= 场景 9：玩家画像 =================
def s_profile(ctx, t, d):
    title_block(ctx, "09 / 画像", "这群人到底是谁？", "三条硬数字", seg(t, 0.1, 0.9),
                size=58, c2=MINT_D)
    foot(ctx, "TPS = 每秒转动数；PB = 个人最佳；轮数 = 一次还原的转动次数", a=0.55)

    stats = [
        ("平均 PB", f"{_O['pb_mean']:.1f}", "秒", 1.0, CORAL),
        ("平均 TPS", f"{_O['tps_mean']:.2f}", "转 / 秒", 1.7, SKY_D),
        ("平均步数", f"{_O['turn_mean']:.0f}", "转", 2.4, LILAC_D),
    ]
    for i, (lab, val, unit, t0, col) in enumerate(stats):
        a = seg(t, t0, t0 + 0.7)
        if a <= 0: continue
        x = M + i * 522
        y = 408
        card(ctx, x, y, 470, 214, a, PAPER2, seed=90 + i)
        draw_text(ctx, lab, x + 34, y + 52, 26, INK_SOFT, bold=False, alpha=a)
        k = ease_out(seg(t, t0 + 0.1, t0 + 0.95), 2.5)
        sn = f"{float(val) * k:.1f}" if i == 0 else (f"{float(val) * k:.2f}" if i == 1 else f"{float(val) * k:.0f}")
        draw_text(ctx, sn, x + 32, y + 150, 82, col, alpha=a)
        draw_text(ctx, unit, x + 40 + text_width(ctx, sn, 82), y + 144, 27, INK_SOFT,
                  bold=False, alpha=a)

    # TPS 分布条
    ba = seg(t, 3.4, 4.3)
    if ba > 0:
        draw_text(ctx, "手速分布（TPS）", M, 726, 30, INK, alpha=ba)
        bx, by, bw = M + 6, 800, 1120
        ctx.new_path(); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*INK, 0.09 * ba)
        ctx.move_to(bx, by); ctx.line_to(bx + bw, by); ctx.stroke()
        ctx.new_path(); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*MINT, 0.80 * ba)
        ctx.move_to(bx, by); ctx.line_to(bx + bw * 0.62 * ease_out(ba), by); ctx.stroke()
        # 中位标记
        mx = bx + bw * 0.62
        ctx.new_path(); ctx.set_line_width(4); ctx.set_source_rgba(*INK, 0.85 * ba)
        ctx.move_to(mx, by - 30); ctx.line_to(mx, by + 30); ctx.stroke()
        draw_text(ctx, "中位 3.1", mx, by - 44, 24, MINT_D, align="center", bold=True, alpha=ba)
        for v, lab in ((0.0, "0"), (0.31, "1.5"), (0.62, "3.1"), (1.0, "5.0")):
            draw_text(ctx, lab, bx + bw * v, by + 52, 21, INK_SOFT, align="center",
                      bold=False, alpha=ba)
        draw_text(ctx, "转 / 秒", bx + bw + 16, by + 8, 22, INK_SOFT, bold=False, alpha=ba)


# ================= 场景 10：你在哪一段 =================
_BANDS = [b for b in _D["bands"] if b["n"] > 0]
_BTOT = sum(b["n"] for b in _BANDS)


def s_rank(ctx, t, d):
    title_block(ctx, "10 / 位置", "你在哪一段？", "成绩的阶梯", seg(t, 0.1, 0.9),
                size=58, c2=CORAL)
    foot(ctx, "按 130,104 条成绩分段统计，右侧为该段占全样本比例", a=0.55)

    # 阶梯条：标签固定左栏，条形按占比，百分比固定右栏
    lx, x0, x1, px = 246, 282, 1000, 1130
    y0 = 316
    hh = 44
    gap = 8
    show = [b for b in _BANDS if b["n"] / _BTOT > 0.0004]
    for i, b in enumerate(show):
        a = seg(t, 0.7 + i * 0.10, 1.2 + i * 0.10)
        if a <= 0: continue
        frac = b["n"] / _BTOT
        w = (x1 - x0) * frac * ease_out(a, 2.6)
        y = y0 + i * (hh + gap)
        col = mix(MINT, CORAL, clamp(i / max(1, len(show) - 1.0)))
        lab = f"{b['lo']:g}–{b['hi']:g}s"
        draw_text(ctx, lab, lx, y + 28, 22, INK, align="right", alpha=a)
        rrect(ctx, x0, y, max(11.0, w), hh, 9, col, INK, 2.8, seed=120 + i, amp=0.5)
        draw_text(ctx, f"{frac * 100:.1f}%", px, y + 28, 22, INK_SOFT, bold=False,
                  align="right", alpha=a)

    # 关键读数
    ra = seg(t, 2.9, 3.8)
    if ra > 0:
        for i, (a1, a2, col, y) in enumerate((
                ("一半人", "40 秒内", CORAL, 380),
                ("最好的一成", "20 秒内", MINT_D, 570),
                ("最慢的一成", "60 秒以上", LILAC_D, 760))):
            aa = seg(t, 2.9 + i * 0.28, 3.5 + i * 0.28)
            draw_text(ctx, a1, 1430, y, 28, INK_SOFT, bold=False, alpha=aa)
            draw_text(ctx, a2, 1430, y + 62, 54, col, alpha=aa)

    # 小方
    ka = seg(t, 1.0, 1.8)
    if ka > 0:
        draw_cube(ctx, 1700, 268 + math.sin(t * 2.2) * 8, 62 * ease_out_back(ka), t,
                  rot=0.06, expr="normal", look=(-1.0, 0.6), arms=(1.4, 0.4, 1.4, 0.4))


# ================= 场景 11：结论 =================
def s_answer(ctx, t, d):
    # 大结论
    a = [seg(t, 0.2, 0.9), seg(t, 0.9, 1.6), seg(t, 1.6, 2.3), seg(t, 2.3, 3.0)]
    c = ease_out_back(a[0])
    if c > 1e-3:
        ctx.save(); zoom(ctx, M, 0, c)
        draw_text(ctx, "所以答案是", M, 268, 44, INK_SOFT)
        ctx.restore()

    c = ease_out_back(a[1])
    if c > 1e-3:
        ctx.save(); zoom(ctx, M, 0, c)
        draw_text(ctx, "对数正态", M - 4, 400, 118, CORAL)
        ctx.restore()
    draw_text(ctx, "Lognormal", M + 4, 470, 40, INK_SOFT, bold=False, alpha=a[1])

    # 三条理由
    reasons = [("一局成绩 = 五个小阶段相乘", 1.9, INK),
               ("取对数 → 乘法变加法", 2.4, INK),
               ("很多小项相加 → 中间高、两头低的钟形", 2.9, INK_SOFT)]
    for i, (s, t0, col) in enumerate(reasons):
        aa = seg(t, t0, t0 + 0.7)
        if aa <= 0: continue
        y = 590 + i * 86
        ctx.new_path(); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*CORAL, 0.85 * aa)
        ctx.move_to(M, y - 12); ctx.line_to(M + 34, y - 12); ctx.stroke()
        draw_text(ctx, s, M + 56, y, 32, col, alpha=aa)

    # 右侧：钟形 + 提示
    ma = seg(t, 1.2, 2.4)
    if ma > 0:
        cx, cy, hw = 1288, 452, 168
        ctx.save()
        ctx.set_line_width(5); ctx.set_source_rgba(*INK, 0.25 * ma)
        ctx.move_to(cx - hw, cy + 118); ctx.line_to(cx + hw, cy + 118); ctx.stroke()
        ctx.new_path()
        for i in range(121):
            u = i / 120.0
            x = cx - hw + 2 * hw * u
            y = cy + 118 - 236 * math.exp(-0.5 * ((u - 0.42) / 0.17) ** 2) * ease_out(ma)
            if i == 0: ctx.move_to(x, y)
            else: ctx.line_to(x, y)
        ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*MINT_D, 0.9 * ma); ctx.stroke()
        draw_text(ctx, "ln(成绩)", cx, cy + 170, 24, INK_SOFT, align="center",
                  bold=False, alpha=ma)
        ctx.restore()

    # 右侧曲线的注释：钟的顶点落在中位数上
    na = seg(t, 3.2, 4.0)
    if na > 0:
        draw_text(ctx, "钟的顶点 = 中位数附近", 1288, 246, 25, INK_SOFT, align="center",
                  bold=False, alpha=na)
        rough_arrow(ctx, 1288, 268, 1288, 326, 3.0, INK_SOFT, 12, 0, 4, alpha=na * 0.8)

    # 老芭
    s = stand_s(560)
    laoba_at(ctx, 1684, 1040, s, t, expr="happy", look=(-0.7, -0.3),
             pose=((0.24, 0.10), (1.95, 0.45)),
             blink=blink_at(t + 0.4), bob=math.sin(t * 2.4) * 3.0)


# ================= 场景 12：片尾 =================
def s_outro(ctx, t, d):
    a = seg(t, 0.2, 1.1)
    c = ease_out_back(a)
    if c > 1e-3:
        ctx.save(); zoom(ctx, W / 2, 0, c)
        draw_text(ctx, "CubeStation 数据小剧场", W / 2, 210, 66, INK, align="center")
        ctx.restore()
    draw_text(ctx, "数据：130,104 条真实 SUB 成绩 · 画面与配乐全部由代码生成",
              W / 2, 316, 30, INK_SOFT, align="center", bold=False, alpha=seg(t, 1.5, 2.4))

    # 老芭
    s = stand_s(580)
    laoba_at(ctx, 760, 1040, s, t, expr="happy", look=(0.35, -0.25),
             pose=((0.28, 0.10), (2.10 + 0.22 * math.sin(t * 6.2), 0.48)),
             blink=blink_at(t), bob=math.sin(t * 2.5) * 3.2)
    # 小方
    ka = seg(t, 0.4, 1.2)
    if ka > 0:
        hop = abs(math.sin((t - 0.4) * 3.2)) * 34
        draw_cube(ctx, 1170, 890 - hop, 80 * ease_out_back(ka), t,
                  rot=math.sin(t * 2.0) * 0.09, expr="happy", look=(0.2, -0.2),
                  arms=(1.9 + 0.35 * math.sin(t * 5), 0.4, 1.9 + 0.35 * math.sin(t * 5 + 1.6), 0.4))

    # 淡出：最后 1.1s 收纸（跟随场景时长）
    fade = seg(t, max(0.0, d - 1.1), d - 0.02)
    if fade > 0:
        ctx.new_path(); ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(*PAPER, fade); ctx.fill()
