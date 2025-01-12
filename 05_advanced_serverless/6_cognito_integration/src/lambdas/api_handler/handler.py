import json
import os
import uuid

import boto3
from boto3.dynamodb.conditions import Key

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


def _signup(cognito_client, user_pool_id, client_id, details):
    _LOG.info("Signing up to %s user pool, %s client", user_pool_id, client_id)

    email = details.get("email", "")
    password = details.get("password", "")
    _LOG.info("Email: %s", email)
    _LOG.info("Password: %s", password)

    _LOG.info("Signing up user: %s", email)
    response = cognito_client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'email_verified',
                'Value': 'True'
            }
        ],
        TemporaryPassword=password,
        MessageAction='SUPPRESS'
    )
    _LOG.info("User successfully created: %s", response)

    return {"statusCode": 200}


def _signin(cognito_client, user_pool_id, client_id, details):
    _LOG.info("Signing in to %s user pool, %s client", user_pool_id, client_id)

    email = details.get("email", "")
    password = details.get("password", "")
    _LOG.info("Email: %s", email)
    _LOG.info("Password: %s", "****")

    response = cognito_client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password
        }
    )

    if response.get("ChallengeName", "") == "NEW_PASSWORD_REQUIRED":
        _LOG.info("A new password required: %s", response)
        response = cognito_client.admin_respond_to_auth_challenge(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            ChallengeResponses={
                'USERNAME': email,
                'NEW_PASSWORD': password
            },
            Session=response['Session']
        )

    _LOG.info("User successfully signed in: %s", response)

    access_token = response.get("AuthenticationResult", {}).get("IdToken", "")

    return {"statusCode": 200, "body": '{"accessToken": "' + access_token + '"}'}


def _build_tables_item(data):
    _LOG.info("Building tables item from data: %s", data)

    id_ = str(data.get("id", ""))
    number_ = str(data.get("number", ""))
    is_vip = data.get("isVip", "")
    min_order = str(data.get("minOrder", ""))
    _LOG.info("id: %s", id_)
    _LOG.info("number: %s", number_)
    _LOG.info("isVip: %s", is_vip)
    _LOG.info("minOrder: %s", min_order)

    item = {
        "id": {
            "N": id_
        },
        "number": {
            "N": number_
        },
        "isVip": {
            "BOOL": is_vip
        },
        "minOrder": {
            "N": min_order
        }
    }

    return item


def _build_reservations_item(data):
    _LOG.info("Building reservations item from data: %s", data)

    id_ = str(uuid.uuid4())
    table_number = str(data.get("tableNumber", ""))
    client_name = data.get("clientName", "")
    phone_number = data.get("phoneNumber", "")
    date = data.get("date", "")
    slot_time_start = data.get("slotTimeStart", "")
    slot_time_end = data.get("slotTimeEnd", "")

    _LOG.info("id: %s", id_)
    _LOG.info("table_number: %s", table_number)
    _LOG.info("client_name: %s", client_name)
    _LOG.info("phone_number: %s", phone_number)
    _LOG.info("date: %s", date)
    _LOG.info("slot_time_start: %s", slot_time_start)
    _LOG.info("slot_time_end: %s", slot_time_end)

    item = {
        "id": {
            "S": id_
        },
        "table_number": {
            "N": table_number
        },
        "client_name": {
            "S": client_name
        },
        "phone_number": {
            "S": phone_number
        },
        "date": {
            "S": date
        },
        "slot_time_start": {
            "S": slot_time_start
        },
        "slot_time_end": {
            "S": slot_time_end
        }
    }

    return item


def _build_tables_item_str_func(item):
    item_str = '{ ' + \
               '  "id": ' + str(item.get("id", "")) + \
               ', "number": ' + str(item.get("number", "")) + \
               ', "places": ' + str(item.get("places", "")) + \
               ', "isVip": ' + str(item.get("isVip", "")) + \
               ', "minOrder": ' + str(item.get("minOrder", "")) + \
               '}'
    return item_str


def _build_reservations_item_str_func(item):
    item_str = '{ ' + \
               '  "tableNumber": ' + str(item.get("table_number", "")) + \
               ', "clientName": "' + item.get("client_name", "") + '"' + \
               ', "phoneNumber": "' + item.get("phone_number", "") + '"' + \
               ', "date": "' + item.get("date", "") + '"' + \
               ', "slotTimeStart": "' + item.get("slot_time_start", "") + '"' + \
               ', "slotTimeEnd": "' + item.get("slot_time_end", "") + '"' + \
               '}'
    return item_str


