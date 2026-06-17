# HUDict

[English](README.md) | [简体中文](README.zh-CN.md)

HUDict 是一个面向英语学习的 Windows 屏幕取词工具。

按住热键指向英文单词时，HUDict 会截取鼠标附近的一小块屏幕，使用本地 Windows OCR 识别文字，再选择离鼠标最近的英文单词，并用 ECDICT 显示简洁的中文释义。

HUDict 面向沉浸式英语学习：看影视、读字幕、玩游戏或浏览网页时，在保留原句语境的同时快速查一个词。它帮助你理解单词，但仍然让上下文承担主要的学习作用。

## 演示

![HUDict 演示](demo.webp)

[观看演示视频](demo.mp4)

## 功能

- 使用 Windows 本地 OCR，识别速度快，也更适合离线使用。
- 使用 ECDICT 做英中词典查询。
- 只截取鼠标附近区域，不做全屏 OCR。
- 对多行文字使用“最近词”命中逻辑。
- 按住热键时显示 PyQt 浮窗，松开后隐藏。
- 可选 debug 输出：截图、OCR 结果、词框、命中词、查词结果和耗时。

## 环境要求

- Windows 10 或更新版本。
- Windows 英文 OCR 语言支持。大多数英文环境 Windows 已经自带。
- 如果从源码安装，需要 Python 3.10 或更新版本。
- 如果需要本地生成词典，需要 ECDICT 的 CSV 数据。

## 使用 Release

最简单的方式是从 [GitHub Releases](https://github.com/YsielX/HUDict/releases) 下载 Windows 压缩包。

1. 下载 `HUDict-vX.Y.Z-windows-x64.zip`。
2. 解压到普通文件夹，例如 `Downloads\HUDict` 或 `Documents\HUDict`。
3. 运行 `run-hudict.bat`。
4. 把鼠标放到英文单词上，然后按住 `p`。
5. 松开 `p` 后浮窗隐藏。

这些文件需要保持在同一个文件夹里：

- `HUDict.exe`：应用本体。
- `run-hudict.bat`：推荐使用的启动脚本。
- `config.ini`：热键、截图大小、字体、颜色和 debug 设置。
- `dictionary.pkl`：本地英中词典。

使用 release 压缩包时不需要安装 Python。

如果 Windows 首次运行时拦截应用，可以选择 **更多信息**，再选择 **仍要运行**。未签名的开源 Windows 工具有时会触发这个提示。

如果按住 `p` 没有反应，请检查 Windows 是否安装了英文 OCR。可以打开 **设置 > 时间和语言 > 语言和区域**，按需添加 English，并确认对应的 OCR 支持可用。

## 从源码安装

在项目目录下创建虚拟环境并安装：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

## 生成词典

HUDict 默认读取项目目录下的 `dictionary.pkl`。

如果 ECDICT 仓库和 HUDict 放在同一级目录，可以运行：

```powershell
.\.venv\Scripts\python.exe -m hudict.tools.build_ecdict ..\ECDICT\ecdict.csv -o dictionary.pkl
```

只有在 ECDICT 数据更新时才需要重新生成。

## 运行

启动：

```powershell
.\run-hudict.bat
```

默认交互：

- 把鼠标放到英文单词上。
- 按住 `p`。
- HUDict 截取鼠标附近区域并进行 OCR。
- 如果命中词典，会在鼠标附近弹出中文释义。
- 松开 `p` 后浮窗隐藏。

## 配置

HUDict 从项目目录读取 `config.ini`。如果文件不存在，首次运行时会自动创建。

常用配置：

```ini
[Settings]
hotkey = p
capture_width = 420
capture_height = 160
debug_capture = true
debug_dir =
font_family = Microsoft YaHei
```

说明：

- `capture_width` 和 `capture_height` 控制鼠标附近的 OCR 截图大小。
- 截图区域越小，干扰越少，但也更容易截断文字。
- `debug_dir` 留空时，默认使用项目目录下的 `debug/`。
- 排查完问题后，可以把 `debug_capture` 改成 `false`，避免持续写截图和 JSON。

## 灵感来源

HUDict 受到这些工具的启发：

- [dominostars/playtranslate](https://github.com/dominostars/playtranslate)：尤其是 Android 上点按取词的使用体验。
- [rtr46/meikipop](https://github.com/rtr46/meikipop)：尤其是 OCR 驱动的桌面弹窗词典思路。

HUDict 则聚焦 Windows 上的英语学习场景，使用本地 OCR 和 ECDICT。
