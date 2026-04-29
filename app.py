import streamlit as st
import pandas as pd
import swisseph as swe
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. THE NAKSHATRA MAPPING
NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 2. THE CALCULATION ENGINE
def get_sidereal_positions(jd_ut):
    swe.set_sid_mode(swe.SIDM_LAHIRI) # Locks in your Lahiri Ayanamsha 
    planets = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}
    results = {}
    for name, swe_id in planets.items():
        res, _ = swe.calc_ut(jd_ut, swe_id, swe.FLG_SIDEREAL)
        results[name] = res[0]
    results["Ketu"] = (results["Rahu"] + 180) % 360
    return results

def get_ascendant(jd_ut, lat, lon):
    # Using Whole Sign system to match your Houston chart [cite: 21, 125, 139]
    res, _ = swe.houses_ex(jd_ut, lat, lon, b'W', swe.FLG_SIDEREAL)
    return res[0]

def format_position(deg):
    sign_idx = int(deg / 30)
    nak_idx = int(deg / 13.333333) % 27
    return f"{int(deg % 30)}° {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 3. INTERFACE
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("🧭 Birth Details")
    u_name = st.text_input("Name", value="Leah G")
    u_city = st.text_input("Birth City", value="Houston, TX")
    u_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    u_time = st.time_input("Birth Time", value=time(22, 59))

# --- YOUR UPDATED STABLE GEOLOCATOR ---
geolocator = Nominatim(user_agent="LeahG_Sky_Sanctuary_App_v1") 

location = None
if u_city:
    try:
        location = geolocator.geocode(u_city, timeout=10) 
    except:
        st.error("The coordinate service is a bit busy. Please wait a moment and try again.")
# --------------------------------------

if location:
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    tz = pytz.timezone(tz_name)
    dt_local = datetime.combine(u_date, u_time)
    dt_utc = tz.localize(dt_local).astimezone(pytz.utc)
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60)

    if st.button("✨ Reveal My Stars"):
        positions = get_sidereal_positions(jd_ut)
        asc_deg = get_ascendant(jd_ut, location.latitude, location.longitude)
        
        st.header(f"The Soul-Map for {u_name}")
        t_cols = st.columns(3)
        trinity = [("Ascendant", asc_deg), ("Sun", positions["Sun"]), ("Moon", positions["Moon"])]
        
        for i, (label, deg) in enumerate(trinity):
            pos_str, nak = format_position(deg)
            with t_cols[i]:
                st.metric(label, nak)
                st.caption(pos_str)
