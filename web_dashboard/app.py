import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Ensure project root is in sys.path for robust importing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from web_dashboard.utils import load_price_data
except ImportError:
    from utils import load_price_data

# Page configuration
st.set_page_config(
    page_title="Agri Price Monitor - Market Price Overview",
    page_icon="🌾",
    layout="wide"
)

# Load data
df = load_price_data()

if df.empty:
    st.warning("No data found in database. Please run the ETL pipeline (`python main.py`) first or check database connection.")
else:
    # Header
    st.title("🌾 AGRI PRICE MONITOR")
    st.markdown("### Market Price Overview | Daily Market Price Analytics")
    st.markdown("---")

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # City Filter
    cities = sorted(df['city_name'].dropna().unique())
    selected_cities = st.sidebar.multiselect("Select City/Cities", options=cities, default=cities)

    # Market Filter based on selected cities
    filtered_df_city = df[df['city_name'].isin(selected_cities)]
    markets = sorted(filtered_df_city['market_name'].dropna().unique())
    selected_markets = st.sidebar.multiselect("Select Market(s)", options=markets, default=markets)

    # Category Filter
    categories = sorted(df['category_name'].dropna().unique())
    selected_categories = st.sidebar.multiselect("Select Category/Categories", options=categories, default=categories)

    # Date Filter
    dates = sorted(df['price_date'].dropna().unique(), reverse=True)
    if dates:
        selected_date = st.sidebar.selectbox("Select Price Date", options=dates, index=0)
    else:
        selected_date = None

    # Apply filters
    filtered_df = df[
        df['city_name'].isin(selected_cities) &
        df['market_name'].isin(selected_markets) &
        df['category_name'].isin(selected_categories)
    ]

    if selected_date:
        date_filtered_df = filtered_df[filtered_df['price_date'] == selected_date]
    else:
        date_filtered_df = filtered_df

    # --- KPI Metrics Cards ---
    st.subheader(f"📊 Summary Metrics for {selected_date if selected_date else 'All Dates'}")
    
    col1, col2, col3, col4, col5 = st.columns(5)

    latest_date = str(df['price_date'].max()) if not df.empty else "N/A"
    avg_price = date_filtered_df['price_average'].mean() if not date_filtered_df.empty else 0.0
    total_items = date_filtered_df['item_name'].nunique() if not date_filtered_df.empty else 0
    total_markets = date_filtered_df['market_name'].nunique() if not date_filtered_df.empty else 0
    total_records = len(date_filtered_df)

    col1.metric("Latest Price Date", latest_date)
    col2.metric("Average Price", f"₱{avg_price:,.2f}")
    col3.metric("Items Covered", total_items)
    col4.metric("Markets Covered", total_markets)
    col5.metric("Total Records", total_records)

    st.markdown("---")

    # --- Charts Section ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("#### 📈 Price Trend Over Time")
        if not filtered_df.empty:
            trend_df = filtered_df.groupby(['price_date', 'category_name'])['price_average'].mean().reset_index()
            fig_trend = px.line(
                trend_df,
                x='price_date',
                y='price_average',
                color='category_name',
                markers=True,
                labels={'price_date': 'Date', 'price_average': 'Average Price (PHP)', 'category_name': 'Category'}
            )
            fig_trend.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_trend, width='stretch')
        else:
            st.info("No data available for the selected filters.")

    with row1_col2:
        st.markdown("#### 🏷️ Average Price by Category")
        if not date_filtered_df.empty:
            cat_df = date_filtered_df.groupby('category_name')['price_average'].mean().reset_index()
            fig_cat = px.bar(
                cat_df,
                x='category_name',
                y='price_average',
                color='category_name',
                text_auto='.2f',
                labels={'category_name': 'Category', 'price_average': 'Average Price (PHP)'}
            )
            fig_cat.update_layout(height=400, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
            st.plotly_chart(fig_cat, width='stretch')
        else:
            st.info("No data available for the selected filters.")

    # Second row: Market Comparison bar chart
    st.markdown("#### 🛒 Average Price by Market")
    if not date_filtered_df.empty:
        market_df = date_filtered_df.groupby(['market_name', 'city_name'])['price_average'].mean().reset_index()
        fig_market = px.bar(
            market_df,
            x='market_name',
            y='price_average',
            color='city_name',
            text_auto='.2f',
            barmode='group',
            labels={'market_name': 'Market Name', 'price_average': 'Average Price (PHP)', 'city_name': 'City'}
        )
        fig_market.update_layout(height=450, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_market, width='stretch')
    else:
        st.info("No data available for the selected filters.")

    # Data Table Preview
    with st.expander("📋 View Filtered Raw Data"):
        st.dataframe(date_filtered_df, use_container_width=True)
