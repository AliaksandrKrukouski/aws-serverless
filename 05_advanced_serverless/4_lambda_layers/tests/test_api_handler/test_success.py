from unittest.mock import patch
from tests.test_api_handler import ApiHandlerLambdaTestCase

from pathlib import Path

class TestSuccess(ApiHandlerLambdaTestCase):
    @patch('lambdas.api_handler.handler.get_weather_forecast')
    def test_success(self, requests_mock):
        mock_response = {
            "latitude": 52.52,
            "longitude": 13.41,
            "timezone": "Europe/Berlin",
            "current": {
                "temperature_2m": 22.9,
                "wind_speed_10m": 5.7
            }
        }
        requests_mock.return_value = mock_response

        actual_result = self.HANDLER.handle_request(dict(), dict())
        print("actual_result:\n", actual_result)

        self.assertEqual(actual_result, mock_response)

