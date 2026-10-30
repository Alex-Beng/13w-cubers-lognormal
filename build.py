# -*- coding: utf-8 -*-
"""一键重建整部视频。

流水线（每步产物都由上一步决定，可单独重跑）：

    1. 逐帧渲染   render.py  -> frames_<voice>/00000.png ...
    2. 合成配乐   music.py   -> music_<voice>.wav, cues_<voice>.json
    3. 封装成片   mux.py     -> cube_stats_<voice>.mp4

用法：

    python build.py                # 默认音色 hanabi，全流程
    python build.py barbara        # 指定另一版音色
    python build.py hanabi --skip-render   # 复用已有帧，只重做音轨+封装

前置条件：
    - 旁白 vo_<voice>.json 与 vo/<voice>/*.wav 已就位（见 README「旁白」一节）
    - 已安装 ffmpeg / ffprobe，Python 依赖见 requirements.txt
    - 系统已安装字体 Noto Sans SC（随附内嵌字库则无需）
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, args=None, env_extra=None):
    args = args or []
    env = os.environ.copy()
    env["PYTHONPATH"] = HERE + os.pathsep + env.get("PYTHONPATH", "")
    if env_extra:
        env.update(env_extra)
    cmd = [sys.executable, os.path.join(HERE, script)] + args
    print("\n>>> " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=HERE, env=env)


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    voice = argv[0] if argv else os.environ.get("VOICE", "hanabi")
    env = {"VOICE": voice}

    if "--skip-render" not in flags:
        run("render.py", env_extra=dict(env, FRAMES=os.path.join(HERE, f"frames_{voice}")))
    else:
        print(f"[skip] render（复用 frames_{voice}/）")

    run("music.py", env_extra=env)
    run("mux.py", [voice], env_extra=env)
    print(f"\n完成：{os.path.join(HERE, f'cube_stats_{voice}.mp4')}")


if __name__ == "__main__":
    main()
