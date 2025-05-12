from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/usr/local/airflow/serving/app')  # Adjust if needed

from predict import run_inference

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

def run_batch():
    run_inference(
        input_csv_path="/usr/local/airflow/serving/app/dummy_input.csv",
        model_path="/usr/local/airflow/serving/app/model.onnx",
        output_csv_path="/usr/local/airflow/serving/app/daily_predictions.csv"
    )

with DAG("batch_prediction_dag", default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    batch_task = PythonOperator(
        task_id="run_daily_batch_prediction",
        python_callable=run_batch
    )
