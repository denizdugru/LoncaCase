import os


class InternalConfig:
    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    ASSETS_DIR_PATH = os.environ.get("ASSETS_DIR_PATH", "assets")
