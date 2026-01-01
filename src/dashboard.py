"""
Interactive Dashboard - Updated for ZIP Code Analysis
Streamlit app for exploring laundromat market analysis by ZIP code
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Laundromat Market Analysis",
    page_icon="🧺",
    layout="wide"
)


@st.cache_data
def load_data():
    """Load analysis results - tries both ZIP and neighborhood versions"""
    
    # Try ZIP version with location names first
    zip_with_names = Path('outputs/zip_scores_with_names.csv')
    if zip_with_names.exists():
        df = pd.read_csv(zip_with_names)
        df['display_name'] = df['location_name']
        return df, 'zip_with_names'
    
    # Try ZIP version without names
    zip_scores = Path('outputs/zip_scores.csv')
    if zip_scores.exists():
        df = pd.read_csv(zip_scores)
        df['display_name'] = 'ZIP ' + df['zip_code'].astype(str)
        return df, 'zip_only'
    
    # Fallback to neighborhood version
    neighborhood_scores = Path('outputs/neighborhood_scores.csv')
    if neighborhood_scores.exists():
        df = pd.read_csv(neighborhood_scores)
        df['display_name'] = df['neighborhood']
        df['zip_code'] = df.get('neighborhood', 'N/A')  # Placeholder
        return df, 'neighborhood'
    
    st.error("Data not found. Please run the analysis first.")
    st.stop()


def main():
    """Main dashboard function"""
    
    # Header
    st.title("🧺 Laundromat Market Analysis Dashboard")
    st.markdown("**Data-driven site selection for laundromat businesses**")
    
    # Load data
    df, data_type = load_data()
    
    # Show data type indicator
    if data_type == 'zip_with_names':
        st.success("✓ Displaying ZIP-level analysis with location names")
    elif data_type == 'zip_only':
        st.info("ℹ️ Displaying ZIP-level analysis (run add_location_names.py to add place names)")
    else:
        st.info("ℹ️ Displaying neighborhood-level analysis")
    
    st.divider()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    min_score = st.sidebar.slider(
        "Minimum Total Score",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )
    
    max_competitors = st.sidebar.slider(
        "Maximum Competitors",
        min_value=0,
        max_value=int(df['competitor_count'].max()) if df['competitor_count'].max() > 0 else 10,
        value=int(df['competitor_count'].max()) if df['competitor_count'].max() > 0 else 10,
        step=1
    )
    
    # Filter data
    filtered_df = df[
        (df['total_score'] >= min_score) & 
        (df['competitor_count'] <= max_competitors)
    ]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Areas Analyzed",
            len(df)
        )
    
    with col2:
        st.metric(
            "Top Score",
            f"{df['total_score'].max():.1f}"
        )
    
    with col3:
        st.metric(
            "Underserved Markets",
            len(df[df['competitor_count'] == 0])
        )
    
    with col4:
        st.metric(
            "Avg Competition",
            f"{df['competition_density'].mean():.2f}"
        )
    
    st.divider()
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🎯 Top Opportunities", 
        "📈 Detailed Analysis",
        "🗺️ Market Map"
    ])
    
    with tab1:
        st.header("Market Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Score distribution
            fig1 = px.histogram(
                df,
                x='total_score',
                nbins=20,
                title="Distribution of Market Scores",
                labels={'total_score': 'Total Score', 'count': 'Number of Areas'},
                color_discrete_sequence=['#1f77b4']
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Competition vs Score
            fig2 = px.scatter(
                df,
                x='competitor_count',
                y='total_score',
                size='population',
                hover_data=['display_name', 'zip_code'],
                title="Competition vs. Market Score",
                labels={
                    'competitor_count': 'Number of Competitors',
                    'total_score': 'Market Score',
                    'population': 'Population'
                },
                color='total_score',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.header("Top Opportunities")
        
        # Show top 10 areas
        top_10 = df.nlargest(10, 'total_score')
        
        for idx, row in top_10.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.subheader(f"#{int(row['rank'])} {row['display_name']}")
                    if 'zip_code' in row and row['zip_code']:
                        st.caption(f"ZIP: {row['zip_code']} | Score: {row['total_score']:.1f}/100")
                    else:
                        st.caption(f"Score: {row['total_score']:.1f}/100")
                
                with col2:
                    st.metric("Population", f"{int(row['population']):,}")
                    st.metric("Median Income", f"${int(row['median_income']):,}")
                
                with col3:
                    st.metric("Competitors", int(row['competitor_count']))
                    st.metric("Renter Rate", f"{row['renter_rate']*100:.0f}%")
                
                # Score breakdown
                scores_breakdown = pd.DataFrame({
                    'Category': ['Income Match', 'Renter Rate', 'Pop. Density', 'Low Competition'],
                    'Score': [
                        row['income_score'],
                        row['renter_score'],
                        row['density_score'],
                        row['competition_score']
                    ]
                })
                
                fig = px.bar(
                    scores_breakdown,
                    x='Category',
                    y='Score',
                    title=f"Score Breakdown",
                    color='Score',
                    color_continuous_scale='RdYlGn',
                    range_color=[0, 100]
                )
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
    
    with tab3:
        st.header("Detailed Area Analysis")
        
        # Area selector
        selected_area = st.selectbox(
            "Select an area to analyze:",
            options=df['display_name'].tolist()
        )
        
        area_data = df[df['display_name'] == selected_area].iloc[0]
        
        # Display ZIP if available
        if 'zip_code' in area_data and area_data['zip_code']:
            st.info(f"📍 ZIP Code: {area_data['zip_code']}")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rank", f"#{int(area_data['rank'])}")
            st.metric("Total Score", f"{area_data['total_score']:.1f}")
        
        with col2:
            st.metric("Population", f"{int(area_data['population']):,}")
            st.metric("Pop. Density", f"{area_data['population_density']:.0f}/sq mi")
        
        with col3:
            st.metric("Median Income", f"${int(area_data['median_income']):,}")
            st.metric("Renter Rate", f"{area_data['renter_rate']*100:.0f}%")
        
        with col4:
            st.metric("Competitors", int(area_data['competitor_count']))
            st.metric("Comp. Density", f"{area_data['competition_density']:.2f}")
        
        # Radar chart
        categories = ['Income Match', 'Renter Rate', 'Pop. Density', 'Low Competition']
        scores = [
            area_data['income_score'],
            area_data['renter_score'],
            area_data['density_score'],
            area_data['competition_score']
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name=selected_area
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title=f"Performance Profile: {selected_area}",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison to market average
        st.subheader("Comparison to Market Average")
        comparison_data = pd.DataFrame({
            'Metric': ['Total Score', 'Income ($K)', 'Renter Rate (%)', 'Pop. Density (K)'],
            selected_area: [
                area_data['total_score'],
                area_data['median_income']/1000,
                area_data['renter_rate']*100,
                area_data['population_density']/1000
            ],
            'Market Average': [
                df['total_score'].mean(),
                df['median_income'].mean()/1000,
                df['renter_rate'].mean()*100,
                df['population_density'].mean()/1000
            ]
        })
        
        fig = px.bar(
            comparison_data,
            x='Metric',
            y=[selected_area, 'Market Average'],
            barmode='group',
            title="Selected Area vs. Market Average"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Market Ranking")
        
        # Show top 20 in horizontal bar chart
        top_20 = df.nlargest(20, 'total_score')
        
        fig = px.bar(
            top_20.sort_values('total_score', ascending=True),
            x='total_score',
            y='display_name',
            orientation='h',
            title="Top 20 Market Opportunities",
            labels={'total_score': 'Market Score', 'display_name': 'Location'},
            color='total_score',
            color_continuous_scale='RdYlGn',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("Full Data Table")
        
        # Prepare columns to display
        display_cols = ['rank', 'display_name', 'zip_code', 'total_score', 'population',
                       'median_income', 'renter_rate', 'competitor_count',
                       'competition_density']
        
        # Only include columns that exist
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        
        st.dataframe(
            filtered_df[available_cols].style.format({
                'total_score': '{:.1f}',
                'population': '{:,}',
                'median_income': '${:,}',
                'renter_rate': '{:.1%}',
                'competition_density': '{:.2f}'
            }),
            use_container_width=True
        )
    
    # Footer
    st.divider()
    st.caption("💡 Scalable market analysis tool - works for any US county")
    
    # Show instruction if location names not added yet
    if data_type == 'zip_only':
        st.info("💡 **Tip**: Run `python3 add_location_names.py` to add friendly location names (e.g., 'Koreatown, Los Angeles' instead of 'ZIP 90020')")


if __name__ == "__main__":
    main()