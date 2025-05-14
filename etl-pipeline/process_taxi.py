import os
import pandas as pd
import time
from prometheus_client import start_http_server, Counter, Gauge

# Prometheus metrics
taxi_rows = Counter("taxi_rows_processed_total", "Total number of taxi rows processed")
skipped_files = Counter("taxi_files_skipped_total", "Total number of taxi files skipped due to errors")
etl_duration = Gauge("etl_duration_seconds", "Duration of the ETL process in seconds")

# Start Prometheus HTTP server on port 9200
start_http_server(9200)

# ETL start
start_time = time.time()

INPUT_DIR = "/data/output"
OUTPUT_CSV = os.path.join(INPUT_DIR, "taxi_demand_by_zone_hour.csv")

print("Scanning input directory:", INPUT_DIR)
parquet_files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".parquet"))

# frames = []
# for file in parquet_files:
#     path = os.path.join(INPUT_DIR, file)
#     print(f"Reading {file} ...")
#     df = pd.read_parquet(path, engine="pyarrow")

#     # Skip files that don't have expected columns
#     if "tpep_pickup_datetime" not in df.columns or "PULocationID" not in df.columns:
#         print(f"Skipping {file}: Missing expected columns.")
#         continue

#     # Extract necessary fields
#     df = df[["tpep_pickup_datetime", "PULocationID"]].copy()
#     df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
#     df["date"] = df["pickup_datetime"].dt.date
#     df["hour"] = df["pickup_datetime"].dt.hour

#     # Aggregate pickup counts by date, hour, and pickup zone
#     grouped = df.groupby(["date", "hour", "PULocationID"]).size().reset_index(name="pickup_count")
#     frames.append(grouped)

# print("Merging monthly data ...")
# result = pd.concat(frames, ignore_index=True)

# print(f"Saving output CSV to {OUTPUT_CSV}")
# result.to_csv(OUTPUT_CSV, index=False)
# print("Processing complete.")

frames = []
for file in parquet_files:
    path = os.path.join(INPUT_DIR, file)
    print(f"Reading {file} ...")
    try:
        df = pd.read_parquet(path, engine="pyarrow")
    except Exception as e:
        print(f"Error reading {file}: {e}")
        skipped_files.inc()
        continue

    if "tpep_pickup_datetime" not in df.columns or "PULocationID" not in df.columns:
        print(f"Skipping {file}: Missing expected columns.")
        skipped_files.inc()
        continue

    df = df[["tpep_pickup_datetime", "PULocationID"]].copy()
    df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["date"] = df["pickup_datetime"].dt.date
    df["hour"] = df["pickup_datetime"].dt.hour

    grouped = df.groupby(["date", "hour", "PULocationID"]).size().reset_index(name="pickup_count")
    taxi_rows.inc(len(grouped))  # Increment metric
    frames.append(grouped)

print("Merging monthly data ...")
result = pd.concat(frames, ignore_index=True)

print(f"Saving output CSV to {OUTPUT_CSV}")
result.to_csv(OUTPUT_CSV, index=False)
print("Processing complete.")

# ETL end
etl_duration.set(time.time() - start_time)

# --- Keep Prometheus server running after ETL ---
print("ETL complete. Prometheus metrics server is still running on port 9200.")
print("Press Ctrl+C to exit (or stop the container).")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting gracefully.")
