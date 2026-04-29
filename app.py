import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from geopy.geocoders import Nominatim

# 1. SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. DATA ARRAYS
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. GEOGRAPHIC & ASTRONOMIC ENGINE
def get_coords(city_name):
    try:
        geolocator = Nominatim(user_agent="birth_sky_sanctuary")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        return 29.76, -95.36 # Default to Houston if not found
    except:
        return 29.76, -95.36

def calculate_precision_sky(jd, lon):
    ayanamsa = 24.13 # Lahiri 
    # GMST Calculation
    t = (jd - 2451545.0) / 36525.0
    gmst = (280.46061837 + 360.98564736629 * (jd - 2451545.0)) % 360
    lst = (gmst + lon) % 360
    
    # Lagna Projection
    asc_raw = (lst + 90) % 360
    sidereal_asc = (asc_raw - ayanamsa) % 360
    
    # Sun & Moon Speeds
    sun_raw = ((jd - 2451545.0) * 0.9856 + 280.46 - ayanamsa) % 360
    moon_raw = ((jd - 2451545.0) * 13.176 + 218.31 - ayanamsa) % 360
    
    return sun_raw, moon_raw, sidereal_asc

def get_label(degree):
    sign = ZODIAC_LIST[int(degree / 30)]
    nak = NAK_LIST[int(degree / (360/27))]
    return sign, nak

# 4. SIDEBAR INPUTS
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("Name", value="Matthew")
    y = st.number_input("Year", 1200, 2026, 1995)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t_input = st.time_input("Birth Time")
    birth_place = st.text_input("City of Birth", value="Houston, TX")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE NARRATIVE OUTPUT
if submit:
    lat, lon = get_coords(birth_place)
    dt = datetime.combine(date(y, m, d), t_input)
    jd = pd.Timestamp(dt).to_julian_date()
    
    s_deg, m_deg, a_deg = calculate_precision_sky(jd, lon)
    s_s, s_n = get_label(s_deg)
    m_s, m_n = get_label(m_deg)
    a_s, a_n = get_label(a_deg)

    st.header(f"✨ Welcome to your Sanctuary, {name}")
    st.write(f"Born in **{birth_place}** | Coordinates: {lat}, {lon}")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.metric("Ascendant (Lagna)", a_s)
        st.write(f"**Nakshatra:** {a_n}")
        st.write(f"**Sun:** {s_s} ({s_n})")
        st.write(f"**Moon:** {m_s} ({m_n})")
    
    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**Alignment Strategy:**\n\nNourish your {s_s} nature.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:**\n\nBalance your {a_n} Rising energy.")

    st.info(f"**Teacher's Insight:** Your Ascendant in {a_s} with the power of {a_n} suggests a soul that meets the world through {a_n}'s specific Shakti.")

else:
    st.write("The Sanctuary awaits your details.")
