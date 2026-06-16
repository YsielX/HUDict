import threading
import time

import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
from pynput import mouse

from hudict.config import config
from hudict.debug import dump_lookup
from hudict.dictionary import Dictionary
from hudict.hit_test import nearest_word
from hudict.ocr import WindowsOcr
from hudict.screen import ScreenCapture


class LookupWorker(QObject):
    entries_ready = pyqtSignal(object)
    hide_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.mouse = mouse.Controller()
        self.capture = ScreenCapture()
        self.ocr = WindowsOcr()
        self.dictionary = Dictionary()
        self.thread = threading.Thread(target=self.run, daemon=True, name="HUDictWorker")

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False

    def run(self):
        was_down = False
        while self.running:
            try:
                is_down = keyboard.is_pressed(config.hotkey)
                if is_down and not was_down:
                    self.lookup_once()
                elif not is_down and was_down:
                    self.hide_requested.emit()
                was_down = is_down
            except Exception:
                pass
            time.sleep(0.01)

    def lookup_once(self):
        timing = {"input": time.perf_counter()}
        mouse_x, mouse_y = self.mouse.position
        image, region = self.capture.capture_around_mouse(int(mouse_x), int(mouse_y))
        timing["capture_done"] = time.perf_counter()
        lines = self.ocr.scan(image)
        timing["ocr_done"] = time.perf_counter()
        mouse_image_x = mouse_x - region["left"]
        mouse_image_y = mouse_y - region["top"]
        word = nearest_word(lines, mouse_image_x, mouse_image_y)
        timing["hit_done"] = time.perf_counter()
        entries = self.dictionary.lookup(word.text) if word else []
        timing["lookup_done"] = time.perf_counter()
        self.dump_debug(image, region, mouse_x, mouse_y, mouse_image_x, mouse_image_y, lines, word, entries, timing)
        self.entries_ready.emit(entries)

    def dump_debug(self, image, region, mouse_x, mouse_y, mouse_image_x, mouse_image_y, lines, word, entries, timing):
        base = timing["input"]
        timing_ms = {key: round((value - base) * 1000, 2) for key, value in timing.items()}
        timing_ms["capture"] = round((timing["capture_done"] - timing["input"]) * 1000, 2)
        timing_ms["ocr"] = round((timing["ocr_done"] - timing["capture_done"]) * 1000, 2)
        timing_ms["hit_test"] = round((timing["hit_done"] - timing["ocr_done"]) * 1000, 2)
        timing_ms["lookup"] = round((timing["lookup_done"] - timing["hit_done"]) * 1000, 2)
        timing_ms["total_to_lookup"] = round((timing["lookup_done"] - timing["input"]) * 1000, 2)
        dump_lookup(image, {
            "mouse_screen": {"x": int(mouse_x), "y": int(mouse_y)},
            "mouse_image": {"x": mouse_image_x, "y": mouse_image_y},
            "capture": region,
            "lines": [line.to_dict() for line in lines],
            "hit_word": word.to_dict() if word else None,
            "entries": [
                {"word": entry.word, "phonetic": entry.phonetic, "glosses": entry.glosses}
                for entry in entries
            ],
            "timing_ms": timing_ms,
        })
