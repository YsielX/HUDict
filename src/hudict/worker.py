import threading
import time

import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
from pynput import mouse

from hudict.config import config
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
        mouse_x, mouse_y = self.mouse.position
        image, region = self.capture.capture_around_mouse(int(mouse_x), int(mouse_y))
        lines = self.ocr.scan(image)
        mouse_image_x = mouse_x - region["left"]
        mouse_image_y = mouse_y - region["top"]
        word = nearest_word(lines, mouse_image_x, mouse_image_y)
        entries = self.dictionary.lookup(word.text) if word else []
        self.entries_ready.emit(entries)
