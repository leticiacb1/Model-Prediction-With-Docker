import requests

input_json = {
    "person": {
        "age": 42,
        "job": "entrepreneur",
        "marital": "married",
        "education": "primary",
        "balance": 558,
        "housing": "yes",
        "duration": 186,
        "campaign": 2,
    }
}

# Update with api_endpoint got it from create_gateway.py
api_endpoint = '' 

try: 
    
    # Test the API response
    print(f"\n    [INFO] Test API.\n")
    api_response = requests.post(api_endpoint, json=input_json)
    print(api_response.json())

except Exception as e:
    print(f"\n    [ERROR] An error occurred: \n {e}")
