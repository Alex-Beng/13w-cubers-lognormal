# -*- coding: utf-8 -*-
"""把画帧 + 配乐 + 该音色的旁白封装成 mp4

python mux.py hanabi
"""
import json, os, subprocess, sys, wave
import numpy as np

VOICE = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("VOICE", "hanabi")
os.environ["VOICE"] = VOICE
_HERE = os.path.dirname(os.path.abspath(__file__))
import timeline as TL  # noqa: E402  (必须在设置 VOICE 之后导入)

FRAMES = os.path.join(_HERE, f"frames_{VOICE}")
OUT = os.path.join(_HERE, f"cube_stats_{VOICE}.mp4")
MIX = os.path.join(_HERE, "_mix.wav")
SR = 48000


def read_wav(path):
    with wave.open(path, "rb") as w:
        nch, sw, sr = w.getnchannels(), w.getsampwidth(), w.getframerate()
        raw = w.readframes(w.getnframes())
    assert sw == 2, path
    a = np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if nch > 1:
        a = a.reshape(-1, nch).mean(axis=1)
    return a, sr


def resample(a, sr_from, sr_to):
    if sr_from == sr_to:
        return a
    n = int(round(len(a) * sr_to / sr_from))
    x = np.arange(n) * (sr_from / sr_to)
    return np.interp(x, np.arange(len(a)), a)


# ---- 旁白轨 ----
N = int(round(TL.DUR * SR)) + SR          # 多留 1s，封装时按 -t 截断
voice = np.zeros(N, dtype=np.float64)
_vtbl = {o["id"]: o for o in
         json.load(open(os.path.join(_HERE, f"vo_{VOICE}.json"), encoding="utf-8"))["lines"]}
for name, (t0, t1) in TL.VO.items():
    p = _vtbl[name]["file"]
    if not os.path.isabs(p):
        p = os.path.join(_HERE, p)
    a, sr = read_wav(p)
    a = resample(a, sr, SR)
    # 轻微淡入淡出，避免爆音
    f = int(0.012 * SR)
    if len(a) > 2 * f:
        a[:f] *= np.linspace(0, 1, f)
        a[-f:] *= np.linspace(1, 0, f)
    i0 = int(t0 * SR)
    n = min(len(a), N - i0)
    voice[i0:i0 + n] += a[:n] * 1.0

# 两个音色原始响度不同，只对齐峰值会导致长期响度差 3~4 dB；
# 这里按“有效语音段的 RMS”对齐，再压回峰值上限。
_sp = voice[np.abs(voice) > 0.02]
rms = float(np.sqrt(np.mean(_sp ** 2))) if len(_sp) else 1.0
voice *= 0.052 / rms
vp = float(np.max(np.abs(voice))) or 1.0
if vp > 0.92:
    voice *= 0.92 / vp
print(f"{VOICE}: 语音 RMS {rms:.4f} → 对齐；峰值 {vp:.2f}")

# ---- 配乐轨 ----
mus, msr = read_wav(os.path.join(_HERE, f"music_{VOICE}.wav"))
mus = resample(mus, msr, SR)
n = min(len(mus), N)
music = np.zeros(N)
music[:n] = mus[:n]

# ---- 闪避：旁白在说话时把配乐压下去 ----
env = np.abs(voice)
k = int(0.12 * SR)
env = np.convolve(env, np.ones(k) / k, mode="same")
gate = np.clip(env * 26.0, 0.0, 1.0)          # 说话 -> 1
duck = 1.0 - 0.42 * gate                       # 最深压到 58%
music *= duck

mix = music * 0.72 + voice * 1.55
# 统一峰值：两版都归一化到 -3 dBFS，避免并排对比时音量起伏
peak = np.max(np.abs(mix)) or 1.0
mix *= 0.708 / peak
peak = np.max(np.abs(mix))
st = np.stack([mix, mix], axis=1)
pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
with wave.open(MIX, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print(f"{VOICE}: {TL.DUR:.1f}s  voice peak {np.max(np.abs(voice)):.2f}  mix peak {peak:.2f}")

# ---- 两遍 loudnorm：两版对齐到同一响度（-16 LUFS / TP -1.5 dBTP） ----
r = subprocess.run([
    "ffmpeg", "-hide_banner", "-i", MIX,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
    "-f", "null", "NUL",
], capture_output=True, text=True)
txt = r.stderr
i0 = txt.rfind("{")
_j = json.loads(txt[i0:txt.rfind("}") + 1]) if i0 >= 0 else {}
ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:"
      f"measured_I={_j.get('input_i','-16')}:measured_TP={_j.get('input_tp','-1.5')}:"
      f"measured_LRA={_j.get('input_lra','11')}:measured_thresh={_j.get('input_thresh','-26')}:"
      f"offset={_j.get('target_offset','0')}:linear=true")
print("loudnorm:", _j.get("input_i"), "LUFS →", "-16")

subprocess.run([
    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
    "-framerate", "30", "-i", os.path.join(FRAMES, "%05d.png"),
    "-i", MIX,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-pix_fmt", "yuv420p", "-t", f"{TL.DUR:.3f}",
    "-af", ln,
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
    "-movflags", "+faststart", OUT,
], check=True)
print("wrote", OUT, os.path.getsize(OUT) // 1024, "KB")
