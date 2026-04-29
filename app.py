import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. COORDINATE & NAKSHATRA DATA
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE PRECISION ENGINE
def calculate_lagna(jd, lon):
    # LST Calculation: Finding the exact point rising on the horizon
    # Based on Julian Date and Longitude
    ayanamsa = 24.13 # Lahiri Offset
    
    # Calculate Greenwich Mean Sidereal Time (GMST)
    t = (jd - 2451545.0) / 36525.0
    gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t**2 - t**3 / 38710000
    
    # Local Sidereal Time (LST)
    lst = (gmst + lon) % 360
    
    # Ascendant Calculation (Simplified Geometric Projection)
    # This aligns the LST to the Ecliptic to find the Lagna
    asc_deg = (lst + 90) % 360
    sidereal_asc = (asc_deg - ayanamsa) % 360
    
    return sidereal_asc

def get_sign_and_nak(degree):
    sign = ZODIAC_LIST[int(degree / 30)]
    nak = NAK_LIST[int(degree / (360/27))]
    return sign, nak

# 4. SIDEBAR INPUTS
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("Full Name", value="Matthew")
    y = st.number_input("Year", 1200, 2026, 1995)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t_input = st.time_input("Birth Time")
    
    # We need the longitude to fix the Ascendant error
    st.caption("Longitude is key for the Ascendant. Houston is -95.3, Austin is -97.7")
    lon = st.number_input("Longitude (Decimal)", value=-95.36) 
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE OUTPUT
if submit:
    dt = datetime.combine(date(y, m, d), t_input)
    jd = pd.Timestamp(dt).to_julian_date()
    
    # Calculate Sun & Moon (Date/Time based)
    sun_raw = ((jd - 2451545.0) * 0.9856 + 280.46 - 24.13) % 360
    moon_raw = ((jd - 2451545.0) * 13.176 + 218.31 - 24.13) % 360
    
    # Calculate Ascendant (Location based)
    asc_raw = calculate_lagna(jd, lon)
    
    # Convert to Signs/Nakshatras
    s_sign, s_nak = get_sign_and_nak(sun_raw)
    m_sign, m_nak = get_sign_and_nak(moon_raw)
    a_sign, a_nak = get_sign_and_nak(asc_raw)

    st.header(f"✨ Welcome to your Sanctuary, {name}")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.metric("Ascendant (Lagna)", a_sign)
        st.write(f"**Nakshatra:** {a_nak}")
        st.write(f"**Sun:** {s_sign} ({s_nak})")
        st.write(f"**Moon:** {m_sign} ({m_nak})")
    
    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**Focus:** Balancing the {s_sign} core.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:** Nurturing the {a_nak} rising.")

else:
    st.write("Please enter the birth details. The Ascendant requires the decimal Longitude for precision.")
