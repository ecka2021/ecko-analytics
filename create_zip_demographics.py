#!/usr/bin/env python3
"""
Create ZIP-level demographics (SCALABLE VERSION)
Works for any city - no hardcoded neighborhoods
Supports city-specific directories
"""

import pandas as pd
import numpy as np
from pathlib import Path
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Aggregate census tracts to ZIP codes')
parser.add_argument('--data-dir', default='data', help='Input data directory')
args = parser.parse_args()

data_dir = Path(args.data_dir)

print("="*70)
print("CREATING ZIP-LEVEL DEMOGRAPHICS (SCALABLE)")
print("="*70)

# Load data
print("\n[1/5] Loading data...")
census = pd.read_csv(data_dir / 'demographics_raw.csv')

# Try to load full US crosswalk first, fall back to LA-only
crosswalk_file = Path('data/us_tract_zip_crosswalk.csv')
if crosswalk_file.exists():
    crosswalk = pd.read_csv(crosswalk_file)
    
    # Get state/county from census data and convert to int (handles "06" → 6, "037" → 37)
    state_fips = int(census['state'].iloc[0])
    county_fips = int(census['county'].iloc[0])
    
    print(f"  Using nationwide crosswalk")
    print(f"  Filtering for state {state_fips}, county {county_fips}")
    
    # Filter to only this state/county (integer comparison)
    crosswalk = crosswalk[
        (crosswalk['state_fips'] == state_fips) & 
        (crosswalk['county_fips'] == county_fips)
    ]
    
    print(f"  Filtered to {len(crosswalk)} county-specific mappings")
else:
    # Fallback to LA-only for backwards compatibility
    crosswalk = pd.read_csv('data/la_tract_zip_crosswalk.csv')
    print(f"  Using LA County crosswalk only")

competitors = pd.read_csv(data_dir / 'competitors_raw.csv')

print(f"  Census tracts: {len(census)}")
print(f"  Tract-ZIP mappings: {len(crosswalk)}")
print(f"  Businesses: {len(competitors)}")

# Match census tracts to ZIP codes
print("\n[2/5] Matching census tracts to ZIP codes...")

census['tract_clean'] = census['tract'].astype(str).str.replace('.', '')
crosswalk['tract_code'] = crosswalk['tract_code'].astype(str)
crosswalk['zip_code'] = crosswalk['zip_code'].astype(str).str.zfill(5)

census_with_zip = census.merge(
    crosswalk[['tract_code', 'zip_code']],
    left_on='tract_clean',
    right_on='tract_code',
    how='left'
)

matched = census_with_zip['zip_code'].notna().sum()
print(f"  Matched {matched} / {len(census)} census tracts to ZIP codes")

# Handle duplicates (tracts that match multiple ZIPs)
print("\n[3/5] Deduplicating (keeping first ZIP per tract)...")
census_dedup = census_with_zip.drop_duplicates(subset=['tract_clean'], keep='first')
print(f"  After dedup: {len(census_dedup)} unique tracts")

# Aggregate by ZIP code
print("\n[4/5] Aggregating census data by ZIP code...")

zip_demographics = census_dedup.groupby('zip_code').agg({
    'population': 'sum',
    'median_income': 'median',
    'renter_rate': 'mean',
    'median_age': 'mean',
    'area_sq_miles': 'sum',
    'tract_clean': 'count'  # Count of tracts per ZIP
}).reset_index()

zip_demographics.columns = [
    'zip_code', 'population', 'median_income', 'renter_rate',
    'median_age', 'area_sq_miles', 'tract_count'
]

zip_demographics['population_density'] = (
    zip_demographics['population'] / 
    zip_demographics['area_sq_miles']
).replace([np.inf, -np.inf], 0)

print(f"  Created demographics for {len(zip_demographics)} ZIP codes")

# Add competitor data
print("\n[5/5] Adding competitor counts by ZIP...")

competitors['zip_code'] = competitors['zip_code'].astype(str).str.zfill(5)

comp_counts = competitors.groupby('zip_code').agg({
    'business_name': 'count',
    'rating': 'mean',
    'review_count': 'sum'
}).reset_index()

comp_counts.columns = ['zip_code', 'competitor_count', 'avg_rating', 'total_reviews']

# Merge
final_data = zip_demographics.merge(
    comp_counts, on='zip_code', how='left'
)

final_data['competitor_count'] = final_data['competitor_count'].fillna(0)
final_data['avg_rating'] = final_data['avg_rating'].fillna(0)
final_data['total_reviews'] = final_data['total_reviews'].fillna(0)

# Display results
print("\n" + "="*70)
print("ZIP-LEVEL DEMOGRAPHICS (Top 20 by population)")
print("="*70)

summary = final_data.nlargest(20, 'population').copy()
summary['population'] = summary['population'].astype(int)
summary['median_income'] = summary['median_income'].round(0).astype(int)
summary['renter_rate'] = (summary['renter_rate'] * 100).round(1)
summary['pop_density'] = summary['population_density'].round(0).astype(int)
summary['competitors'] = summary['competitor_count'].astype(int)

display_cols = ['zip_code', 'population', 'median_income', 'renter_rate',
                'pop_density', 'tract_count', 'competitors']
print(summary[display_cols].to_string(index=False))

# Save
output_file = data_dir / 'zip_demographics.csv'
final_data.to_csv(output_file, index=False)

print(f"\n✓ Saved to: {output_file}")

# Also save tract-to-ZIP mapping
census_dedup[['tract_name', 'tract_clean', 'zip_code']].to_csv(
    data_dir / 'tract_to_zip_mapping.csv', index=False
)

print(f"✓ Saved tract mapping to: {data_dir / 'tract_to_zip_mapping.csv'}")

print("\n" + "="*70)
print("SUCCESS!")
print("="*70)
print(f"\nCreated demographics for {len(final_data)} ZIP codes")
print(f"Based on {len(census_dedup)} census tracts")
print(f"\nThis approach works for ANY city/county!")
print(f"No hardcoded neighborhoods required.")