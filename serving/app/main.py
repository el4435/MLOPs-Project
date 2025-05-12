from fastapi import FastAPI, UploadFile, File, Query
from pydantic import BaseModel
from app.model_utils import load_model
from datetime import datetime
import pandas as pd
import numpy as np
import os

app = FastAPI()
session = load_model()

# Ensure log files exist
os.makedirs("app", exist_ok=True)

if not os.path.exists("app/request_logs.csv"):
    with open("app/request_logs.csv", "w") as f:
        f.write("timestamp,input,prediction\n")

if not os.path.exists("app/feedback.csv"):
    with open("app/feedback.csv", "w") as f:
        f.write("timestamp,hour,zone,predicted,actual\n")

class Input(BaseModel):
    features: list

@app.post("/predict/")
def predict(data: Input):
    try:
        X = np.array(data.features, dtype=np.float32).reshape(1, -1)
        input_name = session.get_inputs()[0].name
        prediction = session.run(None, {input_name: X})[0].tolist()

        with open("app/request_logs.csv", "a") as f:
            f.write(f"{datetime.now()},{data.features},{prediction}\n")

        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}

@app.post("/batch_predict/")
def batch_predict():
    try:
        df = pd.read_csv("app/dummy_input.csv")
        X = df.values.astype(np.float32)
        input_name = session.get_inputs()[0].name
        predictions = session.run(None, {input_name: X})[0]

        pd.DataFrame(predictions, columns=["prediction"]).to_csv("app/batch_output.csv", index=False)
        return {"status": "batch prediction completed", "rows": len(predictions)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/feedback/")
def feedback(
    hour: int = Query(...),
    zone: str = Query(...),
    predicted: float = Query(...),
    actual: float = Query(...)
):
    with open("app/feedback.csv", "a") as f:
        f.write(f"{datetime.now()},{hour},{zone},{predicted},{actual}\n")
    return {"status": "feedback recorded"}
