import logging
import os
from datetime import datetime
from config.logging import settings


class InotifyFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return "in-event" not in message and "InotifyEvent" not in message


def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = (
        f"{log_dir}/epi_assistant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger()
    logger.setLevel(settings.LOGGING_LEVEL)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    inotify_filter = InotifyFilter()
    file_handler.addFilter(inotify_filter)
    console_handler.addFilter(inotify_filter)

    return logger


logger = setup_logger()
logger.addFilter(InotifyFilter())
