# -*- coding: utf-8 -*-
"""场景 03：长尾没有上限，但成绩有明显上限

只讲一件笼统的事：
  · 慢的那一头可以无限长——一局可以拖到天荒地老
  · 快的那一头，人类明显有个上限
  · 从软件数据看，最快是 1.96 秒
不做预测、不推理论地板、不列一堆换算数字。
"""
import math
from art import *
from stage import *
from scenes1 import _D, blink_at

# ---------- 数据 ----------
_N = _D["raw"]["linear"]["n"]                  # 130,104
_REC = _D["raw"]["linear"]["min"]              # 1.963
_MINV = 1.0                                    # 图上刻度下沿
_MAXV = 60.0                                   # 图上刻度上沿
_BINS = list(zip(_D["hist"]["lin"]["counts"], _D["hist"]["lin"]["edges"][:-1]))

# ---------- 画布 ----------
CX0, CX1 = 214, 1086
CY0, CY1 = 352, 862


def _L(t):
    return math.log10(max(t, _MINV * 0.92) / _MINV) / math.log10(_MAXV / _MINV)


def Y(t):
    return CY0 + (CY1 - CY0) * _L(t)


def _hatch(ctx, x, y, w, h, col=INK, a=0.10, gap=13):
    n = int((w + h) / gap) + 3
    ctx.save()
    ctx.rectangle(x, y, w, h); ctx.clip()
    ctx.set_line_width(1.8); ctx.set_source_rgba(*col, a)
    for k in range(-n, n + 1):
        px = x + k * gap
        ctx.move_to(px, y); ctx.line_to(px + h, y + h)
    ctx.stroke()
    ctx.restore()


def _chip(ctx, s, x, y, size=19, fill=PAPER, col=INK_SOFT, a=1.0, pad=7, align="center"):
    """带底色的标签：压在排线上也能读"""
    if a <= 0.004:
        return
    w = text_width(ctx, s, size, bold=False)
    h = size * 1.42
    bx = x - w / 2 if align == "center" else (x - w if align == "right" else x)
    rrect(ctx, bx - pad, y - size * 1.0, w + 2 * pad, h, 7, fill, fill, 0, seed=5, amp=0.5)
    draw_text(ctx, s, x, y, size, col, bold=False, align=align, alpha=a)


