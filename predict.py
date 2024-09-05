import sys
import json

def run(event, context) -> json:
    '''
    Receive a person input and return a prediction.
    
    Parameters:

        - event: dict, required
        The event object that contains the input to the Lambda function. 
        Expect the input to have a person key:
            "person" : {
                        "age": 42,
                        "job": "entrepreneur",
                        "marital": "married",
                        "education": "primary",
                        "balance": 558,
                        "housing": "yes",
                        "duration": 186,
                        "campaign": 2,
                    }

        
        - context: object, required
        The context object provided by AWS Lambda, containing metadata and runtime information.
    
    Returns:

        - json:
            {   
                "input": person,
                "prediction": value_prediction
            }
    
    '''

    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary.")
    
    body = event.get("body")
    if not body:
        return {
            "Error": "Invalid input: no body found."
        }

    try:
        json_body = json.loads(body)
    except json.JSONDecodeError:
        return {
            "Error": "Invalid input: unable to parse JSON body."
        }
    person = json_body.get("person")
    
    if not isinstance(person, dict):
        return {
            "Error": "Invalid input: 'person' must be a string."
        }

    return {
        "input" : person,
        "prediciton": "predict_value"
    }