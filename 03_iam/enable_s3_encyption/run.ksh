#bin/bash

ROLE_NAME=cmtr-e858adde-iam-sewk-iam_role
BUCKET_NAME=cmtr-e858adde-iam-sewk-bucket-9318339-1
ENCRYPTED_BUCKET_NAME=cmtr-e858adde-iam-sewk-bucket-9318339-2
KMS_KEY_ARN=arn:aws:kms:eu-central-1:905418349556:key/dd7f0521-8e16-4512-aeb8-4e73aa7cfddc

echo "Step 1: Grant Permissions for IAM Role to Use KMS Key"
aws iam put-role-policy --role-name $ROLE_NAME --policy-name AllowKMSPolicy --policy-document file://iam_allow_kms_policy.json

echo "Step 2: Enable Server-Side Encryption for S3 Bucket"
aws s3api put-bucket-encryption --bucket $ENCRYPTED_BUCKET_NAME --server-side-encryption-configuration file://s3_bucket_encryption.json

echo "Step 3: Copy an Object to the Encrypted Bucket"
aws s3 cp s3://$BUCKET_NAME/confidential_credentials.csv s3://$ENCRYPTED_BUCKET_NAME/confidential_credentials.csv