import os
import pandas as pd

INPUT_DIR = "/data/output"
OUTPUT_CSV = os.path.join(INPUT_DIR, "taxi_demand_by_zone_hour.csv")

print("Scanning input directory:", INPUT_DIR)
parquet_files = sorted(f for f in os.listdir(INPUT_DIR) if f.endswith(".parquet"))

frames = []
for file in parquet_files:
    path = os.path.join(INPUT_DIR, file)
    print(f"Reading {file} ...")
    df = pd.read_parquet(path, engine="pyarrow")

    # Skip files that don't have expected columns
    if "tpep_pickup_datetime" not in df.columns or "PULocationID" not in df.columns:
        print(f"Skipping {file}: Missing expected columns.")
        continue

    # Extract necessary fields
    df = df[["tpep_pickup_datetime", "PULocationID"]].copy()
    df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["date"] = df["pickup_datetime"].dt.date
    df["hour"] = df["pickup_datetime"].dt.hour

    # Aggregate pickup counts by date, hour, and pickup zone
    grouped = df.groupby(["date", "hour", "PULocationID"]).size().reset_index(name="pickup_count")
    frames.append(grouped)

print("Merging monthly data ...")
result = pd.concat(frames, ignore_index=True)

print(f"Saving output CSV to {OUTPUT_CSV}")
result.to_csv(OUTPUT_CSV, index=False)
print("Processing complete.")
