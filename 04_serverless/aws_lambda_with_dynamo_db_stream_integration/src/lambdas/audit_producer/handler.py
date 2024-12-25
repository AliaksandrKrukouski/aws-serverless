import boto3
import os
import uuid

from datetime import datetime

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TARGET_TABLE = os.environ.get('target_table')

class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        dynamo_db = boto3.client('dynamodb')

        _LOG.info("Received event: %s", event)

        for record in event.get('Records'):
            item_id = str(uuid.uuid4())
            item_key = record["dynamodb"]["Keys"]["key"]["S"]
            modification_time = \
                datetime.utcfromtimestamp(record["dynamodb"]["ApproximateCreationDateTime"]).strftime(DATE_FORMAT)
            event_name = record["eventName"]

            item = {
                'id': {"S": item_id},
                'itemKey': {"S": item_key},
                'modificationTime': {"S": modification_time}
            }

            if event_name == "INSERT":
                _LOG.info("Insert event")

                new_image = record["dynamodb"]["NewImage"]
                item["newValue"] = {
                    "M": new_image
                }
            elif event_name == "MODIFY":
                _LOG.info("Modify event")

                item["updatedAttribute"] = {"S": "value"}
                item["oldValue"] = record["dynamodb"]["OldImage"]["value"]
                item["newValue"] = record["dynamodb"]["NewImage"]["value"]
            else:
                raise ValueError(f"Unsupported event type: {record.get('eventName')}")

            _LOG.info("Put item: %s", item)
            response = dynamo_db.put_item(TableName=TARGET_TABLE, Item=item)

            _LOG.info("Response: %s", response)

        return 200
    

HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
