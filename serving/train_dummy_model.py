# train_dummy_model.py
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import os

# 🚨 Define input with 2 features
X = np.array([
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6]
])
y = np.array([3, 5, 7, 9, 11])  # y = x1 + x2

model = LinearRegression()
model.fit(X, y)

# ✅ Save model to correct path
os.makedirs(".", exist_ok=True)
joblib.dump(model, "model.pkl")
