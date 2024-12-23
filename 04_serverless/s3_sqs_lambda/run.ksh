#bin/bash

S3_BUCKET_NAME=cmtr-e858adde-s3-snlt-bucket-952862
SQS_QUEUE_ARN=arn:aws:sqs:eu-central-1:905418349556:cmtr-e858adde-s3-snlt-queue
LAMBDA_FUNCTION_NAME=cmtr-e858adde-s3-snlt-lambda

echo "Enable S3 bucket notification to SQS"
aws s3api put-bucket-notification-configuration \
    --bucket $S3_BUCKET_NAME \
    --notification-configuration file://s3-notification.json

echo "Create Lambda trigger on SQS"
aws lambda create-event-source-mapping \
    --function-name $LAMBDA_FUNCTION_NAME \
    --batch-size 10 --event-source-arn $SQS_QUEUE_ARN