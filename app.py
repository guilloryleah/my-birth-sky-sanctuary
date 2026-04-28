import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime

# 1. Setup & Styling
st.set_page_config(page_title="My Birth Sky", layout="wide")

st.markdown(
    """
    <style>
    .main { 
        background-color: #004d40; 
        color: #ffffff; 
    }
    h1, h2, h3 { color: #ffca28 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    </style>
    """, 
    unsafe_allow_html=True
)

# 2. Header
st.title("✨ My Birth Sky")
st.subheader("High-Precision Astronomical Birth Map")
st.write("This map uses NASA JPL data to show the exact positions of the stars and planets at your moment of birth.")

# 3. User Inputs
with st.sidebar:
    st.header("Birth Details")
    birth_date = st.date_input("Date of Birth", value=datetime(1970, 1, 1))
    birth_time = st.time_input("Time of Birth", value=datetime.strptime("12:00", "%H:%M").time())
    lat = st.number_input("Latitude (e.g., 29.76 for Houston)", value=29.76)
    lon = st.number_input("Longitude (e.g., -95.36 for Houston)", value=-95.36)

# 4. Astronomical Calculations
try:
    ts = load.timescale()
    eph = load('de421.bsp')  # Standard NASA JPL ephemeris
    
    # Combine date and time
    dt = datetime.combine(birth_date, birth_time)
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    
    # Define location
    location = eph['earth'] + Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    st.write(f"### Results for {birth_date} at {birth_time}")
    
    # Calculate major points
    planets = {
        'Sun': eph['sun'],
        'Moon': eph['moon'],
        'Mars': eph['mars'],
        'Jupiter': eph['jupiter_barycenter'],
        'Venus': eph['venus'],
        'Saturn': eph['saturn_barycenter']
    }

    cols = st.columns(3)
    for i, (name, body) in enumerate(planets.items()):
        astrometric = location.at(t).observe(body)
        ra, dec, distance = astrometric.radec()
        
        with cols[i % 3]:
            st.metric(label=name, value=f"{ra.hours:.2f}h RA")
            st.write(f"Declination: {dec.degrees:.2f}°")

except Exception as e:
    st.error(f"Waiting for data: {e}")

st.write("---")
st.caption("Data provided by Skyfield and NASA JPL.")
