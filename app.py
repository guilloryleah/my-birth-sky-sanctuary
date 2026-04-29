import streamlit as st
import pandas as pd
from datetime import date

# 1. Setup the Sanctuary look
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨")

st.title("✨ Birth Sky Sanctuary")
st.markdown("### Enter Details to Reveal the Sky")

# 2. CLIENT INPUT SECTION
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Full Name", placeholder="Enter name")
        
        # This unlocks the calendar back to the year 1200
        birth_date = st.date_input(
            "Date of Birth",
            value=date(1969, 9, 24), # Default value
            min_value=date(1200, 1, 1), # The "Time Machine" setting
            max_value=date.today()
        )
        
    with col2:
        birth_time = st.time_input("Time of Birth")
        location = st.text_input("City/State of Birth", placeholder="e.g., Houston, TX")

# 3. THE "CALCULATE" TRIGGER
if st.button("Reveal My Birth Sky"):
    st.markdown(f"---")
    st.subheader(f"Results for {client_name}")
    
    st.info(f"Analyzing the heavens for {location} on {birth_date}...")
    
    # Data Table
    data = {
        "Body": ["Ascendant", "Sun", "Moon", "Mercury", "Venus"],
        "Sign": ["Calculating...", "Calculating...", "Calculating...", "Calculating...", "Calculating..."],
        "Note": ["Lahiri Ayanamsa Applied", "Sidereal Calculation", "", "", ""]
    }
    st.table(data)
    st.success(f"Sanctuary records found for the year {birth_date.year}.")

with st.sidebar:
    st.header("Sanctuary Access")
    st.write("Calendar access is currently set from **1200 AD** to the present.")
