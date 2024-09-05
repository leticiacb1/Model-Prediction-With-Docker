from dataclass.gateway import Gateway
import time

# Variaveis
username  = 'leticiacb1'

function_name = 'aps3_prediction_' + username
api_gateway_name = "api_aps3_prediction_" + username

try: 
    # Instances
    gateway = Gateway()

    # Create API for access lambda function
    gateway.create_client()
    gateway.get_lambda_function(function_name=function_name)
    gateway.create_api(api_name= api_gateway_name)
    gateway.set_permissions(function_name=function_name)
    gateway.create_route(HTTP_method="POST", route_key="POST /prediction")
    gateway.see_all_gateways()

except Exception as e:
    print(f"\n    [ERROR] An error occurred: \n {e}")
finally:
    # Cleaning - Uncomment the line if you want to delete the gateway
    gateway.cleanup(function_name=function_name)