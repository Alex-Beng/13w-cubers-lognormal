# -*- coding: utf-8 -*-
"""全片时间轴：画面、配音、字幕与音乐共享同一份表

节奏：120 BPM，1 小节 = 2.0s，所有切点落在小节线上。
配音源：vo_<voice>.json（svtts.py 用本地 GPT-SoVITS 生成）
  - 每个场景的长度 = 起播偏移 + 该句时长 + 余量，向上取到 2s 整
  - 换音色重跑 svtts.py，这里会自动跟着变

用法：VOICE=hanabi（默认）/ VOICE=barbara
"""
import json, math, os

FPS = 30
BAR = 2.0

_HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", "hanabi")

# 场景顺序（与画面一一对应）
# 推理链：长什么样 → 长尾 → 两头（慢无止境 / 快有上限）
#        → 为什么会长尾 → 多阶段相乘假设 → 取对数 → 大数定律 → 钟形
#        → 对照验证 → 幕间 → 人 → 结论
ORDER = ["title", "data", "skew", "tail", "why", "model", "log", "law",
         "fit", "interlude", "profile", "rank", "answer", "outro"]

# 旁白：场景 -> (起播偏移, 句末余量)
LEAD = {
    "title": (0.70, 0.70), "data": (0.55, 0.65), "skew": (0.55, 0.70),
    "tail": (0.60, 0.85), "why": (0.55, 0.70), "model": (0.55, 0.85),
    "log": (0.55, 0.70), "law": (0.55, 0.80), "fit": (0.55, 0.75),
    "interlude": (0.45, 0.90),
    "profile": (0.55, 0.65), "rank": (0.50, 0.70), "answer": (0.50, 1.10),
    "outro": (0.70, 1.10),
}

_MISSING = {"dur": 6.0, "text": ""}     # 缺配音时的兜底


def _vo_table(voice):
    p = os.path.join(_HERE, f"vo_{voice}.json")
    if not os.path.exists(p):
        return {}
    return {o["id"]: o for o in json.load(open(p, encoding="utf-8"))["lines"]}


_VO = _vo_table(VOICE)


def _round_up(x):
    return max(BAR, round(math.ceil(x / BAR - 1e-9) * BAR, 6))


SCENES = []
_t = 0.0
for _name in ORDER:
    _v = _VO.get(_name, _MISSING)
    _lead, _tailp = LEAD.get(_name, (0.6, 0.6))
    _len = _round_up(_lead + float(_v["dur"]) + _tailp)
    SCENES.append((round(_t, 6), round(_t + _len, 6), _name))
    _t += _len

DUR = round(_t, 6)
CUTS = [s[0] for s in SCENES] + [DUR]

# ---------------- 音效关键点 ----------------
# 每个场景里放几拍，位置按场景长度等分；最后一个场景只放收尾两下
_BEATS = {
    "title":     [(0.13, "impact"), (0.42, "pop"), (0.78, "pop")],
    "data":      [(0.10, "whoosh"), (0.28, "pop"), (0.52, "pop"), (0.74, "pop"), (0.92, "pop")],
    "skew":      [(0.10, "impact"), (0.32, "boing"), (0.55, "pop"), (0.76, "pop"), (0.92, "pop")],
    "tail":      [(0.06, "impact"), (0.14, "pop"), (0.21, "pop"), (0.30, "pop"), (0.40, "boing"),
                  (0.55, "pop"), (0.68, "pop"), (0.80, "impact"), (0.92, "pop")],
    "why":       [(0.10, "impact"), (0.32, "pop"), (0.54, "pop"), (0.74, "pop"), (0.92, "boing")],
    "model":     [(0.06, "impact"), (0.16, "pop"), (0.26, "pop"), (0.36, "pop"), (0.46, "pop"),
                  (0.56, "pop"), (0.68, "boing"), (0.82, "impact")],
    "log":       [(0.12, "impact"), (0.34, "whoosh"), (0.56, "boing"), (0.78, "pop")],
    "law":       [(0.10, "impact"), (0.28, "pop"), (0.44, "pop"), (0.60, "pop"), (0.76, "pop"),
                  (0.90, "impact")],
    "fit":       [(0.12, "pop"), (0.32, "pop"), (0.52, "pop"), (0.72, "pop"), (0.90, "pop")],
    "interlude": [(0.18, "whoosh"), (0.55, "pop"), (0.82, "pop")],
    "profile":   [(0.10, "impact"), (0.30, "pop"), (0.52, "pop"), (0.74, "pop")],
    "rank":      [(0.10, "impact"), (0.28, "pop"), (0.48, "pop"), (0.68, "pop"), (0.86, "pop")],
    "answer":    [(0.12, "pop"), (0.40, "pop"), (0.66, "boing")],
    "outro":     [(0.26, "impact"), (0.62, "pop")],
}

HITS = []
for _a, _b, _n in SCENES:
    _L = _b - _a
    for _u, _k in _BEATS.get(_n, []):
        HITS.append((round(_a + _u * _L, 3), _k))
HITS = [(t, k) for t, k in HITS if t < DUR - 0.2]

RISERS = [(round(SCENES[-1][0] - 1.6, 3), 1.8), (round(DUR - 2.6, 3), 1.8)]


def scene_at(t):
    """返回 (场景名, 场景内时间, 场景时长)"""
    for a, b, name in SCENES:
        if a <= t < b:
            return name, t - a, b - a
    a, b, name = SCENES[-1]
    return name, t - a, b - a


# ---------------- 配音 / 字幕 ----------------
def _split(text):
    """按标点切成字幕片段；同时给换气留一个很短的间隙"""
    out, buf = [], ""
    for ch in text:
        buf += ch
        if ch in "，。？；：—、" and len(buf) >= 5:
            out.append(buf.rstrip("，。？；：、—"))
            buf = ""
    if buf.strip():
        out.append(buf.strip())
    return [s for s in out if s]


VO = {}
SUBS = []      # (start, end, text)
for a, b, name in SCENES:
    v = _VO.get(name)
    if not v:
        continue
    lead = LEAD.get(name, (0.6, 0.6))[0]
    t0 = a + lead
    d_all = float(v["dur"])
    VO[name] = (round(t0, 3), round(t0 + d_all, 3))
    frags = _split(v["text"])
    if not frags:
        continue
    tot = sum(len(f) for f in frags) or 1
    cur = t0
    for f in frags:
        d = d_all * len(f) / tot
        SUBS.append((round(cur, 3), round(cur + d, 3), f))
        cur += d
