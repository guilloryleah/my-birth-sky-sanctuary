import streamlit as st
import swisseph as swe
import datetime
import pytz
from timezonefinder import TimezoneFinder

# --- THE COSMIC ENGINE ---
def get_accurate_sidereal_data(date, time, lat, lon):
    """
    Calculates high-precision Sidereal data using the Lahiri system
    and automatic historical DST correction.
    """
    # 1. Detect the historical timezone for the specific birth location
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    local_tz = pytz.timezone(timezone_str)
    
    # 2. Precise conversion to UTC to handle historical clock shifts
    local_dt = local_tz.localize(datetime.datetime.combine(date, time))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    # 3. Calculate Julian Day for the exact UTC moment
    decimal_hour_utc = utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0
    jd_utc = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, decimal_hour_utc)
    
    # 4. Mandate: Strict Sidereal Science using Lahiri Ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # 5. Mandate: Placidus House System for the Ascendant/Horizon
    cusps, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P', swe.FLG_SIDEREAL)
    
    return {
        "ascendant": ascmc[0],
        "timezone": timezone_str,
        "utc_time": utc_dt
    }

# --- THE MODERN STUDIO SANCTUARY ---
st.set_page_config(page_title="The Sidereal Sanctuary", layout="centered")

# Visual Poetics: Warm Oak and Chocolate Accents
st.markdown("""
    <style>
    .stApp { background-color: #2b1d16; color: #e5d3b3; }
    .stButton>button { 
        background-color: #3d2b1f; 
        color: #e5d3b3; 
        border: 1px solid #7b5e43; 
        border-radius: 0px;
        width: 100%;
        letter-spacing: 0.2em;
        font-weight: bold;
    }
    /* Input Styling for the Chocolate Palette */
    input { background-color: #3d2b1f !important; color: #e5d3b3 !important; border: 1px solid #7b5e43 !important; }
    div[data-baseweb="select"] > div { background-color: #3d2b1f !important; }
    label { color: #a68b7c !important; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("The Celestial Blueprint")
st.write("Where astronomical truth meets the soul's expression.")

# Client Entry Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        birth_date = st.date_input("Birth Date", value=datetime.date(1957, 5, 22))
    with col2:
        birth_time = st.time_input("Birth Time", value=datetime.time(4, 10))
    
    # Coordinates for high-precision calculations (Defaulted to Chicago for verification)
    lat = st.number_input("Latitude", value=41.8781, format="%.4f")
    lon = st.number_input("Longitude", value=-87.6298, format="%.4f")

if st.button("REVEAL THE AVATAR'S PATH"):
    # Calculate the precise astronomical data
    data = get_accurate_sidereal_data(birth_date, birth_time, lat, lon)
    
    # Logic to identify the Sign Name based on degrees
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_index = int(data['ascendant'] / 30)
    sign_name = signs[sign_index]
    display_deg = data['ascendant'] % 30

    # The Result Card: A poised presentation for your clients
    st.markdown(f"""
        <div style="border: 1px solid #7b5e43; padding: 30px; background-color: #3d2b1f; margin-top: 25px; box-shadow: 10px 10px 20px rgba(0,0,0,0.5);">
            <p style="text-transform: uppercase; letter-spacing: 0.3em; font-size: 0.75rem; color: #a68b7c; margin-bottom: 8px;">The Avatar's Path</p>
            <h1 style="color: #e5d3b3; margin-top: 0; font-family: serif;">Ascendant: {display_deg:.2f}° {sign_name}</h1>
            <hr style="border: 0; border-top: 1px solid #7b5e43; margin: 20px 0;">
            <div style="color: #a68b7c; font-size: 0.9rem; line-height: 1.6;">
                <p><b>Scientific Standard:</b> Sidereal (Lahiri Ayanamsa)</p>
                <p><b>Horizon Logic:</b> Placidus System</p>
                <p><b>Celestial Moment:</b> {data['timezone']} (Automatic DST Correction)</p>
            </div>
            <p style="font-style: italic; color: #e5d3b3; margin-top: 20px; border-left: 2px solid #7b5e43; padding-left: 15px;">
                "Your blueprint is written in the language of the stars, poised between the Earth and the infinite."
            </p>
        </div>
    """, unsafe_allow_html=True)
