"""
ECKO Analytics - Results Dashboard
Market Analysis Results
"""

import streamlit as st
import pandas as pd
import subprocess
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import time
import base64

# Page config
st.set_page_config(
    page_title="Analysis Results - ECKO Analytics",
    page_icon="📊",
    layout="wide"
)

# Function to load background image
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load results background
bg_image = get_base64_image("uploads/image2.jpg")

# Professional CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), 
                          url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Header */
    .results-header {{
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(59, 130, 246, 0.2) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .header-title {{
        font-size: 2rem;
        font-weight: 800;
        color: white;
    }}
    
    .header-subtitle {{
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.25rem;
    }}
    
    /* Section headers */
    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(59, 130, 246, 0.3);
    }}
    
    /* KPI cards */
    .kpi-card {{
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.5);
    }}
    
    /* Info boxes */
    .info-box {{
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        color: #cbd5e1;
        margin: 1rem 0;
    }}
    
    .success-box {{
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 8px;
        color: #d1fae5;
        margin: 1rem 0;
    }}
    
    /* AI Assistant placeholder */
    .ai-assistant {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 2px dashed rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
    }}
    
    .ai-icon {{
        font-size: 4rem;
        color: #a78bfa;
        margin-bottom: 1rem;
    }}
    
    .ai-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #e9d5ff;
        margin-bottom: 0.5rem;
    }}
    
    .ai-desc {{
        color: #c4b5fd;
        font-size: 1rem;
        max-width: 600px;
        margin: 0 auto;
    }}
    
    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
    }}
    
    /* Hide Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Dataframe styling */
    .dataframe {{
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
    }}
</style>
""", unsafe_allow_html=True)

# Check if we have a ZIP to analyze
if 'analysis_zip' not in st.session_state or not st.session_state.get('run_analysis'):
    st.warning("No ZIP code selected. Redirecting to home...")
    time.sleep(2)
    st.switch_page("ecko_app_main.py")
    st.stop()

zip_code = st.session_state['analysis_zip']

# Header with back button
col_back, col_title = st.columns([1, 5])

with col_back:
    if st.button("← Back", key="back_btn"):
        st.session_state['run_analysis'] = False
        st.switch_page("ecko_app_main.py")

with col_title:
    st.markdown(f"""
    <div class="header-title">Market Analysis: ZIP {zip_code}</div>
    <div class="header-subtitle">Powered by US Census Bureau & Yelp Fusion API</div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Run analysis
status_container = st.container()

