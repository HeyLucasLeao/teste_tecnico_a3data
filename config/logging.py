# -*- coding: utf-8 -*-
"""Pipeline configuration."""
from pydantic_settings import BaseSettings


class Pipeline(BaseSettings):
    LOGGING_LEVEL: str = "DEBUG"

    class Config:
        """Config sub-class needed to customize BaseSettings settings.

        More details can be found in pydantic documentation:
        https://pydantic-docs.helpmanual.io/usage/settings/

        """

        case_sensitive = True
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Pipeline()
