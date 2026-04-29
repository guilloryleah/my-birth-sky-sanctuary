import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim

# 1. SANCTUARY CONFIG
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

# 3. THE ASTRONOMICAL ENGINE
def get_coords(city_name):
    try:
        geolocator = Nominatim(user_agent="sanctuary_v4")
        loc = geolocator.geocode(city_name)
        return (loc.latitude, loc.longitude) if loc else (29.76, -95.36)
    except:
        return 29.76, -95.36

def calculate_precision_sky(jd, lat, lon, offset):
    # Adjust Julian Date for Local Time Zone
    jd_utc = jd + (offset / 24.0)
    ayan = 24.13 # Lahiri Ayanamsha
    
    # LST Calculation
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.4606 + 360.985647 * (jd_utc - 2451545.0)) % 360
    lst_deg = (gmst + lon) % 360
    
    # Spherical Projection for the Ascendant
    eps = math.radians(23.439)
    phi = math.radians(lat)
    lst_rad = math.radians(lst_deg)
    
    num = -math.cos(lst_rad)
    den = (math.sin(lst_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    asc_deg = math.degrees(math.atan2(num, den)) % 360
    
    # Final Sidereal Positions
    sid_asc = (asc_deg - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

def get_label(deg):
    return ZODIAC_LIST[int(deg / 30)], NAK_LIST[int(deg / (360/27))]

# 4. SIDEBAR
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("Name", value="Matthew")
    y = st.number_input("Year", 1200, 2026, 1995)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t_in = st.time_input("Birth Time")
    place = st.text_input("Place of Birth", value="Houston, TX")
    
    # Timezone correction (Central is -5 or -6)
    tz = st.selectbox("Time Zone Offset", options=[-6, -5, 0, 1], index=0, help="Central Time is usually -6")
    
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE OUTPUT
if submit:
    lat, lon = get_coords(place)
    dt = datetime.combine(date(y, m, d), t_in)
    jd = pd.Timestamp(dt).to_julian_date()
    
    s_d, m_d, a_d = calculate_precision_sky(jd, lat, lon, -tz) # Flip sign for UTC math
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
        st.success(f"**Alignment Strategy:**\n\nAs a {a_s} rising, your system favors precision. Focus on Vata-balancing rituals.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:**\n\nGrounding for {a_n} energy.")
