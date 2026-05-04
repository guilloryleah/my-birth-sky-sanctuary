import streamlit as st
import swisseph as swe
import datetime
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# --- THE COSMIC ENGINE ---
def get_accurate_sidereal_data(date, time, lat, lon):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    local_tz = pytz.timezone(timezone_str)
    
    # Precise conversion to UTC for historical accuracy (handles Chicago 1957 DST)
    local_dt = local_tz.localize(datetime.datetime.combine(date, time))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd_utc = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                        utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
    
    # Strict Sidereal Mandate: Lahiri Ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Horizon Logic: Placidus System
    cusps, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P', swe.FLG_SIDEREAL)
    
    return {"ascendant": ascmc[0], "timezone": timezone_str}

# --- THE MODERN STUDIO SANCTUARY ---
st.set_page_config(page_title="The Sidereal Sanctuary", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #2b1d16; color: #e5d3b3; }
    .stButton>button { 
        background-color: #3d2b1f; color: #e5d3b3; border: 1px solid #7b5e43; 
        border-radius: 0px; width: 100%; letter-spacing: 0.2em;
    }
    input { background-color: #3d2b1f !important; color: #e5d3b3 !important; border: 1px solid #7b5e43 !important; }
    label { color: #a68b7c !important; text-transform: uppercase; letter-spacing: 0.1em; }
    </style>
    """, unsafe_allow_html=True)

st.title("The Celestial Blueprint")
st.write("Where astronomical truth meets the soul's expression.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("Birth Date", value=datetime.date(1957, 5, 22))
    with col2:
        birth_time = st.time_input("Birth Time", value=datetime.time(4, 10))
    
    # New City Input replacing manual coordinates
    city_input = st.text_input("Birth City (e.g., Chicago, IL, USA)", value="Chicago, IL, USA")

if st.button("REVEAL THE AVATAR'S PATH"):
    # Geocoding the city to find lat/long
    geolocator = Nominatim(user_agent="sidereal_sanctuary")
    location = geolocator.geocode(city_input)
    
    if location:
        data = get_accurate_sidereal_data(birth_date, birth_time, location.latitude, location.longitude)
        
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_name = signs[int(data['ascendant'] / 30)]
        display_deg = data['ascendant'] % 30

        st.markdown(f"""
            <div style="border: 1px solid #7b5e43; padding: 30px; background-color: #3d2b1f; margin-top: 25px;">
                <p style="text-transform: uppercase; letter-spacing: 0.3em; font-size: 0.75rem; color: #a68b7c;">The Avatar's Path</p>
                <h1 style="color: #e5d3b3; margin-top: 0;">Ascendant: {display_deg:.2f}° {sign_name}</h1>
                <hr style="border: 0; border-top: 1px solid #7b5e43; margin: 20px 0;">
                <div style="color: #a68b7c; font-size: 0.9rem;">
                    <p><b>Standard:</b> Sidereal (Lahiri)</p>
                    <p><b>Horizon:</b> Placidus</p>
                    <p><b>Location:</b> {location.address}</p>
                    <p><b>Moment:</b> {data['timezone']} (Corrected)</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("The cosmos could not find that location. Please try a more specific city and state.")
