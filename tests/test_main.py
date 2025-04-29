import pytest
from unittest.mock import patch, MagicMock
import requests

from my_package.main import fetch_data


def test_fetch_data_success():
    """Tests successful data fetching."""
    # Ожидаемые данные
    expected_data = {"userId": 1, "id": 1, "title": "Test title", "completed": False}
    test_url = "https://test-url.com/success"
    test_timeout = 15

    mock_response = MagicMock()
    mock_response.json.return_value = expected_data
    mock_response.raise_for_status.return_value = None

    with patch("my_package.main.requests.get", return_value=mock_response) as mock_get:
        result = fetch_data(test_url, timeout=test_timeout)

        assert result == expected_data

        mock_get.assert_called_once_with(test_url, timeout=test_timeout)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()


def test_fetch_data_timeout():
    """Tests handling of requests.exceptions.Timeout."""
    test_url = "https://test-url.com/timeout"
    test_timeout = 5

    with patch("my_package.main.requests.get", side_effect=requests.exceptions.Timeout) as mock_get:
        with pytest.raises(requests.exceptions.Timeout):
            fetch_data(test_url, timeout=test_timeout)

        mock_get.assert_called_once_with(test_url, timeout=test_timeout)


def test_fetch_data_http_error():
    """Tests handling of HTTP errors via raise_for_status."""
    test_url = "https://test-url.com/notfound"
    test_timeout = 10

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("my_package.main.requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(requests.exceptions.RequestException):
            fetch_data(test_url, timeout=test_timeout)

        mock_get.assert_called_once_with(test_url, timeout=test_timeout)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_not_called()


def test_fetch_data_json_decode_error():
    """Tests handling of JSONDecodeError."""
    test_url = "https://test-url.com/badjson"
    test_timeout = 10

    # Create mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    error_msg = "Expecting value"
    error_doc = ""
    error_pos = 0
    json_error = requests.exceptions.JSONDecodeError(error_msg, error_doc, error_pos)

    mock_response.json.side_effect = json_error

    with patch("my_package.main.requests.get", return_value=mock_response) as mock_get:
        # Check that the function raises RequestException (base class for JSONDecodeError in requests)
        with pytest.raises(requests.exceptions.RequestException):
            fetch_data(test_url, timeout=test_timeout)

        mock_get.assert_called_once_with(test_url, timeout=test_timeout)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()
