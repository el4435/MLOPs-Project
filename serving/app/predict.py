import onnxruntime as ort
import pandas as pd
import numpy as np

def run_inference(input_csv_path, model_path, output_csv_path):
    # Load input data
    input_df = pd.read_csv(input_csv_path)
    input_data = input_df.values.astype(np.float32)

    # Load ONNX model
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # Run inference
    predictions = session.run([output_name], {input_name: input_data})[0]

    # Save output
    output_df = pd.DataFrame(predictions, columns=["prediction"])
    output_df.to_csv(output_csv_path, index=False)
    return output_df

