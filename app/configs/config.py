import os
import logging


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


class InternalConfig:
    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    ASSETS_DIR_PATH = os.environ.get("ASSETS_DIR_PATH", "assets")
