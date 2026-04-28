import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime

# 1. Setup & Styling
st.set_page_config(page_title="My Birth Sky", layout="wide")

# Initialize "memory" so the results don't disappear
if 'generated' not in st.session_state:
    st.session_state.generated = False

st.markdown(
    """
    <style>
    .main { background-color: #004d40; color: #ffffff; }
    h1, h2, h3 { color: #ffca28 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; }
    .stButton>button {
        background-color: #ffca28;
        color: #004d40;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 2. Header
st.title("✨ My Birth Sky")
st.subheader("High-Precision Astronomical Birth Map")

# 3. User Inputs in Sidebar
with st.sidebar:
    st.header("Birth Details")
    birth_date = st.date_input("Date of Birth", value=datetime(1970, 1, 1))
    birth_time = st.time_input("Time of Birth", value=datetime.strptime("12:00", "%H:%M").time())
    lat = st.number_input("Latitude", value=29.76)
    lon = st.number_input("Longitude", value=-95.36)
    
    if st.button("Generate My Sky Map"):
        st.session_state.generated = True

# 4. Display Results
if st.session_state.generated:
    try:
        ts = load.timescale()
        eph = load('de421.bsp')
        
        dt = datetime.combine(birth_date, birth_time)
        t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        location = eph['earth'] + Topos(latitude_degrees=lat, longitude_degrees=lon)
        
        st.write(f"### Your Astronomical Blueprint: {birth_date}")
        
        planets = {
            'Sun': eph['sun'], 'Moon': eph['moon'], 'Mars': eph['mars'],
            'Jupiter': eph['jupiter_barycenter'], 'Venus': eph['venus'], 'Saturn': eph['saturn_barycenter']
        }

        cols = st.columns(3)
        for i, (name, body) in enumerate(planets.items()):
            astrometric = location.at(t).observe(body)
            ra, dec, distance = astrometric.radec()
            with cols[i % 3]:
                st.metric(label=name, value=f"{ra.hours:.2f}h RA")
                st.write(f"Declination: {dec.degrees:.2f}°")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    # This is the "Welcome" screen that shows until they hit the button
    st.info("👈 Enter your birth details in the sidebar and click the gold button to reveal your map!")
    st.write("---")
    st.write("### Why use astronomical data?")
    st.write("Standard systems use fixed dates, but the sky is always moving. This app uses NASA data to show you where the planets *actually* were when you took your first breath.")
