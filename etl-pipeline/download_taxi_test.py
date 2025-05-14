import os
import urllib.request

base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
year = "2025"
month = "01"

output_dir = "/data/output"
os.makedirs(output_dir, exist_ok=True)

file_name = f"yellow_tripdata_{year}-{month}.parquet"
url = f"{base_url}/{file_name}"
dest = os.path.join(output_dir, file_name)

print(f"Downloading {file_name} ...")
urllib.request.urlretrieve(url, dest)
print(f"Downloaded: {file_name}")
