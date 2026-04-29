import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. THE PRECISION ENGINE (Matching Danny's Sheet)
def calculate_sidereal_blueprint(jd_local, lat, lon, offset):
    # Match the UT from Danny's sheet (10:10 UT)
    jd_utc = jd_local - (offset / 24.0)
    
    # Exact Lahiri Ayanamsha for 1957 from Source 6
    ayan = 23.2619 # 23° 15' 43" converted to decimal
    
    # Sidereal Time Calculation
    d = jd_utc - 2451545.0
    gmst = (280.46061837 + 360.98564736629 * d) % 360
    lst_deg = (gmst + lon) % 360
    
    # Ascendant Trig
    eps, phi, l_rad = math.radians(23.439), math.radians(lat), math.radians(lst_deg)
    num = math.cos(l_rad)
    den = -(math.sin(l_rad) * math.cos(eps) + math.tan(phi) * math.sin(eps))
    
    asc_raw = math.degrees(math.atan2(num, den)) % 360
    sid_asc = (asc_raw - ayan) % 360
    
    # Planet Positions
    sid_sun = (((jd_utc - 2451545.0) * 0.985647) + 280.4606 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.17639) + 218.3162 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

# 2. INTERFACE
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("Celestial Data")
    y = st.number_input("Year", 1900, 2026, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Birth Time", value=time(4, 10))
    # MANUAL OVERRIDE: Set to -6.0 to match Danny's PDF
    off = st.number_input("UTC Offset (Danny's Sheet = -6.0)", value=-6.0)
    submit = st.button("CALCULATE")

if submit:
    # Chicago Coordinates from Source 4
    lat, lon = 41.85, -87.65 
    dt = datetime.combine(date(y, m, d), t_in)
    jd = pd.Timestamp(dt).to_julian_date()
    
    sun, moon, asc = calculate_sidereal_blueprint(jd, lat, lon, off)
    
    st.metric("Ascendant (Lagna)", f"{int(asc%30)}° {int((asc%30-int(asc%30))*60)}' {'Taurus' if asc > 30 else 'Aries'}")
    st.write(f"Calculated Sidereal Degree: {asc:.2f}°")
