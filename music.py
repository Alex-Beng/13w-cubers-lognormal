# -*- coding: utf-8 -*-
"""全代码合成配乐 + 音效：120 BPM，8-bit 方波 + 木琴 + 马林巴

结构完全由 timeline.SCENES 推出：每个场景按自己的实际时长铺小节，
场景之间不留缝；另外始终有一层很轻的铺底，保证任何时刻都有声音。
"""
import json, math, wave, os
import numpy as np

from timeline import CUTS as FILM_CUTS, HITS, RISERS, DUR as FILM_DUR, SCENES, VOICE

_HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC_OUT = os.path.join(_HERE, f"music_{VOICE}.wav")

SR = 48000
BPM = 120.0
BEAT = 60.0 / BPM
BAR = BEAT * 4
DUR = FILM_DUR
N = int(SR * DUR)
rng = np.random.default_rng(20261027)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)


def adsr(n, a=0.005, d=0.06, s=0.6, r=0.08):
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    env = np.ones(n, dtype=np.float64)
    a_n = min(a_n, n); d_n = min(d_n, max(0, n - a_n)); r_n = min(r_n, n)
    if a_n > 0: env[:a_n] = np.linspace(0, 1, a_n)
    if d_n > 0: env[a_n:a_n + d_n] = np.linspace(1, s, d_n)
    if n - a_n - d_n > 0: env[a_n + d_n:] = s
    if r_n > 0: env[-r_n:] *= np.linspace(1, 0, r_n)
    return env


def env_exp(n, tau):
    return np.exp(-np.arange(n) / (SR * tau))


# ---------- 音色 ----------
def sq(freq, dur, duty=0.5, vol=0.3, vib=0.0, slide=1.0):
    n = max(2, int(dur * SR))
    t = np.arange(n) / SR
    f = freq * (1 + vib * np.sin(2 * np.pi * 5.2 * t)) * np.linspace(1.0, slide, n)
    ph = np.cumsum(f) / SR
    y = np.where((ph % 1.0) < duty, 1.0, -1.0)
    return y * env_exp(n, dur * 0.55) * vol


def tri(freq, dur, vol=0.25, slide=1.0):
    n = max(2, int(dur * SR))
    f = freq * np.linspace(1.0, slide, n)
    ph = np.cumsum(f) / SR
    y = 2 * np.abs(2 * (ph % 1.0) - 1) - 1
    return y * adsr(n, 0.006, 0.05, 0.80, 0.06) * vol


def marimba(freq, dur, vol=0.3, bright=1.0):
    n = max(2, int(dur * SR))
    t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 7.0)
         + 0.45 * bright * np.sin(2 * np.pi * freq * 4.0 * t) * np.exp(-t * 22.0)
         + 0.18 * bright * np.sin(2 * np.pi * freq * 9.2 * t) * np.exp(-t * 40.0))
    return y * vol * 0.8


def bell(freq, dur, vol=0.22):
    n = max(2, int(dur * SR))
    t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * freq * t) * np.exp(-t * 3.0)
         + 0.6 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t * 6.0)
         + 0.3 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-t * 12.0))
    return y * vol


def pad(freqs, dur, vol=0.10):
    """柔和的持续铺底：三角波叠加 + 缓慢起落，用来兜住任何空档"""
    n = max(2, int(dur * SR))
    t = np.arange(n) / SR
    y = np.zeros(n)
    for f in freqs:
        y += np.sin(2 * np.pi * f * t) * (1.0 + 0.06 * np.sin(2 * np.pi * 0.23 * t))
    y /= max(1, len(freqs))
    env = np.minimum(1.0, t / 0.35) * np.minimum(1.0, (dur - t) / 0.45)
    return y * np.clip(env, 0, 1) * vol


def kick(vol=0.55, dur=0.14):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 110 * np.exp(-t * 28) + 42
    ph = np.cumsum(f) / SR
    return np.sin(2 * np.pi * ph) * np.exp(-t * 16) * vol


def snare(vol=0.30, dur=0.13):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    noise = np.diff(noise, prepend=0)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 40) * 0.5
    return (noise * np.exp(-t * 26) * 0.5 + body) * vol


def hat(vol=0.16, dur=0.05):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    noise = np.diff(noise, n=2, prepend=[0, 0])
    return noise * env_exp(n, 0.012) * vol


def wood(vol=0.30, dur=0.09):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1180 * t) * np.exp(-t * 45)
            + 0.6 * np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 60)) * vol


