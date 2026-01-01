#!/usr/bin/env python3
"""
Debug script to check Yelp ZIP codes
"""

import pandas as pd

# Load competitor data
competitors = pd.read_csv('data/competitors_raw.csv')

print("="*60)
print("YELP DATA ANALYSIS")
print("="*60)

print(f"\nTotal businesses: {len(competitors)}")

print("\nZIP codes in data:")
zip_counts = competitors['zip_code'].value_counts()
print(zip_counts)

print("\nSample businesses:")
print(competitors[['business_name', 'city', 'zip_code']].head(10))

print("\nUnique ZIP codes:")
unique_zips = competitors['zip_code'].unique()
print(sorted([str(z) for z in unique_zips]))

print("\nData types:")
print(competitors.dtypes)