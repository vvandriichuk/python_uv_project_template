import logging
from typing import Any

_logger = logging.getLogger(__name__)


def process_data_util(data: dict[str, Any]) -> str:
    """
    Example utility function that logs messages.
    """
    _logger.debug(f"Received data for processing in util: {data}")

    if not data:
        _logger.warning("Received empty data dict.")
        return "No data processed."

    user_id = data.get("userId", "Unknown")
    item_id = data.get("id", "Unknown")
    title = data.get("title", "No Title")
    completed = data.get("completed", False)

    _logger.info(f"Processing item {item_id} for user {user_id}. Title: '{title}'. Completed: {completed}")

    result_message = f"Processed item {item_id} (User: {user_id}, Completed: {completed})"
    _logger.debug("Data processing finished in util.")

    return result_message