def clap(vol=0.24):
    n = int(0.16 * SR)
    out = np.zeros(n)
    for k in range(4):
        off = int(k * 0.011 * SR)
        seg = rng.standard_normal(n - off) * env_exp(n - off, 0.018)
        out[:n - off] += seg * (0.7 ** k)
    return out * vol


def whoosh(dur=0.5, vol=0.22, up=True):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    k = 9
    noise = np.convolve(noise, np.ones(k) / k, mode='same')
    t = np.linspace(0, 1, n)
    env = (t ** 2 if up else (1 - t) ** 2) * (1 - t if up else t ** 0.3)
    return noise * env * vol * 4


def synth_hit(dur=0.5, vol=0.4):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 300 * np.exp(-t * 18) + 60
    ph = np.cumsum(f) / SR
    body = np.sin(2 * np.pi * ph) * np.exp(-t * 6)
    click = rng.standard_normal(n) * np.exp(-t * 90) * 0.5
    return (body + click) * vol


def pop_sfx(vol=0.3):
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = 600 * np.exp(-t * 30) + 240
    ph = np.cumsum(f) / SR
    return np.sin(2 * np.pi * ph) * np.exp(-t * 30) * vol


def boing(vol=0.25):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 320 * (1 + 0.55 * np.sin(2 * np.pi * 17 * t) * np.exp(-t * 6))
    ph = np.cumsum(f) / SR
    return np.sin(2 * np.pi * ph) * np.exp(-t * 5) * vol


def riser(dur=1.4, vol=0.18):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    noise = np.convolve(noise, np.ones(5) / 5, mode='same')
    t = np.linspace(0, 1, n)
    return noise * (t ** 2.2) * vol * 3


# ---------- 混音 ----------
mix = np.zeros((N, 2), dtype=np.float64)


def add(sig, t, pan=0.0, gain=1.0):
    if sig is None or t >= DUR: return
    i0 = int(max(0, t) * SR)
    n = min(len(sig), N - i0)
    if n <= 0: return
    s = sig[:n] * gain
    l = math.cos((pan + 1) * math.pi / 4)
    r = math.sin((pan + 1) * math.pi / 4)
    mix[i0:i0 + n, 0] += s * l
    mix[i0:i0 + n, 1] += s * r


cues = []


def cue(t, kind, beat=None):
    cues.append({"t": round(t, 4), "kind": kind, "beat": beat})


def b(beat):
    return beat * BEAT


# ---------- 和声与旋律 ----------
CH = {
    "A":  [57, 61, 64, 69],
    "E":  [52, 56, 59, 64],
    "F#m":[54, 57, 61, 66],
    "D":  [50, 54, 57, 62],
}
MEL_A = [
    (0, 69, 0.5), (0.5, 71, 0.5), (1, 73, 0.5), (1.5, 76, 0.5),
    (2, 73, 0.5), (2.5, 71, 0.5), (3, 69, 1.0),
    (4, 71, 0.5), (4.5, 73, 0.5), (5, 76, 0.5), (5.5, 78, 0.5),
    (6, 76, 0.5), (6.5, 73, 0.5), (7, 71, 1.0),
]
MEL_B = [
    (0, 76, 0.5), (0.5, 78, 0.5), (1, 81, 0.75), (1.75, 78, 0.25), (2, 76, 0.5), (2.5, 73, 0.5), (3, 76, 1.0),
    (4, 74, 0.5), (4.5, 76, 0.5), (5, 78, 0.75), (5.75, 76, 0.25), (6, 73, 0.5), (6.5, 71, 0.5), (7, 69, 1.0),
]
PROG = ["A", "E", "F#m", "D"]

SEC = {n: (a, b) for a, b, n in SCENES}
ORDER = [n for _, _, n in SCENES]


def bar_of(t):
    return int(round(t / BAR))


def scene_at(t):
    for a, e, n in SCENES:
        if a <= t < e:
            return n
    return SCENES[-1][2]


