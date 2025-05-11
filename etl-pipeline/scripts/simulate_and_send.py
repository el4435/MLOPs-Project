import random
import time
import requests
import json
from datetime import datetime, timedelta

zones = list(range(1, 264))  # NYC zone IDs

def generate_request():
    now = datetime.now()
    future_time = now + timedelta(minutes=random.randint(0, 60))
    pickup_zone = random.choice(zones)

    # hour 和 zone ID
    feature_vector = [future_time.hour, pickup_zone]

    return {
        "features": feature_vector,
        "timestamp": future_time.strftime("%Y-%m-%d %H:%M:%S"),
        "zone": pickup_zone
    }

if __name__ == "__main__":
    endpoint = "http://localhost:8000/predict"
    print("Starting simulated prediction stream...")

    while True:
        req = generate_request()
        payload = {"features": req["features"]}

        try:
            response = requests.post(endpoint, json=payload)
            prediction = response.json()
            print(f"[{req['timestamp']}] Zone {req['zone']} → Prediction: {prediction}")
        except Exception as e:
            print("Prediction failed:", e)

        time.sleep(2)  
