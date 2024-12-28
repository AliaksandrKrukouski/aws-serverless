#bin/bash

S3_BUCKET_NAME=cmtr-e858adde-cloudfront-sswo-bucket-7851649
CLOUDFRONT_DISTRIBUTION_ID=E1W9MOWR791NQM

# echo "Get CloudFront distribution config"
# aws cloudfront get-distribution-config --id $CLOUDFRONT_DISTRIBUTION_ID --output json > ./cloudfront-distribution-config.json
#
# echo "Update CloudFront distribution config"
# aws cloudfront update-distribution --id $CLOUDFRONT_DISTRIBUTION_ID --if-match EDHKUF0B0T11O --distribution-config file://cloudfront-distribution-config-updated.json

echo "Enable S3 access for CloudFront"
aws s3api put-bucket-policy --bucket $S3_BUCKET_NAME --policy file://s3-bucket-policy.json

# echo "Get CloudFront distribution config"
# aws cloudfront get-distribution-config --id $CLOUDFRONT_DISTRIBUTION_ID --output json > ./cloudfront-distribution-config.json
#
# echo "Update CloudFront distribution config"
# aws cloudfront update-distribution --id $CLOUDFRONT_DISTRIBUTION_ID --if-match E3L45GH1G4A2EL --distribution-config file://cloudfront-distribution-config-updated.json

echo "Disable public access to S3 bucket"
aws s3api put-public-access-block \
    --bucket $S3_BUCKET_NAME \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"