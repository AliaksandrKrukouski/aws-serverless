# aws_lambda_with_dynamo_db_integration

High level project overview - business value it brings, non-detailed technical overview.

### Notice
All the technical details described below are actual for the particular
version, or a range of versions of the software.
### Actual for versions: 1.0.0

## aws_lambda_with_dynamo_db_integration diagram

![aws_lambda_with_dynamo_db_integration](pics/aws_lambda_with_dynamo_db_integration_diagram.png)

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
1. ```syndicate generate lambda --name api_handler --runtime python```
2. ```syndicate generate meta api_gateway  --resource_name task5_api --deploy_stage api ```
3. ```syndicate generate meta dynamodb --resource_name Events  --hash_key_name id --hash_key_type S ```
4. ```syndicate generate meta api_gateway_resource  --api_name task5_api --path /events  --enable_cors false ```
5. ```syndicate generate meta api_gateway_resource_method --api_name task5_api --path /events --method POST --integration_type lambda --lambda_name api_handler --api_key_required false ```
