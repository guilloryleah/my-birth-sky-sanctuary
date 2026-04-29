import streamlit as st
import pandas as pd
import swisseph as swe
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. THE NAKSHATRA MAPPING (The 27 Mansions)
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", 
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", 
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", 
    "Uttara Bhadrapada", "Revati"
]

ZODIAC_LIST = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# 2. THE CALCULATION ENGINE
def get_sidereal_positions(jd_ut):
    """Calculates planetary positions using the Lahiri Ayanamsha."""
    swe.set_sid_mode(swe.SIDM_LAHIRI) # Forces the 24-degree correction [cite: 14]
    
    planets_to_calc = {
        "Ascendant": None, # Handled by house calculation
        "Sun": swe.SUN, 
        "Moon": swe.MOON, 
        "Mercury": swe.MERCURY, 
        "Venus": swe.VENUS, 
        "Mars": swe.MARS, 
        "Jupiter": swe.JUPITER, 
        "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
        "Ketu": None # Ketu is always 180 degrees from Rahu
    }
    
    results = {}
    for name, swe_id in planets_to_calc.items():
        if name == "Ascendant": continue # We'll calculate this with houses
        res, _ = swe.calc_ut(jd_ut, swe_id, swe.FLG_SIDEREAL)
        results[name] = res[0]
        
    results["Ketu"] = (results["Rahu"] + 180) % 360
    return results

def get_ascendant(jd_ut, lat, lon):
    """Calculates the exact Rising Sign based on coordinates."""
    # Using Whole Sign House System as per Leah's chart [cite: 21]
    res, _ = swe.houses_ex(jd_ut, lat, lon, b'W', swe.FLG_SIDEREAL)
    return res[0] # The Ascendant degree

def format_position(deg):
    """Converts raw degrees into Sign and Nakshatra names."""
    sign_idx = int(deg / 30)
    deg_in_sign = deg % 30
    nak_idx = int(deg / 13.333333) % 27
    return f"{int(deg_in_sign)}° {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 3. THE USER INTERFACE
st.title("✨ The Nakshatra Sanctuary")
st.subheader("Discover your place in the actual sky.")

with st.sidebar:
    st.header("🧭 Birth Details")
    u_name = st.text_input("Name", value="Leah G")
    u_city = st.text_input("Birth City", value="Houston, TX")
    u_date = st.date_input("Birth Date", value=date(1969, 9, 24))
    u_time = st.time_input("Birth Time", value=time(22, 59))

# GEOGRAPHIC LOGIC
geolocator = Nominatim(user_agent="sanctuary_engine")
location = geolocator.geocode(u_city)

if location:
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    tz = pytz.timezone(tz_name)
    
    # Time Conversion to Universal Time (UT) 
    dt_local = datetime.combine(u_date, u_time)
    dt_utc = tz.localize(dt_local).astimezone(pytz.utc)
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60)

    if st.button("✨ Reveal My Stars"):
        st.balloons()
        
        # Calculations
        positions = get_sidereal_positions(jd_ut)
        asc_deg = get_ascendant(jd_ut, location.latitude, location.longitude)
        
        # Display Results
        st.header(f"The Soul-Map for {u_name}")
        
        # The Trinity
        t_cols = st.columns(3)
        trinity = [("Ascendant", asc_deg), ("Sun", positions["Sun"]), ("Moon", positions["Moon"])]
        
        for i, (label, deg) in enumerate(trinity):
            pos_str, nak = format_position(deg)
            with t_cols[i]:
                st.metric(label, nak)
                st.write(f"**Position:** {pos_str}")
                
        # The Council
        st.divider()
        st.subheader("🪐 The Planetary Council")
        council_cols = st.columns(4)
        planets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
        
        for i, p in enumerate(planets):
            pos_str, nak = format_position(positions[p])
            with council_cols[i % 4]:
                st.write(f"**{p}**")
                st.info(f"{nak}\n\n({pos_str})")
else:
    st.error("Please enter a valid city to begin.")
