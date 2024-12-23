#bin/bash

ROLE_NAME=cmtr-e858adde-iam-peld-iam_role
S3_BUCKET_NAME=cmtr-e858adde-iam-peld-bucket-9486637
S3_FULL_ACCESS_POLICY_ARN=arn:aws:iam::aws:policy/AmazonS3FullAccess

echo "Attaching S3 Full Access Policy to $ROLE_NAME IAM Role..."
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn $S3_FULL_ACCESS_POLICY_ARN

echo "Updating S3 Bucket Policy..."
aws s3api put-bucket-policy --bucket $S3_BUCKET_NAME --policy file://s3_bucket_policy.json