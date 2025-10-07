import pandas as pd
import requests
from io import BytesIO
import re

file_url = "https://www.twc.texas.gov/sites/default/files/finance/docs/wage-hour-liens-over-2k-twc.xlsx"

r = requests.get(file_url, allow_redirects=True, timeout=60)
r.raise_for_status()

# Read only columns A–F
df = pd.read_excel(BytesIO(r.content), engine="openpyxl", usecols="A:F")
df = df.dropna(how="all")

# Rename columns to AP style (lowercase, underscores)
df.columns = [
    "employer_name",
    "employer_address_1",
    "employer_address_2",
    "employer_address_3",
    "first_date_of_lien",
    "delinquent_amount"
]

# --- Split city and zip/state ---
def split_city_zip(value):
    if pd.isna(value):
        return pd.Series([None, None])
    # Remove stray quotes/spaces
    value = str(value).strip().replace("  ", " ").replace(" ,", ",")
    # Example: "AUSTIN TX,  78745-5742"
    parts = re.split(r",\s*", value)
    city_state = parts[0].strip()
    zip_part = parts[1].strip() if len(parts) > 1 else None

    # Try to separate city from state (pattern: CITY STATE)
    m = re.match(r"^(.*)\s+([A-Z]{2})$", city_state)
    if m:
        city = m.group(1).title()
        state = m.group(2)
    else:
        # fallback if city_state like "AUSTIN TX"
        tokens = city_state.split()
        city = " ".join(tokens[:-1]).title() if len(tokens) > 1 else city_state.title()
        state = tokens[-1] if len(tokens) > 1 else None

    return pd.Series([city, f"{state} {zip_part}" if state and zip_part else state or zip_part])

df[["city", "state_zip"]] = df["employer_address_3"].apply(split_city_zip)
df = df.drop(columns=["employer_address_3"])

# Clean capitalization and spacing in employer names and addresses
def title_clean(s):
    if pd.isna(s):
        return None
    s = re.sub(r"[^A-Za-z0-9&.,' ]+", "", str(s))
    return s.title().replace("L.L.C.", "LLC").replace("L.L.C", "LLC").replace("Inc.", "Inc")

df["employer_name"] = df["employer_name"].apply(title_clean)
df["employer_address_1"] = df["employer_address_1"].apply(title_clean)
df["employer_address_2"] = df["employer_address_2"].apply(title_clean)

# Reorder and rename columns in Title Case for Datawrapper
df = df[
    [
        "employer_name",
        "employer_address_1",
        "employer_address_2",
        "city",
        "state_zip",
        "first_date_of_lien",
        "delinquent_amount",
    ]
]

# Title Case the column headers for output
df.columns = [
    "Employer Name",
    "Employer Address 1",
    "Employer Address 2",
    "City",
    "State Zip",
    "First Date of Lien",
    "Delinquent Amount",
]

print(f"✅ Cleaned {len(df)} rows × {len(df.columns)} columns (Title Case headers)")
df.to_csv("liens.csv", index=False)
print("✅ liens.csv written successfully.")
