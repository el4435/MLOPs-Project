'''import joblib

def load_model():
    model = joblib.load("model.joblib")
    return model
'''
import joblib
import os

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'model.pkl')
    return joblib.load(model_path)
