import os
import logging
from logging.handlers import RotatingFileHandler


def configure_logging():
    """
    This function is used for configuring the root logger
    """
    # Configure the root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create a file handler for the .log file
    file_handler = RotatingFileHandler(
        os.path.join(InternalConfig.ASSETS_DIR_PATH, "app.log"),
        maxBytes=1024 * 1024,
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    # Add the file handler to the root logger
    logging.getLogger("").addHandler(file_handler)


class InternalConfig:
    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    ASSETS_DIR_PATH = os.environ.get("ASSETS_DIR_PATH", "assets")
