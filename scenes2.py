# -*- coding: utf-8 -*-
"""场景 08、10：对照验证、幕间

（取对数 / 机制 / 假设 / 大数定律 已移到 scenes5.py，顺序见 timeline.ORDER）
"""
import math
from art import *
from stage import *
from scenes1 import _D, _BINS, _PK, blink_at

_LOGMAX = max(_D["hist"]["log"]["counts"])
_MU = _D["trimmed"]["mu"]
_SG = _D["trimmed"]["sigma"]
_N = _D["raw"]["linear"]["n"]
_LEDG = _D["hist"]["log"]["edges"]
_LNMIN, _LNMAX = math.log(1.0), math.log(300.0)
_BW = (_LNMAX - _LNMIN) / (len(_LEDG) - 1)


def _fit(lnv):
    z = (lnv - _MU) / _SG
    return _N * _BW * math.exp(-0.5 * z * z) / (_SG * math.sqrt(2 * math.pi))


# ================= 场景 08：对照 =================
_QU = _D["quantiles"]
_QK = ["0.01", "0.05", "0.25", "0.5", "0.75", "0.9", "0.95", "0.99"]
_QLAB = ["1%", "5%", "25%", "中位", "75%", "90%", "95%", "99%"]


def s_fit(ctx, t, d):
    draw_text(ctx, "08 / 对照", M, 118, 25, INK_SOFT, bold=True, alpha=seg(t, 0.1, 0.8) * 0.9)
    draw_text(ctx, "预测 vs 实测", M, 196, 58, INK, alpha=seg(t, 0.15, 0.95))
    draw_text(ctx, "一个点一个点对得上", M, 264, 42, MINT_D, alpha=seg(t, 0.55, 1.35))
    foot(ctx, "单位：秒 · 预测曲线只用两个数：ln(成绩) 的平均值和波动幅度", a=0.55)

    # 表头
    tx, tw = 620, 1080
    hd = seg(t, 0.9, 1.5)
    draw_text(ctx, "分位", tx + 8, 356, 26, INK_SOFT, bold=False, alpha=hd)
    draw_text(ctx, "实测", tx + 250, 356, 26, INK_SOFT, bold=False, alpha=hd)
    draw_text(ctx, "预测", tx + 500, 356, 26, INK_SOFT, bold=False, alpha=hd)
    draw_text(ctx, "差", tx + 800, 356, 26, INK_SOFT, bold=False, alpha=hd)
    ctx.set_line_width(3); ctx.set_source_rgba(*INK, 0.35 * hd)
    ctx.move_to(tx, 374); ctx.line_to(tx + tw - 60, 374); ctx.stroke()

    for i, (k, lab) in enumerate(zip(_QK, _QLAB)):
        a = seg(t, 1.3 + i * 0.24, 1.9 + i * 0.24)
        if a <= 0: continue
        y = 422 + i * 58
        e = _QU["emp"][k]
        ln = _QU["lognormal"][k]
        col = MINT_D if abs(e - ln) < 2.2 else CORAL
        if i % 2 == 0:
            ctx.new_path(); ctx.rectangle(tx - 12, y - 34, tw - 30, 58)
            ctx.set_source_rgba(*INK, 0.035 * a); ctx.fill()
        draw_text(ctx, lab, tx + 8, y, 30, INK, alpha=a)
        draw_text(ctx, f"{e:.1f}", tx + 250, y, 32, INK, alpha=a)
        draw_text(ctx, f"{ln:.1f}", tx + 500, y, 32, INK, alpha=a)
        draw_text(ctx, f"{e - ln:+.1f}", tx + 800, y, 32, col, alpha=a)
        # 小条形
        bx = tx + 900
        wmax = 130
        ctx.new_path()
        ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*MINT, 0.55 * a)
        ctx.move_to(bx, y - 10); ctx.line_to(bx + wmax * clamp(e / 150.0), y - 10); ctx.stroke()
        ctx.new_path()
        ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*CORAL, 0.55 * a)
        ctx.move_to(bx, y - 10); ctx.line_to(bx + wmax * clamp(ln / 150.0), y - 10); ctx.stroke()

    # 结论
    ribbon(ctx, "预测不是拟合出来的，是先算出来再去对", 1180, 872, 32, INK, BUTTER,
           seg(t, 4.0, 4.8), pad=22)

    # 老芭在左，讲解
    s = stand_s(650)
    laoba_at(ctx, 322, 1036, s, t, expr="smug" if t > 4.4 else "normal",
             look=(0.55, -0.25), pose=((0.62, 0.55), (0.30, 0.12)),
             blink=blink_at(t + 1.3), bob=math.sin(t * 2.0) * 2.6)


# ================= 场景 10：幕间 =================
def s_interlude(ctx, t, d):
    a = seg(t, 0.15, 0.9)
    c = ease_out_back(a)
    if c > 1e-3:
        ctx.save(); zoom(ctx, 1090, 400, c)
        draw_text(ctx, "所以这口钟", 1090, 360, 62, INK, align="center")
        draw_text(ctx, "长在对数轴上", 1090, 470, 82, CORAL, align="center")
        ctx.restore()
    draw_text(ctx, "成绩本身右偏，ln(成绩) 才是一条钟形曲线", 1090, 570, 30, INK_SOFT,
              align="center", bold=False, alpha=seg(t, 1.2, 2.1))
    draw_text(ctx, "这叫「对数正态」", 1090, 630, 34, MINT_D, align="center",
              alpha=seg(t, 2.2, 3.1))

    # 老芭大幅挥手
    s = stand_s(700)
    wave = math.sin(t * 7.0)
    laoba_at(ctx, 470, 1044, s, t, expr="happy", look=(0.45, -0.15),
             pose=((0.30, 0.12), (2.05 + 0.28 * wave, 0.50 + 0.20 * wave)),
             blink=blink_at(t + 0.2), bob=math.sin(t * 2.6) * 4.0)

    # 小方在右侧蹦
    ka = seg(t, 0.6, 1.4)
    if ka > 0:
        hop = abs(math.sin((t - 0.6) * 3.4)) * 56
        draw_cube(ctx, 1560, 800 - hop, 92 * ease_out_back(ka), t,
                  rot=math.sin(t * 2.4) * 0.12, expr="happy", look=(-0.4, -0.2),
                  arms=(2.0 + 0.4 * math.sin(t * 6), 0.3, 2.0 + 0.4 * math.sin(t * 6 + 1.5), 0.3))

    # 星点
    for i in range(6):
        ph = t * 2.2 + i * 1.7
        x = 880 + (i % 3) * 190 + math.sin(ph) * 20
        y = 240 + (i // 3) * 620 + math.cos(ph) * 16
        sparkle(ctx, x, y, 15 + 4 * math.sin(ph), CREAM, rot=ph, width=4.4,
                alpha=seg(t, 0.8 + i * 0.15, 1.4 + i * 0.15) * 0.9)
