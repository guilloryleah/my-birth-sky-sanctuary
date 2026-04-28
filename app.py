import streamlit as st
from skyfield.api import load, Topos
from datetime import datetime

# 1. Page Setup
st.set_page_config(page_title="My Birth Sky", layout="wide")

# 2. Force the background and text colors
st.markdown(
    """
    <style>
    .stApp {
        background-color: #004d40;
        color: #ffffff;
    }
    h1, h2, h3, [data-testid="stMetricValue"] {
        color: #ffca28 !important;
    }
    .stMarkdown, p, label {
        color: #ffffff !important;
    }
    div.stButton > button {
        background-color: #ffca28 !important;
        color: #004d40 !important;
        font-weight: bold;
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 3. Sidebar Inputs
with st.sidebar:
    st.header("Birth Details")
    b_date = st.date_input("Date of Birth", value=datetime(1970, 1, 1))
    b_time = st.time_input("Time of Birth", value=datetime.strptime("12:00", "%H:%M").time())
    lat = st.number_input("Latitude (e.g. 29.76)", value=29.76)
    lon = st.number_input("Longitude (e.g. -95.36)", value=-95.36)
    
    # We use a direct "if" check for the button here
    generate = st.button("✨ Reveal My Birth Sky")

# 4. Main Display
st.title("✨ My Birth Sky")

if generate:
    try:
        with st.spinner("Consulting NASA JPL Data..."):
            # Load timescale and ephemeris (The NASA Data)
            ts = load.timescale()
            # This line handles the download if the file is missing
            eph = load('de421.bsp')
            
            # Create the specific moment in time
            dt = datetime.combine(b_date, b_time)
            t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)
            
            # Set the observer's location
            location = eph['earth'] + Topos(latitude_degrees=lat, longitude_degrees=lon)
            
            st.write(f"## Your Astronomical Blueprint")
            st.write(f"Positions for **{b_date}** at **{b_time}**")
            
            # Planets to track
            bodies = {
                'Sun': eph['sun'], 'Moon': eph['moon'], 'Mars': eph['mars'],
                'Jupiter': eph['jupiter_barycenter'], 'Venus': eph['venus'], 
                'Saturn': eph['saturn_barycenter'], 'Mercury': eph['mercury']
            }

            # Create columns for the results
            cols = st.columns(3)
            for i, (name, body) in enumerate(bodies.items()):
                astrometric = location.at(t).observe(body)
                ra, dec, distance = astrometric.radec()
                
                with cols[i % 3]:
                    st.metric(label=name, value=f"{ra.hours:.2f}h RA")
                    st.caption(f"Declination: {dec.degrees:.2f}°")
                    
    except Exception as e:
        st.error(f"Something went wrong: {e}")
else:
    # This is the "Welcome" screen
    st.info("Everything is ready! Just enter your details in the sidebar and click the button to see your sky.")
    st.write("---")
    st.markdown("""
    ### About this Blueprint
    Unlike traditional systems, this app uses the **Skyfield** library and **NASA JPL** data to calculate exactly where the planets were relative to the stars. 
    - **RA (Right Ascension):** The longitude of the sky.
    - **Declination:** The latitude of the sky.
    """)
