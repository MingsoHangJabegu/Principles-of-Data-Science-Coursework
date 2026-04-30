import xml.etree.ElementTree as ET
import os
import pandas as pd


def xml_council_tax(bands=None):
    # Load and parse the XML file
    tree = ET.parse(os.getcwd() + "/council_tax.xml")
    root = tree.getroot()

    # Extract data into a list of dictionaries
    tax_data = []
    for district in root.findall('District'):
        for area in district.findall('area'):
            area_name = area.attrib.get('name', '')
            for band in area.findall('band'):
                row = {'area': area_name}
                band_type = band.find('type')
                amount = band.find('amount')
                if band_type is not None and amount is not None:
                    row['band'] = band_type.text
                    row['amount'] = amount.text
                    tax_data.append(row)

    # Convert to DataFrame
    tax_df = pd.DataFrame(tax_data)

    # Question 11
    # Convert amount to float for calculations
    tax_df['amount'] = tax_df['amount'].astype(float)

    # By default
    if bands is None:
        bands = ['A', 'B', 'C']
    
    # For selected bands
    if isinstance(bands, str):
        bands = [bands]
    bands = [str(band).upper() for band in bands if isinstance(band, str)]
    bands = bands[:3] if bands else ['A', 'B', 'C']

    # Filter for selected bands
    filtered_df = tax_df[tax_df['band'].isin(bands)]

    # Calculate average per area for selected bands
    area_averages = filtered_df.groupby('area')['amount'].mean()

    # Question 12
    # Find town with highest Band C tax
    band_c_df = tax_df[tax_df['band'] == 'C']
    max_row = band_c_df.loc[band_c_df['amount'].idxmax()]
    return area_averages, max_row    