def _post_table_item(dynamodb_client, table_name, item, callback_body_template):
    _LOG.info("Posting to %s table:\n%s", table_name, item)

    _LOG.info("Put item: %s", item)
    response = dynamodb_client.put_item(TableName=table_name, Item=item)

    _LOG.info('Response: %s', response)

    try:
        item_id = item["id"]["N"]
    except KeyError:
        item_id = item["id"]["S"]

    callback_body = callback_body_template % item_id

    return {"statusCode": 200, "body": callback_body}


def _get_table_items(dynamodb_resource, table_name, build_item_str_func, key_condition_expression=None):
    _LOG.info("Getting items from table", table_name)

    table_resource = dynamodb_resource.Table(table_name)

    if key_condition_expression:
        _LOG.info("Get items with key condition expression: %s", key_condition_expression)
        response = table_resource.query(KeyConditionExpression=key_condition_expression)
    else:
        _LOG.info("Get all items")
        response = table_resource.scan()

    _LOG.info("Response: %s", response)

    items = []
    for item in response.get("Items", []):
        item_str = build_item_str_func(item)

        _LOG.info("Item: %s", item_str)
        items.append(item_str)

    _LOG.info("Items: %s", items)

    if key_condition_expression:
        body = items[0]
    else:
        items_str = ', '.join(items)
        if table_name == os.environ['tables_table']:
            body = '{"tables": [' + items_str + ']}'
        elif table_name == os.environ['reservations_table']:
            body = '{"reservations": [' + items_str + ']}'
        else:
            raise Exception(f"Unsupported table name: {table_name}")

    _LOG.info("Body: %s", body)

    return {"statusCode": 200, "body": body}


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info("Event: %s", event)
        _LOG.info("Context: %s", context)

        cognito_client = boto3.client('cognito-idp')
        dynamodb_client = boto3.client('dynamodb')
        dynamodb_resource = boto3.resource('dynamodb')

        request_context = event.get("requestContext", {})
        resource_path = request_context.get("resourcePath", "")
        http_method = request_context.get("httpMethod", "")
        _LOG.info("Resource path: %s", resource_path)
        _LOG.info("HTTP method: %s", http_method)

        body = json.loads(event.get("body", "{}") or "{}")
        _LOG.info("Body: %s", body)

        user_pool_id = os.environ['cup_id']
        client_id = os.environ['cup_client_id']
        _LOG.info("User pool id: %s", user_pool_id)

        try:
            if resource_path == "/signup" and http_method == "POST":
                result = _signup(cognito_client, user_pool_id, client_id, body)
            elif resource_path == "/signin" and http_method == "POST":
                result = _signin(cognito_client, user_pool_id, client_id, body)
            elif resource_path == "/tables" and http_method == "POST":
                table_name = os.environ['tables_table']
                table_item = _build_tables_item(body)
                result = _post_table_item(dynamodb_client, table_name, table_item, '{"id": %s}')
            elif resource_path.startswith("/tables") and http_method == "GET":
                table_name = os.environ['tables_table']

                path_parameters = event.get("pathParameters")
                if path_parameters:
                    _LOG.info("Path parameters: %s", path_parameters)

                    table_id = path_parameters.get("tableId")
                    _LOG.info("Building key condition expression for table id: %s", table_id)
                    key_condition_expression = Key("id").eq(int(table_id))
                else:
                    _LOG.info("No path parameters provided")
                    key_condition_expression = None

                result = _get_table_items(dynamodb_resource, table_name, _build_tables_item_str_func,
                                          key_condition_expression)
            elif resource_path == "/reservations" and http_method == "POST":
                table_name = os.environ['reservations_table']
                table_item = _build_reservations_item(body)
                result = _post_table_item(dynamodb_client, table_name, table_item, '{"reservationId": "%s"}')
            elif resource_path == "/reservations" and http_method == "GET":
                table_name = os.environ['reservations_table']
                result = _get_table_items(dynamodb_resource, table_name, _build_reservations_item_str_func)
            else:
                raise Exception(f"Unsupported resource path: {resource_path} and http method: {http_method}")
        except Exception as e:
            _LOG.error("Error: %s", e)
            result = {"statusCode": 400, "body": str(e)}

        return result
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
