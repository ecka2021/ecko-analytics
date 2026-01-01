#!/usr/bin/env python3
"""
Process HUD ZIP-TRACT crosswalk for ALL US counties
Replaces process_manual_crosswalk.py (which only did LA County)
"""

import pandas as pd

print("Processing manually downloaded crosswalk file...")
print("This version extracts ALL US counties, not just LA County")

# Read the Excel file - force TRACT column as string to preserve leading zeros
df = pd.read_excel('data/zip_tract_crosswalk.xlsx', dtype={'TRACT': str})

print(f"\nTotal records: {len(df):,}")
print(f"Columns: {list(df.columns)}")

# Find tract and ZIP columns
tract_col = [c for c in df.columns if 'TRACT' in c.upper()][0]
zip_col = [c for c in df.columns if 'ZIP' in c.upper()][0]

print(f"\nUsing columns: {tract_col}, {zip_col}")

# Show sample of tract codes
print(f"\nSample TRACT values from file:")
print(df[tract_col].head(10).tolist())

# The TRACT column format is: 06037101110 (as string now)
# Where: 06 = state FIPS, 037 = county FIPS, 101110 = tract code

# Extract components - keeping as strings with padding
df['tract_full'] = df[tract_col].astype(str).str.zfill(11)  # Pad to 11 digits
df['state_fips'] = df['tract_full'].str[:2].astype(int)  # First 2 chars as int
df['county_fips'] = df['tract_full'].str[2:5].astype(int)  # Next 3 chars as int
df['tract_code'] = df['tract_full'].str[5:]  # Rest is tract code (as string)
df['zip_code'] = df[zip_col].astype(str).str.zfill(5)

print(f"\nSample extracted tract codes:")
print(df[['state_fips', 'county_fips', 'tract_code', 'zip_code']].head(10))

# Count by state
print(f"\nRecords per state (top 10):")
state_counts = df.groupby('state_fips').size().sort_values(ascending=False)
print(state_counts.head(10))

# Save the FULL nationwide crosswalk
output = df[['state_fips', 'county_fips', 'tract_code', 'zip_code']].drop_duplicates()
output.to_csv('data/us_tract_zip_crosswalk.csv', index=False)

print(f"\n✓ Saved FULL US crosswalk to: data/us_tract_zip_crosswalk.csv")
print(f"  {len(output):,} unique tract-ZIP mappings for ALL US counties")

# Also save LA County separately for backwards compatibility
la_data = df[df['state_fips'] == '06']
la_data = la_data[la_data['county_fips'] == '037']
la_output = la_data[['tract_code', 'zip_code']].drop_duplicates()
la_output.to_csv('data/la_tract_zip_crosswalk.csv', index=False)

print(f"\n✓ Also saved LA County to: data/la_tract_zip_crosswalk.csv")
print(f"  {len(la_output)} LA County tract-ZIP mappings")

# Show Cook County (Chicago) as example
cook_data = df[df['state_fips'] == '17']
cook_data = cook_data[cook_data['county_fips'] == '031']

if len(cook_data) > 0:
    cook_output = cook_data[['tract_code', 'zip_code']].drop_duplicates()
    cook_output.to_csv('data/cook_tract_zip_crosswalk.csv', index=False)
    
    print(f"\n✓ Also saved Cook County (Chicago) to: data/cook_tract_zip_crosswalk.csv")
    print(f"  {len(cook_output)} Cook County tract-ZIP mappings")
    
    print(f"\nSample Cook County mappings:")
    print(cook_output.head(10))

print(f"\n" + "="*70)
print("SUCCESS!")
print("="*70)
print(f"\nYou now have:")
print(f"  1. Full US crosswalk: data/us_tract_zip_crosswalk.csv ({len(output):,} mappings)")
print(f"  2. LA County: data/la_tract_zip_crosswalk.csv ({len(la_output)} mappings)")
if len(cook_data) > 0:
    print(f"  3. Cook County: data/cook_tract_zip_crosswalk.csv ({len(cook_output)} mappings)")