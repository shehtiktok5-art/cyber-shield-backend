"""Configuration management for CYBER-SHIELD Backend"""

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings"""

    # App Settings
    APP_NAME: str = "CYBER-SHIELD Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    DEMO_MODE: bool = Field(default=True, env="DEMO_MODE")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")

    # API Settings
    API_V1_STR: str = "/api/v1"
    FRONTEND_URL: str = Field(default="https://saudi.oneapp.dev", env="FRONTEND_URL")
    BACKEND_CORS_ORIGINS: list = [
        "https://saudi.oneapp.dev",
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Database - PostgreSQL
    DATABASE_URL: str = Field(
        default="postgresql://cybershield:password@localhost:5432/cybershield",
        env="DATABASE_URL"
    )
    DB_POOL_SIZE: int = Field(default=20, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=10, env="DB_MAX_OVERFLOW")
    DB_ECHO: bool = Field(default=False, env="DB_ECHO")

    # Database - Elasticsearch
    ELASTICSEARCH_URL: str = Field(
        default="http://localhost:9200",
        env="ELASTICSEARCH_URL"
    )
    ELASTICSEARCH_INDEX_PREFIX: str = "cybershield"

    # Database - Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    REDIS_CACHE_TTL: int = Field(default=3600, env="REDIS_CACHE_TTL")

    # JWT Authentication
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production-min-32-chars",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # Celery Configuration
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        env="CELERY_BROKER_URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        env="CELERY_RESULT_BACKEND"
    )
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: bool = True
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 30 * 60

    # Threat Intelligence APIs
    MISP_URL: str = Field(default="http://localhost:8080", env="MISP_URL")
    MISP_API_KEY: str = Field(default="test-key", env="MISP_API_KEY")
    
    OTX_API_KEY: str = Field(default="", env="OTX_API_KEY")
    OTX_BASE_URL: str = "https://otx.alienvault.com/api/v1"
    
    VIRUSTOTAL_API_KEY: str = Field(default="", env="VIRUSTOTAL_API_KEY")
    VIRUSTOTAL_BASE_URL: str = "https://www.virustotal.com/api/v3"
    
    SHODAN_API_KEY: str = Field(default="", env="SHODAN_API_KEY")
    ABUSEIPDB_API_KEY: str = Field(default="", env="ABUSEIPDB_API_KEY")

    # Suricata IDS Integration
    SURICATA_ENABLED: bool = Field(default=False, env="SURICATA_ENABLED")
    SURICATA_EVE_LOG_PATH: str = Field(
        default="/var/log/suricata/eve.json",
        env="SURICATA_EVE_LOG_PATH"
    )
    SURICATA_UNIX_SOCKET: str = Field(
        default="/var/run/suricata/suricata-command.socket",
        env="SURICATA_UNIX_SOCKET"
    )
    SURICATA_CONFIG_PATH: str = Field(
        default="/etc/suricata/suricata.yaml",
        env="SURICATA_CONFIG_PATH"
    )

    # Zeek Integration
    ZEEK_ENABLED: bool = Field(default=False, env="ZEEK_ENABLED")
    ZEEK_LOG_DIR: str = Field(
        default="/var/log/zeek",
        env="ZEEK_LOG_DIR"
    )

    # Network Monitoring
    PACKET_CAPTURE_ENABLED: bool = Field(default=False, env="PACKET_CAPTURE_ENABLED")
    PACKET_CAPTURE_INTERFACE: str = Field(default="eth0", env="PACKET_CAPTURE_INTERFACE")
    PACKET_CAPTURE_FILTER: str = "tcp or udp"

    # ML Model Settings
    ML_MODEL_PATH: str = Field(default="./models", env="ML_MODEL_PATH")
    ML_TRAINING_ENABLED: bool = Field(default=False, env="ML_TRAINING_ENABLED")
    ML_BATCH_SIZE: int = Field(default=32, env="ML_BATCH_SIZE")
    ML_EPOCHS: int = Field(default=10, env="ML_EPOCHS")
    ML_LOOKBACK_DAYS: int = Field(default=30, env="ML_LOOKBACK_DAYS")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = "json"
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")

    # Monitoring
    PROMETHEUS_METRICS_ENABLED: bool = Field(default=True, env="PROMETHEUS_METRICS_ENABLED")
    PROMETHEUS_PORT: int = Field(default=8001, env="PROMETHEUS_PORT")

    # Security
    ENABLE_HTTPS: bool = Field(default=False, env="ENABLE_HTTPS")
    SSL_CERT_PATH: Optional[str] = Field(default=None, env="SSL_CERT_PATH")
    SSL_KEY_PATH: Optional[str] = Field(default=None, env="SSL_KEY_PATH")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_REQUESTS_PER_MINUTE")

    # Data Retention
    DATA_RETENTION_DAYS: int = Field(default=90, env="DATA_RETENTION_DAYS")
    ALERT_RETENTION_DAYS: int = Field(default=180, env="ALERT_RETENTION_DAYS")
    INCIDENT_RETENTION_DAYS: int = Field(default=365, env="INCIDENT_RETENTION_DAYS")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
