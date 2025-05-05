import joblib

def load_model():
    model = joblib.load("model.joblib")
    return model
