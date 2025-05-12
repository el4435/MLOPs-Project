import onnxruntime as ort
import numpy as np
import pandas as pd
from datetime import datetime

session = ort.InferenceSession("app/model.onnx")
input_name = session.get_inputs()[0].name

# Inputs: [has_event, hour, day_of_week, is_weekend]
hours = list(range(24))
locations = list(range(5))  # if you want to loop over zones
inputs = [[1, h, h % 7, int(h >= 5)] for h in hours for _ in locations]  # fake inputs

X = np.array(inputs, dtype=np.float32)
predictions = session.run(None, {input_name: X})[0]

df = pd.DataFrame(inputs, columns=["has_event", "hour", "day_of_week", "is_weekend"])
df["predicted_demand"] = predictions
df["date"] = datetime.today().strftime('%Y-%m-%d')

df.to_csv("app/daily_predictions.csv", index=False)
print("✅ Daily batch predictions saved.")
