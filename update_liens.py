import pandas as pd
import requests
from io import BytesIO

# Direct file URL from the TWC page
file_url = "https://www.twc.texas.gov/sites/default/files/finance/docs/wage-hour-liens-over-2k-twc.xlsx"

print("Downloading:", file_url)
r = requests.get(file_url, allow_redirects=True)
r.raise_for_status()

# Verify we actually got an Excel file
ctype = r.headers.get("Content-Type", "")
if "excel" not in ctype and not file_url.endswith(".xlsx"):
    raise RuntimeError(f"Download failed or not an Excel file: {ctype}")

# Read Excel straight from memory
df = pd.read_excel(BytesIO(r.content), engine="openpyxl")
df.to_csv("liens.csv", index=False)
print("✅ liens.csv updated successfully.")
