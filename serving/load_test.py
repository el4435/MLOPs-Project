import requests
import time

url = "http://localhost:8000/predict/"
payload = {"features": [1, 14, 6, 1]}
durations = []

for i in range(50):
    start = time.time()
    res = requests.post(url, json=payload)
    end = time.time()
    durations.append(end - start)
    print(f"Request {i+1}: {res.status_code}, Time: {end - start:.4f}s")

avg = sum(durations) / len(durations)
print(f"\n✅ Average Inference Time: {avg:.4f} seconds")
