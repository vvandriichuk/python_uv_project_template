import logging
import sys
import traceback
from typing import Any

import requests

from config.logger.logging_setup import setup_logging
from config.settings.setup import AppSettings, load_app_settings
from my_package.utils import process_data_util

try:
    print("INFO: Loading application settings...", file=sys.stderr)
    app_settings: AppSettings = load_app_settings()
    print("INFO: Application settings loaded successfully.", file=sys.stderr)
except Exception as settings_err:
    print(f"CRITICAL: Failed to load application settings: {settings_err}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

try:
    print("INFO: Configuring logging system...", file=sys.stderr)
    setup_logging(core_settings=app_settings.core)
except Exception as setup_err:
    print(f"CRITICAL: Failed during logging setup: {setup_err}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

_logger = logging.getLogger(__name__)

_logger.info("Logging system initialized successfully.")
_logger.debug(f"Running in '{app_settings.core.ENVIRONMENT.value}' environment.")
if app_settings.mypackage.DEBUG_MODE:
    _logger.debug("Debug mode is enabled.")


def fetch_data(url: str, timeout: int) -> dict[str, Any]:
    """Fetch data from a given URL using configured timeout."""
    _logger.debug(f"Fetching data from URL: {url} with timeout: {timeout}s")
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        result: dict[str, Any] = response.json()
    except requests.exceptions.Timeout:
        _logger.error(f"Request timed out after {timeout}s for URL: {url}")
        raise
    except requests.exceptions.RequestException as e:
        _logger.error(f"Error fetching data from {url}: {e}")
        raise
    else:
        _logger.debug(f"Successfully fetched data from {url}")
        return result


def main() -> None:
    """Run the main application."""
    _logger.info("Application starting...")

    api_url = str(app_settings.mypackage.API_BASE_URL).rstrip("/") + "/todos/1"
    timeout = app_settings.mypackage.REQUEST_TIMEOUT

    try:
        _logger.info(f"Attempting to fetch data from: {api_url}")
        data = fetch_data(url=api_url, timeout=timeout)
        _logger.info(f"Fetched data: {data}")

        processing_result = process_data_util(data)
        _logger.info(f"Processing result from utils: {processing_result}")

    except Exception:
        _logger.exception("An error occurred during main execution:")

    _logger.info("Application finished.")


if __name__ == "__main__":
    main()
