import streamlit as st
import requests
import pandas as pd
import sqlite3
import time

# The address of your FastAPI server
BASE_URL = "http://127.0.0.1:8000"

st.title("🦋 The Butterfly Tracker")
st.subheader("Simulate User Interactions")

st.subheader("📊 Live Sniper Feed")

# 1. This function reads the database and turns it into a table
def get_live_data():
    conn = sqlite3.connect('butterfly_tracker.db')
    # We use Pandas to read the SQL table easily
    df = pd.read_sql_query("SELECT * FROM interactions ORDER BY id DESC", conn)
    conn.close()
    return df

# 2. This is the "Magic" part: A fragment that runs every 2 seconds
@st.fragment(run_every=2)
def show_live_table():
    data = get_live_data()
    # Display the data as a nice interactive table
    st.dataframe(data, width="stretch")

    # Add a checkbox at the top or bottom
    show_stats = st.checkbox("Show Sniper Analytics")

    if show_stats:
        st.subheader("📈 Interaction Breakdown")
        status_counts = data['email'].isna().value_counts()
        status_counts.index = status_counts.index.map({True: 'Butterflies🦋', False: 'Identified✅'})
        st.bar_chart(status_counts, horizontal=True, x_label="Total Actions", y_label="Status")

# 3. Call the fragment
show_live_table()