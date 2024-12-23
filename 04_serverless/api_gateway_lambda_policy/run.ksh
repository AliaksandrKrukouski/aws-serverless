#bin/bash

LAMBDA_ARN=arn:aws:lambda:eu-central-1:905418349556:function:cmtr-e858adde-iam-lp-lambda
LAMBDA_ROLE_NAME=cmtr-e858adde-iam-lp-iam_role

echo "Attaching AWSLambda_ReadOnlyAccess policy to $ROLE_NAME"
aws iam attach-role-policy \
    --role-name $LAMBDA_ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/AWSLambda_ReadOnlyAccess

echo "Adding permission to invoke lambda from API Gateway"
aws lambda add-permission \
    --statement-id AllowInvokeLambdaFromAPIGateway \
    --action lambda:InvokeFunction \
    --function-name $LAMBDA_ARN \
    --principal apigateway.amazonaws.com
#     --source-arn "arn:aws:execute-api:eu-central-1:905418349556:z31nh8irl0/*/*/get_list"
