import pandas as pd
import os
from pathlib import Path

# Defining paths
EXCEL_DIR = r"c:\Users\Jabegu\Desktop\SQL\Principles-of-Data-Science-Coursework\Data\Raw"
OUTPUT_DIR = r"c:\Users\Jabegu\Desktop\SQL\Principles-of-Data-Science-Coursework\Data\Cleaned Data"

# House Prices data

# Path
prices_file = os.path.join(EXCEL_DIR, "HPSSA Dataset 37 - Median price paid by ward.xls")

# Read the house prices data
df_prices = pd.read_excel(prices_file, sheet_name='1a', skiprows=5)

# Remove rows where all price columns are NaN
price_columns = [col for col in df_prices.columns if col.startswith('Year ending')]
df_prices = df_prices.dropna(subset=price_columns, how='all')

# Keep only essential columns
essential_cols = ['Local authority code', 'Local authority name', 'Ward code', 'Ward name'] + price_columns
df_prices = df_prices[essential_cols].copy()

# Remove rows with empty ward names
df_prices = df_prices[df_prices['Ward name'].notna() & (df_prices['Ward name'] != '')]

# Filter for Oxfordshire data
ox_districts = ['Cherwell', 'Oxford', 'South Oxfordshire', 'Vale of White Horse', 'West Oxfordshire']
df_prices_ox = df_prices[
    df_prices['Local authority name'].astype(str).str.contains('|'.join(ox_districts), case=False, na=False)
].copy()

# Convert price columns to numeric (removing any non-numeric values)
for col in price_columns:
    df_prices_ox[col] = pd.to_numeric(df_prices_ox[col], errors='coerce')

# Save cleaned house prices data
prices_output = os.path.join(OUTPUT_DIR, "house_prices_cleaned.csv")
df_prices_ox.to_csv(prices_output, index=False)
print("House prices data cleaned and saved.")



# Broadband Data

# Paths
broadband_file = os.path.join(EXCEL_DIR, "BroadbandDashboardDataFile.xlsx")
ward_list_file = os.path.join(EXCEL_DIR, "MSOA21_WD25_LAD25_EW_LU_v3.csv")

# Read the data
df_broadband = pd.read_excel(broadband_file, sheet_name='Sub-constituency data', header=2)
df_ward_list = pd.read_csv(ward_list_file)

# Extract ward codes
df_wards_ox = df_ward_list[
    df_ward_list['LAD25NM'].astype(str).str.contains('|'.join(ox_districts), case=False, na=False)
].copy()
ox_ward_codes = df_wards_ox['MSOA21CD'].unique()

# Filter broadband by confirmed Oxfordshire area codes only
df_broadband_filtered = df_broadband[df_broadband['Area code'].isin(ox_ward_codes)].copy()

# Remove rows with all NaN values
df_broadband = df_broadband.dropna(how='all')

# Save cleaned broadband data
broadband_output = os.path.join(OUTPUT_DIR, "broadband_cleaned.csv")
df_broadband_filtered.to_csv(broadband_output, index=False)
print("Broadband data cleaned and saved.")