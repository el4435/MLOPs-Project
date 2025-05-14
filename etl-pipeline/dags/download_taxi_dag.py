from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import urllib.request
import pandas as pd
import subprocess

default_args = {
    'owner': 'erxi',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def download_latest_taxi_data():
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    year = datetime.now().year
    month = datetime.now().month
    file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
    url = f"{base_url}/{file_name}"
    output_dir = "/mnt/data/output"
    os.makedirs(output_dir, exist_ok=True)
    dest = os.path.join(output_dir, file_name)
    if os.path.exists(dest):
        print(f"Already exists: {file_name}")
        return
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded: {file_name}")

def process_taxi_data():
    INPUT_DIR = "/mnt/data/output"
    OUTPUT_CSV = os.path.join(INPUT_DIR, "taxi_demand_by_zone_hour.csv")
    parquet_files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".parquet"))
    frames = []
    for file in parquet_files:
        path = os.path.join(INPUT_DIR, file)
        try:
            df = pd.read_parquet(path, engine="pyarrow")
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        if "tpep_pickup_datetime" not in df.columns or "PULocationID" not in df.columns:
            print(f"Skipping {file}: Missing expected columns.")
            continue

        df = df[["tpep_pickup_datetime", "PULocationID"]].copy()
        df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
        df["date"] = df["pickup_datetime"].dt.date
        df["hour"] = df["pickup_datetime"].dt.hour

        grouped = df.groupby(["date", "hour", "PULocationID"]).size().reset_index(name="pickup_count")
        frames.append(grouped)

    if frames:
        result = pd.concat(frames, ignore_index=True)
        result.to_csv(OUTPUT_CSV, index=False)
        print(f"Saved output to: {OUTPUT_CSV}")
    else:
        print("No files processed.")

def upload_taxi_demand_csv():
    src = "/mnt/data/output/taxi_demand_by_zone_hour.csv"
    dest = "chi_tacc:object-persist-project-21/online/taxi"
    try:
        result = subprocess.run(
            ["rclone", "copy", src, dest, "--progress"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Upload output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Upload failed:\n", e.stderr)
        raise

with DAG(
    dag_id="download_process_upload_taxi_data",
    default_args=default_args,
    start_date=datetime(2025, 5, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Download, process and upload yellow taxi demand data daily",
) as dag:

    task_download = PythonOperator(
        task_id="download_taxi_data",
        python_callable=download_latest_taxi_data
    )

    task_process = PythonOperator(
        task_id="process_taxi_data",
        python_callable=process_taxi_data
    )

    task_upload = PythonOperator(
        task_id="upload_taxi_csv",
        python_callable=upload_taxi_demand_csv
    )

    task_download >> task_process >> task_upload
