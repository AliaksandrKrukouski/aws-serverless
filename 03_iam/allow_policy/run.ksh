#bin/bash

ROLE_NAME=cmtr-e858adde-iam-pela-iam_role
S3_BUCKET_NAME=cmtr-e858adde-iam-pela-bucket-1-2138108

echo "Attaching S3 List All Buckets policy to $ROLE_NAME IAM Role..."
aws iam put-role-policy --role-name $ROLE_NAME --policy-name AllowListAllMyBuckets --policy-document file://s3_allow_list_buckets_policy.json

#aws iam detach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

echo "Updating S3 Bucket Policy..."
aws s3api put-bucket-policy --bucket $S3_BUCKET_NAME --policy file://s3_allow_list_get_put_bucket_policy.json