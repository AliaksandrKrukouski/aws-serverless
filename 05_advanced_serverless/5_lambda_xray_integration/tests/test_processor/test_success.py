from unittest.mock import patch, MagicMock

from tests.test_processor import ProcessorLambdaTestCase


class TestSuccess(ProcessorLambdaTestCase):

    @patch("lambdas.processor.handler.requests")
    @patch("lambdas.processor.handler.boto3.client")
    def test_success(self, mock_boto_client, mock_requests):
        mock_boto_client.put_item.return_value = {}

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "elevation": 10,
            "generationtime_ms": 100,
            "hourly": {
                "temperature_2m": [20],
                "time": ["2021-01-01T00:00:00Z"]
            },
            "hourly_units": {
                "temperature_2m": 30,
                "time": "2021-01-01T00:00:00Z"
            },
            "latitude": 40,
            "longitude": 50
        }
        mock_requests.get.return_value = mock_response


        self.assertEqual(self.HANDLER.handle_request(dict(), dict()), 200)

