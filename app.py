import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE PERMANENT NAKSHATRA WHEEL
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE CALCULATION ENGINE (Astronomical Math)
def calculate_sidereal_position(jd):
    # This is a high-level math bridge to find the degree of the moon/asc
    # Based on the Julian Date (jd)
    # We apply the Lahiri Ayanamsa (~24 degrees)
    ayanamsa = 24.2  
    
    # SUN (Approximate degree)
    sun_deg = (jd - 2451545.0) * 0.9856 + 280.46
    sun_sidereal = (sun_deg - ayanamsa) % 360
    
    # MOON (Fast moving - moves ~13.2 deg per day)
    moon_deg = (jd - 2451545.0) * 13.176 + 218.31
    moon_sidereal = (moon_deg - ayanamsa) % 360
    
    # ASCENDANT (Changes based on time of day - approx 15 deg per hour)
    # This is a simplified LST calculation for the Lagna
    hour_offset = (jd % 1) * 360
    asc_sidereal = (moon_sidereal + hour_offset) % 360 # Proxy for Lagna
    
    return sun_sidereal, moon_sidereal, asc_sidereal

def get_sign_and_nak(degree):
    sign = ZODIAC_LIST[int(degree / 30)]
    nak = NAK_LIST[int(degree / (360/27))]
    return sign, nak

# 4. SIDEBAR INPUTS
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("Name", value="Matthew")
    y = st.number_input("Year", 1200, 2026, 1969)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t = st.time_input("Birth Time")
    place = st.text_input("Place of Birth", "Houston, TX")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE OUTPUT
if submit:
    # Convert inputs to Julian Date for the math engine
    dt = datetime.combine(date(y, m, d), t)
    jd = pd.Timestamp(dt).to_julian_date()
    
    sun_d, moon_d, asc_d = calculate_sidereal_position(jd)
    sun_s, sun_n = get_sign_and_nak(sun_d)
    moon_s, moon_n = get_sign_and_nak(moon_d)
    asc_s, asc_n = get_sign_and_nak(asc_d)

    st.header(f"✨ Welcome, {name}")
    st.write(f"Your unique sky over {place} is now live.")
    
    # THE 3 SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.info(f"**Sun:** {sun_s} ({sun_n})\n\n**Moon:** {moon_s} ({moon_n})\n\n**Ascendant:** {asc_s} ({asc_n})")
    
    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**Alignment Strategy:**\n\nBalance the {sun_s} essence with grounding rituals.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:**\n\nNurture the {asc_n} energy through heart-centered flow.")

    st.divider()
    st.markdown(f"### Detailed Analysis for {name}")
    st.write(f"Your **{sun_n}** Sun gives you the power to manifest, while your **{moon_n}** resonance connects you to the collective Ubuntu heart. Finally, your **{asc_n}** Ascendant is the gateway to your life's purpose.")

else:
    st.write("Enter the birth details in the sidebar to begin the calculation.")
