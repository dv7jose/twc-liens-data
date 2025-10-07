import pandas as pd
import requests
from io import BytesIO

file_url = "https://www.twc.texas.gov/sites/default/files/finance/docs/wage-hour-liens-over-2k-twc.xlsx"

r = requests.get(file_url, allow_redirects=True, timeout=60)
r.raise_for_status()

# Only read columns A–F (first six)
df = pd.read_excel(BytesIO(r.content), engine="openpyxl", sheet_name=0, usecols="A:F")

# Clean up
df = df.dropna(how="all", axis=0)
df.columns = df.columns.str.strip()

print(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns (A–F only)")
df.to_csv("liens.csv", index=False)
print("✅ liens.csv ready for commit.")
