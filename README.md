# 十三万条魔方成绩 · 数据可视化短片

一支用纯代码渲染的科普短片：从一份魔方玩家成绩样本出发，讲清「为什么成绩不是正态分布，而是**对数正态**」。

画面每一个像素由 [pycairo](https://pycairo.readthedocs.io/) 绘制，配乐与音效由 numpy 实时合成，旁白可由任意 TTS 提供，最终用 `ffmpeg` 封装成片。没有任何预渲染素材——**源码 + 一份统计数据即可重建整部视频**。

---

## 一、它能重建出什么

- 14 个场景、约 100 秒、1920×1080 @ 30fps
- 全片时间轴（场景切点、字幕、音效落点）由 `timeline.py` 一份表统一驱动
- 两版旁白音色（`hanabi` / `barbara`）切换，时长与字幕自动跟随

## 二、目录结构（平铺）

| 文件 | 作用 |
| --- | --- |
| `art.py` | 绘图原语、配色、字体选择 |
| `characters.py` / `characters2.py` / `characters3.py` | 角色与魔方几何 |
| `stage.py` | 纸张底、标题、进度条、字幕条等公共件 |
| `timeline.py` | **全片时间轴**：场景顺序/切点/字幕/音效点 |
| `scenes1.py` … `scenes5.py` | 14 个场景的绘制函数 `s_<scene>()` |
| `render.py` | 逐帧渲染，输出 `frames_<voice>/NNNNN.png` |
| `music.py` | 全代码合成配乐 + 音效，输出 `music_<voice>.wav` |
| `mux.py` | 混音 + 响度归一 + `ffmpeg` 封装 mp4 |
| `narration.py` | 台词表（旁白内容源头） |
| `svtts.py` | 调本地 GPT-SoVITS 生成旁白的参考实现（可选） |
| `extract.py` | 从原始抓取数据重算 `stats.json`（可选） |
| `build.py` | 一键串起 render → music → mux |
| `stats.json` | **数据聚合结果**（入库，画帧数据源） |
| `vo_hanabi.json` / `vo_barbara.json` | 旁白元数据（时长/字幕切分依赖） |

## 三、构建

### 1. 环境

```bash
pip install -r requirements.txt
# 另需系统级 ffmpeg / ffprobe（含 libx264、aac、loudnorm）在 PATH 中
```

字体：`art.py` 使用系统字体 **Noto Sans SC**（`FONT_CJK`）与 **Yu Gothic**（`FONT_JP`）。
请先安装，否则中文会回退成方框。跨平台部署建议把字体文件一并放入并改用 `cairo.FontFace` 载入。

### 2. 旁白（自备）

渲染时间轴依赖 `vo_<voice>.json`，其结构为：

```json
{
  "voice": "hanabi",
  "label": "花火",
  "lines": [
    { "id": "title", "text": "……", "dur": 3.74, "file": "vo/hanabi/title.wav" }
  ]
}
```

- `id` 必须与 `timeline.py` 的 `ORDER` 场景名一一对应（`title` `data` `skew` `tail` `why` `model` `log` `law` `fit` `interlude` `profile` `rank` `answer` `outro`）
- `dur` 为该句音频时长（秒），场景长度据此自动取整到 2s 整
- `file` 为音频路径，相对 `vo_<voice>.json` 所在目录或绝对路径均可，**单声道 16bit WAV**

**生成方式任选其一：**

1. **任意 TTS**：按 `narration.py` 的 `LINES` 逐句合成 WAV，测出时长后写出上述 JSON。
2. **GPT-SoVITS 参考实现**：`svtts.py` 约定本地服务接口：

   ```
   POST http://localhost:8001/tts
   Body: {"text": "<台词>", "voice": "hanabi" | "barbara"}
   返回: RIFF/WAV 字节流（status 200）
   ```

   跑通后执行 `python svtts.py hanabi` 即生成 `vo/hanabi/*.wav` 与 `vo_hanabi.json`。
   任何实现了该 `/tts` 契约的服务（换模型、换语言）都能直接替换。

> 仓库不附带旁白音频（`vo/` 已被 `.gitignore` 忽略），需自备。

### 3. 一键构建

```bash
python build.py                # 默认 hanabi
python build.py barbara        # 另一版音色
python build.py hanabi --skip-render   # 复用已渲染的帧
```

产出 `cube_stats_<voice>.mp4`。

### 4. 分步构建（调试用）

```bash
python render.py               # 输出 frames_<voice>/，可用 FRAMES 环境变量改目录
python render.py 0 300         # 只渲染某段帧，快速预览
python music.py                # 生成 music_<voice>.wav / cues_<voice>.json
python mux.py hanabi           # 混音并封装
```

均可用环境变量 `VOICE=hanabi|barbara` 选择音色（`mux.py` 也可用第一个位置参数）。

## 四、数据来源

`stats.json` 是对 **504,277 行原始抓取记录**（`scan-1e8.ndjson`，约 379MB）的**聚合结果**：
直方图、分位数、线性/对数矩、KS 与 D'Agostino 正态检验 p 值等。它是画帧的唯一数据源，**已入库**（约 13KB），因此无需原始数据即可重建视频。

如需从原始数据重新计算：

```bash
SRC=/path/to/scan-1e8.ndjson python extract.py   # 输出 stats.json
```

原始 `scan-1e8.ndjson` 因体积过大**不入库**，请自行准备。

## 五、许可

代码供学习与二次创作。数据源自公开成绩样本，请遵循其原始条款。
