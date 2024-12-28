#bin/bash

LAMBDA_FUNCTION_NAME=cmtr-e858adde-lambda-fgufc-lambda

echo "Creating zip for Lambda function handler"
rm -f lambda-handler.zip
zip lambda-handler.zip lambda_function.py

echo "Updating Lambda function code"
aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --zip-file fileb://lambda-handler.zip