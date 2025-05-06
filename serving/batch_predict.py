# serving/batch_predict.py
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

model = joblib.load("model.pkl")

# Dummy input: each row is [hour, location_id]
hours = list(range(24))
locations = list(range(5))  # assume 5 zones
inputs = [[h, l] for h in hours for l in locations]

X = np.array(inputs)
predictions = model.predict(X)

df = pd.DataFrame(inputs, columns=["hour", "location"])
df["predicted_demand"] = predictions
df["date"] = datetime.today().strftime('%Y-%m-%d')

df.to_csv("daily_predictions.csv", index=False)
print("Daily batch predictions saved.")
