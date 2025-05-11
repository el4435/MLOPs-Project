from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import urllib.request
import urllib.parse
import pandas as pd

default_args = {
    'owner': 'erxi',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def download_event_data():
    output_dir = "/mnt/data/events"
    os.makedirs(output_dir, exist_ok=True)

    base_url = "https://data.cityofnewyork.us/resource/bkfu-528j.csv"
    limit = 50000
    today = datetime.now()
    year, month = today.year, today.month

    start = datetime(year, month, 1)
    end = (start + timedelta(days=31)).replace(day=1)
    start_str = start.strftime("%Y-%m-%dT00:00:00")
    end_str = end.strftime("%Y-%m-%dT00:00:00")
    where_clause = f"start_date_time between '{start_str}' and '{end_str}'"
    encoded_where = urllib.parse.quote(where_clause)

    combined_df = []
    offset = 0
    page = 1

    while True:
        url = f"{base_url}?$where={encoded_where}&$limit={limit}&$offset={offset}&$order=start_date_time"
        try:
            print(f"Fetching page {page} ...")
            df = pd.read_csv(url)
            if df.empty:
                break
            combined_df.append(df)
            if len(df) < limit:
                break
            offset += limit
            page += 1
        except Exception as e:
            print(f"Download failed: {e}")
            break

    if combined_df:
        result = pd.concat(combined_df, ignore_index=True)
        file_path = os.path.join(output_dir, f"events_{year}-{month:02d}.csv")
        result.to_csv(file_path, index=False)
        print(f"Saved: {file_path}")
    else:
        print("No data downloaded.")

def process_event_data():
    input_dir = "/mnt/data/events"
    today = datetime.now()
    year = today.year
    output_path = os.path.join(input_dir, f"processed_events_{year}.csv")

    frames = []
    for file in sorted(os.listdir(input_dir)):
        if file.startswith(f"events_{year}-") and file.endswith(".csv"):
            path = os.path.join(input_dir, file)
            try:
                df = pd.read_csv(path)
            except Exception as e:
                print(f"Failed to read {file}: {e}")
                continue

            df.columns = df.columns.str.strip()

            if "start_date_time" in df.columns:
                df["start_date_time"] = pd.to_datetime(df["start_date_time"], errors="coerce")
            if "end_date_time" in df.columns:
                df["end_date_time"] = pd.to_datetime(df["end_date_time"], errors="coerce")

            selected_cols = [
                "event_id", "event_name", "start_date_time", "end_date_time",
                "event_type", "event_borough", "event_location", "street_closure_type"
            ]
            df = df[[col for col in selected_cols if col in df.columns]]
            frames.append(df)

    if frames:
        result = pd.concat(frames, ignore_index=True)
        result.to_csv(output_path, index=False)
        print(f"Saved: {output_path}, Total: {len(result)} rows")
    else:
        print("No valid event files found.")

with DAG(
    dag_id="download_and_process_event_data",
    default_args=default_args,
    start_date=datetime(2025, 5, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Download and clean NYC event data",
) as dag:

    task_download_events = PythonOperator(
        task_id="download_event_data",
        python_callable=download_event_data
    )

    task_process_events = PythonOperator(
        task_id="process_event_data",
        python_callable=process_event_data
    )

    task_download_events >> task_process_events
