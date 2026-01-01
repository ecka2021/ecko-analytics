"""
ECKO Analytics - Professional Market Intelligence Platform
Data-Driven Site Selection for Commercial Real Estate
"""

import streamlit as st
import pandas as pd
import subprocess
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import time

# Page config
st.set_page_config(
    page_title="ECKO Analytics - Market Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -5%;
        width: 400px;
        height: 400px;
        background: rgba(255,255,255,0.08);
        border-radius: 50%;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.95;
        margin-bottom: 2rem;
    }
    
    .hero-stats {
        display: flex;
        gap: 3rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    /* Info boxes */
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #0ea5e9;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-title">ECKO Analytics</div>
        <div class="hero-subtitle">Enterprise-Grade Market Intelligence for Commercial Real Estate</div>
        <p style="font-size: 1.1rem; opacity: 0.9; max-width: 800px;">
            Leverage real-time Census and business data to identify high-value investment opportunities 
            across 3,143 US counties. Make data-driven decisions in under 30 seconds.
        </p>
        <div class="hero-stats">
            <div class="stat-item">
                <span class="stat-number">3,143</span>
                <span class="stat-label">Counties Covered</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">25M+</span>
                <span class="stat-label">Population Analyzed</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">30s</span>
                <span class="stat-label">Analysis Time</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">90%+</span>
                <span class="stat-label">Coverage Rate</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Trust indicators
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #3b82f6; margin-bottom: 0.5rem;">📊</div>
        <div style="font-weight: 600; color: #1e293b;">Real-Time Data</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">Live API integration</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #3b82f6; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-weight: 600; color: #1e293b;">Nationwide Coverage</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">All 50 states</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #3b82f6; margin-bottom: 0.5rem;">⚡</div>
        <div style="font-weight: 600; color: #1e293b;">Instant Analysis</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">Results in 30 seconds</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 2rem; color: #3b82f6; margin-bottom: 0.5rem;">🔒</div>
        <div style="font-weight: 600; color: #1e293b;">Data Security</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">Private & secure</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Analysis Section
st.markdown('<div class="section-header">Market Analysis Tool</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    zip_code = st.text_input(
        "ZIP Code",
        placeholder="Enter 5-digit ZIP code (e.g., 90027, 60614, 10001)",
        label_visibility="collapsed",
        help="Enter any US ZIP code to analyze the entire county market",
        key="zip_input"
    )

with col2:
    analyze_button = st.button("Run Analysis", type="primary", use_container_width=True)

# Example ZIPs in clean layout
st.markdown("**Quick Start Examples:**")
example_col1, example_col2, example_col3, example_col4, example_col5 = st.columns(5)

clicked_example = None
with example_col1:
    if st.button("Los Angeles", use_container_width=True, key="ex1"):
        clicked_example = "90027"

with example_col2:
    if st.button("Chicago", use_container_width=True, key="ex2"):
        clicked_example = "60614"

with example_col3:
    if st.button("New York", use_container_width=True, key="ex3"):
        clicked_example = "10001"

with example_col4:
    if st.button("Houston", use_container_width=True, key="ex4"):
        clicked_example = "77002"

with example_col5:
    if st.button("Atlanta", use_container_width=True, key="ex5"):
        clicked_example = "30308"

if clicked_example:
    zip_code = clicked_example
    analyze_button = True

st.markdown("<br><br>", unsafe_allow_html=True)

# Run analysis
if analyze_button and zip_code:
    
    st.markdown(f'<div class="section-header">Analysis in Progress: ZIP {zip_code}</div>', unsafe_allow_html=True)
    
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    status_text.markdown('<div class="info-box"><b>Step 1 of 3:</b> Validating location and retrieving county information</div>', unsafe_allow_html=True)
    progress_bar.progress(10)
    
    try:
        status_text.markdown('<div class="info-box"><b>Step 2 of 3:</b> Collecting demographic data from US Census Bureau (2022 ACS)</div>', unsafe_allow_html=True)
        progress_bar.progress(30)
        
        result = subprocess.run(
            ['python3', 'ecko_zip.py', '--zip', zip_code, '--force'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        progress_bar.progress(60)
        status_text.markdown('<div class="info-box"><b>Step 3 of 3:</b> Mapping competition via Yelp Fusion API and calculating opportunity scores</div>', unsafe_allow_html=True)
        
        time.sleep(0.5)
        progress_bar.progress(100)
        
        if "✓ SUCCESS - ANALYSIS COMPLETE" in result.stdout or "DONE!" in result.stdout:
            
            status_text.empty()
            progress_bar.empty()
            
            # Extract county info
            county_name = "Unknown County"
            state = "Unknown State"
            county_slug = None
            
            output_lines = result.stdout.split('\n')
            
            for line in output_lines:
                if "ANALYZING:" in line:
                    parts = line.split('ANALYZING:')[1].strip().split(',')
                    if len(parts) >= 2:
                        county_name = parts[0].strip()
                        state = parts[1].strip()
                        county_slug = county_name.lower().replace(' county', '').replace(' ', '_') + '_county_' + state.lower().replace(' ', '_')
                    break
            
            if county_slug:
                county_dir = Path(f'outputs/{county_slug}')
                
                if county_dir.exists():
                    st.markdown(f'<div class="success-box"><b>Analysis Complete:</b> {county_name}, {state}</div>', unsafe_allow_html=True)
                    
                    # Load data
                    insights_file = county_dir / 'analysis_insights.json'
                    scores_file = county_dir / 'zip_scores.csv'
                    scores_with_names_file = county_dir / 'zip_scores_with_names.csv'
                    
                    if insights_file.exists() and scores_file.exists():
                        
                        with open(insights_file) as f:
                            insights = json.load(f)
                        
                        scores_df = pd.read_csv(scores_file)
                        
                        if scores_with_names_file.exists():
                            names_df = pd.read_csv(scores_with_names_file)[['zip_code', 'location_name']]
                            scores_df = scores_df.merge(names_df, on='zip_code', how='left')
                        else:
                            scores_df['location_name'] = 'ZIP ' + scores_df['zip_code'].astype(str)
                        
                        total_population = int(scores_df['population'].sum())
                        total_competitors = int(scores_df['competitor_count'].sum())
                        
                        # RESULTS
                        st.markdown(f'<div class="section-header">Market Overview: {county_name}, {state}</div>', unsafe_allow_html=True)
                        
                        # KPIs
                        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                        
                        with kpi1:
                            st.metric("ZIP Codes Analyzed", f"{insights['total_zips']:,}")
                        
                        with kpi2:
                            st.metric("Total Population", f"{total_population:,}")
                        
                        with kpi3:
                            st.metric("Existing Competitors", f"{total_competitors:,}")
                        
                        with kpi4:
                            avg_per = int(total_population / total_competitors) if total_competitors > 0 else total_population
                            st.metric("Market Size per Business", f"{avg_per:,}")
                        
                        # Top Opportunities
                        st.markdown('<div class="section-header">Investment Opportunities</div>', unsafe_allow_html=True)
                        
                        top10 = scores_df.nlargest(10, 'total_score')[[
                            'location_name', 'zip_code', 'population', 
                            'competitor_count', 'total_score'
                        ]].copy()
                        
                        top10['total_score'] = top10['total_score'].round(1)
                        top10.columns = ['Location', 'ZIP Code', 'Population', 'Competitors', 'Opportunity Score']
                        
                        # Highlight top opportunity
                        st.markdown(f"""
                        <div class="success-box">
                            <b>Highest Opportunity:</b> {top10.iloc[0]['Location']} 
                            <span style="float: right; font-weight: 700; color: #059669;">Score: {top10.iloc[0]['Opportunity Score']}/100</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.dataframe(
                            top10,
                            hide_index=True,
                            use_container_width=True,
                            column_config={
                                "Opportunity Score": st.column_config.ProgressColumn(
                                    "Opportunity Score",
                                    format="%.1f",
                                    min_value=0,
                                    max_value=100,
                                ),
                            }
                        )
                        
                        # Visualizations
                        st.markdown('<div class="section-header">Market Intelligence Visualizations</div>', unsafe_allow_html=True)
                        
                        viz_col1, viz_col2 = st.columns(2)
                        
                        with viz_col1:
                            fig1 = px.histogram(
                                scores_df,
                                x='total_score',
                                nbins=25,
                                title='Opportunity Score Distribution',
                                labels={'total_score': 'Opportunity Score', 'count': 'Number of ZIP Codes'},
                                color_discrete_sequence=['#3b82f6']
                            )
                            fig1.update_layout(
                                showlegend=False,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="Inter, sans-serif")
                            )
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        with viz_col2:
                            top50 = scores_df.nlargest(50, 'population')
                            fig2 = px.scatter(
                                top50,
                                x='population',
                                y='competitor_count',
                                size='total_score',
                                hover_data=['location_name'],
                                title='Competition Density Analysis',
                                labels={'population': 'Population', 'competitor_count': 'Number of Competitors'},
                                color='total_score',
                                color_continuous_scale='Blues'
                            )
                            fig2.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="Inter, sans-serif")
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Export Options
                        st.markdown('<div class="section-header">Export & Reports</div>', unsafe_allow_html=True)
                        
                        dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)
                        
                        with dl_col1:
                            csv = scores_df.to_csv(index=False)
                            st.download_button(
                                "Download Full Dataset (CSV)",
                                csv,
                                f"ecko_analysis_{county_dir.name}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                        
                        with dl_col2:
                            top_csv = top10.to_csv(index=False)
                            st.download_button(
                                "Download Top 10 (CSV)",
                                top_csv,
                                f"ecko_top10_{county_dir.name}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                        
                        with dl_col3:
                            if st.button("Generate PDF Report", use_container_width=True, key="pdf"):
                                st.info("**Pro Feature** - Professional PDF reports available on paid plans. Contact: hello@eckoanalytics.com")
                        
                        with dl_col4:
                            if st.button("Email Report", use_container_width=True, key="email"):
                                st.info("**Pro Feature** - Email delivery available on paid plans. Contact: hello@eckoanalytics.com")
                        
                        # Methodology
                        with st.expander("Methodology & Score Interpretation"):
                            st.markdown("""
                            ### Opportunity Score Components
                            
                            Our proprietary algorithm evaluates four key factors:
                            
                            1. **Population Metrics** (40% weight)
                               - Total population size
                               - Population density
                               - Growth indicators
                            
                            2. **Economic Indicators** (30% weight)
                               - Median household income
                               - Income distribution
                               - Purchasing power
                            
                            3. **Demographic Fit** (20% weight)
                               - Renter rate (critical for laundromat demand)
                               - Age distribution
                               - Household composition
                            
                            4. **Competitive Landscape** (10% weight)
                               - Number of existing competitors
                               - Market saturation ratio
                               - Service gaps
                            
                            ### Score Interpretation
                            
                            - **80-100:** High opportunity - Strong demand with minimal competition
                            - **60-79:** Moderate opportunity - Balanced market conditions
                            - **40-59:** Competitive market - Requires differentiation strategy
                            - **0-39:** Saturated market - High competition, limited opportunity
                            
                            ### Recommended Due Diligence
                            
                            1. Visit top-ranked locations in person
                            2. Assess local commercial real estate availability
                            3. Verify foot traffic patterns and accessibility
                            4. Consult with local real estate professionals
                            5. Review zoning regulations and permit requirements
                            6. Conduct independent market research
                            """)
                    
                    else:
                        st.error("Analysis files not found. Please try again.")
        
        else:
            status_text.empty()
            progress_bar.empty()
            st.markdown('<div class="warning-box"><b>Analysis Unavailable:</b> This county may not currently be supported.</div>', unsafe_allow_html=True)
            
            st.markdown("""
            **Supported Markets:** Major US counties with complete Census coverage
            
            **Try These Locations:**
            - Los Angeles, CA (90027)
            - Chicago, IL (60614)
            - New York, NY (10001)
            - Houston, TX (77002)
            - Atlanta, GA (30308)
            - Austin, TX (78701)
            """)
                    
    except subprocess.TimeoutExpired:
        status_text.empty()
        progress_bar.empty()
        st.error("Analysis timeout. Please try again.")
    except Exception as e:
        status_text.empty()
        progress_bar.empty()
        st.error(f"System error: {str(e)}")

elif zip_code and not analyze_button:
    st.info("Click 'Run Analysis' to begin")

# Footer sections
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Platform Information</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Data Sources", "Pricing", "FAQ", "Legal"])

with tab1:
    st.markdown("""
    ### Official Data Sources
    
    **US Census Bureau**
    - 2022 American Community Survey (ACS)
    - Official demographic and economic data
    - Variables: Population, income, housing, age distribution
    - Update frequency: Annual
    
    **Yelp Fusion API**
    - Real-time business listings
    - Location-verified competition data
    - Ratings and review metadata
    - Update frequency: Real-time
    
    **HUD USPS Crosswalk Files**
    - ZIP Code to Census Tract mappings
    - 189,375 nationwide mappings
    - Ensures geographic precision
    - Update frequency: Quarterly
    
    ### Data Quality Standards
    
    - All data is sourced from authoritative government and verified commercial APIs
    - No synthetic or modeled data is used
    - Data is processed and analyzed in real-time
    - Geographic boundaries are verified against official sources
    """)

with tab2:
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown("""
        #### Free Tier
        **$0/month**
        
        - Unlimited county analyses
        - Real-time data access
        - Top 10 opportunities
        - CSV exports
        - Interactive visualizations
        
        *Current offering*
        """)
    
    with col_b:
        st.markdown("""
        #### Professional
        **$49/month**
        
        - All Free features
        - PDF report generation
        - Complete ZIP rankings
        - Email delivery
        - Priority support
        - Historical data (3 months)
        
        *Coming Q1 2026*
        """)
    
    with col_c:
        st.markdown("""
        #### Enterprise
        **Custom pricing**
        
        - All Pro features
        - API access
        - White-label reports
        - Multi-business types
        - Dedicated support
        - Custom integrations
        
        *Contact for details*
        """)

with tab3:
    st.markdown("""
    ### Frequently Asked Questions
    
    **Is the data accurate and current?**
    
    Yes. We use official US Census Bureau data (2022 ACS) and real-time Yelp business data. However, all data should be independently verified before making investment decisions.
    
    **How is the opportunity score calculated?**
    
    Our proprietary algorithm weighs population metrics (40%), economic indicators (30%), demographic fit (20%), and competitive landscape (10%). Higher scores indicate better market potential based on data analysis.
    
    **Can I analyze multiple counties?**
    
    Yes. There are no limits on the number of analyses you can run on the free tier.
    
    **What geographic areas are covered?**
    
    We support 3,143 US counties across all 50 states, with a 90%+ success rate for major metropolitan areas.
    
    **Do you provide investment advice?**
    
    No. We provide data analysis and market intelligence only. Users should consult with licensed professionals before making investment decisions.
    
    **Can I use this for other business types?**
    
    Currently optimized for laundromat site selection. Support for additional business types (restaurants, gyms, coffee shops) is planned for 2026.
    
    **How long does analysis take?**
    
    Most analyses complete in 20-30 seconds, depending on county size and data availability.
    
    **Is my data private?**
    
    Yes. We do not share, sell, or monetize user data. All analyses are private to your account.
    """)

with tab4:
    st.markdown("""
    ### Legal Disclaimer
    
    **Educational and Informational Use Only**
    
    This platform provides data analysis and market intelligence for educational and informational purposes only. 
    ECKO Analytics does not provide investment advice, financial advice, legal advice, or business consulting services.
    
    **User Responsibilities**
    
    Users must:
    - Conduct independent due diligence
    - Consult with qualified licensed professionals (attorneys, CPAs, real estate brokers, business advisors)
    - Verify all data with local sources
    - Consider local regulations, zoning laws, and market-specific factors
    - Make investment decisions based on professional guidance
    
    **Limitations of Liability**
    
    ECKO Analytics is not responsible for:
    - Investment outcomes or financial losses
    - The accuracy or completeness of third-party data
    - Changes in market conditions
    - Local factors not captured in demographic data
    - Business success or failure
    
    **No Warranty**
    
    This service is provided "as is" without warranty of any kind, express or implied, including but not limited to 
    warranties of merchantability, fitness for a particular purpose, or non-infringement.
    
    **Data Attribution**
    
    - US Census Bureau (2022 American Community Survey)
    - Yelp Inc. (Yelp Fusion API)
    - US Department of Housing and Urban Development (HUD Crosswalk Files)
    
    By using this platform, you acknowledge that you have read, understood, and agree to these terms.
    
    **Contact:** hello@eckoanalytics.com
    """)

# Clean footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 2rem 0; border-top: 1px solid #e2e8f0;'>
    <p style='font-weight: 600; color: #64748b;'>ECKO Analytics</p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
        Market Intelligence Platform | Not Investment Advice | Educational Use Only
    </p>
    <p style='font-size: 0.75rem; margin-top: 0.5rem;'>
        © 2025 ECKO Analytics | Powered by Census Bureau & Yelp Data
    </p>
</div>
""", unsafe_allow_html=True)