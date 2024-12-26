# aws_lambda_with_cloudwatch_rule_integration

High level project overview - business value it brings, non-detailed technical overview.

### Notice
All the technical details described below are actual for the particular
version, or a range of versions of the software.
### Actual for versions: 1.0.0

## aws_lambda_with_cloudwatch_rule_integration diagram

![aws_lambda_with_cloudwatch_rule_integration](pics/aws_lambda_with_cloudwatch_rule_integration_diagram.png)

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
1. ```syndicate generate lambda --name uuid_generator --runtime python```
2. ```syndicate generate meta s3_bucket --resource_name uuid-storage ```
3. ```syndicate generate meta cloudwatch_event_rule --resource_name uuid-trigger  --rule_type schedule --expression "rate(1 minute)"```