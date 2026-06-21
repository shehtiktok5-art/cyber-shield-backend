"""Logging configuration for CYBER-SHIELD Backend"""

import logging
import json
from typing import Optional
from pythonjsonlogger import jsonlogger

from src.config import get_settings

settings = get_settings()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""
    
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = record.created
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['service'] = settings.APP_NAME


def setup_logging():
    """Setup logging configuration"""
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    
    if settings.LOG_FORMAT == "json":
        formatter = CustomJsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s'
        )
    else:
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
