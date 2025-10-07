library(httr2)
library(readxl)
library(readr)

url <- "https://www.twc.texas.gov/sites/default/files/2024-10/liens.xlsx"

req_perform(req(url), path = "liens.xlsx")
read_excel("liens.xlsx") |> write_csv("liens.csv")

