import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_batch_predictions():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "serving", "dummy_input.csv")
    predictions_path = os.path.join(base_dir, "serving", "daily_predictions.csv")
    output_path = os.path.join(base_dir, "serving", "batch_output.csv")

    input_data = pd.read_csv(input_path)
    predictions = pd.read_csv(predictions_path)
    results = []

    for _, row in input_data.iterrows():
        hour, loc = row['hour'], row['location']
        match = predictions[(predictions["hour"] == hour) & (predictions["location"] == loc)]
        predicted = match["predicted_demand"].values[0] if not match.empty else None
        results.append({"hour": hour, "location": loc, "prediction": predicted})

    pd.DataFrame(results).to_csv(output_path, index=False)
    print("✅ Batch predictions saved to:", output_path)

default_args = {'start_date': datetime(2024, 1, 1), 'retries': 1}

with DAG("daily_batch_prediction", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:
    run_prediction = PythonOperator(
        task_id="run_batch_prediction",
        python_callable=run_batch_predictions
    )
