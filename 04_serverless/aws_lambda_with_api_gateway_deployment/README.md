# aws_lambda_with_api_gateway_deployment

High level project overview - business value it brings, non-detailed technical overview.

### Notice
All the technical details described below are actual for the particular
version, or a range of versions of the software.
### Actual for versions: 1.0.0

## aws_lambda_with_api_gateway_deployment diagram

![aws_lambda_with_api_gateway_deployment](pics/aws_lambda_with_api_gateway_deployment_diagram.png)

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
1. ```syndicate generate lambda --name hello_world --runtime python```
2. ```syndicate generate meta api_gateway  --resource_name task3_api  --deploy_stage api ```
3. ```syndicate generate meta api_gateway_resource  --api_name task3_api  --path /hello  --enable_cors false ```
4. ```syndicate generate meta api_gateway_resource_method --api_name task3_api  --path /hello  --method GET  --integration_type lambda --lambda_name hello_world --api_key_required false ```

