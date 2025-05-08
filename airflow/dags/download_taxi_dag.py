from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import urllib.request

def download_taxi_data(**context):
    execution_date = context['execution_date']
    year = execution_date.year
    month = execution_date.month

    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
    url = f"{base_url}/{filename}"

    # Save to: AIRFLOW_HOME/data/taxi/YYYY-MM/
    output_dir = os.path.join(os.environ["AIRFLOW_HOME"], "data", "raw_taxi", f"{year}-{month:02d}")
    os.makedirs(output_dir, exist_ok=True)

    dest = os.path.join(output_dir, filename)
    urllib.request.urlretrieve(url, dest)
    print(f"✅ Saved to: {dest}")

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG(
    "download_taxi_dag",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=False
) as dag:

    download_task = PythonOperator(
        task_id="download_monthly_taxi_data",
        python_callable=download_taxi_data,
        provide_context=True  # <-- lets you use **context
    )
