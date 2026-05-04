import streamlit as st
import swisseph as swe
import datetime

# --- ASTRONOMICAL ENGINE ---
def get_accurate_ascendant(jd_utc, lat, lon):
    # Strictly follow the Lahiri system (Chitra Paksha)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    # Calculate using Placidus ('P') in Sidereal mode
    cusps, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P', swe.FLG_SIDEREAL)
    return ascmc[0]  # This is the exact Ascendant degree

# --- MODERN STUDIO INTERFACE ---
st.set_page_config(page_title="The Sidereal Sanctuary")

# Styling for Warm Oak and Chocolate accents
st.markdown("""
    <style>
    .stApp { background-color: #2b1d16; color: #e5d3b3; }
    .stButton>button { border-radius: 0px; border: 1px solid #7b5e43; color: #7b5e43; }
    </style>
    """, unsafe_allow_html=True)

st.title("The Celestial Blueprint")
st.write("A scientifically grounded view of your birth sky.")

# Input Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Birth Date", value=datetime.date(1957, 5, 22))
    with col2:
        time = st.time_input("Birth Time", value=datetime.time(4, 10))
    
    lat = st.number_input("Latitude", value=41.8781, format="%.4f")
    lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
    tz = st.number_input("Timezone Offset (UTC)", value=-5.0) # Chicago 1957 CDT was UTC-5

if st.button("Cast the Chart"):
    # Convert to UTC Julian Day
    decimal_hour = (time.hour + time.minute/60.0) - tz
    jd_utc = swe.julday(date.year, date.month, date.day, decimal_hour)
    
    asc_deg = get_accurate_ascendant(jd_utc, lat, lon)
    
    # Visual Output
    st.markdown(f"""
        <div style="border: 1px solid #7b5e43; padding: 20px; background-color: #3d2b1f;">
            <p style="text-transform: uppercase; letter-spacing: 0.2em; font-size: 0.8rem; color: #a68b7c;">The Avatar's Path</p>
            <h2 style="color: #e5d3b3;">Ascendant Degree: {asc_deg:.2f}°</h2>
            <p style="font-style: italic; color: #a68b7c;">Calculated via Lahiri Ayanamsa & Placidus Horizon</p>
        </div>
    """, unsafe_allow_html=True)
