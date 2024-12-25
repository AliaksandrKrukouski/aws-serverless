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
        dynamo_db = boto3.resource('dynamodb')
        dynamo_table = dynamo_db.Table(TARGET_TABLE)

        _LOG.info("Received event: %s", event)

        record = event.get('Records')[0]

        item_id = str(uuid.uuid4())
        item_key = record["dynamodb"]["Keys"]["key"]["S"]
        modification_time = \
            datetime.utcfromtimestamp(record["dynamodb"]["ApproximateCreationDateTime"]).strftime(DATE_FORMAT)
        event_name = record["eventName"]

        item = {
            'id': item_id,
            'itemKey': item_key,
            'modificationTime': modification_time
        }

        if event_name == "INSERT":
            _LOG.info("Insert event")

            key = record["dynamodb"]["NewImage"]["key"]["S"]
            value = record["dynamodb"]["NewImage"]["value"]

            item["newValue"] = {
                "key": key,
                "value": value.get("S", value.get("N"))
            }
        elif event_name == "MODIFY":
            _LOG.info("Modify event")

            old_value = record["dynamodb"]["OldImage"]["value"]
            new_value = record["dynamodb"]["NewImage"]["value"]

            item["updatedAttribute"] = "value"
            item["oldValue"] = old_value.get("S", old_value.get("N"))
            item["newValue"] = new_value.get("S", new_value.get("N"))
        else:
            raise ValueError(f"Unsupported event type: {record.get('eventName')}")

        _LOG.info("Put item: %s", item)
        response = dynamo_table.put_item(Item=item)

        _LOG.info("Response: %s", response)

        return 200
    

HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
