import os
import uuid

import boto3
import requests

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('Processor-handler')

TARGET_TABLE = os.environ.get('TARGET_TABLE')
URL = os.environ.get('URL')

class Processor(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info('Processing event: %s', event)

        dynamodb_client = boto3.client('dynamodb')

        _LOG.info('Making request to URL: %s', URL)
        response = requests.get(URL)
        data = response.json()

        item = {
            "id": {
                "S": str(uuid.uuid4())
            },
            "forecast": {
                "M": {
                    "elevation": {
                        "N": str(data.get("elevation"))
                    },
                    "generationtime_ms": {
                        "N": str(data.get("generationtime_ms"))
                    },
                    "hourly": {
                        "M": {
                            "temperature_2m": {"L": [{"N": str(t)} for t in data.get("hourly").get("temperature_2m")]},
                            "time": {"L": [{"S": t} for t in data.get("hourly").get("time")]}
                        }
                    },
                    "hourly_units": {
                        "M": {
                            "temperature_2m": {"S": data.get("hourly_units").get("temperature_2m")},
                            "time": {"S": data.get("hourly_units").get("time")}
                        }
                    },
                    "latitude": {
                        "N": str(data.get("latitude"))
                    },
                    "longitude": {
                        "N": str(data.get("longitude"))
                    },
                    "timezone": {
                        "S": data.get("timezone")
                    },
                    "timezone_abbreviation": {
                        "S": data.get("timezone_abbreviation")
                    },
                    "utc_offset_seconds": {
                        "N": str(data.get("utc_offset_seconds"))
                    }
                }
            }
        }

        _LOG.info('Put item: %s', item)
        response = dynamodb_client.put_item(TableName=TARGET_TABLE, Item=item)

        _LOG.info('Response: %s', response)

        return 200
    

HANDLER = Processor()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
