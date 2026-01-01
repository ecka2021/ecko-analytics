#!/usr/bin/env python3
"""
Download nationwide county database for FIPS code lookup
This eliminates hardcoding - works for ALL 3,143 US counties
"""

import pandas as pd
import requests
import io
from pathlib import Path

print("="*70)
print("DOWNLOADING US COUNTY DATABASE")
print("="*70)

try:
    # Free county database from US Census Bureau
    url = "https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt"
    
    print(f"\nDownloading from US Census Bureau...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    # Parse the CSV (no header in source file)
    df = pd.read_csv(
        io.StringIO(response.text),
        names=['state_abbr', 'state_fips', 'county_fips', 'county_name', 'classification']
    )
    
    print(f"✓ Downloaded {len(df):,} US counties")
    
    # Clean data
    df['state_fips'] = df['state_fips'].astype(str).str.zfill(2)
    df['county_fips'] = df['county_fips'].astype(str).str.zfill(3)
    df['full_fips'] = df['state_fips'] + df['county_fips']
    
    # Create searchable name
    df['search_name'] = df['county_name'].str.lower().str.replace(' county', '').str.replace(' parish', '')
    
    # Save
    output_file = Path('data/us_counties.csv')
    df.to_csv(output_file, index=False)
    
    print(f"✓ Saved to: {output_file}")
    
    # Show examples
    print("\n" + "="*70)
    print("SAMPLE DATA")
    print("="*70)
    
    print("\nCalifornia counties:")
    ca = df[df['state_abbr'] == 'CA'].head(10)
    print(ca[['county_name', 'state_abbr', 'state_fips', 'county_fips']])
    
    print("\nIllinois counties:")
    il = df[df['state_abbr'] == 'IL'].head(10)
    print(il[['county_name', 'state_abbr', 'state_fips', 'county_fips']])
    
    print("\n" + "="*70)
    print("HOW TO USE")
    print("="*70)
    print("""
Now you can look up ANY county:

>>> import pandas as pd
>>> counties = pd.read_csv('data/us_counties.csv')

# Find Los Angeles County
>>> la = counties[(counties['state_abbr'] == 'CA') & 
                  (counties['search_name'] == 'los angeles')]
>>> print(la['state_fips'], la['county_fips'])
06 037

# Find Cook County (Chicago)
>>> cook = counties[(counties['state_abbr'] == 'IL') & 
                    (counties['search_name'] == 'cook')]
>>> print(cook['state_fips'], cook['county_fips'])
17 031

# Find Travis County (Austin)
>>> travis = counties[(counties['state_abbr'] == 'TX') & 
                      (counties['search_name'] == 'travis')]
>>> print(travis['state_fips'], travis['county_fips'])
48 453

Works for ALL 3,143 US counties!
    """)
    
    print("\n✓ County database ready for ECKO Analytics!")
    
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("\nManual download:")
    print("1. Go to: https://www2.census.gov/geo/docs/reference/codes/files/")
    print("2. Download: national_county.txt")
    print("3. Save as: data/us_counties.csv")