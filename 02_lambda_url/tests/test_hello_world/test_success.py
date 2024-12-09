from tests.test_hello_world import HelloWorldLambdaTestCase


class TestSuccess(HelloWorldLambdaTestCase):

    def test_success(self):

        event = {
            'requestContext': {
                'http': {
                    'method': 'GET',
                    'path': '/hello'
                }
            }
        }

        expected_result = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
        }

        self.assertEqual(self.HANDLER.handle_request(event, dict()), expected_result)

