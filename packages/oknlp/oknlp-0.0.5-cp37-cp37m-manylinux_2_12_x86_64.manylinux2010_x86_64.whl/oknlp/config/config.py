import os
import yaml

HOME = os.path.expanduser("~")
CONFIG_FILE = ".oknlp.config.yaml"
DEFAULT_CONFIG = {
    "path": os.path.join(HOME, ".oknlp"),
    "source": "https://data.thunlp.org/ink/"
}


class Config:
    """
    Attributes:
        path: str
        source: str, data source url ending with "/"
    """

    def __init__(self):
        self.path = DEFAULT_CONFIG["path"]
        self.source = DEFAULT_CONFIG["source"]     
        self.set_config_from_file(HOME)
        self.set_config_from_file("")
        self.create_default_config_file()

    def create_default_config_file(self):
        file_path = os.path.join(HOME, CONFIG_FILE)
        if os.path.exists(file_path):
            return
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                yaml.dump(DEFAULT_CONFIG, file)
        except OSError:
            pass

    def set_config_from_file(self, directory: str):
        file_path = os.path.join(directory, CONFIG_FILE)
        config_data = {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                config_data = yaml.load(file, Loader=yaml.FullLoader)
        except OSError:
            pass
        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
