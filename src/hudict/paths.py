import os

from platformdirs import PlatformDirs


class Paths:
    def __init__(self):
        self._dirs = PlatformDirs("HUDict", appauthor=False, ensure_exists=True)

    @property
    def data_dir(self):
        return self._dirs.user_data_dir

    @property
    def config_path(self):
        return os.path.join(self._dirs.user_config_dir, "config.ini")

    @property
    def dictionary_path(self):
        return os.path.join(self.data_dir, "dictionary.pkl")

    @property
    def debug_dir(self):
        return os.path.join(self.data_dir, "debug")


paths = Paths()
