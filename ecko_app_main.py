"""
ECKO Analytics - Landing Page
Enterprise Market Intelligence Platform
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import base64

# Page config
st.set_page_config(
    page_title="ECKO Analytics - Market Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to load background image
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load background image
bg_image = get_base64_image("uploads/image1.jpeg")

# Professional CSS with background
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Background overlay */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.92)), 
                          url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Main container */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }}
    
    /* Header */
    .header {{
        text-align: center;
        padding: 1rem 0 3rem 0;
    }}
    
    .logo {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }}
    
    .tagline {{
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
    }}
    
    /* Hero section */
    .hero {{
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(59, 130, 246, 0.2) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 24px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 3rem 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }}
    
    .hero-title {{
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1.5rem;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}
    
    .hero-subtitle {{
        font-size: 1.4rem;
        color: #cbd5e1;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 3rem auto;
        line-height: 1.6;
    }}
    
    /* Input section */
    .input-container {{
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 600px;
    }}
    
    .input-label {{
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: block;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Feature cards */
    .features-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 4rem 0;
    }}
    
    .feature-card {{
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.5);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        color: #60a5fa;
        margin-bottom: 1rem;
    }}
    
    .feature-title {{
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    
    .feature-desc {{
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    
    /* Stats */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 2rem;
        margin: 3rem 0;
        padding: 2rem;
        background: rgba(30, 41, 59, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }}
    
    .stat-item {{
        text-align: center;
    }}
    
    .stat-number {{
        font-size: 2.5rem;
        font-weight: 800;
        color: #60a5fa;
        display: block;
        margin-bottom: 0.5rem;
    }}
    
    .stat-label {{
        color: #cbd5e1;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Buttons */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
    }}
    
    /* Input fields */
    .stTextInput>div>div>input {{
        background: rgba(15, 23, 42, 0.6);
        border: 2px solid rgba(148, 163, 184, 0.3);
        border-radius: 12px;
        color: white;
        padding: 1rem 1.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 0.1em;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }}
    
    .stTextInput>div>div>input::placeholder {{
        color: #64748b;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Examples */
    .examples {{
        text-align: center;
        margin: 1.5rem 0;
    }}
    
    .example-label {{
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        display: block;
    }}
    
    .example-buttons {{
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }}
    
    /* Responsive */
    @media (max-width: 968px) {{
        .features-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .hero-title {{
            font-size: 2.5rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="logo">ECKO ANALYTICS</div>
    <div class="tagline">Enterprise Market Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero">
    <h1 class="hero-title">Find Your Perfect Location</h1>
    <p class="hero-subtitle">
        Leverage real-time Census and business data to identify high-value investment 
        opportunities across the United States. Make data-driven decisions in under 30 seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# Coverage Map
st.markdown('<div class="section-title" style="color: #e2e8f0; font-size: 1.5rem; font-weight: 700; text-align: center; margin: 3rem 0 2rem 0;">NATIONWIDE COVERAGE</div>', unsafe_allow_html=True)

# Create US map showing coverage
fig = go.Figure(data=go.Choropleth(
    locations=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
               'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
               'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
               'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
               'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
    z=[1]*50,
    locationmode='USA-states',
    colorscale=[[0, '#1e3a8a'], [1, '#3b82f6']],
    showscale=False,
    marker_line_color='#60a5fa',
    marker_line_width=1.5,
))

fig.update_layout(
    geo=dict(
        scope='usa',
        bgcolor='rgba(0,0,0,0)',
        lakecolor='rgba(30, 41, 59, 0.5)',
        landcolor='rgba(30, 41, 59, 0.3)',
        showlakes=True,
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=0, b=0),
    height=400,
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Stats
st.markdown("""
<div class="stats-grid">
    <div class="stat-item">
        <span class="stat-number">3,143</span>
        <span class="stat-label">Counties</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">25M+</span>
        <span class="stat-label">Population</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">30s</span>
        <span class="stat-label">Analysis Time</span>
    </div>
    <div class="stat-item">
        <span class="stat-number">90%</span>
        <span class="stat-label">Success Rate</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<span class="input-label">Enter ZIP Code to Analyze</span>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    zip_code = st.text_input(
        "ZIP Code",
        placeholder="90027",
        label_visibility="collapsed",
        key="zip_input"
    )

with col2:
    analyze_button = st.button("ANALYZE", type="primary")

# Examples
st.markdown("""
<div class="examples">
    <span class="example-label">QUICK START</span>
</div>
""", unsafe_allow_html=True)

ex_col1, ex_col2, ex_col3, ex_col4, ex_col5 = st.columns(5)

clicked_example = None
with ex_col1:
    if st.button("Los Angeles", key="ex1"):
        clicked_example = "90027"
with ex_col2:
    if st.button("Chicago", key="ex2"):
        clicked_example = "60614"
with ex_col3:
    if st.button("New York", key="ex3"):
        clicked_example = "10001"
with ex_col4:
    if st.button("Houston", key="ex4"):
        clicked_example = "77002"
with ex_col5:
    if st.button("Atlanta", key="ex5"):
        clicked_example = "30308"

if clicked_example:
    zip_code = clicked_example
    analyze_button = True

st.markdown('</div>', unsafe_allow_html=True)

# Handle analysis
if analyze_button and zip_code:
    if not zip_code.isdigit() or len(zip_code) != 5:
        st.error("Please enter a valid 5-digit ZIP code")
    else:
        # Store in session state and redirect to results page
        st.session_state['analysis_zip'] = zip_code
        st.session_state['run_analysis'] = True
        st.switch_page("pages/results.py")

# Features
st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <i class="fas fa-chart-line feature-icon"></i>
        <div class="feature-title">Real-Time Data</div>
        <div class="feature-desc">Live integration with Census Bureau and Yelp APIs</div>
    </div>
    <div class="feature-card">
        <i class="fas fa-globe-americas feature-icon"></i>
        <div class="feature-title">Nationwide</div>
        <div class="feature-desc">Complete coverage across all 50 United States</div>
    </div>
    <div class="feature-card">
        <i class="fas fa-bolt feature-icon"></i>
        <div class="feature-title">Instant Analysis</div>
        <div class="feature-desc">Comprehensive results delivered in 30 seconds</div>
    </div>
    <div class="feature-card">
        <i class="fas fa-shield-alt feature-icon"></i>
        <div class="feature-title">Secure & Private</div>
        <div class="feature-desc">Your data is encrypted and never shared</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 3rem 0 2rem 0; margin-top: 4rem; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
    <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>
        © 2025 ECKO Analytics | Market Intelligence Platform
    </p>
    <p style='font-size: 0.8rem; color: #475569;'>
        Educational Use Only | Not Investment Advice
    </p>
</div>
""", unsafe_allow_html=True)