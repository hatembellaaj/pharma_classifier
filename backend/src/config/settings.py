"""Centralized configuration using pydantic settings."""
from __future__ import annotations

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    env: str = Field(default="development", alias="ENV")
    data_dir: str = Field(default="/app/data", alias="DATA_DIR")
    model_path: str = Field(default="/app/models/model.onnx", alias="MODEL_PATH")
    history_path: str = Field(default="/app/data/history.csv", alias="HISTORY_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> AppSettings:
    """Return cached settings instance."""
    return AppSettings()
