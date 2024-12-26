from tests.test_uuid_generator import UuidGeneratorLambdaTestCase
from unittest.mock import patch, MagicMock


class TestSuccess(UuidGeneratorLambdaTestCase):

    @patch('src.lambdas.uuid_generator.handler.boto3.client')
    def test_success(self, mock_boto_client):
        mock_resource = MagicMock()
        mock_boto_client.return_value = mock_resource
        mock_resource.put_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        self.assertEqual(self.HANDLER.handle_request(dict(), dict()), 200)

