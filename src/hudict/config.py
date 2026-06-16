import configparser
import os

from hudict.paths import paths


class Config:
    _SCHEMA = {
        "Settings": {
            "hotkey": "p",
            "capture_width": 420,
            "capture_height": 160,
            "debug_capture": True,
            "debug_dir": "",
            "background_opacity": 245,
            "font_family": "Microsoft YaHei",
            "font_size_header": 20,
            "font_size_definition": 16,
            "color_background": "#2E2E2E",
            "color_foreground": "#F0F0F0",
            "color_word": "#88D8FF",
            "color_reading": "#90EE90",
        }
    }

    def __init__(self):
        self.load()

    def load(self):
        parser = configparser.ConfigParser()
        parser.read(paths.config_path, encoding="utf-8")
        for section, values in self._SCHEMA.items():
            for key, default in values.items():
                if parser.has_option(section, key):
                    if isinstance(default, bool):
                        value = parser.getboolean(section, key)
                    elif isinstance(default, int):
                        value = parser.getint(section, key)
                    elif isinstance(default, float):
                        value = parser.getfloat(section, key)
                    else:
                        value = parser.get(section, key)
                else:
                    value = default
                setattr(self, key, value)
        if not os.path.exists(paths.config_path):
            self.save()

    def save(self):
        parser = configparser.ConfigParser()
        for section, values in self._SCHEMA.items():
            parser.add_section(section)
            for key in values:
                value = getattr(self, key)
                parser.set(section, key, str(value).lower() if isinstance(value, bool) else str(value))
        os.makedirs(os.path.dirname(paths.config_path), exist_ok=True)
        with open(paths.config_path, "w", encoding="utf-8") as f:
            parser.write(f)

    @property
    def resolved_debug_dir(self):
        return self.debug_dir or paths.debug_dir


config = Config()
