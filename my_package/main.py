from typing import Any

import requests


def fetch_data(url: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch data from a given URL.

    Args:
        url: The URL to fetch data from.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as a dictionary.
    """
    response = requests.get(url, timeout=timeout)
    result: dict[str, Any] = response.json()
    return result


def main() -> None:
    """Run the main application."""
    data = fetch_data("https://jsonplaceholder.typicode.com/todos/1")
    print(f"Fetched data: {data}")


if __name__ == "__main__":
    main()
