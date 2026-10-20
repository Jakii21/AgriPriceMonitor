import pandas as pd
from load.db_connection import get_connection
import streamlit as st

@st.cache_data(ttl=600)
def load_price_data():
    try:
        conn = get_connection()
        query = "SELECT * FROM vw_price_analysis"
        df = pd.read_sql(query, conn)
        conn.close()
        if not df.empty:
            df['price_date'] = pd.to_datetime(df['price_date']).dt.date
        return df
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return pd.DataFrame()
