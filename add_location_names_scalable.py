#!/usr/bin/env python3
"""
Add location names using free nationwide ZIP code database
Works for ANY US state/county - completely scalable
"""

import pandas as pd
import requests
from pathlib import Path
import io
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Add location names to ZIP codes')
parser.add_argument('--data-dir', default='data', help='Input data directory')
parser.add_argument('--output-dir', default='outputs', help='Output directory')
args = parser.parse_args()

data_dir = Path(args.data_dir)
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

print("="*70)
print("DOWNLOADING NATIONWIDE ZIP CODE DATABASE")
print("="*70)

# Step 1: Download free ZIP code database
print("\n[1/4] Downloading free US ZIP code database...")
print("Source: https://github.com/scpike/us-state-county-zip")

try:
    # This GitHub repo has a comprehensive ZIP code database
    url = "https://raw.githubusercontent.com/scpike/us-state-county-zip/master/geo-data.csv"
    
    print(f"Downloading from: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Load into DataFrame
    zip_database = pd.read_csv(io.StringIO(response.text))
    
    print(f"✓ Downloaded {len(zip_database):,} ZIP codes")
    print(f"\nColumns: {list(zip_database.columns)}")
    print(f"\nSample data:")
    print(zip_database.head())
    
    # Save for future use
    db_file = Path('data/us_zip_database.csv')
    zip_database.to_csv(db_file, index=False)
    print(f"\n✓ Saved to: {db_file}")
    
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("\nTrying alternative source...")
    
    try:
        # Alternative: simplemaps.com free basic database
        # This requires manual download, but let's try their API
        url = "https://simplemaps.com/static/data/us-zips/1.82/basic/simplemaps_uszips_basicv1.82.csv"
        
        print(f"Trying: {url}")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            zip_database = pd.read_csv(io.StringIO(response.text))
            print(f"✓ Downloaded {len(zip_database):,} ZIP codes")
        else:
            raise Exception(f"HTTP {response.status_code}")
            
    except Exception as e2:
        print(f"\n❌ Also failed: {e2}")
        print("\n" + "="*70)
        print("MANUAL DOWNLOAD REQUIRED")
        print("="*70)
        print("\nPlease download manually:")
        print("1. Go to: https://simplemaps.com/data/us-zips")
        print("2. Download the FREE 'Basic' version (no account needed)")
        print("3. Extract the CSV file")
        print("4. Save as: data/us_zip_database.csv")
        print("5. Run this script again")
        exit(1)

# Step 2: Clean and prepare the database
print("\n[2/4] Preparing ZIP code database...")

# Standardize column names (different sources use different names)
column_mapping = {
    'zip': 'zip_code',
    'zipcode': 'zip_code',
    'ZIP': 'zip_code',
    'ZIPCODE': 'zip_code',
    'city': 'city',
    'CITY': 'city',
    'primary_city': 'city',
    'state': 'state',
    'STATE': 'state',
    'state_id': 'state',
    'county': 'county',
    'COUNTY': 'county',
    'county_name': 'county',
}

# Rename columns if they exist
for old_name, new_name in column_mapping.items():
    if old_name in zip_database.columns:
        zip_database = zip_database.rename(columns={old_name: new_name})

# Ensure we have the essential columns
required_cols = ['zip_code', 'city', 'state']
missing = [col for col in required_cols if col not in zip_database.columns]

if missing:
    print(f"Error: Missing columns: {missing}")
    print(f"Available columns: {list(zip_database.columns)}")
    exit(1)

# Clean ZIP codes (ensure 5 digits)
zip_database['zip_code'] = zip_database['zip_code'].astype(str).str.zfill(5)

print(f"✓ Prepared {len(zip_database):,} ZIP codes")

# Step 3: Load ZIP scores
print("\n[3/4] Loading your analysis results...")

scores_file = data_dir / 'zip_demographics.csv'
if not scores_file.exists():
    print(f"Error: {scores_file} not found")
    print(f"Run create_zip_demographics.py first")
    exit(1)

scores = pd.read_csv(scores_file)
scores['zip_code'] = scores['zip_code'].astype(str).str.zfill(5)

print(f"✓ Loaded {len(scores)} ZIP codes from demographics")

# Step 4: Match and add location names
print("\n[4/4] Adding location names...")

# Merge with ZIP database
scores_with_names = scores.merge(
    zip_database[['zip_code', 'city', 'state']],
    on='zip_code',
    how='left'
)

# Create friendly location name with ZIP for specificity
def create_location_name(row):
    if pd.notna(row.get('city')) and pd.notna(row.get('state')):
        # Include ZIP in parentheses for specificity
        return f"{row['city']}, {row['state']} ({row['zip_code']})"
    else:
        return f"ZIP {row['zip_code']}"

scores_with_names['location_name'] = scores_with_names.apply(create_location_name, axis=1)

# Count matches
matched = scores_with_names['city'].notna().sum()
unmatched = len(scores) - matched

print(f"✓ Matched: {matched} / {len(scores)} ZIP codes ({matched/len(scores)*100:.1f}%)")
if unmatched > 0:
    print(f"  Unmatched: {unmatched} ZIPs (will show as 'ZIP XXXXX')")

# Save
output_file = output_dir / 'zip_scores_with_names.csv'
scores_with_names.to_csv(output_file, index=False)

print(f"\n✓ Saved to: {output_file}")

# Display results
print("\n" + "="*70)
print("TOP 10 ZIP CODES BY POPULATION")
print("="*70)

# Display results - SKIP IF EMPTY
if len(scores_with_names) > 0:
    print("\n" + "="*70)
    print("TOP 10 ZIP CODES BY POPULATION")
    print("="*70)
    
    top10 = scores_with_names.nlargest(10, 'population')[[
        'location_name', 'zip_code', 'population', 'competitor_count'
    ]]
    
    print(top10.to_string(index=False))
    
    print("\n" + "="*70)
    print("AREAS WITH COMPETITION")
    print("="*70)
    
    with_comp = scores_with_names[scores_with_names['competitor_count'] > 0].head(10)[[
        'location_name', 'zip_code', 'population', 'competitor_count'
    ]]
    
    if len(with_comp) > 0:
        print(with_comp.to_string(index=False))
    else:
        print("No areas with competition found")
else:
    print("\n⚠️  No ZIP codes to display")


# top10 = scores_with_names.nlargest(10, 'population')[[
#     'location_name', 'zip_code', 'population', 'competitor_count'
# ]]

# print(top10.to_string(index=False))

print("\n" + "="*70)
print("AREAS WITH COMPETITION")
print("="*70)

with_comp = scores_with_names[scores_with_names['competitor_count'] > 0].head(10)[[
    'location_name', 'zip_code', 'population', 'competitor_count'
]]

if len(with_comp) > 0:
    print(with_comp.to_string(index=False))
else:
    print("No areas with competition found")

print("\n" + "="*70)
print("SUCCESS!")
print("="*70)
print(f"\n✓ Location names added from nationwide ZIP database")
print(f"✓ Works for ANY US state/county")
print(f"✓ Database saved to: data/us_zip_database.csv")
print(f"✓ Results saved to: {output_file}")
print("\nNow run the dashboard:")
print("  streamlit run src/dashboard.py")