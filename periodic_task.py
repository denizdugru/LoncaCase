import schedule
import time
import logging

from app.logic._extractor import Extractor
from app.configs.config import InternalConfig, configure_logging

from mongoengine import connect

logger = logging.getLogger(__name__)

MONGO_URI = f"mongodb://{InternalConfig.MONGO_HOST}:27017/test"

# Create MongoDB instance
connect(host=MONGO_URI)


if __name__ == "__main__":
    configure_logging()
    logger.info("Initializing the extractor...")
    xml_extractor = Extractor()
    logger.info("Initializing the periodic XML extraction...")
    schedule.every(60).minutes.do(xml_extractor.extract_periodically)
    while True:
        schedule.run_pending()
