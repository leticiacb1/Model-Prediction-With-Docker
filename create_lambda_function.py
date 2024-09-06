from dataclass.lambda_function import LambdaFunction
import time
import json

# Variaveis
username  = 'leticiacb1'
function_input = {
    "body": json.dumps({
        "person": {"atributo": "valor-do-atributo"}
    })
}

repository_name = 'aps3-mlops-' + username
function_name = 'aps3-prediction-' + username

try: 
    # Instances
    _lambda = LambdaFunction()

    # Image URI (follow the pattern <repositoryUri>:<imageTag>)
    image_uri = _lambda.config.ACCOUNT_ID + '.dkr.ecr.' + _lambda.config.REGION + '.amazonaws.com/' + repository_name + ':latest'

    # Lambda Function
    _lambda.create_client()
    _lambda.create_function_image(function_name=function_name , image_uri= image_uri)

    time.sleep(5) # Wait lambda function to be deployed

    _lambda.check_function(function_name=function_name, input = function_input)
    _lambda.see_all_lambda_functions()

except Exception as e:
    print(f"\n    [ERROR] An error occurred: \n {e}")
finally:
    ...
    # Cleaning - Uncomment the line if you want to delete the lambda function
    # _lambda.cleanup(function_name=function_name)