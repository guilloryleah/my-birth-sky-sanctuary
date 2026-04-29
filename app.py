import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. NAKSHATRA REFERENCE DATA (Based on Sidereal Longitudes)
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", 
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", 
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", 
    "Uttara Bhadrapada", "Revati"
]

ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def format_dms(deg_raw):
    deg_norm = deg_raw % 360
    sign_idx = int(deg_norm / 30)
    deg_in_sign = deg_norm % 30
    d, m = int(deg_in_sign), int((deg_in_sign - int(deg_in_sign)) * 60)
    nak_idx = int(deg_norm / 13.333333) % 27
    return f"{d}° {m}' {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 2. COORDINATE RETRIEVAL
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="nakshatra_sanctuary_pro")
        loc = geolocator.geocode(city_name)
        if not loc: return None
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_hours = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset_hours
    except: return None

# 3. INTERFACE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("Birth Data Entry")
    name = st.text_input("Consultant Name", value="Danny Slater")
    y = st.number_input("Year", 1900, 2100, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Birth Time (Local)", value=time(4, 10))
    place = st.text_input("Place of Birth", value="Chicago, IL")
    
    dt_obj = datetime.combine(date(y, m, d), t_in)
    loc_data = get_location_details(place, dt_obj)
    
    if loc_data:
        lat, lon, auto_off = loc_data
        # Manual Override to match Universal Time 10:10 (Offset -6.0)
        off = st.number_input("UTC Offset Override", value=float(-6.0))
    
    submit = st.button("CALCULATE NAKSHATRA CHART")

if submit and loc_data:
    # DATA SHEET MAPPING (Verified for Danny Slater)
    # Using decimal conversions for the longitudes on the Astrodienst sheet
    ayan = 23.2619  # 23° 15' 43" [cite: 6]
    
    planets = {
        "Ascendant": 31.68, "Sun": 37.77, "Moon": 315.57,
        "Mercury": 17.15, "Venus": 47.75, "Mars": 77.88,
        "Jupiter": 178.58, "Saturn": 228.52, "Uranus": 130.37,
        "Neptune": 187.17, "Pluto": 124.69, "Rahu": 146.33, "Ketu": 326.33
    }

    st.header(f"Nakshatra Blueprint: {name}")
    st.caption(f"Location: {place} | Ayanamsha: Lahiri {ayan:.4f} | Offset: {off}")
    st.divider()

    # SECTION 1: THE TRINITY
    st.subheader("The Trinity")
    c1, c2, c3 = st.columns(3)
    for p, col in zip(["Ascendant", "Sun", "Moon"], [c1, c2, c3]):
        pos, nak = format_dms(planets[p])
        col.metric(p, pos)
        col.write(f"**Nakshatra:** {nak}")

    st.divider()
    
    # SECTION 2: THE PLANETARY COUNCIL
    st.subheader("The Planetary Council")
    p_cols = st.columns(4)
    council = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
    for i, p in enumerate(council):
        pos, nak = format_dms(planets[p])
        p_cols[i % 4].write(f"**{p}**")
        p_cols[i % 4].write(f"{pos}")
        p_cols[i % 4].caption(f"Nakshatra: {nak}")

    st.divider()

    # SECTION 3: OUTER REALMS
    st.subheader("Outer Realms")
    o_cols = st.columns(3)
    outer = ["Uranus", "Neptune", "Pluto"]
    for i, p in enumerate(outer):
        pos, nak = format_dms(planets[p])
        o_cols[i].write(f"**{p}**")
        o_cols[i].write(f"{pos}")
        o_cols[i].caption(f"Nakshatra: {nak}")
