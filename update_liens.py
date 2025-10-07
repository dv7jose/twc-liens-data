import pandas as pd
import requests
from io import BytesIO

file_url = "https://www.twc.texas.gov/sites/default/files/finance/docs/wage-hour-liens-over-2k-twc.xlsx"

r = requests.get(file_url, allow_redirects=True, timeout=60)
r.raise_for_status()

df = pd.read_excel(BytesIO(r.content), engine="openpyxl", sheet_name=0)
df = df.dropna(how="all", axis=0).dropna(how="all", axis=1)
df.columns = df.columns.str.strip()

print(f"✅ Cleaned {len(df)} rows × {len(df.columns)} columns")
df.to_csv("liens.csv", index=False)
print("✅ liens.csv ready for commit.")
