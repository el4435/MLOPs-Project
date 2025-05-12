import onnxruntime as ort

def load_model():
    session = ort.InferenceSession("app/model.onnx")
    return session
