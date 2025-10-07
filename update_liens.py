import pandas as pd
import requests

url = "https://www.twc.texas.gov/sites/default/files/2024-10/liens.xlsx"

r = requests.get(url)
with open("liens.xlsx", "wb") as f:
    f.write(r.content)

df = pd.read_excel("liens.xlsx")
df.to_csv("liens.csv", index=False)
