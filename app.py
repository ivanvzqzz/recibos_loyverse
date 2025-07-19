import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
from dateutil.parser import isoparse

load_dotenv()

# Time filter: 31 days ago
one_month_ago = (datetime.today() - timedelta(days=31)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

# Load existing file
file_path = Path("receipts.json")

# Get the latest date from receipts, if such file exists
def get_latest_created_at(receipts):
    timestamps = [r["created_at"] for r in receipts if "created_at" in r]
    if not timestamps:
        return None
    latest = max(isoparse(t) for t in timestamps)

    latest_plus = latest + timedelta(seconds=1)
    return latest_plus.strftime("%Y-%m-%dT%H:%M:%S.000Z")

# Load existing receipts
if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            existing_receipts = json.load(f)
        except json.JSONDecodeError:
            existing_receipts = []
else:
    existing_receipts = []

# Call the function to use as parameter
created_at_min = get_latest_created_at(existing_receipts)
if not created_at_min:
    created_at_min = one_month_ago

# API credentials
ACCESS_TOKEN = os.getenv("LOYVERSE_ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise EnvironmentError("No access token found in .env")

# API request setup
url = "https://api.loyverse.com/v1.0/receipts"
urlheaders = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept":"application/json"}

params = {"limit": 50, "created_at_min": created_at_min}
next_cursor = None
new_receipts = []

# HTTP request
while True:
    if next_cursor:
        params["cursor"] = next_cursor
    else:
        params.pop("cursor", None)

    response = requests.get(url, headers=urlheaders, params=params)

    if response.status_code == 200:
        data = response.json()
        receipts = data.get("receipts", [])
        new_receipts.extend(receipts)

        next_cursor = data.get("cursor")
        if not next_cursor:
            break
    else:
        print(f"Error {response.status_code}: {response.text}")
        break

# Combine the receipts
all_receipts = existing_receipts + new_receipts

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(all_receipts, f, ensure_ascii=False, indent=4)

if len(new_receipts) == 0:
    print("No new receipts")
elif len(new_receipts) == 1:
    print(f"Appended 1 new receipt. Total now: {len(all_receipts)}")
else:
    print(f"Appended {len(new_receipts)} new receipts. Total now: {len(all_receipts)}")