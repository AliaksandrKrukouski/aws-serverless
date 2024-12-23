#bin/bash

S3_BUCKET_NAME=cmtr-e858adde-s3-snlt-bucket-952862

aws s3 cp ./test.txt  s3://$S3_BUCKET_NAME/input/test.txt