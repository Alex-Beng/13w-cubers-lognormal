# -*- coding: utf-8 -*-
"""用本地 GPT-SoVITS（localhost:8001）跑两版旁白：花火 / 芭芭拉

产出：
  vo/<voice>/<tag>.wav
  vo_<voice>.json   —— timeline._vo_table() 直接读这个
"""
import json, os, subprocess, sys, time
import urllib.request, urllib.error

from narration import LINES

BASE = "http://localhost:8001"
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_HERE, "vo")
VOICES = [("hanabi", "花火"), ("barbara", "芭芭拉")]


def post(path, obj, timeout=600):
    data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read(), time.time() - t0


def dur_of(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def run(voice, label):
    d = os.path.join(OUT, voice)
    os.makedirs(d, exist_ok=True)
    out = []
    for i, (tag, text) in enumerate(LINES, 1):
        p = os.path.join(d, f"{tag}.wav")
        st, body, el = post("/tts", {"text": text, "voice": voice})
        if st != 200 or not body.startswith(b"RIFF"):
            print(f"  [{i:2d}/{len(LINES)}] {tag:10s} FAIL {st} {body[:160]!r}")
            sys.exit(1)
        open(p, "wb").write(body)
        dur = dur_of(p)
        rel = os.path.relpath(p, _HERE).replace("\\", "/")
        out.append({"id": tag, "text": text, "dur": round(dur, 3), "file": rel})
        print(f"  [{i:2d}/{len(LINES)}] {tag:10s} {dur:6.2f}s  gen {el:5.1f}s")
    tbl = {"voice": voice, "label": label, "lines": out}
    json.dump(tbl, open(os.path.join(_HERE, f"vo_{voice}.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{label}: {len(out)} 条，合计 {sum(o['dur'] for o in out):.2f}s -> vo_{voice}.json\n")
    return tbl


if __name__ == "__main__":
    want = sys.argv[1:] or [v for v, _ in VOICES]
    for voice, label in VOICES:
        if voice not in want:
            continue
        print(f"== {label} ({voice}) ==")
        run(voice, label)
