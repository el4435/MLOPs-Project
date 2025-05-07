# Taxi Demand Prediction — Airflow DAGs for Batch Inference

This folder contains Apache Airflow DAGs that automate **daily batch predictions** for taxi pickup demand using a trained model. The batch process reads input pairs of `[hour, location]` and matches them to a precomputed predictions file or runs a `.pkl` model to generate predictions.

---

## DAG Overview

| DAG ID                  | Purpose                               | Schedule     |
|-------------------------|----------------------------------------|--------------|
| `daily_batch_prediction`| Predict demand for all hours/locations| `@daily`     |

The DAG executes a Python task (`run_batch_prediction`) that reads a CSV of inputs and outputs prediction results to a CSV file.

---

## Setup Instructions

### 1. Create Python 3.10 virtual environment

```bash
python3.10 -m venv airflow310
source airflow310/bin/activate
```

### 2. Install Airflow (v2.8.1)

```bash
pip install "apache-airflow==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.10.txt"
```

### 3. Set Airflow home and initialize DB

```bash
export AIRFLOW_HOME=$(pwd)/airflow
mkdir -p $AIRFLOW_HOME/dags
airflow db init
```

### 4. Create a user

```bash
airflow users create \
  --username admin \
  --password admin \
  --firstname User \
  --lastname Admin \
  --role Admin \
  --email example@example.com
```

---

## Running Airflow

### Webserver

```bash
airflow webserver --port 8080
```

### Scheduler (in a separate terminal)

```bash
airflow scheduler
```

Access the UI at: [http://localhost:8080](http://localhost:8080)

**Login:**

- Username: `admin`
- Password: `admin`

---

## 📂 DAG Logic

The DAG reads:

- `serving/dummy_input.csv` (columns: `hour`, `location`)
- `serving/daily_predictions.csv` (precomputed model output)

It writes:

- `serving/batch_output.csv` (joined prediction output)

If the model is ready and is replaced, then  the model (with a `.pkl` extension), update the logic in `batch_prediction.py` to load and run the new model.

---

## 📁 File Structure

| File                          | Purpose                               |
|-------------------------------|----------------------------------------|
| `dags/batch_prediction.py`    | DAG definition that runs batch prediction |
| `serving/dummy_input.csv`     | Hour/location pairs for inference     |
| `serving/daily_predictions.csv` | Precomputed predictions to read from |
| `serving/batch_output.csv`    | Output saved after DAG run            |

---

## 📝 Notes for Team

- Make sure all required files (`dummy_input.csv`, `daily_predictions.csv`) exist in the expected `serving/` folder.
- Use absolute paths inside `batch_prediction.py` if file detection fails.
- This DAG does not train or tune models — it only serves daily predictions in batch.
- The current model is a dummy linear regressor; update it once Imani shares the trained `.pkl`.
- For some reaon you have to for now copy files form the dummy_input in the main serving folder to the on in the airflow (I'll fix this as soon as i can find a solution)
---

## Status (as of May 6, 2025)

- ✅ DAG loads successfully in UI  
- ✅ Batch predictions run and generate correct `batch_output.csv`  
- ✅ FastAPI and Airflow operate independently but use shared data

---

## Future Plans

- Connect DAG outputs to FastAPI logs or dashboards  
- Schedule DAG via event triggers (e.g. file drop or webhook)
