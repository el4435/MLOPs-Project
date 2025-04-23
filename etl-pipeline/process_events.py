import os
import pandas as pd

input_dir = "/data/events"
output_path = os.path.join(input_dir, "processed_events_2024.csv")

frames = []
for file in sorted(os.listdir(input_dir)):
    if file.startswith("events_2024-") and file.endswith(".csv"):
        path = os.path.join(input_dir, file)
        print(f"Reading: {file}")
        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f"Failed to read {file}: {e}")
            continue

        df.columns = df.columns.str.strip()

        # Ensure datetime format
        if "start_date_time" in df.columns:
            df["start_date_time"] = pd.to_datetime(df["start_date_time"], errors="coerce")
        if "end_date_time" in df.columns:
            df["end_date_time"] = pd.to_datetime(df["end_date_time"], errors="coerce")

        # Keep selected fields
        selected_cols = [
            "event_id",
            "event_name",
            "start_date_time",
            "end_date_time",
            "event_type",
            "event_borough",
            "event_location",
            "street_closure_type"
        ]
        df = df[[col for col in selected_cols if col in df.columns]]

        frames.append(df)

# Merge
if frames:
    result = pd.concat(frames, ignore_index=True)
    result.to_csv(output_path, index=False)
    print(f"Saved merged dataset to: {output_path}")
    print(f"Total events processed: {len(result)}")
else:
    print("No valid files found to process.")
