import streamlit as st
import pandas as pd
import swisseph as swe
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. DATA MAPS
NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def format_position(deg):
    sign_idx = int(deg / 30)
    nak_idx = int(deg / 13.333333) % 27
    return f"{int(deg % 30)}° {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 2. INTERFACE
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("🧭 Birth Details")
    u_name = st.text_input("Name", value="Leah G")
    u_city = st.text_input("Birth City", value="Houston, TX")
    
    # THE SAFETY SWITCH
    manual_mode = st.toggle("Enter coordinates manually if service is busy")
    if manual_mode:
        lat = st.number_input("Latitude (e.g. 29.76 for Houston)", value=29.76)
        lon = st.number_input("Longitude (e.g. -95.36 for Houston)", value=-95.36)
    
    u_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    u_time = st.time_input("Birth Time", value=time(22, 59))
    u_offset = st.number_input("UTC Offset (Manual)", value=-5.0)

# 3. THE CALCULATION
if st.button("✨ Reveal My Stars"):
    # Determine coordinates
    final_lat, final_lon = None, None
    
    if manual_mode:
        final_lat, final_lon = lat, lon
    else:
        try:
            geolocator = Nominatim(user_agent="LeahG_Sky_Sanctuary_Final")
            location = geolocator.geocode(u_city, timeout=10)
            if location:
                final_lat, final_lon = location.latitude, location.longitude
            else:
                st.error("City not found. Please try the 'Manual' toggle.")
        except:
            st.error("The map service is busy. Please use the 'Manual' toggle in the sidebar to proceed.")

    if final_lat is not None:
        # JULIAN DAY CALCULATION
        # Note: Using manual offset for ultimate reliability
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        h_decimal = u_time.hour + (u_time.minute / 60.0) - u_offset
        jd_ut = swe.julday(u_date.year, u_date.month, u_date.day, h_decimal)

        # PLANETARY POSITIONS
        st.header(f"The Soul-Map for {u_name}")
        
        # Calculate Ascendant (Taurus/Rohini)
        res, _ = swe.houses_ex(jd_ut, final_lat, final_lon, b'W', swe.FLG_SIDEREAL)
        asc_deg = res[0]
        
        # Calculate Sun/Moon
        sun_res, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SIDEREAL)
        moon_res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)
        
        t_cols = st.columns(3)
        trinity = [("Ascendant", asc_deg), ("Sun", sun_res[0]), ("Moon", moon_res[0])]
        
        for i, (label, deg) in enumerate(trinity):
            pos_str, nak = format_position(deg)
            with t_cols[i]:
                st.metric(label, nak)
                st.write(f"**{pos_str}**")
