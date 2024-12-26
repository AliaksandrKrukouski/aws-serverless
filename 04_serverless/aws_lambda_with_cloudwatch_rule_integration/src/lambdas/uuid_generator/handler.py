import os
import uuid
from datetime import datetime

import boto3

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('UuidGenerator-handler')

TARGET_BUCKET = os.environ.get('target_bucket')

class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info('Event received: %s', event)

        filename = datetime.now().isoformat()[:-3] + 'Z'
        data = {'ids': [str(uuid.uuid4()) for i in range(10)]}

        _LOG.info('Initialising s3 client')
        s3_client = boto3.client('s3')

        _LOG.info('Uploading data to s3://%s/%s', TARGET_BUCKET, filename)
        response = s3_client.put_object(Bucket=TARGET_BUCKET, Key=filename, Body=str(data))

        _LOG.info('Response: %s', response)

        return 200
    

HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
