from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('HelloWorld-handler')


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']

        success_result = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
        }

        bad_result = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": {
                "statusCode": 400,
                "message": f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
            }
        }

        result = success_result if method == 'GET' and path == '/hello' else bad_result

        return result

HANDLER = HelloWorld()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
