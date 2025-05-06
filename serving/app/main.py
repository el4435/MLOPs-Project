'''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    value: float

@app.post("/predict")
def predict(data: Input):
    return {"prediction": data.value * 2}
'''
'''from fastapi import FastAPI
from app.schemas import Input

from app.model_utils import load_model
import numpy as np

app = FastAPI()

# Load the model at startup
model = load_model()


@app.post("/predict")
def predict(data: Input):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}'''
from fastapi import FastAPI
from pydantic import BaseModel
from app.model_utils import load_model
import numpy as np

app = FastAPI()
model = load_model()

class Input(BaseModel):
    features: list  # e.g., [3, 4]

@app.post("/predict")
def predict(data: Input):
    try:
        print(f"Received input: {data.features}")
        X = np.array(data.features).reshape(1, -1)
        prediction = model.predict(X)
        print(f"Prediction result: {prediction}")
        return {"prediction": prediction.tolist()}
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return {"error": str(e)}
