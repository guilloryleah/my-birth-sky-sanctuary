import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. DATA
NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def format_dms(deg_raw):
    deg_norm = deg_raw % 360
    sign_idx = int(deg_norm / 30)
    deg_in_sign = deg_norm % 30
    d = int(deg_in_sign)
    m = int((deg_in_sign - d) * 60)
    nak_idx = int(deg_norm / 13.333333) % 27
    return f"{d}° {m}' {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 2. PRECISION ENGINE
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_final_v12")
        loc = geolocator.geocode(city_name)
        if not loc: return 41.87, -87.62, -5.0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        # Force DST check
        offset_hours = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset_hours
    except: return 41.87, -87.62, -5.0

def calculate_sidereal_blueprint(jd_local, lat, lon, offset):
    jd_utc = jd_local - (offset / 24.0)
    ayan = 23.25 
    
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.46061837 + 360.98564736629 * (jd_utc - 2451545.0) + 0.000387933 * t**2) % 360
    lst_deg = (gmst + lon) % 360
    
    eps, phi, l_rad = math.radians(23.439), math.radians(lat), math.radians(lst_deg)
    
    # Refined Ascendant math for Eastern Horizon
    # We use a more direct formula: tan(Asc) = cos(LST) / -(sin(LST)cos(eps) + tan(phi)sin(eps))
    num = math.cos(l_rad)
    den = -(math.sin(l_rad) * math.cos(eps) + math.tan(phi) * math.sin(eps))
    
    asc_raw = math.degrees(math.atan2(num, den)) % 360
    
    sid_asc = (asc_raw - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    return sid_sun, sid_moon, sid_asc

# 3. INTERFACE
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    name = st.text_input("Name", value="Danny")
    y = st.number_input("Year", 1900, 2026, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Exact Birth Time", value=time(4, 10))
    place = st.text_input("Birth City", value="Chicago, IL")
    submit = st.button("REVEAL CHART")

if submit:
    dt = datetime.combine(date(y, m, d), t_in)
    lat, lon, off = get_location_details(place, dt)
    jd_local = pd.Timestamp(dt).to_julian_date()
    
    s_d, m_d, a_d = calculate_sidereal_blueprint(jd_local, lat, lon, off)
    sun_fmt, sun_nak = format_dms(s_d)
    moon_fmt, moon_nak = format_dms(m_d)
    asc_fmt, asc_nak = format_dms(a_d)

    st.header(f"The Star Map for {name}")
    st.write(f"Calculated using UTC Offset: {off}") # This will confirm if it's -5.0
    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🌅 Ascendant")
        st.metric("Lagna", asc_fmt)
        st.write(f"**Nakshatra:** {asc_nak}")
    with c2:
        st.subheader("☀️ Sun")
        st.metric("Surya", sun_fmt)
        st.write(f"**Nakshatra:** {sun_nak}")
    with c3:
        st.subheader("🌙 Moon")
        st.metric("Chandra", moon_fmt)
        st.write(f"**Nakshatra:** {moon_nak}")
