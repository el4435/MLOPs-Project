import pandas as pd
import os

input_path = "/data/output/taxi_demand_by_zone_hour.csv"
output_dir = "/data/output"
os.makedirs(output_dir, exist_ok=True)

print(f"Reading: {input_path}")
df = pd.read_csv(input_path)

# Ensure datetime format
df["pickup_hour"] = pd.to_datetime(df["pickup_hour"], errors="coerce")

# Split based on time
train_df = df[(df["pickup_hour"] >= "2024-01-01") & (df["pickup_hour"] < "2024-10-01")]
val_df   = df[(df["pickup_hour"] >= "2024-10-01") & (df["pickup_hour"] < "2025-01-01")]
test_df  = df[(df["pickup_hour"] >= "2025-01-01") & (df["pickup_hour"] < "2025-02-01")]

# Save splits
train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
val_df.to_csv(os.path.join(output_dir, "val.csv"), index=False)
test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)

print("Dataset split complete.")
print(f"Train: {len(train_df)} rows")
print(f"Val:   {len(val_df)} rows")
print(f"Test:  {len(test_df)} rows")
