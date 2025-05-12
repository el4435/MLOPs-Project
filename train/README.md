
# Taxi Driver Event Time & Location Prediction — Model Training

This folder trains a random forest model to predict how many trips will be requested from a certain location within a 15 minute time frame. The model uses MLFlow to travk experiments. 

---

## Features

- Predicts taxi trip counts per location per 15-minute interval
- Uses `RandomForestRegressor` from scikit-learn
- Distributed hyperparameter tuning using Ray
- Tracks experiments using MLFlow (metrics, models, parameters)

---

## How to run the model

1. **Run the main.py notebook and ssh into the given session a local terminal**

2. **Compose the Docker container:**
   ```bash
   docker compose -f MLOPs-Project/train/docker-compose.yaml up -d
   ```

3. **Find the token and subsitute the IP address with the floating IP:**
   ```bash
   http://127.0.0.1:8888/lab?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

## 🧾 File Overview

| File                   | Purpose                                          |
|------------------------|--------------------------------------------------|
| `DockerFile`           | Sets the Docker configuration of dependencies    |
| `docker-compose.yaml`   | Sets the scipy-notebook image                    |
| `docker-compose.mlflow.yaml` | Sets MLFlow workflow with PostgreSQL and a Ray cluster   |
| `train.ipnyb`            | trains the model and implements MLFlow         |




