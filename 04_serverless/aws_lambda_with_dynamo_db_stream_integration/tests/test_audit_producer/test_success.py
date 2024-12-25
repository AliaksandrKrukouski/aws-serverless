from unittest.mock import MagicMock, patch

from tests.test_audit_producer import AuditProducerLambdaTestCase


class TestSuccess(AuditProducerLambdaTestCase):

    @patch('src.lambdas.audit_producer.handler.boto3.resource')
    def test_success(self, mock_boto_resource):
        mock_resource = MagicMock()
        mock_boto_resource.return_value = mock_resource

        mock_table = MagicMock()
        mock_resource.Table.return_value = mock_table
        mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        mock_event = {
            "Records": [
                {
                    "dynamodb": {
                        "Keys": {
                            "key": {
                                "S": "test_id"
                            }
                        },
                        "ApproximateCreationDateTime": 1616560000,
                        "NewImage": {
                            "key": {
                                "S": "test_key"
                            },
                            "value": {
                                "S": "test_value"
                            }
                        }
                    },
                    "eventName": "INSERT"
                }
            ]
        }

        self.assertEqual(self.HANDLER.handle_request(mock_event, dict()), 200)

