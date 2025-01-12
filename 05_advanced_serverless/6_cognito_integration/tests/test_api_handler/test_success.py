from unittest.mock import patch, MagicMock

from tests.test_api_handler import ApiHandlerLambdaTestCase


class TestSuccess(ApiHandlerLambdaTestCase):
    @patch("lambdas.api_handler.handler.boto3.client")
    @patch("lambdas.api_handler.handler.os")
    def test_success(self, mock_os, mock_boto_client):
        mock_os.environ = {
            'cup_id': 'test_user_pool_name',
            'cup_client_id': 'test_client_id',
        }

        mock_client = MagicMock()
        mock_client.list_user_pools.return_value = {"UserPools": [{"Name": "test_user_pool_name", "Id": "test_user_pool_id"}]}
        mock_client.admin_create_user.return_value = {}
        mock_boto_client.return_value = mock_client

        event = {
            "requestContext": {
                "resourcePath": "/signin",
                "httpMethod": "POST"
            },
            "body": '{ "firstName": "John", "lastName": "Doe", "email": "John.Doe@email.com", "password": "password"}'
        }

        self.assertEqual(self.HANDLER.handle_request(event, dict())["statusCode"], 200)
