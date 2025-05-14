import urllib.request
import urllib.parse
import os
import pandas as pd
from datetime import datetime, timedelta

output_dir = "/data/events"
os.makedirs(output_dir, exist_ok=True)

base_url = "https://data.cityofnewyork.us/resource/bkfu-528j.csv"
limit = 50000

months = [(2024, m) for m in range(1, 13)]

for year, month in months:
    print(f"\nFetching events for {year}-{month:02d} ...")
    start = datetime(year, month, 1)
    end = (start + timedelta(days=31)).replace(day=1)
    start_str = start.strftime("%Y-%m-%dT00:00:00")
    end_str = end.strftime("%Y-%m-%dT00:00:00")
    where_clause = f"start_date_time between '{start_str}' and '{end_str}'"
    encoded_where = urllib.parse.quote(where_clause)

    combined_df = []
    offset = 0
    page = 1

    while True:
        url = f"{base_url}?$where={encoded_where}&$limit={limit}&$offset={offset}&$order=start_date_time"
        filename = f"temp_{year}-{month:02d}_page{page}.csv"
        dest = os.path.join(output_dir, filename)

        print(f"Downloading page {page} with offset {offset} ...")
        try:
            urllib.request.urlretrieve(url, dest)
            df = pd.read_csv(dest)
            if df.empty:
                print(f"No more data at offset {offset}. Done.")
                os.remove(dest)
                break

            combined_df.append(df)
            print(f"Downloaded {len(df)} rows.")
            os.remove(dest)

            if len(df) < limit:
                print(f"Final page reached at offset {offset}.")
                break

            offset += limit
            page += 1
        except Exception as e:
            print(f"Download failed at offset {offset}: {e}")
            break

    if combined_df:
        full_month_df = pd.concat(combined_df, ignore_index=True)
        final_path = os.path.join(output_dir, f"events_{year}-{month:02d}.csv")
        full_month_df.to_csv(final_path, index=False)
        print(f"Saved complete month to: {final_path}")
    else:
        print(f"No data found for {year}-{month:02d}")
