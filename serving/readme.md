
# Taxi Driver Event Time & Location Prediction — Model Serving

This folder sets up a FastAPI server to serve predictions using a trained `.pkl` model. Currently, it uses a dummy model trained with `LinearRegression` for testing purposes. The setup is containerized with Docker for reproducibility and ease of deployment.

---

## Features

- FastAPI app with a `/predict` endpoint
- Dummy model that accepts 2 inputs and returns 1 output
- Docker-ready: Easily build and run locally
- Compatible with ONNX for future model optimizations
- Simple path for upgrading to real models trained by the ML team

---

## How to Test the API Locally

1. **Navigate to the serving folder:**
   ```bash
   cd serving
   ```

2. **Build the Docker image:**
   ```bash
   docker build -t taxi-model-serving .
   ```

3. **Run the container:**
   ```bash
   docker run -p 8000:8000 taxi-model-serving
   ```

4. **Open the browser and test the endpoint:**

   Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

   Try this sample input:
   ```json
   {
     "features": [3.0, 4.0]
   }
   ```

   You should see this output:
   ```json
   {
     "prediction": [7.0]
   }
   ```

---

##  Instructions for Imani – Updating the Real Model

1. After training your model, export it as `.pkl`:
   ```python
   import joblib
   joblib.dump(your_model, "model.pkl")
   ```

2. Place the new `model.pkl` in the root of the `serving/` folder (overwrite the dummy one).

3. Rebuild and run the Docker container:
   ```bash
   docker build -t taxi-model-serving .
   docker run -p 8000:8000 taxi-model-serving
   ```

4. If your model input shape or format is different, update `main.py` to reflect those changes.

---

## Notes for Erxi – Input/Output Expectations

- The API currently expects a POST request to `/predict` with JSON payload like:
  ```json
  {
    "features": [feature1, feature2]
  }
  ```
- This can represent any two numeric features relevant to the taxi/event prediction task.
- If feature preprocessing or scaling is required, integrate it into `main.py` before inference.

---

## 🧾 File Overview

| File                   | Purpose                                          |
|------------------------|--------------------------------------------------|
| `app/main.py`          | FastAPI server with POST `/predict` route       |
| `app/model_utils.py`   | Loads the `.pkl` model using `joblib`           |
| `train_dummy_model.py` | Script to generate the dummy LinearRegression   |
| `model.pkl`            | Dummy model file                                |
| `requirements.txt`     | Dependencies list (`fastapi`, `sklearn`, etc.)  |
| `Dockerfile`           | Docker image setup                              |
| `docker-compose.yaml`  | (Optional) Multi-service deployment setup       |
| `predictions_log.csv`  | Stores past prediction requests (for monitoring)|
| `readme.md`            | You're reading it!                              |

---

## Next  Work to do

- Integrate ONNX export + quantization
- Enable Prometheus/Grafana monitoring
- Add versioned model registry
- Canary deploy new models using event zones

---

