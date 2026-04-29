import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE MASTER DATA
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE ASTRONOMICAL ENGINE
def get_coords(city_name):
    try:
        geolocator = Nominatim(user_agent="sanctuary_app_v3")
        loc = geolocator.geocode(city_name)
        return (loc.latitude, loc.longitude) if loc else (29.76, -95.36)
    except:
        return 29.76, -95.36

def calculate_precision_sky(jd, lat, lon):
    # Ayanamsha (Lahiri for 1995/2026 approx)
    ayan = 24.13 
    
    # 1. Calculate Local Sidereal Time (LST) in Degrees
    t = (jd - 2451545.0) / 36525.0
    gmst = (280.46061837 + 360.98564736629 * (jd - 2451545.0)) % 360
    lst_deg = (gmst + lon) % 360
    lst_rad = math.radians(lst_deg)
    
    # 2. Obliquity of the Ecliptic (Earth's Tilt)
    eps = math.radians(23.4392911)
    phi = math.radians(lat)
    
    # 3. THE ASCENDANT FORMULA (Spherical Trigonometry)
    # λAsc = arctan(-cos θL / (sin θL cos ε + tan φ sin ε))
    num = -math.cos(lst_rad)
    den = (math.sin(lst_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    asc_rad = math.atan2(num, den)
    asc_deg = math.degrees(asc_rad) % 360
    
    # 4. Sidereal Adjustments
    sidereal_asc = (asc_deg - ayan) % 360
    sun_raw = ((jd - 2451545.0) * 0.9856 + 280.46 - ayan) % 360
    moon_raw = ((jd - 2451545.0) * 13.176 + 218.31 - ayan) % 360
    
    return sun_raw, moon_raw, sidereal_asc

def get_label(deg):
    return ZODIAC_LIST[int(deg / 30)], NAK_LIST[int(deg / (360/27))]

# 4. SIDEBAR
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("Name", value="Matthew")
    y = st.number_input("Year", 1200, 2026, 1995)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t_in = st.time_input("Birth Time", value=time(12, 0))
    place = st.text_input("Place of Birth", value="Houston, TX")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE OUTPUT
if submit:
    lat, lon = get_coords(place)
    dt = datetime.combine(date(y, m, d), t_in)
    jd = pd.Timestamp(dt).to_julian_date()
    
    s_d, m_d, a_d = calculate_precision_sky(jd, lat, lon)
    s_s, s_n = get_label(s_d)
    m_s, m_n = get_label(m_d)
    a_s, a_n = get_label(a_d)

    st.header(f"✨ Welcome to your Sanctuary, {name}")
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
        st.success(f"**Focus:** Cooling the {s_s} intensity.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:** Opening flow for {a_n}.")