with status_container:
    st.markdown('<div class="section-title">Analysis in Progress</div>', unsafe_allow_html=True)
    
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    status_text.markdown('<div class="info-box"><b>Step 1:</b> Validating location and retrieving county information</div>', unsafe_allow_html=True)
    progress_bar.progress(10)
    
    try:
        status_text.markdown('<div class="info-box"><b>Step 2:</b> Collecting demographic data from US Census Bureau</div>', unsafe_allow_html=True)
        progress_bar.progress(30)
        
        
            # Increase timeout to 300 seconds (5 minutes) for Streamlit Cloud
        result = subprocess.run(
            ['python3', 'ecko_zip.py', '--zip', zip_code, '--force'],
            capture_output=True,
            text=True,
            timeout=300  # Increased from 120
        )

        # DEBUG: Show what happened
        st.write(f"DEBUG: Return code: {result.returncode}")
        st.write(f"DEBUG: Output length: {len(result.stdout)}")
        if result.stderr:
            st.error(f"DEBUG: Errors: {result.stderr[:500]}")
        
        # result = subprocess.run(
        #     ['python3', 'ecko_zip.py', '--zip', zip_code, '--force'],
        #     capture_output=True,
        #     text=True,
        #     timeout=120
        # )
        
        progress_bar.progress(70)
        status_text.markdown('<div class="info-box"><b>Step 3:</b> Mapping competition and calculating opportunity scores</div>', unsafe_allow_html=True)
        
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
                    st.markdown(f'<div class="success-box"><i class="fas fa-check-circle"></i> <b>Analysis Complete:</b> {county_name}, {state}</div>', unsafe_allow_html=True)
                    
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
                        
                        # KPIs
                        st.markdown('<div class="section-title">Market Overview</div>', unsafe_allow_html=True)
                        
                        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                        
                        with kpi1:
                            st.metric("ZIP Codes", f"{insights['total_zips']:,}")
                        with kpi2:
                            st.metric("Total Population", f"{total_population:,}")
                        with kpi3:
                            st.metric("Competitors", f"{total_competitors:,}")
                        with kpi4:
                            avg_per = int(total_population / total_competitors) if total_competitors > 0 else total_population
                            st.metric("Market Size / Business", f"{avg_per:,}")
                        
                        # Top Opportunities
                        st.markdown('<div class="section-title">Top Investment Opportunities</div>', unsafe_allow_html=True)
                        
                        top10 = scores_df.nlargest(10, 'total_score')[[
                            'location_name', 'zip_code', 'population', 
                            'competitor_count', 'total_score'
                        ]].copy()
                        
                        top10['total_score'] = top10['total_score'].round(1)
                        top10.columns = ['Location', 'ZIP', 'Population', 'Competitors', 'Score']
                        
                        st.markdown(f"""
                        <div class="success-box">
                            <i class="fas fa-trophy"></i> <b>Highest Opportunity:</b> {top10.iloc[0]['Location']} 
                            <span style="float: right; font-weight: 700;">Score: {top10.iloc[0]['Score']}/100</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.dataframe(
                            top10,
                            hide_index=True,
                            use_container_width=True,
                            column_config={
                                "Score": st.column_config.ProgressColumn(
                                    "Opportunity Score",
                                    format="%.1f",
                                    min_value=0,
                                    max_value=100,
                                ),
                            }
                        )
                        
                        # Charts
                        st.markdown('<div class="section-title">Market Intelligence</div>', unsafe_allow_html=True)
                        
                        viz_col1, viz_col2 = st.columns(2)
                        
                        with viz_col1:
                            fig1 = px.histogram(
                                scores_df,
                                x='total_score',
                                nbins=25,
                                title='Opportunity Score Distribution',
                                labels={'total_score': 'Score', 'count': 'ZIP Codes'},
                                color_discrete_sequence=['#3b82f6']
                            )
                            fig1.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#e2e8f0'),
                                title_font_size=16
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
                                title='Population vs Competition',
                                labels={'population': 'Population', 'competitor_count': 'Competitors'},
                                color='total_score',
                                color_continuous_scale='Blues'
                            )
                            fig2.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#e2e8f0'),
                                title_font_size=16
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # AI Assistant Placeholder
                        st.markdown('<div class="section-title">AI Market Assistant (Coming Soon)</div>', unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="ai-assistant">
                            <i class="fas fa-robot ai-icon"></i>
                            <div class="ai-title">Ask AI Anything About This Market</div>
                            <div class="ai-desc">
                                Future feature: Chat with an AI assistant about your analysis.
                                Ask questions like "Why is this ZIP ranked #1?" or "Compare these 3 locations for me"
                            </div>
                            <div style="margin-top: 2rem; color: #a78bfa;">
                                <i class="fas fa-flask"></i> In Development - Pro Feature
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Export
                        st.markdown('<div class="section-title">Export & Reports</div>', unsafe_allow_html=True)
                        
                        dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)
                        
                        with dl_col1:
                            csv = scores_df.to_csv(index=False)
                            st.download_button(
                                "Download Full Dataset",
                                csv,
                                f"ecko_{county_dir.name}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                        
                        with dl_col2:
                            top_csv = top10.to_csv(index=False)
                            st.download_button(
                                "Download Top 10",
                                top_csv,
                                f"top10_{county_dir.name}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                        
                        with dl_col3:
                            if st.button("Generate PDF Report", use_container_width=True):
                                st.info("Pro Feature - Contact: hello@eckoanalytics.com")
                        
                        with dl_col4:
                            if st.button("Email Report", use_container_width=True):
                                st.info("Pro Feature - Contact: hello@eckoanalytics.com")
                        
                        # Methodology
                        with st.expander("View Methodology"):
                            st.markdown("""
                            ### Scoring Algorithm
                            
                            **Population (40%):** Size and density analysis
                            
                            **Economics (30%):** Income levels and purchasing power
                            
                            **Demographics (20%):** Renter rates and household composition
                            
                            **Competition (10%):** Market saturation and gaps
                            
                            ### Data Sources
                            - US Census Bureau 2022 ACS
                            - Yelp Fusion API (real-time)
                            - HUD ZIP-Tract Crosswalk
                            """)
    
    except subprocess.TimeoutExpired:
        st.error("Analysis timeout. Please try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem 0; margin-top: 3rem; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
    <p style='font-size: 0.85rem;'>© 2025 ECKO Analytics | Educational Use Only</p>
</div>
""", unsafe_allow_html=True)