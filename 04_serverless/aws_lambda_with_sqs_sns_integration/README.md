# aws_lambda_with_sqs_sns_integration

High level project overview - business value it brings, non-detailed technical overview.

### Notice
All the technical details described below are actual for the particular
version, or a range of versions of the software.
### Actual for versions: 1.0.0

## aws_lambda_with_sqs_sns_integration diagram

![aws_lambda_with_sqs_sns_integration](pics/aws_lambda_with_sqs_sns_integration_diagram.png)

## Lambdas descriptions

### Lambda `lambda-name`
Lambda feature overview.

### Required configuration
#### Environment variables
* environment_variable_name: description

#### Trigger event
```buildoutcfg
{
    "key": "value",
    "key1": "value1",
    "key2": "value3"
}
```
* key: [Required] description of key
* key1: description of key1

#### Expected response
```buildoutcfg
{
    "status": 200,
    "message": "Operation succeeded"
}
```
---

## Deployment from scratch
1. ```syndicate generate lambda --name sqs_handler --runtime python --event_sources {}```
2. ```syndicate generate lambda --name sns_handler --runtime python```
3. ```syndicate generate meta sqs_queue  --resource_name async_queue  --fifo_queue false ```
4. ```aws sqs send-message --queue-url https://sqs.eu-central-1.amazonaws.com/905418349556/cmtr-e858adde-async_queue --message-body "Hello"```
5. ```syndicate generate meta sns_topic --resource_name lambda_topic --region eu-central-1 ```
6. ```aws sns publish --topic-arn arn:aws:sns:eu-central-1:905418349556:cmtr-e858adde-lambda_topic --message "Hello"```