# 每个场景的编曲性格：有没有鼓、木琴密度、旋律、音量
STYLE = {
    "title":     dict(drums=False, arp="slow", lead=None,  lead_vol=0.0,  bass=False),
    "data":      dict(drums=True,  arp="eight", lead=MEL_A, lead_vol=0.15, bass=True),
    "skew":      dict(drums=True,  arp="eight", lead=MEL_A, lead_vol=0.14, bass=True),
    "tail":      dict(drums=True,  arp="sixteen", lead=MEL_A, lead_vol=0.13, bass=True),
    "why":       dict(drums=True,  arp="eight", lead=MEL_B, lead_vol=0.14, bass=True),
    "model":     dict(drums=True,  arp="eight", lead=MEL_B, lead_vol=0.14, bass=True),
    "log":       dict(drums=True,  arp="eight", lead=MEL_B, lead_vol=0.15, bass=True),
    "law":       dict(drums=True,  arp="eight", lead=MEL_A, lead_vol=0.15, bass=True),
    "fit":       dict(drums=True,  arp="eight", lead=MEL_B, lead_vol=0.15, bass=True),
    "interlude": dict(drums=False, arp="slow", lead=None,  lead_vol=0.0,  bass=False),
    "profile":   dict(drums=True,  arp="eight", lead=MEL_A, lead_vol=0.15, bass=True),
    "rank":      dict(drums=True,  arp="eight", lead=MEL_B, lead_vol=0.16, bass=True),
    "answer":    dict(drums=False, arp="slow", lead=MEL_A[:8], lead_vol=0.15, bass=True),
    "outro":     dict(drums=False, arp="slow", lead=None,  lead_vol=0.0,  bass=True),
}


def play_bar(k, st):
    """按场景性格铺一个小节；k = 全局小节号"""
    bb = k * 4
    ch = CH[PROG[k % 4]]
    if st["bass"]:
        add(tri(midi(ch[0] - 12), BEAT * 0.9, 0.26), b(bb), -0.05)
        add(tri(midi(ch[0] - 12), BEAT * 0.5, 0.20), b(bb + 2.0), -0.05)
        add(tri(midi(ch[0] - 5), BEAT * 0.45, 0.14), b(bb + 3.5), -0.05)
    # 木琴
    if st["arp"] == "sixteen":
        seq = [ch[1], ch[2], ch[3], ch[2]]
        for i in range(16):
            nn = seq[i % 4] + (12 if i % 4 == 2 else 0)
            add(marimba(midi(nn), 0.26, 0.085), b(bb + i * 0.25),
                -0.35 if i % 2 else 0.35)
    elif st["arp"] == "eight":
        seq = [ch[1], ch[2], ch[3], ch[2]]
        for i in range(8):
            nn = seq[i % 4] + (12 if i % 4 == 2 else 0)
            if i == 3 or i == 7:
                nn = ch[1] + 12
            add(marimba(midi(nn), 0.34, 0.105 + (0.025 if i in (0, 4) else 0)),
                b(bb + i * 0.5), -0.35 if i % 2 else 0.35)
    else:  # slow
        for i, nn in enumerate([ch[3], ch[2], ch[1], ch[2]]):
            add(marimba(midi(nn + 12), 0.9, 0.12), b(bb + i), 0.30 if i % 2 else -0.30)
        add(bell(midi(ch[3] + 24), 1.6, 0.055), b(bb), 0.4)
    # 鼓
    if st["drums"]:
        for i in range(4):
            add(kick(0.40), b(bb + i), 0.0)
        add(snare(0.24), b(bb + 1.0), 0.05)
        add(snare(0.24), b(bb + 3.0), 0.05)
        add(clap(0.14), b(bb + 3.0), -0.05)
        for i in range(8):
            add(hat(0.10 if i % 2 else 0.14), b(bb + i * 0.5), 0.35 if i % 2 else -0.35)
    else:
        add(hat(0.05), b(bb + 2), 0.4)
    # 铃音点缀
    if k % 4 == 0:
        add(bell(midi(88), 0.9, 0.05), b(bb), 0.5)
    # 主旋律
    lead = st["lead"]
    if lead:
        for (off, nn, ln) in lead:
            t0 = b(bb + off)
            add(sq(midi(nn), BEAT * ln * 0.92, duty=0.5, vol=st["lead_vol"], vib=0.004), t0, 0.0)
            add(sq(midi(nn + 12), BEAT * ln * 0.92, duty=0.25, vol=st["lead_vol"] * 0.28), t0, 0.1)
            add(sq(midi(nn), BEAT * ln * 0.5, duty=0.5, vol=st["lead_vol"] * 0.20), t0 + BEAT * 0.75, -0.3)


# ================= 铺满整片（不再按硬编码小节数） =================
# 终曲前 2 秒是终止和弦，之后留白给淡出
END_T = max(0.0, DUR - 2.0)
total_bars = int(math.ceil(DUR / BAR))

