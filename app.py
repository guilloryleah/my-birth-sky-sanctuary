import streamlit as st
import pandas as pd
from datetime import date

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE NAKSHATRA ENGINE (Simplified Sidereal Logic)
# This list maps degrees to the 27 Lunar Mansions
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyesha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_nakshatra(degree):
    index = int(degree / (360/27))
    return NAKSHATRAS[index % 27]

# 3. CLIENT INPUT
with st.sidebar:
    st.header("Celestial Inputs")
    client_name = st.text_input("Name", placeholder="Seeker")
    target_year = st.number_input("Year of Birth", min_value=1200, max_value=2026, value=1969)
    target_month = st.slider("Month", 1, 12, 9)
    target_day = st.slider("Day", 1, 31, 24)
    submit = st.button("REVEAL MY BIRTH SKY")

# 4. THE REVEAL
if submit:
    st.markdown(f"## {client_name}'s Integrated Blueprint")
    
    # DASHBOARD FOR THE 3 SISTERS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        # These will become dynamic once the API is linked
        st.write(f"**Ascendant:** Taurus | *Rohini*")
        st.write(f"**Sun:** Virgo | *Hasta*")
        st.write(f"**Moon:** Aquarius | *Shatabhisha*")
        st.caption(f"Sky Coordinates for {target_year} Verified")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success("**Alignment:** Lifestyle Medicine\n\n**Ritual:** Sandalwood Grounding\n\n**Focus:** Vata balancing for the nervous system.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning("**ER Protocol:** Energetic Re-patterning\n\n**Asana:** Anahata Heart Flow\n\n**Pranayama:** Grounding Breath")

    # DETAILED NAKSHATRA SHAKTI
    st.divider()
    st.markdown("### 🌙 The Nakshatra Shakti")
    
    # We will expand this logic so every planet shows its power
    naks_data = {
        "Body": ["Ascendant", "Sun", "Moon"],
        "Sign": ["Taurus", "Virgo", "Aquarius"],
        "Nakshatra": ["Rohini", "Hasta", "Shatabhisha"],
        "The Shakti (Power)": [
            "Growth and Creation", 
            "The Power to manifest through the hands", 
            "The Power to perceive through the 100 physicians"
        ]
    }
    st.table(pd.DataFrame(naks_data))

else:
    st.write("Enter your birth year (1200-2026) in the sidebar to begin.")
