import os


class Paths:
    @property
    def app_dir(self):
        return os.getcwd()

    @property
    def data_dir(self):
        return self.app_dir

    @property
    def config_path(self):
        return os.path.join(self.app_dir, "config.ini")

    @property
    def dictionary_path(self):
        return os.path.join(self.data_dir, "dictionary.pkl")

    @property
    def debug_dir(self):
        return os.path.join(self.data_dir, "debug")


paths = Paths()