for k in range(total_bars):
    t_bar = k * BAR
    # 前 4 小节是引子：极轻
    if t_bar < 4 * BAR:
        ch = CH[PROG[k % 4]]
        for i in range(8):
            nn = ch[(i % 4)] + 12 + (12 if i % 4 == 2 else 0)
            add(marimba(midi(nn), 0.5, 0.075), b(k * 4 + i * 0.5), 0.4 if i % 2 else -0.4)
        add(bell(midi(ch[3] + 12), 1.2, 0.05), b(k * 4), 0.3)
        add(pad([midi(ch[0]), midi(ch[0] + 7), midi(ch[0] + 12)], BAR, 0.035), t_bar, 0)
        continue
    if t_bar >= END_T - 1e-6:
        # 尾声：只留铺底 + 铃，终止和弦自己收尾
        ch = CH[PROG[k % 4]]
        add(pad([midi(ch[0]), midi(ch[0] + 7), midi(ch[0] + 12)], BAR, 0.030), t_bar, 0)
        add(marimba(midi(ch[3] + 12), 1.4, 0.07), t_bar, 0.25)
        continue

    st = STYLE.get(scene_at(t_bar), STYLE["data"])
    play_bar(k, st)
    # 始终垫一层极轻的和声，任何时刻都有声音
    ch = CH[PROG[k % 4]]
    pv = 0.030 if st["drums"] else 0.038
    add(pad([midi(ch[0]), midi(ch[0] + 7), midi(ch[0] + 12)], BAR + 0.04, pv), t_bar, 0)

# 终止和弦：落在片尾前 2s
for i, nn in enumerate([57, 61, 64, 69, 76]):
    add(marimba(midi(nn + 12), 2.4, 0.15), END_T, (i - 2) * 0.18)
    add(bell(midi(nn + 24), 2.0, 0.045), END_T, (i - 2) * 0.2)
add(tri(midi(45), 1.8, 0.26), END_T, -0.05)
add(kick(0.50), END_T, 0)
add(synth_hit(0.9, 0.16), END_T, 0)

# ---------- 音效 & 卡点 cue（唯一来源：timeline.py） ----------
_LAST = DUR - 0.02
for t in FILM_CUTS:
    if 0.05 < t < _LAST:
        add(whoosh(0.28, 0.075, up=True), max(0, t - 0.16), 0.1)
        add(wood(0.075), t, -0.2)
    cue(t, "cut")

_HIT_VOL = {"impact": 0.42, "pop": 0.24, "boing": 0.24, "whoosh": 0.24}
for t, kind in HITS:
    if not (0 <= t < _LAST): continue
    v = _HIT_VOL.get(kind, 0.3)
    if kind == "impact":
        add(synth_hit(0.6, v), t, 0); add(kick(0.40), t, 0)
    elif kind == "pop":
        add(pop_sfx(v), t, 0.1)
    elif kind == "boing":
        add(boing(v), t, -0.1)
    elif kind == "whoosh":
        add(whoosh(0.5, v, True), t, 0)
    cue(t, kind)

for t, dur in RISERS:
    add(riser(dur, 0.16), t, 0.0)
    cue(t, "riser")


# ---------- 简易混响 ----------
def reverb(x, wet=0.10):
    out = x.copy()
    for d, g in ((int(0.031 * SR), 0.35), (int(0.047 * SR), 0.28), (int(0.071 * SR), 0.20)):
        y = np.zeros_like(x)
        y[d:] = x[:-d] * g
        out += y * wet
    return out


mix = reverb(mix, 0.10)

# ---------- 音量拉平：按 1 秒窗做慢速 RMS 归一，再软限幅 ----------
def rms_env(x, win=1.0):
    n = int(win * SR)
    k = np.ones(n) / n
    e = np.sqrt(np.convolve(np.mean(x ** 2, axis=1), k, mode='same'))
    return e


env = rms_env(mix, 1.0)
env = np.maximum(env, 1e-4)
# 只在长窗内比较，避免把鼓点本身削平
target = np.percentile(env, 62)
gain = np.clip(target / env, 0.62, 1.45)
gain = np.convolve(gain, np.ones(int(0.6 * SR)) / int(0.6 * SR), mode='same')
gain = np.clip(gain, 0.55, 1.50)
mix *= gain[:, None]

mix = np.tanh(mix * 1.02) * 0.76
peak = np.max(np.abs(mix))
if peak > 0:
    mix *= (0.92 / peak)

# 首尾淡入淡出
fin = int(0.25 * SR)
mix[:fin] *= np.linspace(0, 1, fin)[:, None]
fade = int(1.0 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]

out = (mix * 32767).astype(np.int16)
with wave.open(MUSIC_OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(out.tobytes())

with open(os.path.join(_HERE, f"cues_{VOICE}.json"), "w", encoding="utf-8") as f:
    json.dump({"bpm": BPM, "voice": VOICE, "cues": sorted(cues, key=lambda c: c["t"])},
              f, ensure_ascii=False, indent=1)
print(MUSIC_OUT, os.path.getsize(MUSIC_OUT) // 1024, "KB; cues", len(cues))
