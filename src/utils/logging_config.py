"""Logging configuration for CYBER-SHIELD Backend"""

import logging
import json
from typing import Optional

from src.config import get_settings

settings = get_settings()


def setup_logging():
    """Setup logging configuration"""
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    if settings.LOG_FILE:
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setLevel(settings.LOG_LEVEL)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger
