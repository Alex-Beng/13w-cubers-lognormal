# -*- coding: utf-8 -*-
"""逐帧渲染整部片子：python render.py [起] [止]"""
import os, sys, time, importlib
import multiprocessing as mp
import cairo

from stage import W, H, paper, progress, subtitle
from timeline import FPS, DUR, scene_at, SUBS

MODS = ("scenes1", "scenes2", "scenes3", "scenes4", "scenes5")
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("FRAMES") or os.path.join(_HERE, "frames")
_SURF = None
_CTX = None
_FNS = {}


def _init():
    """每个进程复用自己的 surface，避免逐帧分配"""
    global _SURF, _CTX, _FNS
    _SURF = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    _CTX = cairo.Context(_SURF)
    paper(_CTX)                     # 触发一次，之后走缓存
    for m in MODS:
        try:
            mod = importlib.import_module(m)
        except ImportError:
            continue
        for n in dir(mod):
            if n.startswith("s_"):
                _FNS.setdefault(n[2:], mod)


def frame(i):
    t = i / FPS
    ctx = _CTX
    paper(ctx)                      # 不透明底，直接覆盖上一帧
    sc, d, dd = scene_at(t)
    fn = _FNS.get(sc)
    m0 = ctx.get_matrix()
    if fn is not None:
        getattr(fn, "s_" + sc)(ctx, d, dd)
    for s0, s1, txt in SUBS:
        if s0 - 0.02 <= t < s1:
            a = min(1.0, (t - s0) / 0.12, (s1 - t) / 0.10)
            subtitle(ctx, txt, max(0.0, min(1.0, a)))
            break
    m1 = ctx.get_matrix()
    if (m0.xx, m0.xy, m0.yx, m0.yy, m0.x0, m0.y0) != (m1.xx, m1.xy, m1.yx, m1.yy, m1.x0, m1.y0):
        raise RuntimeError(f"CTM leak at frame {i} ({sc})")
    progress(ctx, t)
    _SURF.write_to_png(os.path.join(OUT, f"{i:05d}.png"))
    return i


def main():
    os.makedirs(OUT, exist_ok=True)
    total = int(round(DUR * FPS))
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else total
    idx = list(range(lo, min(hi, total)))
    t0 = time.time()
    nproc = max(1, min(20, os.cpu_count() or 4))
    with mp.Pool(nproc, initializer=_init) as pool:
        done = 0
        for i in pool.imap_unordered(frame, idx, chunksize=4):
            done += 1
            if done % 120 == 0 or done == len(idx):
                el = time.time() - t0
                eta = el / done * (len(idx) - done)
                print(f"{done}/{len(idx)}  {el:.0f}s  eta {eta:.0f}s", flush=True)
    print(f"done {len(idx)} frames in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
