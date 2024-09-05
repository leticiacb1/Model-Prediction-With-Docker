import sys
import json

def hello_from_docker(event, context) -> json:
    return {
        "created_by": "leticiacb1",
        "message": "Hello World!",
        "version": sys.version
    }

# Schemas Model
from ..schemas.model.request import Person
from ..schemas.model.response import PredictResponse

# Other Imports
from typing import Annotated
import pandas as pd

# Create a router
router = APIRouter()

@router.post("/predict")
async def predict(person: Annotated[
        Person,
        Body(
            examples=[
                {
                    "age": 42,
                    "job": "entrepreneur",
                    "marital": "married",
                    "education": "primary",
                    "balance": 558,
                    "housing": "yes",
                    "duration": 186,
                    "campaign": 2,
                }
            ],
        ),
    ], 
    user=Depends(validate_token)) -> PredictResponse:

    """
    Route to make predictions.

    Needs to receive information about the client.
    """

    ohe = ml_models["ohe"]
    model = ml_models["models"]

    df_person = pd.DataFrame([person.dict()])

    person_t = ohe.transform(df_person)
    pred = model.predict(person_t)[0]

    return PredictResponse(prediction=str(pred), username= user["username"])