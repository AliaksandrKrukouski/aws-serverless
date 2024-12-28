import boto3
import json

PRODUCTS_TABLE_NAME = 'cmtr-e858adde-dynamodb-l-table-products'
STOCKS_TABLE_NAME = 'cmtr-e858adde-dynamodb-l-table-stocks'

def lambda_handler(event, context):
    uuid = '14ba3d6a-a5ed-491b-a128-0a32b71a38c4'

    if 'headers' in event and 'random-uuid' in event["headers"]:
        uuid += f'-{event["headers"]["random-uuid"]}'

    dynamodb = boto3.client('dynamodb')
    product_item = {
        'id': {'S': uuid},
        'title': {'S': 'Product Title'},
        'description': {'S': 'This product ...'},
        'price': {'N': '200'}
    }

    stock_item = {
        'product_id': {'S': uuid},
        'count': {'N': '2'}
    }

    # Insert into products table
    dynamodb.put_item(
        TableName=PRODUCTS_TABLE_NAME,
        Item=product_item
    )

    # Insert into stocks table
    dynamodb.put_item(
        TableName=STOCKS_TABLE_NAME,
        Item=stock_item
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Entry created successfully!')
    }