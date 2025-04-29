import sys
import traceback
from pathlib import Path

from pydantic import Field, HttpUrl, PositiveInt, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.enums.enums import Env

__all__ = ["AppSettings", "CoreSettings", "Env", "MyPackageSettings", "load_app_settings"]


class CoreSettings(BaseSettings):
    """Core application settings, primarily for environment."""

    ENVIRONMENT: Env = Field(default=Env.LOCAL)
    ROOT_PATH: Path | None = Field(default=None, description="Optional explicit project root path")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="CORE_")


class MyPackageSettings(BaseSettings):
    """Example settings specific to my_package."""

    API_BASE_URL: HttpUrl = Field(default="https://jsonplaceholder.typicode.com")  # type: ignore[assignment]
    REQUEST_TIMEOUT: PositiveInt = Field(default=10, description="Default request timeout in seconds.")
    DEBUG_MODE: bool = Field(default=False, description="Enable debug mode features.")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="MYPACKAGE_"
    )


class AppSettings(BaseSettings):
    """Main application settings container."""

    core: CoreSettings = CoreSettings()
    mypackage: MyPackageSettings = MyPackageSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",  # Can use CORE__ENVIRONMENT, MYPACKAGE__REQUEST_TIMEOUT
        env_file_encoding="utf-8",
        extra="ignore",
    )


def load_app_settings() -> AppSettings:
    """Loads, validates, and returns the application settings."""
    try:
        loaded_settings = AppSettings()
    except ValidationError as e:
        print("CRITICAL ERROR: Settings validation failed:", file=sys.stderr)
        print(e.json(indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize settings: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    else:
        return loaded_settings
