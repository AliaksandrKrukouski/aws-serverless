import boto3
import json

PRODUCTS_TABLE_NAME = 'cmtr-e858adde-dynamodb-l-table-products'
STOCKS_TABLE_NAME = 'cmtr-e858adde-dynamodb-l-table-stocks'


def lambda_handler(event, context):
    uuid = '14ba3d6a-a5ed-491b-a128-0a32b71a38c4'

    if 'headers' in event and 'random-uuid' in event["headers"]:
        uuid += f'-{event["headers"]["random-uuid"]}'

    dynamodb = boto3.client('dynamodb')
    products_key = {
        'id': {'S': uuid}
    }

    stocks_key = {
        'product_id': {'S': uuid}
    }

    # Retrieve from products table
    product_response = dynamodb.get_item(
        TableName=PRODUCTS_TABLE_NAME,
        Key=products_key
    )
    product = product_response.get('Item')

    # Retrieve from stocks table
    stocks_response = dynamodb.get_item(
        TableName=STOCKS_TABLE_NAME,
        Key=stocks_key
    )
    stock = stocks_response.get('Item')

    # Combine results
    result = product.copy()
    result['count'] = stock['count']

    return result
