from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import urllib.request

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
    output_dir = "/mnt/data"
    os.makedirs(output_dir, exist_ok=True)
    dest = os.path.join(output_dir, file_name)
    if os.path.exists(dest):
        print(f"Already exists: {file_name}")
        return
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded: {file_name}")

with DAG(
    dag_id="download_latest_taxi_data",
    default_args=default_args,
    start_date=datetime(2025, 5, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Download latest yellow taxi data daily",
) as dag:
    task = PythonOperator(
        task_id="download_taxi_data",
        python_callable=download_latest_taxi_data
    )
