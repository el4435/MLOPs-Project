import os
import urllib.request
from datetime import datetime
import time

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
OUTPUT_DIR = "/data/output"

def download_latest_month():
    now = datetime.now()
    year, month = now.year, now.month
    file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
    url = f"{BASE_URL}/{file_name}"
    dest = os.path.join(OUTPUT_DIR, file_name)

    if os.path.exists(dest):
        print(f"[✓] Already exists: {file_name}")
        return

    try:
        print(f"Downloading {file_name} ...")
        urllib.request.urlretrieve(url, dest)
        print(f"Downloaded: {file_name}")
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    while True:
        download_latest_month()
        time.sleep(3600 * 6)  # check every 6 hours
