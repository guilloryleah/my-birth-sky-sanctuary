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

# 2. The Translator Function (Converting RA to Signs)
def get_sign(ra_hours):
    # This translates the 24 hours of the sky into the 12 signs
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    index = int(ra_hours / 2) % 12
    return signs[index]

# 3. Sidebar Inputs
with st.sidebar:
    st.header("Birth Details")
    b_date = st.date_input("Date of Birth", value=datetime(1970, 1, 1))
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
        
        bodies = {
            'Sun': eph['sun'], 'Moon': eph['moon'], 'Mars': eph['mars'],
            'Jupiter': eph['jupiter_barycenter'], 'Venus': eph['venus'], 
            'Saturn': eph['saturn_barycenter'], 'Mercury': eph['mercury']
        }

        # Displaying them as "Cards" for the client
        for name, body in bodies.items():
            astrometric = location.at(t).observe(body)
            ra, dec, distance = astrometric.radec()
            sign = get_sign(ra.hours)
            
            st.markdown(f"""
            <div class="client-card">
                <h2 style="margin:0;">{name}</h2>
                <p style="font-size: 1.2em; color: #ffca28;">Located in: <strong>{sign}</strong></p>
                <p style="font-size: 0.8em; opacity: 0.7;">Astronomical Coordinates: {ra.hours:.2f}h RA / {dec.degrees:.2f}° Dec</p>
            </div>
            """, unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Enter your details in the sidebar to generate your readable blueprint.")
