# API Setup Guide - Production Data Collection

This guide explains how to set up real API access for production-quality data.

## Overview

The project supports **two modes**:

1. **Synthetic Mode** (Default): Uses realistic synthetic data - perfect for learning and demos
2. **Production Mode**: Uses real APIs for actual market data

## Quick Start (Synthetic Data)

No setup needed! Just run:
```bash
python src/data_collection.py --synthetic
```

## Production Setup (Real APIs)

### Step 1: Get API Keys

#### US Census Bureau API (FREE)
**Why**: Official demographic data (population, income, housing)

1. Visit: https://api.census.gov/data/key_signup.html
2. Fill out the form (takes 2 minutes)
3. Check your email for the API key
4. **Cost**: Free, no credit card needed
5. **Rate Limit**: 500 requests/day (plenty for this project)

#### Yelp Fusion API (FREE)
**Why**: Business location and review data

1. Visit: https://www.yelp.com/developers/v3/manage_app
2. Create a Yelp account (if needed)
3. Click "Create New App"
4. Fill in app details (use any name)
5. Copy your API Key
6. **Cost**: Free tier (5000 API calls/day)
7. **Rate Limit**: 5000 calls/day

### Step 2: Configure Environment

1. **Copy the template**:
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` file**:
   ```bash
   # Open in your text editor
   nano .env  # or use any editor
   ```

3. **Add your API keys**:
   ```env
   CENSUS_API_KEY=your_actual_census_key_here
   YELP_API_KEY=your_actual_yelp_key_here
   ```

4. **Save the file**

### Step 3: Run with Real Data

```bash
# Will automatically use real APIs if keys are configured
python src/data_collection.py

# Specify different city
python src/data_collection.py --city "Chicago" --state "IL"

# Force synthetic (ignore API keys)
python src/data_collection.py --synthetic
```

## API Details

### Census API

**What you get**:
- Total population per census tract
- Median household income
- Owner vs renter occupied housing
- Median age
- Land area (for density calculations)

**Data Coverage**: All 50 US states, down to census tract level

**Example Request**:
```python
# The code handles this automatically
GET https://api.census.gov/data/2021/acs/acs5
  ?get=B01001_001E,B19013_001E
  &for=tract:*
  &in=state:06
  &key=YOUR_KEY
```

**Census Variables Used**:
- `B01001_001E`: Total population
- `B19013_001E`: Median household income
- `B25003_003E`: Renter-occupied housing units
- `B25003_002E`: Owner-occupied housing units
- `B01002_001E`: Median age
- `ALAND`: Land area in square meters

**Documentation**: https://www.census.gov/data/developers/data-sets/acs-5year.html

### Yelp API

**What you get**:
- Business names and locations
- Ratings and review counts
- Addresses and coordinates
- Price levels
- Open/closed status

**Data Coverage**: Major cities worldwide (best in US)

**Example Request**:
```python
# The code handles this automatically  
GET https://api.yelp.com/v3/businesses/search
  ?location=Los Angeles, CA
  &categories=laundromat
  &limit=50
  Authorization: Bearer YOUR_KEY
```

**Documentation**: https://docs.developer.yelp.com/reference/v3_business_search

## Troubleshooting

### "Census API key not found"
- Check that `.env` file exists in project root
- Verify `CENSUS_API_KEY=...` has no spaces around `=`
- Make sure you're running from project directory

### "Yelp API authentication failed"
- Verify your API key is correct
- Check that you activated the key on Yelp's developer portal
- Ensure no extra spaces in `.env` file

### "No data returned"
- For Census: Verify state code is correct (e.g., "CA" not "California")
- For Yelp: Try a major city first (Los Angeles, New York)
- Check API rate limits haven't been exceeded

### Still using synthetic data
```bash
# Verify environment variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('CENSUS_API_KEY'))"
```

If this prints `None`, your `.env` file isn't being read.

## Data Quality Comparison

### Synthetic Data (Default)
✓ Perfect for learning and demos  
✓ No setup required  
✓ Consistent results  
✓ Fast (no API calls)  
✗ Not actual market data  
✗ Limited to predefined neighborhoods  

### Real API Data (Production)
✓ Actual census and business data  
✓ Complete geographic coverage  
✓ Up-to-date information  
✓ Can analyze any US city  
✓ More impressive in portfolios/interviews  
✗ Requires API setup (15 minutes)  
✗ Rate limits apply  

## Best Practices

### For Learning/Development
- Use synthetic data initially
- Get comfortable with the analysis workflow
- Switch to real data for final portfolio version

### For Production/Portfolio
1. Get both API keys (takes 15 minutes total)
2. Run with real data for your target cities
3. Save the results (they're cached in `data/` folder)
4. Mention in README: "Uses Census Bureau and Yelp APIs"

### Rate Limiting
The code automatically:
- Adds delays between requests
- Saves data locally (no repeated calls needed)
- Creates timestamped backups

You won't hit rate limits with normal use.

## Advanced: Other Data Sources

Want even more data? The code is extensible:

### Google Places API
- Alternative to Yelp
- Better global coverage
- Paid (but has free tier)
- Setup: https://developers.google.com/maps/documentation/places

### OpenStreetMap
- Free, no API key needed
- Global coverage
- Less business detail than Yelp
- Library: `osmnx`, `overpy`

### County Business Licenses
- Public records (often free)
- Most authoritative source
- Varies by county
- Usually requires web scraping

## For Interviews

When discussing this project:

**If using synthetic data**:
> "I built this using synthetic data modeled on census patterns, but the architecture is production-ready with support for Census Bureau and Yelp APIs."

**If using real APIs**:
> "The project integrates with the Census Bureau API for demographics and Yelp's API for competitor data, with fallback to synthetic data for development."

**Either way, emphasize**:
- Proper error handling
- Environment variable management
- API rate limiting
- Data validation
- Logging and monitoring

## Next Steps

1. Set up API keys (15 min)
2. Run with real data once
3. Compare results to synthetic
4. Update your README to mention API integration
5. Keep both modes working (shows flexibility)

Remember: **Having API integration (even if you demo with synthetic data) shows production-ready thinking.**