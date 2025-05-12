from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

def evaluate_feedback():
    feedback_path = "/usr/local/airflow/serving/app/feedback.csv"
    if not os.path.exists(feedback_path):
        print("No feedback yet.")
        return

    df = pd.read_csv(feedback_path, header=None,
                     names=["timestamp", "hour", "zone", "predicted", "actual"])

    df["error"] = abs(df["predicted"] - df["actual"])
    mae = df["error"].mean()

    print(f"Monthly MAE: {mae:.2f}")

    # Optionally log to file
    with open("/usr/local/airflow/serving/app/eval_log.csv", "a") as f:
        f.write(f"{datetime.now().date()},MAE,{mae:.2f}\n")

with DAG("monthly_evaluation_dag", default_args=default_args, schedule_interval='@monthly', catchup=False) as dag:
    eval_task = PythonOperator(
        task_id="evaluate_prediction_accuracy",
        python_callable=evaluate_feedback
    )
