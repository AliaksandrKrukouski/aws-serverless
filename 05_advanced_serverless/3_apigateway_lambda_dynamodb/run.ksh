#bin/bash

set -e

GET_PRODUCTS_LAMBDA=cmtr-e858adde-dynamodb-l-lambda-getProductsList
GET_PRODUCTS_LAMBDA_ARN=arn:aws:lambda:eu-central-1:905418349556:function:cmtr-e858adde-dynamodb-l-lambda-getProductsList
CREATE_PRODUCT_LAMBDA=cmtr-e858adde-dynamodb-l-lambda-createProduct
CREATE_PRODUCT_LAMBDA_ARN=arn:aws:lambda:eu-central-1:905418349556:function:cmtr-e858adde-dynamodb-l-lambda-createProduct
PRODUCTS_TABLE=cmtr-e858adde-dynamodb-l-table-products
STOCKS_TABLE=cmtr-e858adde-dynamodb-l-table-stocks
PRODUCTS_API_ID=z3vrfi0g5d

echo "Attaching AmazonDynamoDBReadOnlyAccess policy to the lambda functions"
aws iam attach-role-policy --role-name $GET_PRODUCTS_LAMBDA --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess

echo "Attaching AmazonDynamoDBFullAccess policy to the lambda functions"
aws iam attach-role-policy --role-name $CREATE_PRODUCT_LAMBDA --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

echo "Create Lambda package for get_products_list function"
cd lambda_functions
rm -f get_products_list.zip
zip get_products_list.zip get_products_list.py
cd ..

echo "Create Lambda package for create_product function"
cd lambda_functions
rm -f create_product.zip
zip create_product.zip create_product.py
cd ..

echo "Upload Lambda packages to AWS"
aws lambda update-function-code --function-name $GET_PRODUCTS_LAMBDA --zip-file fileb://lambda_functions/get_products_list.zip
aws lambda update-function-code --function-name $CREATE_PRODUCT_LAMBDA --zip-file fileb://lambda_functions/create_product.zip

echo "Create integration for GET, POST methods"
GET_PRODUCTS_INTEGRATION_ID=$(aws apigatewayv2 create-integration \
    --api-id $PRODUCTS_API_ID \
    --integration-method GET \
    --integration-type AWS_PROXY \
    --integration-uri $GET_PRODUCTS_LAMBDA_ARN \
    --payload-format-version 2.0 \
    --output text \
    --query 'IntegrationId')
CREATE_PRODUCT_INTEGRATION_ID=$(aws apigatewayv2 create-integration \
    --api-id $PRODUCTS_API_ID \
    --integration-method POST \
    --integration-type AWS_PROXY \
    --integration-uri $CREATE_PRODUCT_LAMBDA_ARN \
    --payload-format-version 2.0 \
    --output text \
    --query 'IntegrationId')

echo "Create GET, POST routes for /products resource"
aws apigatewayv2 create-route --api-id $PRODUCTS_API_ID --route-key 'GET /products' --target "integrations/$GET_PRODUCTS_INTEGRATION_ID"
aws apigatewayv2 create-route --api-id $PRODUCTS_API_ID --route-key 'POST /products' --target "integrations/$CREATE_PRODUCT_INTEGRATION_ID"

echo "Adding permission to invoke lambda from API Gateway"
aws lambda add-permission --statement-id AllowExecutionFromAPIGateway --action lambda:InvokeFunction --function-name $GET_PRODUCTS_LAMBDA_ARN --principal apigateway.amazonaws.com
aws lambda add-permission --statement-id AllowExecutionFromAPIGateway --action lambda:InvokeFunction --function-name $CREATE_PRODUCT_LAMBDA_ARN --principal apigateway.amazonaws.com
