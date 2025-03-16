import pytest
from unittest.mock import patch, MagicMock
from my_package.main import fetch_data


def test_fetch_data():
    # Create a mock object to simulate the requests response
    mock_response = MagicMock()
    mock_response.json.return_value = {"userId": 1, "id": 1, "title": "Test title", "completed": False}

    # Let's patch the requests.get method so that it returns our mock
    with patch("requests.get", return_value=mock_response) as mock_get:
        # Call the function under test
        result = fetch_data("https://test-url.com")

        # Check that the function returned the correct result
        assert result == {"userId": 1, "id": 1, "title": "Test title", "completed": False}

        # Check that requests.get was called with the correct URL and timeout
        mock_get.assert_called_once_with("https://test-url.com", timeout=30)
