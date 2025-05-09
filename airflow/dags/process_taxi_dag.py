from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd  # Make sure this is imported
import pyarrow  # Make sure pyarrow is installed for parquet reading

def process_taxi_data():
    input_dir = os.path.join(os.environ["AIRFLOW_HOME"], "data", "taxi")
    output_dir = os.path.join(os.environ["AIRFLOW_HOME"], "data", "processed_taxi", "2024-01")
    os.makedirs(output_dir, exist_ok=True)

    all_dfs = []

    for file in os.listdir(input_dir):
        if file.endswith(".parquet") and "2024-01" in file:
            df = pd.read_parquet(os.path.join(input_dir, file))
            if "tpep_pickup_datetime" in df.columns and "PULocationID" in df.columns:
                df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
                df["hour"] = df["pickup_datetime"].dt.hour
                df["location"] = df["PULocationID"]
                hourly = df.groupby(["hour", "location"]).size().reset_index(name="pickup_count")
                all_dfs.append(hourly)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        output_path = os.path.join(output_dir, "hourly_demand_2024-01.csv")
        final_df.to_csv(output_path, index=False)
        print(f" Saved: {output_path}")
    else:
        print("⚠️ No matching data found to process.")

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG(
    dag_id="process_taxi_dag",  # This must exactly match the name used in CLI commands
    default_args=default_args,
    schedule_interval="@monthly",
    catchup=False
) as dag:
    process_task = PythonOperator(
        task_id="process_monthly_taxi_data",
        python_callable=process_taxi_data
    )
