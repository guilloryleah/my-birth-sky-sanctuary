import streamlit as st
import pandas as pd
from datetime import date, time

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

st.title("✨ Birth Sky Sanctuary")
st.markdown("### Astrology • Ayurveda • Yoga")

# 2. CLIENT INPUT - FULL PRECISION
with st.sidebar:
    st.header("Celestial Inputs")
    client_name = st.text_input("Full Name", placeholder="Seeker")
    
    # Year Input (Unlocks 1200 AD)
    target_year = st.number_input("Year of Birth", min_value=1200, max_value=2026, value=1969)
    
    # Month & Day
    col_m, col_d = st.columns(2)
    with col_m:
        target_month = st.number_input("Month", 1, 12, 9)
    with col_d:
        target_day = st.number_input("Day", 1, 31, 24)
    
    # BIRTH TIME (Critical for Ascendant and Nakshatra)
    birth_time = st.time_input("Exact Birth Time", value=time(12, 0))
    
    # LOCATION (Critical for House Alignment)
    location = st.text_input("City/State of Birth", value="Houston, TX")
    
    submit = st.button("REVEAL MY BIRTH SKY")

# 3. THE REVEAL
if submit:
    st.markdown(f"## {client_name}'s Integrated Blueprint")
    st.info(f"Mapping the heavens for {location} at {birth_time} on {target_month}/{target_day}/{target_year}")

    # THE 3 SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        # In the next step, these variables will be tied to the math engine
        st.write("**Ascendant:** Taurus | *Rohini*")
        st.write("**Sun:** Virgo | *Hasta*")
        st.write("**Moon:** Aquarius | *Shatabhisha*")
        st.caption("Sidereal Lahiri Accuracy")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success("**Alignment:** Lifestyle Medicine\n\n**Ritual:** Sandalwood Grounding")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning("**ER Protocol:** Energetic Re-patterning\n\n**Asana:** Anahata Heart Flow")

    # DETAILED NAKSHATRA SHAKTI
    st.divider()
    st.markdown("### 🌙 The Nakshatra & The Shakti")
    
    # Creating the data table for the client
    naks_data = {
        "Placement": ["Ascendant (Lagna)", "Sun (Surya)", "Moon (Chandra)"],
        "Sign": ["Taurus", "Virgo", "Aquarius"],
        "Nakshatra": ["Rohini", "Hasta", "Shatabhisha"],
        "The Shakti (Power)": [
            "The power of growth and creation (Prabhava Shakti)", 
            "The power to manifest through the hands (Hasta Shakti)", 
            "The power of healing and perception (Bheshaja Shakti)"
        ]
    }
    st.table(pd.DataFrame(naks_data))

else:
    st.write("Enter your full birth details in the sidebar. Precision matters for your Sanctuary.")
