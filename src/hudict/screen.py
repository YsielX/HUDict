import mss
from PIL import Image

from hudict.config import config


class ScreenCapture:
    def capture_around_mouse(self, mouse_x, mouse_y):
        with mss.mss() as sct:
            monitor = self._monitor_for_point(sct, mouse_x, mouse_y)
            width = min(config.capture_width, monitor["width"])
            height = min(config.capture_height, monitor["height"])
            left = int(mouse_x - width / 2)
            top = int(mouse_y - height / 2)

            min_left = monitor["left"]
            min_top = monitor["top"]
            max_left = monitor["left"] + monitor["width"] - width
            max_top = monitor["top"] + monitor["height"] - height
            left = max(min_left, min(left, max_left))
            top = max(min_top, min(top, max_top))

            region = {"left": left, "top": top, "width": width, "height": height}
            raw = sct.grab(region)
            image = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
            return image, region

    def _monitor_for_point(self, sct, x, y):
        for monitor in sct.monitors[1:]:
            left = monitor["left"]
            top = monitor["top"]
            right = left + monitor["width"]
            bottom = top + monitor["height"]
            if left <= x < right and top <= y < bottom:
                return monitor
        return sct.monitors[1]
