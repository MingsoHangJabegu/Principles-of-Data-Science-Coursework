import pandas as pd
import os

# Paths
BASE_DIR = os.getcwd()
BB_PATH  = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", "Data",
                         "Cleaned Data", "broadband_cleaned.csv")
HP_PATH  = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                        "Data", "Cleaned Data", "house_prices_cleaned.csv")
CT_PATH  = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                        "Data", "Raw", "Council Tax.xlsx")
DB_PATH  = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", "Coursework.db")


# Read data

# Read broadband data
bb = pd.read_csv(BB_PATH)

# Rename columns for consistency
bb.columns = [
    "area_code", "area_name",
    "superfast_availability", "gigabit_availability",
    "below_uso", "avg_download_speed_mbps",
    "under_10_mbps", "over_30_mbps",
]

# Read house prices data
hp = pd.read_csv(HP_PATH)

# Read council tax data
ct = pd.read_excel(CT_PATH, engine="openpyxl")

# Rename columns for consistency
ct.columns = ["area_name", "A", "B", "C", "D", "E", "F", "G", "H"]

# For local_authority table
local_authority = (
    hp[["Local authority code", "Local authority name"]]
    .drop_duplicates()
    .rename(columns={
        "Local authority code":"local_authority_code",
        "Local authority name":"local_authority_name",
    })
    .reset_index(drop=True)
)

# Save cleaned local authority data
local_authority_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "local_authority.csv")
local_authority.to_csv(local_authority_output, index=False)
print("Local Authority data cleaned and saved.")

# For ward table
ward = (
    hp[["Ward code", "Ward name", "Local authority code"]]
    .drop_duplicates()
    .rename(columns={
        "Ward code":"ward_code",
        "Ward name":"ward_name",
        "Local authority code":"local_authority_code",
    })
    .reset_index(drop=True)
)

# Save cleaned ward data
ward_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "ward.csv")
ward.to_csv(ward_output, index=False)
print("Ward data cleaned and saved.")

# For broadband_area table
broadband_area = (
    bb[["area_code", "area_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Save cleaned broadband area data
broadband_area_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "broadband_area.csv")
broadband_area.to_csv(broadband_area_output, index=False)
print("Broadband Area data cleaned and saved.")

# For broadband_metric table
broadband_metric = bb.drop(columns=["area_name"]).reset_index(drop=True)

# Save cleaned broadband metrics data
broadband_metric_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "broadband_metric.csv")    
broadband_metric.to_csv(broadband_metric_output, index=False)
print("Broadband Metrics data cleaned and saved.")

# For house_price table

# Extract period columns
period_cols = [c for c in hp.columns if c.startswith("Year ending")]

# Pivot from wide to long
house_price = (
    hp[["Ward code"] + period_cols]
    .melt(id_vars="Ward code", var_name="period", value_name="median_price")
    .rename(columns={"Ward code": "ward_code"})
)

# Add period column and remove "Year ending"
house_price["period"] = house_price["period"].str.replace(
    "Year ending ", "", regex=False
)

# Remove missing data
house_price = (
    house_price
    .dropna(subset=["median_price"])
    .reset_index(drop=True)
    [["ward_code", "period", "median_price"]]
)

# Save cleaned house price data
house_price_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "house_price.csv")
house_price.to_csv(house_price_output, index=False)
print("House Price data cleaned and saved.")

# For council_tax_area table
council_tax_area = (
    ct[["area_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Add area_id
council_tax_area["area_id"] = council_tax_area.index + 1

# Reorder columns for consistency
council_tax_area = council_tax_area[["area_id", "area_name"]]

# Save cleaned council tax area data
council_tax_area_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "council_tax_area.csv")
council_tax_area.to_csv(council_tax_area_output, index=False)
print("Council Tax Area data cleaned and saved.")

# For council_tax_rate table
# Pivot from wide to long and remove missing data
council_tax_rate = (
    ct.melt(id_vars="area_name", var_name="tax_band", value_name="tax_amount")
    .dropna(subset=["tax_amount"])
    .reset_index(drop=True)
)

# Merge with council_tax_area to replace area_name with area_id
council_tax_rate = (
    council_tax_rate
    .merge(council_tax_area, on="area_name")
    .drop(columns=["area_name"])
)

# Reorder columns for consistency
council_tax_rate = council_tax_rate[["area_id", "tax_band", "tax_amount"]]

# Save cleaned council tax rate data
council_tax_rate_output = os.path.join(BASE_DIR, "Principles-of-Data-Science-Coursework", 
                                    "Data", "Cleaned Data", "council_tax_rate.csv")
council_tax_rate.to_csv(council_tax_rate_output, index=False)
print("Council Tax Rate data cleaned and saved.")