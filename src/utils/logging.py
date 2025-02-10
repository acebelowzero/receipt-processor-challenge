"""Tracks logging within the app"""

import logging.config
import yaml
from src.utils.config import settings


def setup_logging():
    """Setups the global logger from reading in the
    logging.conf config
    """
    with open(settings.LOG_CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
