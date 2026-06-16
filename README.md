# HUDict

HUDict is a Windows popup dictionary for learning English from what you watch and play.

Hold a hotkey over a word, and HUDict captures a small area around the cursor, runs local Windows OCR, picks the nearest English word, and shows a concise Chinese definition from ECDICT.

HUDict is designed for English immersion: watching a film, reading subtitles, playing a game, or browsing a page while keeping the original sentence in view. It helps you understand one word at a time, so the surrounding context still does the teaching.

## Features

- Local Windows OCR for fast, private recognition.
- English-to-Chinese dictionary lookup powered by ECDICT.
- Cursor-centered capture instead of full-screen OCR.
- Nearest-word hit testing for multi-line text.
- Floating PyQt popup shown while the hotkey is held.
- Optional debug dump with screenshots, OCR words, hit word, lookup result, and timing.

## Inspiration

HUDict is inspired by tools that make lookup feel immediate instead of interruptive:

- [dominostars/playtranslate](https://github.com/dominostars/playtranslate), especially its tap-to-lookup feeling on Android.
- [rtr46/meikipop](https://github.com/rtr46/meikipop), especially the idea of an OCR-powered desktop popup dictionary.

HUDict focuses on English-learning workflows on Windows, using local OCR and ECDICT.

## Requirements

- Windows 10 or later.
- Python 3.10 or later.
- Windows English OCR language support. Most English Windows installations already have it.
- ECDICT CSV data if you want to build the dictionary locally.

## Install

Create a virtual environment and install HUDict in editable mode:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

## Build The Dictionary

HUDict expects `dictionary.pkl` in the project directory.

If you have ECDICT checked out next to this repository, run:

```powershell
.\.venv\Scripts\python.exe -m hudict.tools.build_ecdict ..\ECDICT\ecdict.csv -o dictionary.pkl
```

You only need to rebuild the dictionary when the ECDICT data changes.

## Run

Start HUDict:

```powershell
.\run-hudict.bat
```

Default behavior:

- Hold `p` over an English word.
- HUDict captures a small region around the cursor.
- If OCR and dictionary lookup succeed, a popup appears near the cursor.
- Release `p` to hide the popup.

## Configuration

HUDict reads `config.ini` from the project directory. If it does not exist, HUDict creates it on first import/run.

Useful settings:

```ini
[Settings]
hotkey = p
capture_width = 420
capture_height = 160
debug_capture = true
debug_dir =
font_family = Microsoft YaHei
```

Notes:

- `capture_width` and `capture_height` control the cursor-centered OCR region.
- Smaller capture regions can reduce distractions, but may cut off text.
- `debug_dir` may be left empty; HUDict will use `debug/` in the project directory.
- Set `debug_capture = false` after troubleshooting to avoid writing screenshots and JSON files.

## Debug Files

When `debug_capture = true`, each hotkey press writes:

- `debug/<timestamp>.png`: the actual OCR image.
- `debug/<timestamp>.json`: OCR lines, words, boxes, selected word, dictionary entries, and timing.

The JSON timing section helps diagnose latency:

- `capture`
- `ocr`
- `hit_test`
- `lookup`
- `total_to_lookup`

With Windows OCR, OCR is usually only a few milliseconds on ordinary text.

## Limitations

- HUDict focuses on word lookup for learning in context.
- OCR quality depends on font, scale, contrast, and overlays.
- Some fullscreen exclusive games may block screen capture or popup rendering.
- Online games with anti-cheat may dislike overlays and global hotkeys.

## Development

Useful checks:

```powershell
.\.venv\Scripts\hudict.exe --version
.\.venv\Scripts\python.exe -m hudict.tools.build_ecdict ..\ECDICT\ecdict.csv -o dictionary.pkl
```

## License Notes

HUDict code is separate from ECDICT. Check ECDICT's license before redistributing dictionary data.
