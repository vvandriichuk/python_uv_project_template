import logging
import logging.config
import sys
import traceback
from pathlib import Path

from config.enums.enums import Env
from config.settings.setup import CoreSettings

logger = logging.getLogger(__name__)

# Classification of environments for Fallback
PRODUCTION_LIKE_ENVS = {
    Env.DEVELOPMENT,
}

# Constants for Fallback
FALLBACK_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] [%(name)s:%(lineno)d] %(message)s"

# Constants for third-party loggers
THIRD_PARTY_LOGGERS: dict[str, int] = {}

# Automatically detect project root
try:
    # Using pathlib to determine the root
    DEFAULT_PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent.parent.parent
    DEFAULT_PROJECT_ROOT = str(DEFAULT_PROJECT_ROOT_PATH)
except Exception as e:
    print(f"CRITICAL ERROR: Could not automatically determine project root from {__file__}: {e}", file=sys.stderr)
    sys.exit(1)


def sanitize_filename(name: str) -> str:
    """Replaces characters that are unwanted in a file name (such as /)."""
    return name.replace("/", "-")


def setup_logging(core_settings: CoreSettings) -> None:
    """
    Configures the Python logging system.

    1. Determines the project root (automatically or from settings.core.ROOT_PATH).
    2. Generates the name of the configuration file (logging-*.conf) based on the current
    environment (settings.core.ENVIRONMENT).
    3. Searches for this file in the directory <project_root>/src/config/logger/logging-conf/.
    4. If the file is found, loads the configuration from it.
    5. If the file is not found or an error occurs while loading, uses the
    fallback configuration (logging.basicConfig), whose parameters (level,
    output stream) depend on the type of the current environment
    (production-like or development).
    6. After successfully loading the configuration file, forcibly sets
       the logging levels for known third-party libraries.
    """
    config_loaded_successfully = False
    config_path_str: str | None = None
    used_fallback = False
    current_env: Env = core_settings.ENVIRONMENT

    try:
        project_root_str: str = str(core_settings.ROOT_PATH) if core_settings.ROOT_PATH else DEFAULT_PROJECT_ROOT
        if core_settings.ROOT_PATH:
            print(f"INFO: Using explicit ROOT_PATH from settings: {project_root_str}", file=sys.stderr)

        conf_folder_path = Path(project_root_str) / "config" / "logger" / "logging-conf"

        sanitized_env_name = sanitize_filename(current_env)
        config_filename = f"logging-{sanitized_env_name}.conf"
        config_path = conf_folder_path / config_filename
        config_path_str = str(config_path)

        if config_path.exists() and config_path.is_file():
            logging.config.fileConfig(fname=config_path, disable_existing_loggers=False, encoding="utf-8")
            print(
                f"INFO: Logging configured successfully from: {config_path_str} for environment '{current_env}'",
                file=sys.stdout,
            )
            config_loaded_successfully = True

            # Setting up third-party library levels
            for logger_name, level in THIRD_PARTY_LOGGERS.items():
                try:
                    logging.getLogger(logger_name).setLevel(level)
                except Exception as e_set_level:
                    print(
                        f"ERROR: Failed to set level {level} for logger '{logger_name}': {e_set_level}", file=sys.stderr
                    )
                    traceback.print_exc(file=sys.stderr)

            # Successful setup message
            logging.getLogger().info(
                f"Logging configured from file: {config_path_str}. "
                f"Environment: '{current_env}'. "
                f"Third-party loggers adjusted."
            )

        else:
            # Missing file warning
            print(
                f"WARNING: Logging configuration file not found for environment "
                f"'{current_env}' at {config_path_str}. "
                f"Using basic fallback config.",
                file=sys.stderr,
            )
            used_fallback = True

    except Exception as e:
        # Critical error message
        print(
            f"CRITICAL: Error processing logging configuration. "
            f"Env='{current_env}', Path='{config_path_str}'. Error='{e}'. "
            f"Using basic fallback config.",
            file=sys.stderr,
        )
        traceback.print_exc(file=sys.stderr)
        used_fallback = True

    # Fallback configuration
    if used_fallback or not config_loaded_successfully:
        is_prod_like = current_env in PRODUCTION_LIKE_ENVS
        fallback_level = logging.INFO if is_prod_like else logging.DEBUG
        fallback_stream = sys.stdout if is_prod_like else sys.stderr

        logging.basicConfig(level=fallback_level, format=FALLBACK_LOG_FORMAT, stream=fallback_stream, force=True)

        # Messages about using fallback
        logger.warning(
            f"Using basic fallback logging configuration "
            f"(Level: {logging.getLevelName(fallback_level)}, Output: {fallback_stream.name})."
        )
        if config_path_str:
            logger.warning(f"Attempted to load configuration for env '{current_env}' from: {config_path_str}")
        elif not config_path_str and used_fallback:
            logger.warning(f"Could not determine or process config path for env '{current_env}'.")
