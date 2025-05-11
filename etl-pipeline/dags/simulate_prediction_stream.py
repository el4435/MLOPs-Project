from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import random
import csv
import os
import subprocess

default_args = {
    'owner': 'erxi',
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

ZONES = list(range(1, 264))
ENDPOINT = "http://localhost:8000/predict"
LOG_PATH = "/mnt/data/simulated_predictions_log.csv"
DEST_PATH = "chi_tacc:object-persist-project-21/online/predictions"

def simulate_and_predict():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    with open(LOG_PATH, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if os.stat(LOG_PATH).st_size == 0:
            writer.writerow(["timestamp", "zone", "hour", "prediction"])

        for _ in range(10):
            now = datetime.now()
            pickup_time = now + timedelta(minutes=random.randint(0, 60))
            pickup_zone = random.choice(ZONES)
            hour = pickup_time.hour
            features = [hour, pickup_zone]

            try:
                response = requests.post(ENDPOINT, json={"features": features})
                result = response.json().get("prediction", [None])[0]
                print(f"[{pickup_time}] zone {pickup_zone} → prediction: {result}")
                writer.writerow([pickup_time.isoformat(), pickup_zone, hour, result])
            except Exception as e:
                print("Request failed:", e)

def upload_prediction_log():
    try:
        result = subprocess.run(
            ["rclone", "copy", LOG_PATH, DEST_PATH, "--progress"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Upload output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Upload failed:\n", e.stderr)
        raise

with DAG(
    dag_id="simulate_prediction_stream",
    default_args=default_args,
    start_date=datetime(2025, 5, 1),
    schedule_interval="@hourly",
    catchup=False,
    description="Simulate prediction requests and upload results",
) as dag:

    task_simulate = PythonOperator(
        task_id="simulate_and_send_requests",
        python_callable=simulate_and_predict
    )

    task_upload = PythonOperator(
        task_id="upload_prediction_log_to_object_store",
        python_callable=upload_prediction_log
    )

    task_simulate >> task_upload
