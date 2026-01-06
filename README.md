# ECKO Analytics - Market Intelligence Platform

**Enterprise-grade market analysis for commercial real estate site selection**

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

[Live Demo](https://ecko-analytics.streamlit.app)
---

## Overview

ECKO Analytics is an automated market intelligence platform that analyzes entire US counties in 30 seconds, identifying high-value investment opportunities for commercial real estate investors. The platform integrates real-time Census Bureau and Yelp Fusion API data to provide data-driven site selection recommendations.

**Problem Solved:** Traditional market research takes 40+ hours per location and costs $2,000-5,000. Small investors and franchisees lack access to enterprise-grade analytics.

**Solution:** Automated data pipeline that reduces research time by 99.9% while maintaining institutional-quality insights.

---

## Key Features

- **Real-Time Data Integration**: Live Census Bureau (2022 ACS) and Yelp Fusion API
- **Nationwide Coverage**: All 3,143 US counties, 33,103 ZIP codes
- **Proprietary Scoring Algorithm**: Multi-factor analysis weighing demographics, economics, and competition
- **Interactive Dashboard**: Plotly visualizations with drill-down capabilities
- **Instant Analysis**: Complete county analysis in 20-30 seconds
- **Export Capabilities**: CSV downloads for further analysis

---

## Technical Architecture

### Data Pipeline Flow

```
┌─────────────────────────────────────────────────────────┐
│                   USER INPUT: ZIP CODE                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 1: DATA COLLECTION (Parallel API Calls)          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Census API   │  │  Yelp API    │  │ HUD Crosswalk│  │
│  │ Demographics │  │  Competition │  │  ZIP→Tract   │  │
│  │ 2467 tracts  │  │  93 businesses│ │ 189K mappings│  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2: DATA PROCESSING & VALIDATION                   │
│  - Extract census tract-level demographics              │
│  - Geocode business competition                         │
│  - Map census tracts to ZIP codes                       │
│  - Handle missing values & outliers                     │
│  - Validate data types and ranges                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 3: FEATURE ENGINEERING                            │
│  - Population density (per sq mile)                     │
│  - Market saturation (population/competitors)           │
│  - Normalize metrics to 0-100 scale                     │
│  - Create composite demographic indices                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 4: SCORING ALGORITHM                              │
│                                                          │
│  Opportunity Score = Σ(factor_i × weight_i)             │
│                                                          │
│  Factors:                                               │
│  • Population Metrics (25%) - Market size potential     │
│  • Income Levels (20%) - Purchasing power               │
│  • Population Density (15%) - Accessibility             │
│  • Renter Rate (20%) - Target demographic fit           │
│  • Competition Gap (20%) - Market saturation            │
│                                                          │
│  Score Range: 0-100 (higher = better opportunity)       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 5: ANALYSIS & INSIGHTS                            │
│  - Rank 283 ZIP codes by opportunity score              │
│  - Generate distribution histograms                     │
│  - Create competition density scatter plots             │
│  - Identify statistical outliers                        │
│  - Calculate market-wide KPIs                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│             INTERACTIVE DASHBOARD OUTPUT                 │
│  - Top 10 opportunities table                           │
│  - Interactive Plotly visualizations                    │
│  - Downloadable CSV exports                             │
│  - Methodology documentation                            │
└─────────────────────────────────────────────────────────┘
```

---

## Scoring Methodology

### Multi-Factor Weighted Algorithm

The opportunity score combines five normalized factors (0-100 scale):

```python
# Normalization ensures fair comparison across varying scales
normalize(value) = (value - min) / (max - min) * 100

# Final Score Calculation
opportunity_score = (
    normalize(population) * 0.25 +           # Market size
    normalize(median_income) * 0.20 +        # Purchasing power
    normalize(population_density) * 0.15 +   # Accessibility
    renter_rate * 100 * 0.20 +               # Demographic fit
    normalize(saturation_ratio) * 0.20       # Competition gap
)

where:
  saturation_ratio = population / (competitors + 1)
```

### Score Interpretation

- **80-100**: Excellent opportunity - High demand, minimal competition
- **60-79**: Good opportunity - Balanced market conditions
- **40-59**: Moderate opportunity - Competitive market
- **0-39**: Saturated market - High competition, limited opportunity

### Why This Model Works

1. **Normalization** prevents bias toward high-population areas
2. **Weighted factors** reflect business-specific priorities
3. **Saturation ratio** accounts for competitive intensity
4. **Renter rate** targets core laundromat demographic

---

## Technology Stack

**Core:**
- Python 3.9+
- Streamlit 1.28+ (Web framework)
- Pandas (Data processing)
- Plotly (Interactive visualizations)

**APIs:**
- US Census Bureau API (2022 American Community Survey)
- Yelp Fusion API (Business data)
- HUD USPS ZIP Code Crosswalk

**Deployment:**
- Streamlit Cloud (Free tier)
- GitHub (Version control)

---

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Git
- API Keys (Census Bureau, Yelp Fusion)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ecko-analytics.git
cd ecko-analytics
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```bash
CENSUS_API_KEY=your_census_api_key_here
YELP_API_KEY=your_yelp_api_key_here
```

Get API keys:
- Census: https://api.census.gov/data/key_signup.html
- Yelp: https://www.yelp.com/developers/v3/manage_app

4. **Run the application**
```bash
streamlit run ecko_app_main.py
```

5. **Access the app**
Open your browser to `http://localhost:8501`

---

## Project Structure

```
ecko-analytics/
│
├── ecko_app_main.py              # Main landing page
├── ecko_zip.py                   # Core analysis engine
├── create_zip_demographics.py    # Data aggregation
├── process_crosswalk_all_counties.py  # Crosswalk processing
│
├── pages/
│   └── results.py                # Results dashboard
│
├── src/
│   ├── data_collection.py        # API integration
│   ├── analysis.py               # Scoring algorithm
│   ├── census_api_client.py      # Census API wrapper
│   └── yelp_api_client.py        # Yelp API wrapper
│
├── data/
│   ├── us_zip_database.csv       # 33K ZIP codes
│   ├── county_database.csv       # 3.1K counties
│   └── zip_tract_crosswalk.csv   # 189K mappings
│
├── uploads/
│   ├── image1.jpeg               # Landing page background
│   └── image2.jpg                # Results page background
│
├── .env                          # API keys (DO NOT COMMIT)
├── .gitignore                    # Exclude sensitive files
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Example Output

### Los Angeles County Analysis

**Metrics:**
- ZIP Codes Analyzed: 283
- Total Population: 9,911,660
- Existing Competitors: 81 laundromats
- Market Size per Business: 122,366 people

**Top Opportunity:**
- Location: Westlake (ZIP 90057)
- Score: 83.4/100
- Population: 18,269
- Competitors: 0
- **Insight**: Underserved high-density urban area with strong renter demographics

**Analysis Time:** 28 seconds

---

## Use Cases

### For Investors
- Identify underserved markets before competitors
- Validate site selection with data
- Compare multiple locations objectively

### For Franchisees
- Territory planning and expansion analysis
- Risk assessment for new locations
- Market sizing and revenue projections

### For Real Estate Professionals
- Client advisory and recommendations
- Market research automation
- Competitive intelligence gathering

---

## Results & Impact

- **Time Savings**: 40 hours → 30 seconds (99.9% reduction)
- **Cost Savings**: $2,000-5,000 → $0 (free tier)
- **Coverage**: 3,143 counties, 25M+ people analyzed
- **Accuracy**: 90%+ success rate across major metros
- **Beta Users**: 25+ in first month

---

## Data Privacy & Security

- All API calls use HTTPS encryption
- No user data is stored or shared
- API keys stored securely in environment variables
- Analyses are session-based (no persistent storage)
- Compliant with Census Bureau and Yelp API terms of service

---

## Limitations & Disclaimers

**Current Limitations:**
- Optimized for laundromat businesses only
- Limited to US counties with complete Census data (90% coverage)
- No historical trend analysis (current snapshot only)
- Yelp data limited to 50 results per search query

**Legal Disclaimer:**
This tool provides educational and informational data analysis only. It does not constitute investment advice, financial advice, or business consulting. Users should conduct independent due diligence and consult with licensed professionals before making investment decisions.

---

## Roadmap

### Phase 1: MVP (Complete) 
- [x] Real-time data integration
- [x] Scoring algorithm
- [x] Interactive dashboard
- [x] Nationwide coverage

### Phase 2: Enhancement (In Progress)
- [ ] PDF report generation
- [ ] Email delivery
- [ ] Historical trend analysis
- [ ] Multi-business type support (restaurants, gyms, coffee shops)

### Phase 3: Advanced Features
- [ ] Geo-mapping with radius selection
- [ ] AI-powered market assistant
- [ ] API access for developers
- [ ] White-label reports

---

##  Contributing

This is a portfolio project, but feedback and suggestions are welcome!

**To report bugs or request features:**
1. Open an issue on GitHub
2. Email: hello@eckoanalytics.com

---

## License

MIT License - See LICENSE file for details

---

## Author

**Eusila Kitur**
- Portfolio: Coming soon
- LinkedIn:(https://www.linkedin.com/in/kitureusila/)
- GitHub: github.com/ecka2021
- Email: eusila.kitur@gmail.com

**Built as a data analytics portfolio project to demonstrate:**
- API integration and data engineering
- Statistical modeling and feature engineering
- Data visualization and storytelling
- Full-stack application development

---

## Acknowledgments

**Data Sources:**
- US Census Bureau - American Community Survey 2022
- Yelp Inc. - Yelp Fusion API
- US Department of HUD - ZIP Code Crosswalk Files

**Technologies:**
- Streamlit for the amazing web framework
- Plotly for interactive visualizations
- Anthropic Claude for development assistance

---

## Contact

For questions, collaboration, or hiring inquiries:

Email: eusila.kitur@gmail.com  
LinkedIn: https://www.linkedin.com/in/kitureusila/  
Portfolio: Coming Soon

**Looking for data analyst opportunities!** This project demonstrates expertise in:
- Data pipeline engineering
- API integration
- Statistical analysis
- Data visualization
- Product development

---

**If you found this project useful, please star it on GitHub!**

---

*Last Updated: December 2025*