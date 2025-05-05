'''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    value: float

@app.post("/predict")
def predict(data: Input):
    return {"prediction": data.value * 2}
'''
from fastapi import FastAPI
from pydantic import BaseModel
from app.model_utils import load_model
import numpy as np

app = FastAPI()
model = load_model()

class Input(BaseModel):
    features: list  # Assuming your model takes a list of numeric inputs

@app.post("/predict")
def predict(data: Input):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}
