from tests.test_api_handler import ApiHandlerLambdaTestCase
from unittest.mock import MagicMock, patch

class TestSuccess(ApiHandlerLambdaTestCase):

    @patch('src.lambdas.api_handler.handler.boto3.resource')
    def test_success(self, mock_boto_resource):
        mock_resource = MagicMock()
        mock_boto_resource.return_value = mock_resource

        mock_table = MagicMock()
        mock_resource.Table.return_value = mock_table
        mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        mock_event = {
            'principalId': 'test_principal_id',
            'content': {
                'key1':  'value1',
                'key2': 'value2'
            }
        }

        self.assertEqual(self.HANDLER.handle_request(mock_event, dict())["statusCode"], 201)

