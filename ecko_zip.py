#!/usr/bin/env python3
"""
ECKO Analytics - ZIP Code Based Analysis
Users enter ZIP code, we determine county and analyze
Much simpler and more accurate than city names!
"""

import sys
import subprocess
from pathlib import Path
import pandas as pd
import json
import argparse

def get_county_from_zip(zip_code):
    """
    Look up county information from ZIP code
    
    Args:
        zip_code: 5-digit ZIP code
        
    Returns:
        dict with county info or None
    """
    # Load ZIP database
    zip_db_file = Path('data/us_zip_database.csv')
    
    if not zip_db_file.exists():
        print("⚠️  ZIP database not found. Downloading...")
        subprocess.run(f"{sys.executable} download_county_database.py", shell=True)
        
        if not zip_db_file.exists():
            return None
    
    zip_db = pd.read_csv(zip_db_file)
    
    # Clean ZIP
    zip_clean = str(zip_code).zfill(5)
    
    # Find ZIP
    result = zip_db[zip_db['zipcode'].astype(str) == zip_clean]
    
    if len(result) == 0:
        return None
    
    row = result.iloc[0]
    
    # Load county database to get FIPS codes
    county_db_file = Path('data/us_counties.csv')
    
    if not county_db_file.exists():
        print("⚠️  County database not found. Downloading...")
        subprocess.run(f"{sys.executable} download_county_database.py", shell=True)
        
        if not county_db_file.exists():
            return None
    
    county_db = pd.read_csv(county_db_file)
    
    # Find county FIPS
    county_result = county_db[
        (county_db['state_abbr'] == row['state_abbr']) &
        (county_db['search_name'] == row['county'].lower().replace(' county', '').strip())
    ]
    
    if len(county_result) == 0:
        return None
    
    county_row = county_result.iloc[0]
    
    return {
        'zip_code': zip_clean,
        'city': row['city'],
        'state': row['state_abbr'],
        'state_fips': str(county_row['state_fips']).zfill(2),  # Zero-pad: 6 → "06"
        'county': county_row['county_name'],
        'county_fips': str(county_row['county_fips']).zfill(3),  # Zero-pad: 37 → "037"
    }

def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n{'='*70}")
    print(f"{description}")
    print(f"{'='*70}\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed")
        return False
    
    print(f"\n✓ {description} completed successfully")
    return True

def analyze_by_zip(zip_code, force_refresh=False):
    """
    Analyze market based on ZIP code
    
    Args:
        zip_code: 5-digit ZIP code
        force_refresh: Force re-collection
    """
    
    # Lookup county from ZIP
    print(f"\n{'='*70}")
    print(f"ECKO ANALYTICS - ZIP CODE LOOKUP")
    print(f"{'='*70}")
    print(f"\nLooking up ZIP {zip_code}...")
    
    info = get_county_from_zip(zip_code)
    
    if not info:
        print(f"\n❌ Could not find ZIP code {zip_code}")
        print("Please verify the ZIP code is correct.")
        return False
    
    print(f"\n✓ Found: {info['city']}, {info['state']}")
    print(f"  County: {info['county']}")
    print(f"  State FIPS: {info['state_fips']}, County FIPS: {info['county_fips']}")
    
    # Use county slug for data storage
    county_slug = f"{info['county'].lower().replace(' ', '_')}_{info['state'].lower()}"
    data_dir = Path(f'data/{county_slug}')
    output_dir = Path(f'outputs/{county_slug}')
    
    # Check if data exists
    data_exists = (data_dir / 'zip_demographics.csv').exists()
    
    if data_exists and not force_refresh:
        print(f"\n✓ Data already exists for {info['county']}, {info['state']}")
        print(f"  Use --force to refresh")
        
        # Just run analysis on existing data
        skip_collection = True
    else:
        skip_collection = False
    
    # Create directories
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save metadata
    metadata = {
        'zip_code': info['zip_code'],
        'city': info['city'],
        'state': info['state'],
        'county': info['county'],
        'state_fips': str(info['state_fips']),
        'county_fips': str(info['county_fips']),
        'county_slug': county_slug
    }
    
    with open(data_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"ANALYZING: {info['county']}, {info['state']}")
    print(f"{'='*70}")
    
    # Step 1: Collect data (if needed)
    if not skip_collection:
        print(f"\n[Step 1/4] Collecting Census & Yelp data...")
        
        if not run_command(
            f"{sys.executable} src/data_collection.py --city '{info['city']}' --state {info['state']} --county-fips {info['county_fips']} --county-name '{info['county']}' --output-dir {data_dir}",
            f"Collecting data for {info['city']}"
        ):
            return False
        
        # Step 2: Aggregate to ZIP codes
        print(f"\n[Step 2/4] Aggregating census tracts...")
        
        if not run_command(
            f"{sys.executable} create_zip_demographics.py --data-dir {data_dir}",
            "Creating ZIP-level demographics"
        ):
            return False
    else:
        print(f"\n[Steps 1-2] Skipped (using cached data)")
    
    # Step 3: Add location names
    print(f"\n[Step 3/4] Adding location names...")
    
    if not run_command(
        f"{sys.executable} add_location_names_scalable.py --data-dir {data_dir} --output-dir {output_dir}",
        "Adding location names"
    ):
        return False
    
    # Step 4: Run analysis
    print(f"\n[Step 4/4] Calculating scores...")
    
    if not run_command(
        f"{sys.executable} src/analysis.py --data-dir {data_dir} --output-dir {output_dir}",
        "Running market analysis"
    ):
        return False
    
    print(f"\n{'='*70}")
    print(f"✓ SUCCESS - ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"\nLocation: {info['city']}, {info['state']} (ZIP {info['zip_code']})")
    print(f"Results: {output_dir}")
    print(f"\nNext steps:")
    print(f"  1. View: cat {output_dir}/analysis_insights.json")
    print(f"  2. Dashboard: streamlit run src/dashboard.py")
    
    return True

def main():
    """Main entry point"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='ECKO Analytics - Market Analysis')
    parser.add_argument('--force', action='store_true', help='Force refresh of cached data')
    parser.add_argument('--zip', type=str, help='ZIP code to analyze (skip interactive input)')
    args = parser.parse_args()
    
    print(f"\n{'='*70}")
    print(f"ECKO ANALYTICS - ZIP CODE MARKET ANALYSIS")
    print(f"{'='*70}")
    
    # Get ZIP code
    if args.zip:
        zip_input = args.zip.strip()
        print(f"\nAnalyzing ZIP: {zip_input}")
    else:
        print(f"\nEnter a ZIP code to analyze that market")
        print(f"\nExamples:")
        print(f"  90027 - Hollywood, Los Angeles")
        print(f"  60614 - Lincoln Park, Chicago")
        print(f"  10001 - Chelsea, New York")
        print(f"  30308 - Midtown, Atlanta")
        
        zip_input = input("\nZIP Code: ").strip()
    
    if not zip_input:
        print("\n❌ No ZIP code entered")
        return
    
    # Validate ZIP
    if not zip_input.isdigit() or len(zip_input) != 5:
        print(f"\n❌ Invalid ZIP code: {zip_input}")
        print("ZIP codes must be 5 digits (e.g., 90027)")
        return
    
    # Run analysis with force flag
    success = analyze_by_zip(zip_input, force_refresh=args.force)
    
    if success:
        print(f"\n{'='*70}")
        print(f"DONE!")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    main()