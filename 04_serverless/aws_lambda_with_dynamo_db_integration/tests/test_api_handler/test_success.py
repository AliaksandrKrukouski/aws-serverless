from tests.test_api_handler import ApiHandlerLambdaTestCase
from unittest.mock import MagicMock, patch

class TestSuccess(ApiHandlerLambdaTestCase):

    @patch('src.lambdas.api_handler.handler.boto3.client')
    def test_success(self, mock_boto_client):
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        mock_event = {
            'principalId': 'test_principal_id',
            'content': {
                'key1': {'S': 'value1'},
                'key2': {'S': 'value2'}
            }
        }

        self.assertEqual(self.HANDLER.handle_request(mock_event, dict())["statusCode"], 201)

