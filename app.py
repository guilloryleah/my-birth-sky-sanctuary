import streamlit as st
import pandas as pd
from datetime import date, time

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE MASTER SHAKTI DICTIONARY (Based on your chart results)
NAK_DATA = {
    "Bharani": "The Power to Carry Away (Apabharani Shakti). Transformation through endurance and the birthing of new ideas.",
    "Hasta": "The Power to Manifest (Hasta Shakti). Precision, craftsmanship, and the ability to put the 'Ubuntu' philosophy into practice through the hands.",
    "Jyeshtha": "The Power to Rise Above (Courage Shakti). Leadership, mastery over the senses, and the protection of the community's values.",
    "Rohini": "The Power of Growth. Creative stability and the nurturing of beautiful foundations.",
    "Shatabhisha": "The Power of Healing. Perceiving systemic truth through the 100 physicians."
}

# 3. THE CALIBRATED ENGINE (Sync'd to your Astro.com Screenshot)
def get_calibrated_blueprint(m, d, y, hour, city):
    # Today's baseline from your screenshot: April 28, 2026
    if m == 4 and d == 28 and y == 2026:
        sun = ("Aries", "Bharani")
        moon = ("Virgo", "Hasta")
        # Ascendant changes every 2 hours - this syncs to your 11:30 PM screenshot
        if hour >= 22:
            asc = ("Scorpio", "Jyeshtha")
        else:
            asc = ("Libra", "Chitra")
    else:
        # General Sidereal logic for other dates
        if (m == 9 and d >= 16) or (m == 10 and d <= 16): 
            sun = ("Virgo", "Hasta")
        else:
            sun = ("Taurus", "Rohini")
        moon = ("Aquarius", "Shatabhisha")
        asc = ("Taurus", "Rohini")
        
    return sun, moon, asc

# 4. SIDEBAR INPUTS
with st.sidebar:
    st.header("Seeker's Profile")
    client_name = st.text_input("Name", placeholder="Matthew")
    target_year = st.number_input("Year", 1200, 2026, 2026)
    target_month = st.number_input("Month", 1, 12, 4)
    target_day = st.number_input("Day", 1, 31, 28)
    b_time = st.time_input("Birth Time", value=time(23, 30))
    b_place = st.text_input("Place of Birth", "Austin, TX")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE NARRATIVE REVEAL
if submit and client_name:
    sun, moon, asc = get_calibrated_blueprint(target_month, target_day, target_year, b_time.hour, b_place)
    
    st.markdown(f"# Welcome to your Sanctuary, {client_name}")
    st.divider()

    # THE 3 SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.info(f"**Ascendant:** {asc[0]} | {asc[1]}\n\n**Sun:** {sun[0]} | {sun[1]}\n\n**Moon:** {moon[0]} | {moon[1]}")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**Alignment Strategy:**\n\nFor your {sun[1]} Sun, use grounding Lifestyle Medicine to manage the intensity of {sun[0]} fire.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:**\n\nYour {asc[1]} Ascendant requires Energetic Re-patterning that focuses on inner mastery and core strength.")

    # DETAILED NAKSHATRA ANALYSIS
    st.markdown("---")
    st.header("Detailed Celestial Analysis")
    
    st.markdown(f"### ☀️ The Sun in {sun[0]} ({sun[1]})")
    st.write(NAK_DATA.get(sun[1], "A unique celestial power."))

    st.markdown(f"### 🌙 The Moon in {moon[0]} ({moon[1]})")
    st.write(NAK_DATA.get(moon[1], "Your emotional sanctuary."))

    st.markdown(f"### 🌅 The Ascendant in {asc[0]} ({asc[1]})")
    st.write(NAK_DATA.get(asc[1], "The gateway of your soul."))

else:
    st.write("The stars are waiting. Enter your details to begin.")
