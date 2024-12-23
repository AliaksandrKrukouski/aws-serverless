#bin/bash

LAMBDA_FUNCTION_NAME=cmtr-e858adde-api-gwlp-lambda-contacts
API_GATEWAY_ID=qqe8u7y5ng
ROUTE_ID=y7v6qjl

echo "Update API Gateway route target"
aws apigatewayv2 update-route \
    --api-id $API_GATEWAY_ID \
    --route-id $ROUTE_ID \
    --route-key "GET /contacts"

echo "Adding permission to invoke lambda from API Gateway"
aws lambda add-permission \
    --statement-id AllowExecutionFromAPIGateway \
    --action lambda:InvokeFunction \
    --function-name $LAMBDA_FUNCTION_NAME \
    --principal apigateway.amazonaws.com