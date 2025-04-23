import os
import urllib.request

base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
months = [f"{m:02d}" for m in range(1, 13)]
year = "2024"

output_dir = "/data/output"
os.makedirs(output_dir, exist_ok=True)

for month in months:
    file_name = f"yellow_tripdata_{year}-{month}.parquet"
    url = f"{base_url}/{file_name}"
    dest = os.path.join(output_dir, file_name)

    if os.path.exists(dest):
        print(f"[✓] Already exists: {file_name}")
        continue

    print(f"Downloading {file_name} ...")
    urllib.request.urlretrieve(url, dest)
    print(f"Downloaded: {file_name}")
