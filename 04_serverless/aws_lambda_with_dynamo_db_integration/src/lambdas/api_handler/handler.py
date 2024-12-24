from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

import boto3
from datetime import datetime
import uuid


_LOG = get_logger('ApiHandler-handler')

DB_TABLE_NAME = 'cmtr-e858adde-Events'


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info("Input event: %s", event)

        client = boto3.client('dynamodb')

        item_id = str(uuid.uuid4())
        principal_id = event['principalId']
        created_at = datetime.utcnow().isoformat()[:-3] + "Z"
        content = event['content']

        item = {
            'id': {'S': item_id},
            'principalId': {'N': str(principal_id)},
            'createdAt': {'S': created_at},
            'body': {'M': {key: {'S': value} for key, value in content.items()}}
        }

        _LOG.info("Put item: %s", item)
        response = client.put_item(TableName=DB_TABLE_NAME,
                                   Item=item)

        _LOG.info("Response: %s", response)

        return {
            "statusCode": 201,
            "event": {
                "id": item_id,
                "principalId": principal_id,
                "createdAt": created_at,
                "body": content
            }
}


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
