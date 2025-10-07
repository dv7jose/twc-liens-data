import pandas as pd
import requests
from io import BytesIO

file_url = "https://www.twc.texas.gov/sites/default/files/finance/docs/wage-hour-liens-over-2k-twc.xlsx"

print("Downloading:", file_url)
r = requests.get(file_url, allow_redirects=True, timeout=60)
r.raise_for_status()

# Load only real rows, drop full-NaN lines, avoid ghost sheets
df = pd.read_excel(BytesIO(r.content), engine="openpyxl", sheet_name=0)
df = df.dropna(how="all")

# Optional: limit to visible columns if TWC includes filler columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
df.to_csv("liens.csv", index=False)
print("✅ liens.csv written successfully.")
