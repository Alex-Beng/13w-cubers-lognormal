# -*- coding: utf-8 -*-
"""解说台词（每场一句，喂给 svtts.py）

顺序就是全片的推理顺序：
    长什么样 → 长尾 → 为什么长尾（多阶段相乘）→ 取对数（乘法变加法）
    → 大数定律（很多小项相加 → 钟形）→ 对照验证 → 人 → 结论
面向初中生：不出现"偏度""峰度""显著性"这些词。
"""
import asyncio, json, os, subprocess, sys

VOICE = "zh-CN-XiaoyiNeural"
RATE = "+8%"
_HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(_HERE, "vo")

# (id, 台词)  —— 与场景一一对应，与 timeline.ORDER 同名
LINES = [
    ("title",   "十三万条魔方成绩，为什么不是一条对称的钟形曲线？"),
    ("data",    "十三万个魔方玩家的真实成绩。中位数四十秒，平均四十六秒。"),
    ("skew",    "可是它右边拖着一根长长的尾巴。最慢的一条，二十多分钟都没复原。"),
    ("why",     "为什么会拖出这根尾巴？因为一局成绩不是加出来的，是乘出来的。"),
    ("model",   "观察、判断、找块、转动、收手，每一步都乘上一个时间。任何一步慢一点，整局就被放大。慢的那一头，就是这样被拉长的。"),
    ("log",     "乘法不好算。取个对数，乘法就变成了加法。"),
    ("law",     "而很多互不相干的小数相加，结果总是中间高、两头低，堆成一条钟形曲线。"),
    ("fit",     "验证一下：实测算出来的分位数，和预测几乎一个点一个点对上了。"),
    ("interlude", "所以这口钟，长在对数轴上。"),
    ("profile", "这群人是谁？平均个人最佳三十二秒，每秒转三点一五次。"),
    ("rank",    "一半的人四十秒内完成，最好的一成，二十秒内。"),
    ("answer",  "所以答案是——对数正态。不是成绩正态，是它在对数轴上正态。"),
    ("outro",   "数据不会说谎。谢谢观看。"),
]


def dur_of(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


async def synth(tag, text):
    import edge_tts
    p = os.path.join(OUTDIR, f"{tag}.mp3")
    com = edge_tts.Communicate(text, VOICE, rate=RATE)
    await com.save(p)
    return p


async def main():
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    for tag, text in LINES:
        p = await synth(tag, text)
        d = dur_of(p)
        out.append({"id": tag, "text": text, "dur": round(d, 3), "file": p})
        print(f"{tag:10s} {d:6.2f}s  {text}")
    with open(os.path.join(_HERE, "vo.json"), "w", encoding="utf-8") as f:
        json.dump({"voice": VOICE, "rate": RATE, "lines": out}, f,
                  ensure_ascii=False, indent=1)
    print("total", round(sum(o["dur"] for o in out), 2), "s")


if __name__ == "__main__":
    asyncio.run(main())
