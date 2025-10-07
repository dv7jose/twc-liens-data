url <- "https://www.twc.texas.gov/sites/default/files/2024-10/liens.xlsx"

download.file(url, "liens.xlsx", mode = "wb")

# Use built-in tools: read the Excel as text via shell conversion (simpler)
system("libreoffice --headless --convert-to csv liens.xlsx --outdir .", ignore.stderr = TRUE)

# Rename output (LibreOffice names it liens.csv automatically)
if (!file.exists("liens.csv")) {
  stop("CSV not created")
}
library(httr2)
library(readxl)
library(readr)

url <- "https://www.twc.texas.gov/sites/default/files/2024-10/liens.xlsx"

req_perform(req(url), path = "liens.xlsx")
read_excel("liens.xlsx") |> write_csv("liens.csv")

