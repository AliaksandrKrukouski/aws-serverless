#bin/bash

ASSUME_ROLE_NAME=cmtr-e858adde-iam-ar-iam_role-assume
READONLY_ROLE_NAME=cmtr-e858adde-iam-ar-iam_role-readonly
READONLY_ACCESS_POLICY_ARN=arn:aws:iam::aws:policy/ReadOnlyAccess

echo "Step 1: Configure permissions for the assume role"
aws iam put-role-policy --role-name $ASSUME_ROLE_NAME --policy-name AllowSTSAssumePolicy --policy-document file://iam_allow_sts_assume_policy.json
#aws iam delete-role-policy --role-name $ASSUME_ROLE_NAME --policy-name AllowSTSAssumeRole

echo "Step 2: Grant read-only access for the read-only role"
aws iam attach-role-policy --role-name $READONLY_ROLE_NAME --policy-arn $READONLY_ACCESS_POLICY_ARN

echo "Step 3: Configure trust policy for the read-only role"
aws iam update-assume-role-policy --role-name $READONLY_ROLE_NAME --policy-document file://iam_trust_policy.json