def s_tail(ctx, t, d):
    title_block(ctx, "03 / 两头", "慢的那头没有底", "快的那头有天花板", seg(t, 0.1, 0.9),
                size=58, c2=CORAL)
    foot(ctx, f"同一份数据 · 样本 {_N:,} 条 · 只问一件事：人到底能快到哪", a=0.55)

    ga = seg(t, 0.25, 0.85)

    # ---------- 纸上的“速度尺”：越往下越慢 ----------
    if ga > 0:
        # 记录以上的窄带：还没人进去过
        band = seg(t, 1.5, 2.2)
        if band > 0:
            _hatch(ctx, CX0, Y(1.0), CX1 - CX0, Y(_REC) - Y(1.0), INK, 0.075 * band)
            ctx.new_path()
            ctx.set_line_width(2.2); ctx.set_dash([5, 9])
            ctx.set_source_rgba(*CORAL, 0.60 * band)
            ctx.move_to(CX0, Y(_REC)); ctx.line_to(CX1, Y(_REC)); ctx.stroke()
            ctx.set_dash([])
            _chip(ctx, "人类明显有上限", CX0 + 14, Y(1.0) + 44, 21, PAPER, CORAL, band,
                  8, "left")

        # 轴
        ctx.set_line_width(3.4); ctx.set_source_rgba(*INK, 0.85 * ga)
        ctx.move_to(CX0 - 16, CY0); ctx.line_to(CX0 - 16, CY1); ctx.stroke()
        ctx.move_to(CX0 - 16, CY1 + 22); ctx.line_to(CX0 - 16, CY1 + 22); ctx.stroke()
        for v in (1, 2, 5, 10, 20, 40):
            y = Y(v)
            ctx.set_line_width(2.6); ctx.set_source_rgba(*INK, 0.55 * ga)
            ctx.move_to(CX0 - 16, y); ctx.line_to(CX0, y); ctx.stroke()
            draw_text(ctx, f"{v}s", CX0 - 34, y + 7, 20, INK_SOFT, align="right",
                      bold=False, alpha=ga)

        # 分布：每个 5s 桶一束铅笔痕，越长越常见，束内多笔叠出深浅
        ra = seg(t, 1.6, 2.6)
        if ra > 0:
            pk = max(c for c, _ in _BINS) or 1
            for i, (c, lo) in enumerate(_BINS):
                if c <= 0:
                    continue
                a = seg(t, 1.6 + i * 0.008, 1.95 + i * 0.008) * ra
                y0 = Y(lo + 0.15)
                y1 = Y(lo + 4.85)
                band = max(6.0, y1 - y0 - 2.0)
                span = (CX1 - CX0 - 170) * (c / pk) ** 0.55
                n_ln = 3 + int(3 * (c / pk) ** 0.5)
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                for j in range(n_ln):
                    u = (j + 0.5) / n_ln
                    yy = y0 + 1 + band * u
                    ctx.set_line_width(2.4)
                    ctx.move_to(CX0 + 4 + math.sin(i * 1.9 + j) * 2.5, yy)
                    ctx.line_to(CX0 + 4 + span * (0.96 + 0.04 * math.sin(i + j * 2.3)), yy)
                    ctx.set_source_rgba(*INK, (0.16 + 0.30 * (1 - abs(u - 0.5) * 2)) * a)
                    ctx.stroke()

        # 长尾这一侧：一条往下的箭头，没有终点
        la = seg(t, 2.6, 3.3)
        if la > 0:
            ax = CX1 - 66
            rough_arrow(ctx, ax, Y(30), ax, CY1 - 6, 3.4, INK_SOFT, 14, 0, 4,
                        alpha=la * 0.85)
            _chip(ctx, "可以一直更慢，没有底", ax - 18, Y(44), 21, PAPER, INK_SOFT, la,
                  8, "right")

        # 实测最快那一点
        ba = seg(t, 3.4, 4.1)
        if ba > 0:
            px = CX0 + 22
            py = Y(_REC)
            sc = ease_out_back(ba)
            ctx.new_path(); ctx.arc(px, py, 11 * sc, 0, 2 * math.pi)
            ctx.set_source_rgba(*CORAL, ba); ctx.fill()
            ctx.new_path(); ctx.arc(px, py, 5.2 * sc, 0, 2 * math.pi)
            ctx.set_source_rgba(*PAPER, ba); ctx.fill()
            _chip(ctx, f"最快 {_REC:.2f}s", px + 22, py - 2, 21, PAPER, CORAL, ba,
                  8, "left")

    # ---------- 右上：唯一要记住的数 ----------
    a1 = seg(t, 4.2, 5.0)
    if a1 > 0:
        x, y, w, h = 1176, 352, 620, 236
        card(ctx, x, y, w, h, a1, PAPER2, seed=88)
        draw_text(ctx, "软件数据里最快的单次", x + 28, y + 52, 25, INK_SOFT,
                  bold=False, alpha=a1)
        big = f"{_REC:.2f}"
        draw_text(ctx, big, x + 26, y + 158, 96, CORAL, alpha=a1)
        draw_text(ctx, "秒", x + 30 + text_width(ctx, big, 96) + 12, y + 146, 30, INK_SOFT,
                  bold=False, alpha=a1)
        draw_text(ctx, "十几万条里只有这一条", x + 30, y + 202, 21, INK_SOFT,
                  bold=False, alpha=seg(t, 4.5, 5.2) * 0.9)

    # ---------- 右下：两句人话 ----------
    b1 = seg(t, 5.2, 5.9)
    if b1 > 0:
        x, y, w = 1176, 618, 620
        card(ctx, x, y, w, 214, b1, PAPER2, seed=91)
        draw_text(ctx, "所以，上限是存在的", x + 26, y + 48, 25, INK, alpha=b1)
        rows = [("慢的一头：无底，只看你什么时候放弃。", INK_SOFT),
                ("快的一头：手速、步数、反应，都卡着。", INK_SOFT),
                ("不是外推出来的，是撞出来的。", CORAL)]
        for i, (s, col) in enumerate(rows):
            draw_text(ctx, s, x + 26, y + 96 + i * 40, 22, col, bold=(i == 2),
                      alpha=seg(t, 5.4 + i * 0.16, 6.1 + i * 0.16))

    # ---------- 结论 ----------
    ribbon(ctx, "成绩有天花板，只是没人知道在哪儿", 1500, 872, 24, INK, BUTTER,
           seg(t, 6.4, 7.2), pad=16)

    # ---------- 收尾：把“上限”两个字再钉一次 ----------
    ca = seg(t, 7.6, 8.3)
    if ca > 0:
        _chip(ctx, "再快，就不是人了", CX0 + 300, Y(1.0) + 86, 22, BUTTER, INK, ca, 10)

    # ---------- 老芭 ----------
    s = stand_s(244)
    laoba_at(ctx, 138, 1046, s, t, expr="think" if t < 4.2 else "normal",
             look=(0.85, -0.15), pose=((0.55, 0.70), (0.90, 0.30)),
             blink=blink_at(t + 1.4), bob=math.sin(t * 2.2) * 2.2)

    # ---------- 小方 ----------
    ka = seg(t, 5.8, 6.6)
    if ka > 0:
        draw_cube(ctx, 1836, 940 + math.sin(t * 2.6) * 6, 48 * ease_out_back(ka), t,
                  rot=-0.12, expr="shock" if t > 4.2 else "normal", look=(-0.9, 0.4),
                  arms=(2.4, 0.25, 2.6, 0.20))
