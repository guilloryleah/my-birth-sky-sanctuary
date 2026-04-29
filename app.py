import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="The Nakshatra Sanctuary", page_icon="✨", layout="wide")

# 2. DATA ARRAYS
NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. HELPER FOR DEGREES/MINUTES
def format_dms(deg_raw):
    """Converts raw degrees to a Sign, Degree, Minute string."""
    sign_index = int(deg_raw / 30) % 12
    sign_name = ZODIAC_LIST[sign_index]
    
    deg_in_sign = deg_raw % 30
    d = int(deg_in_sign)
    m = int((deg_in_sign - d) * 60)
    
    # Identify Nakshatra (each is 13°20' or 13.333°)
    nak_index = int(deg_raw / 13.333333) % 27
    nak_name = NAK_LIST[nak_index]
    
    return f"{d}° {m}' {sign_name}", nak_name

# 4. ENGINE
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_final_degrees")
        loc = geolocator.geocode(city_name)
        if not loc: return 41.87, -87.62, -5.0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_hours = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset_hours
    except: return 41.87, -87.62, -5.0

def calculate_sidereal(jd_local, lat, lon, offset):
    jd_utc = jd_local - (offset / 24.0)
    # Ayanamsha for May 1957
    ayan = 23.25 
    
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.4606 + 360.985647 * (jd_utc - 2451545.0)) % 360
    lst = (gmst + lon) % 360
    
    eps, phi, l_rad = math.radians(23.44), math.radians(lat), math.radians(lst)
    num, den = -math.cos(l_rad), (math.sin(l_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    
    sid_asc = (math.degrees(math.atan2(num, den)) - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

# 5. SIDEBAR
with st.sidebar:
    st.header("Seeker's Data")
    name = st.text_input("Name", value="Danny")
    y = st.number_input("Year", 1900, 2026, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Birth Time", value=time(4, 10))
    place = st.text_input("Birth City", value="Chicago, IL")
    submit = st.button("REVEAL THE CHART")

# 6. MAIN PAGE
if submit:
    dt = datetime.combine(date(y, m, d), t_in)
    lat, lon, off = get_location_details(place, dt)
    jd_local = pd.Timestamp(dt).to_julian_date()
    s_d, m_d, a_d = calculate_sidereal(jd_local, lat, lon, off)

    sun_fmt, sun_nak = format_dms(s_d)
    moon_fmt, moon_nak = format_dms(m_d)
    asc_fmt, asc_nak = format_dms(a_d)

    st.header(f"✨ The Celestial Blueprint for {name}")
    st.divider()

    # Metrics with precise degrees
    c1, c2, c3 = st.columns(3)
    c1.metric("Ascendant (Lagna)", asc_fmt)
    c1.write(f"**Nakshatra:** {asc_nak}")
    
    c2.metric("Sun Placement", sun_fmt)
    c2.write(f"**Nakshatra:** {sun_nak}")
    
    c3.metric("Moon Placement", moon_fmt)
    c3.write(f"**Nakshatra:** {moon_nak}")

    st.divider()
    st.subheader("Planetary Degrees")
    
    # A simple table for clarity
    df = pd.DataFrame({
        "Planet": ["Ascendant", "Sun", "Moon"],
        "Position": [asc_fmt, sun_fmt, moon_fmt],
        "Nakshatra": [asc_nak, sun_nak, moon_nak]
    })
    st.table(df)
