import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

model = joblib.load("train/workspace/model.pkl")
initial_type = [("input", FloatTensorType([None, 4]))]  # update shape as needed
onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("airflow/serving/model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

