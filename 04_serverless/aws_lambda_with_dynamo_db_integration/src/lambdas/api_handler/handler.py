import os

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

import boto3
from datetime import datetime
import uuid


_LOG = get_logger('ApiHandler-handler')

DB_TABLE_NAME = os.environ.get('target_table')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info("Input event: %s", event)

        dynamo_db = boto3.resource('dynamodb')
        dynamo_table = dynamo_db.Table(DB_TABLE_NAME)

        item_id = str(uuid.uuid4())
        principal_id = event['principalId']
        created_at = datetime.utcnow().isoformat()[:-3] + "Z"
        body = event['content']

        item = {
            'id': item_id,
            'principalId': principal_id,
            'createdAt': created_at,
            'body': body
        }

        _LOG.info("Put item: %s", item)
        response = dynamo_table.put_item(Item=item)

        _LOG.info("Response: %s", response)

        return {
            "statusCode": 201,
            "event": {
                "id": item_id,
                "principalId": principal_id,
                "createdAt": created_at,
                "body": body
            }
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
