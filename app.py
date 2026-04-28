import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime

# 1. Page Setup & Styling
st.set_page_config(page_title="My Birth Sky", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #004d40; color: #ffffff; }
    h1, h2, h3, [data-testid="stMetricValue"] { color: #ffca28 !important; }
    .stMarkdown, p, label { color: #ffffff !important; }
    div.stButton > button {
        background-color: #ffca28 !important;
        color: #004d40 !important;
        font-weight: bold;
        width: 100%;
        border-radius: 10px;
    }
    .client-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ffca28;
        margin-bottom: 20px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 2. The Translator Function (Sidereal/Astronomical Alignment)
def get_astronomical_sign(ra_hours):
    # 1 hour RA = 15 degrees. 
    total_degrees = ra_hours * 15
    
    # Apply Ayanamsha shift (approx 24 degrees) to get the REAL star positions
    # This ensures April 28 shows as Aries, not Taurus.
    sidereal_degrees = (total_degrees - 24.0) % 360
    
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    sign_index = int(sidereal_degrees / 30)
    degree_in_sign = sidereal_degrees % 30
    return signs[sign_index], degree_in_sign

# 3. Sidebar Inputs
with st.sidebar:
    st.header("Birth Details")
    b_date = st.date_input("Date of Birth", value=datetime.now())
    b_time = st.time_input("Time of Birth", value=datetime.strptime("12:00", "%H:%M").time())
    lat = st.number_input("Latitude", value=29.76)
    lon = st.number_input("Longitude", value=-95.36)
    generate = st.button("✨ Reveal My Birth Sky")

# 4. Main Display
st.title("✨ My Birth Sky")

if generate:
    try:
        ts = load.timescale()
        eph = load('de421.bsp')
        dt = datetime.combine(b_date, b_time)
        t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        location = eph['earth'] + Topos(latitude_degrees=lat, longitude_degrees=lon)
        
        st.write(f"## Your Astronomical Blueprint")
        st.write(f"Actual Star Positions for {b_date}")
        
        bodies = {
            'Sun': eph['sun'], 'Moon': eph['moon'], 'Mars': eph['mars'],
            'Jupiter': eph['jupiter_barycenter'], 'Venus': eph['venus'], 
            'Saturn': eph['saturn_barycenter'], 'Mercury': eph['mercury']
        }

        # Create 3 columns for a cleaner look
        cols = st.columns(3)
        for i, (name, body) in enumerate(bodies.items()):
            astrometric = location.at(t).observe(body)
            ra, dec, dist = astrometric.radec()
            
            # Use our new translation function
            sign_name, sign_degree = get_astronomical_sign(ra.hours)
            
            with cols[i % 3]:
                st.markdown(f"""
