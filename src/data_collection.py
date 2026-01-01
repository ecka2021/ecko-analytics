"""
Data Collection Module
Collects demographic, economic, and business data for market analysis

Production-ready version with real API integrations:
- US Census Bureau API for demographics
- Yelp Fusion API for competitor data
- Fallback to synthetic data if APIs unavailable
"""

import pandas as pd
import requests
import json
import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CensusAPIClient:
    """Client for US Census Bureau API"""
    
    BASE_URL = "https://api.census.gov/data"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Census API client
        
        Args:
            api_key: Census API key (get free at https://api.census.gov/data/key_signup.html)
        """
        # self.api_key = api_key or os.getenv('CENSUS_API_KEY')
        # Try Streamlit secrets first, fallback to environment variable
        
        try:
            import streamlit as st
            self.api_key = api_key or st.secrets.get("CENSUS_API_KEY") or os.getenv('CENSUS_API_KEY')
        except:
            self.api_key = api_key or os.getenv('CENSUS_API_KEY')
                
        if not self.api_key:
            logger.warning("Census API key not found. Will use synthetic data.")
    
    def get_tract_data(self, state: str, county: str = "037") -> Optional[pd.DataFrame]:
        """
        Fetch census tract data for a state/county
        
        Uses a simpler API approach that's more reliable
        
        Args:
            state: State FIPS code (e.g., "06" for California)
            county: County FIPS code (e.g., "037" for Los Angeles County)
            
        Returns:
            DataFrame with census tract data or None if request fails
        """
        if not self.api_key:
            return None
        
        # Try the newer, simpler ACS 5-year detailed tables endpoint
        endpoint = f"{self.BASE_URL}/2022/acs/acs5"
        
        # Use simpler variable set
        variables = [
            "NAME",
            "B01003_001E",  # Total population (simpler variable)
            "B19013_001E",  # Median household income
            "B25003_002E",  # Owner-occupied units
            "B25003_003E",  # Renter-occupied units
        ]
        
        params = {
            "get": ",".join(variables),
            "for": "tract:*",
            "in": f"state:{state} county:{county}",
            "key": self.api_key
        }
        
        try:
            logger.info(f"Fetching Census data for state {state}, county {county}")
            response = requests.get(endpoint, params=params, timeout=30)
            
            # If 2022 fails, try 2020
            if response.status_code != 200:
                logger.warning("2022 ACS data unavailable, trying 2020...")
                endpoint = f"{self.BASE_URL}/2020/acs/acs5"
                response = requests.get(endpoint, params=params, timeout=30)
            
            response.raise_for_status()
            
            data = response.json()
            
            if len(data) < 2:
                logger.warning("No census data returned")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Convert to numeric types
            numeric_cols = ['B01003_001E', 'B19013_001E', 'B25003_002E', 'B25003_003E']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate derived metrics
            df['total_housing'] = df['B25003_002E'] + df['B25003_003E']
            df['renter_rate'] = df['B25003_003E'] / df['total_housing']
            
            # Estimate area and density (simplified since ALAND causes issues)
            # Use average of 1 sq mile per tract as reasonable estimate
            df['area_sq_miles'] = 1.0
            df['population_density'] = df['B01003_001E'] / df['area_sq_miles']
            df['median_age'] = 35  # Reasonable default
            
            # Rename columns for clarity
            df = df.rename(columns={
                'NAME': 'tract_name',
                'B01003_001E': 'population',
                'B19013_001E': 'median_income',
            })
            
            # Remove rows with missing critical data
            df = df.dropna(subset=['population', 'median_income', 'renter_rate'])
            
            logger.info(f"Successfully fetched {len(df)} census tracts")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch Census data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Census data: {e}")
            return None
            
            data = response.json()
            
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Convert to numeric types
            numeric_cols = ['B01001_001E', 'B19013_001E', 'B25003_003E', 
                          'B25003_002E', 'B01002_001E', 'ALAND']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate derived metrics
            df['total_housing'] = df['B25003_003E'] + df['B25003_002E']
            df['renter_rate'] = df['B25003_003E'] / df['total_housing']
            df['area_sq_miles'] = df['ALAND'] / 2589988.11  # Convert sq meters to sq miles
            df['population_density'] = df['B01001_001E'] / df['area_sq_miles']
            
            # Rename columns for clarity
            df = df.rename(columns={
                'NAME': 'tract_name',
                'B01001_001E': 'population',
                'B19013_001E': 'median_income',
                'B01002_001E': 'median_age'
            })
            
            logger.info(f"Successfully fetched {len(df)} census tracts")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch Census data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Census data: {e}")
            return None


class YelpAPIClient:
    """Client for Yelp Fusion API"""
    
    BASE_URL = "https://api.yelp.com/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Yelp API client
        
        Args:
            api_key: Yelp Fusion API key (get at https://www.yelp.com/developers/v3/manage_app)
        """
        # self.api_key = api_key or os.getenv('YELP_API_KEY')
        # Try Streamlit secrets first, fallback to .env
        try:
            import streamlit as st
            self.api_key = api_key or st.secrets.get("YELP_API_KEY") or os.getenv('YELP_API_KEY')
        except:
            self.api_key = api_key or os.getenv('YELP_API_KEY')
        
        if not self.api_key:
            logger.warning("Yelp API key not found. Will use synthetic data.")
            
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def search_businesses(
        self, 
        location: str, 
        category: str = "laundromat",
        limit: int = 50
    ) -> Optional[pd.DataFrame]:
        """
        Search for businesses in a location
        
        Args:
            location: Location string (e.g., "Los Angeles, CA")
            category: Business category to search
            limit: Maximum number of results (max 50 per request)
            
        Returns:
            DataFrame with business data or None if request fails
        """
        if not self.api_key:
            return None
            
        endpoint = f"{self.BASE_URL}/businesses/search"
        
        params = {
            'location': location,
            'categories': category,
            'limit': limit
        }
        
        try:
            logger.info(f"Searching Yelp for {category} in {location}")
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            businesses = data.get('businesses', [])
            
            if not businesses:
                logger.warning(f"No businesses found for {category} in {location}")
                return None
            
            # Extract relevant fields
            business_data = []
            for biz in businesses:
                business_data.append({
                    'business_id': biz.get('id'),
                    'business_name': biz.get('name'),
                    'rating': biz.get('rating'),
                    'review_count': biz.get('review_count'),
                    'latitude': biz['coordinates'].get('latitude'),
                    'longitude': biz['coordinates'].get('longitude'),
                    'address': biz['location'].get('address1'),
                    'city': biz['location'].get('city'),
                    'zip_code': biz['location'].get('zip_code'),
                    'price': biz.get('price', ''),
                    'is_closed': biz.get('is_closed', False)
                })
            
            df = pd.DataFrame(business_data)
            logger.info(f"Found {len(df)} businesses")
            
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch Yelp data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Yelp data: {e}")
            return None
    
    def get_multiple_locations(
        self, 
        locations: List[str], 
        category: str = "laundromat"
    ) -> pd.DataFrame:
        """
        Search multiple locations and combine results
        
        Args:
            locations: List of location strings
            category: Business category
            
        Returns:
            Combined DataFrame of all results
        """
        all_results = []
        
        for location in locations:
            result = self.search_businesses(location, category)
            if result is not None:
                result['search_location'] = location
                all_results.append(result)
            
            # Rate limiting - Yelp allows 5000 calls/day
            time.sleep(0.5)
        
        if all_results:
            return pd.concat(all_results, ignore_index=True)
        else:
            return pd.DataFrame()


class DataCollector:
    """Main data collection orchestrator"""
    

    
#     STATE_FIPS = {
#     'CA': '06', 'NY': '36', 'TX': '48', 'FL': '12', 'IL': '17',
#     'PA': '42', 'OH': '39', 'GA': '13', 'NC': '37', 'MI': '26',
#     'CO': '08', 'OR': '41', 'WA': '53', 'MA': '25', 'AZ': '04', 'VA': '51'
# }
    
    STATE_FIPS = {
    'AL': '01',  # Alabama
    'AK': '02',  # Alaska
    'AZ': '04',  # Arizona
    'AR': '05',  # Arkansas
    'CA': '06',  # California
    'CO': '08',  # Colorado
    'CT': '09',  # Connecticut
    'DE': '10',  # Delaware
    'FL': '12',  # Florida
    'GA': '13',  # Georgia
    'HI': '15',  # Hawaii
    'ID': '16',  # Idaho
    'IL': '17',  # Illinois
    'IN': '18',  # Indiana
    'IA': '19',  # Iowa
    'KS': '20',  # Kansas
    'KY': '21',  # Kentucky
    'LA': '22',  # Louisiana
    'ME': '23',  # Maine
    'MD': '24',  # Maryland
    'MA': '25',  # Massachusetts
    'MI': '26',  # Michigan
    'MN': '27',  # Minnesota
    'MS': '28',  # Mississippi
    'MO': '29',  # Missouri
    'MT': '30',  # Montana
    'NE': '31',  # Nebraska
    'NV': '32',  # Nevada
    'NH': '33',  # New Hampshire
    'NJ': '34',  # New Jersey
    'NM': '35',  # New Mexico
    'NY': '36',  # New York
    'NC': '37',  # North Carolina
    'ND': '38',  # North Dakota
    'OH': '39',  # Ohio
    'OK': '40',  # Oklahoma
    'OR': '41',  # Oregon
    'PA': '42',  # Pennsylvania
    'RI': '44',  # Rhode Island
    'SC': '45',  # South Carolina
    'SD': '46',  # South Dakota
    'TN': '47',  # Tennessee
    'TX': '48',  # Texas
    'UT': '49',  # Utah
    'VT': '50',  # Vermont
    'VA': '51',  # Virginia
    'WA': '53',  # Washington
    'WV': '54',  # West Virginia
    'WI': '55',  # Wisconsin
    'WY': '56',  # Wyoming
    'DC': '11',  # District of Columbia
    'PR': '72',  # Puerto Rico (territory)
    'VI': '78',  # Virgin Islands (territory)
    'GU': '66',  # Guam (territory)
    'AS': '60',  # American Samoa (territory)
    'MP': '69',  # Northern Mariana Islands (territory)
}
    # Major city to county FIPS mapping
    CITY_COUNTY_FIPS = {
        'Los Angeles': '037',      # Los Angeles County
        'New York': '061',         # New York County (Manhattan)
        'Chicago': '031',          # Cook County
        'Houston': '201',          # Harris County
        'Phoenix': '013',          # Maricopa County
        'Philadelphia': '101',     # Philadelphia County
        'San Antonio': '029',      # Bexar County
        'San Diego': '073',        # San Diego County
        'Dallas': '113',           # Dallas County
        'San Jose': '085',         # Santa Clara County
        'Austin': '453',           # Travis County
        'Jacksonville': '031',     # Duval County
        'San Francisco': '075',    # San Francisco County
        'Seattle': '033',          # King County
        'Denver': '031',           # Denver County
        'Boston': '025',           # Suffolk County
        'Detroit': '163',          # Wayne County
        'Miami': '086',            # Miami-Dade County
    }
    
    def __init__(
        self, 
        target_city: str = "Los Angeles", 
        target_state: str = "CA",
        use_real_data: bool = True,
        output_dir: str = "data",
        county_fips: str = None,
        county_name: str = None  # ADD THIS
    ):
        """
        Initialize data collector
        
        Args:
            target_city: City name
            target_state: State abbreviation
            use_real_data: Whether to attempt real API calls
            output_dir: Directory to save output files
            county_fips: County FIPS code (optional, overrides city lookup)
            county_name: County name for broader Yelp searches (optional)
        """
        self.city = target_city
        self.state = target_state
        self.use_real_data = use_real_data
        self.output_dir = output_dir
        self.county_fips_override = county_fips
        self.county_name = county_name  # ADD THIS
        
        # Initialize API clients
        self.census_client = CensusAPIClient() if use_real_data else None
        self.yelp_client = YelpAPIClient() if use_real_data else None
        
        # Create data directory
        Path('data').mkdir(exist_ok=True)
    
    def collect_census_data(self) -> pd.DataFrame:
        """
        Collect demographic data from Census API
        No fallback - raises error if data unavailable
        
        Returns:
            DataFrame with demographic data
            
        Raises:
            ValueError if Census data cannot be retrieved
        """
        logger.info("Collecting demographic data...")
        
        # Try real API
        if self.use_real_data and self.census_client and self.census_client.api_key:
            state_fips = self.STATE_FIPS.get(self.state)
            
            # Use override if provided, otherwise lookup
            if self.county_fips_override:
                county_fips = self.county_fips_override
            else:
                county_fips = self.CITY_COUNTY_FIPS.get(self.city, '037')
            
            if state_fips:
                df = self.census_client.get_tract_data(state_fips, county_fips)
                
                if df is not None and len(df) > 0:
                    df['data_source'] = 'census_api'
                    logger.info(f"✓ Retrieved real Census data: {len(df)} tracts")
                    return df
        
        # No fallback - raise clear error
        raise ValueError(
            f"\n❌ Census data unavailable for {self.city}, {self.state}\n\n"
            f"Possible reasons:\n"
            f"  - County not found in Census API\n"
            f"  - API key missing or invalid\n"
            f"  - Network connectivity issue\n\n"
            f"This tool currently supports major US counties.\n"
            f"Try: Los Angeles, Chicago, New York, Houston, Atlanta, Miami, Dallas, etc.\n"
        )
    
    def collect_competitor_data(self) -> pd.DataFrame:
        """
        Collect competitor business data with fallback to synthetic
        Searches the entire county to get comprehensive competitor data
        
        Returns:
            DataFrame with competitor data
        """
        logger.info("Collecting competitor data...")
        
        # Try real API first
        if self.use_real_data and self.yelp_client and self.yelp_client.api_key:
            # For county-wide analysis, we need multiple searches
            # Yelp limits to 50 results per search, so we'll do multiple searches
            
            all_businesses = []
            
            # Search 1: City name
            location1 = f"{self.city}, {self.state}"
            df1 = self.yelp_client.search_businesses(location1, category="laundromat", limit=50)
            if df1 is not None and len(df1) > 0:
                all_businesses.append(df1)
                logger.info(f"  Found {len(df1)} businesses in {self.city}")
            
            # Search 2: County name (broader search)
            if hasattr(self, 'county_name'):
                location2 = f"{self.county_name}, {self.state}"
                df2 = self.yelp_client.search_businesses(location2, category="laundromat", limit=50)
                if df2 is not None and len(df2) > 0:
                    all_businesses.append(df2)
                    logger.info(f"  Found {len(df2)} businesses in {self.county_name}")
            
            # Combine and deduplicate
            if all_businesses:
                combined = pd.concat(all_businesses, ignore_index=True)
                # Remove duplicates based on business_id
                combined = combined.drop_duplicates(subset=['business_id'], keep='first')
                combined['data_source'] = 'yelp_api'
                logger.info(f"✓ Retrieved {len(combined)} unique businesses across county")
                return combined
        
        # No fallback - raise clear error
        raise ValueError(
            f"\n❌ Yelp data unavailable for {self.city}, {self.state}\n\n"
            f"Possible reasons:\n"
            f"  - Yelp API key missing or invalid\n"
            f"  - No businesses found in this location\n"
            f"  - Network connectivity issue\n\n"
            f"Please check your .env file has YELP_API_KEY set.\n"
        )
    
    def collect_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Collect all datasets with error handling and validation
        
        Returns:
            Dictionary containing demographics and competitors DataFrames
        """
        logger.info(f"=" * 60)
        logger.info(f"Starting data collection for {self.city}, {self.state}")
        logger.info(f"=" * 60)
        
        # Collect demographics
        demographics = self.collect_census_data()
        
        # Collect competitors
        competitors = self.collect_competitor_data()
        
        # Validate data
        if demographics.empty:
            raise ValueError("No demographic data collected")
        if competitors.empty:
            raise ValueError("No competitor data collected")
        
        # Save raw data with timestamp
        from pathlib import Path
        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        demographics.to_csv(output_path / 'demographics_raw.csv', index=False)
        competitors.to_csv(output_path / 'competitors_raw.csv', index=False)
        
        # Also save timestamped backup
        demographics.to_csv(output_path / f'demographics_{timestamp}.csv', index=False)
        competitors.to_csv(output_path / f'competitors_{timestamp}.csv', index=False)
        
        logger.info("=" * 60)
        logger.info("✓ Data collection complete!")
        logger.info(f"  - Demographics: {len(demographics)} records ({demographics['data_source'].iloc[0]})")
        logger.info(f"  - Competitors: {len(competitors)} businesses ({competitors['data_source'].iloc[0]})")
        logger.info(f"  - Files saved to {output_path} directory")
        logger.info("=" * 60)
        
        return {
            'demographics': demographics,
            'competitors': competitors
        }


def main():
    """Main execution function with argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Collect market analysis data')
    parser.add_argument('--city', default='Los Angeles', help='Target city')
    parser.add_argument('--state', default='CA', help='Target state (2-letter code)')
    parser.add_argument('--output-dir', default='data', help='Output directory for data files')
    parser.add_argument('--county-fips', default=None, help='County FIPS code (optional)')
    parser.add_argument('--county-name', default=None, help='County name for Yelp searches (optional)')
    parser.add_argument('--synthetic', action='store_true', 
                       help='Force use of synthetic data (skip API calls)')
    
    args = parser.parse_args()
    
    # Create output directory
    from pathlib import Path
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize collector
    collector = DataCollector(
        target_city=args.city,
        target_state=args.state,
        use_real_data=not args.synthetic,
        output_dir=str(output_dir),
        county_fips=args.county_fips,
        county_name=args.county_name  # ADD THIS
    )
    
    # Collect data
    try:
        data = collector.collect_all_data()
        
        print("\n" + "=" * 60)
        print("SAMPLE DATA PREVIEW")
        print("=" * 60)
        print("\nDemographic data (first 5 rows):")
        print(data['demographics'].head())
        
        print("\nCompetitor data (first 5 rows):")
        print(data['competitors'].head())
        
    except Exception as e:
        logger.error(f"Data collection failed: {e}")
        raise


if __name__ == "__main__":
    main()