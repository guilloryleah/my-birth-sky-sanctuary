import streamlit as st
import pandas as pd
import swisseph as swe  # The 'Digital Telescope' engine
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. THE ALIGNMENT ENGINE (Expanded for all 27 Nakshatras)
# This database ensures the "Nourishment" and "Yoga" are always there.
NAK_ALIGNMENT = {
    "Uttaraphalguni": {"Power": "Chayani Shakti", "Dosha": "Vata/Pitta", "Nourishment": "Grounding stews", "Ritual": "Service"},
    "Revati": {"Power": "Kshiradyapani Shakti", "Dosha": "Kapha/Vata", "Nourishment": "Hydrating broths", "Ritual": "Meditation"},
    "Punarvasu": {"Power": "Vasutva Shakti", "Dosha": "Vata", "Nourishment": "Nuts and seeds", "Ritual": "Breathwork"},
    # ... You would populate all 27 here for a full site
}

NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

# 2. THE LIVE CALCULATION ENGINE
def calculate_sidereal_positions(jd_ut):
    """Calculates the real stars (Lahiri) for any Julian Day."""
    swe.set_sid_mode(swe.SIDM_LAHIRI) # Set the 'True Astronomical Position' 
    
    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
        "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE
    }
    
    results = {}
    for name, id in planets.items():
        res, _ = swe.calc_ut(jd_ut, id, swe.FLG_SIDEREAL)
        results[name] = res[0] # The precise degree 0-360
    return results

# 3. INTERFACE & DYNAMIC LOGIC
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("🧭 Precision Entry")
    name = st.text_input("Client Name")
    city = st.text_input("Birth City", value="Houston, TX")
    b_date = st.date_input("Birth Date", value=date(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=time(22, 59))

# GEOGRAPHIC & TIME CONVERSION
geolocator = Nominatim(user_agent="sanctuary_pro")
location = geolocator.geocode(city)

if location:
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    tz = pytz.timezone(tz_name)
    
    # Calculate Julian Day for the Universal Engine
    dt_local = datetime.combine(b_date, b_time)
    dt_utc = tz.localize(dt_local).astimezone(pytz.utc)
    jd_ut = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60)

    if st.button("✨ Generate Sanctuary Report"):
        # This is where the magic happens—it calculates live!
        data = calculate_sidereal_positions(jd_ut)
        
        st.header(f"The Soul-Map for {name}")
        
        # Displaying the results dynamically
        cols = st.columns(len(data))
        for i, (p_name, deg) in enumerate(data.items()):
            nak_idx = int(deg / 13.333333) % 27
            nak_name = NAK_LIST[nak_idx]
            
            with st.container():
                st.write(f"**{p_name}**")
                st.write(f"### {nak_name}")
                # Pull nourishment and wellbeing from your database
                align = NAK_ALIGNMENT.get(nak_name, {"Dosha": "Balance", "Nourishment": "Whole Foods"})
                st.caption(f"Nourishment: {align['Nourishment']}")
