# HUDict

HUDict is a small Windows English-to-Chinese popup dictionary.

It captures a small region around the mouse, runs local Windows OCR, finds the nearest English word, and shows an ECDICT definition while the hotkey is held.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m hudict.tools.build_ecdict C:\Users\Ysiel\projects\ECDICT\ecdict.csv
.\run-hudict.bat
```

Default hotkey: `p`

Debug files are written to `%LOCALAPPDATA%\HUDict\debug` when `debug_capture = true`.
