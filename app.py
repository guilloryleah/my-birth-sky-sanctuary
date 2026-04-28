import streamlit as st
from skyfield.api import load, wgs84
from skyfield.data import constellations
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# 1. SETUP & DATA LOADING
st.set_page_config(page_title="Sky Sanctuary", layout="wide")
st.title("🔭 The Wayfinder’s Master Blueprint")

@st.cache_resource
def get_data():
    # Downloads the necessary NASA/JPL planetary data
    eph = load('de421.bsp')
    const = constellations.load_atliau()
    return eph, const

try:
    planets_data, load_constellation = get_data()
    ts = load.timescale()
    earth = planets_data['earth']
except Exception as e:
    st.error(f"Data loading error: {e}")
    st.stop()

# 2. ZODIAC & NAKSHATRAS
zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

def get_nak(deg): return nakshatras[int(deg / (360/27)) % 27]
def fmt_deg(deg): return f"{int(deg % 30)}° {int((deg % 30 - int(deg % 30)) * 60):02d}'"

# 3. USER INPUTS
with st.sidebar:
    st.header("Soul Coordinates")
    user_name = st.text_input("Name", value="Leah")
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    lat, lon = 29.76, -95.36 # Houston

if st.button("Generate Master Blueprint"):
    t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
    # Lahiri Ayanamsha for 1969
    lahiri_ayan = 23.418
    
    # TAURUS ASCENDANT ANCHOR
    asc_sign_idx = 1 
    
    bodies = {'Sun': 'sun', 'Moon': 'moon', 'Mercury': 'mercury', 'Venus': 'venus', 
              'Mars': 'mars', 'Jupiter': 'jupiter_barycenter', 'Saturn': 'saturn_barycenter'}
    
    results = {}
    for name, key in bodies.items():
        astrometric = earth.at(t).observe(planets_data[key])
        const_name = load_constellation(astrometric)
        raw_deg = astrometric.ecliptic_latlon()[1].degrees
        sidereal_deg = (raw_deg - lahiri_ayan) % 360
        p_idx = int(sidereal_deg / 30) % 12
        results[name] = {
            "Constellation": const_name,
            "Position": fmt_deg(sidereal_deg),
            "Nakshatra": get_nak(sidereal_deg),
            "RawDeg": sidereal_deg,
            "Sign": zodiac_signs[p_idx],
            "House": (p_idx - asc_sign_idx) % 12 + 1
        }

    # 4. CHART VISUAL
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#00241f')
    ax.set_facecolor('#00241f')
    
    rot = np.deg2rad(asc_sign_idx * 30)
    for i, sign in enumerate(zodiac_signs):
        angle = np.deg2rad(i * 30 + 15) - rot
        ax.text(angle, 1.15, sign, color='#ffca28', fontweight='bold', ha='center')
        ax.plot([np.deg2rad(i*30)-rot, np.deg2rad(i*30)-rot], [0, 1], color='#ffca28', alpha=0.2)
    
    ax.plot([np.pi, 0], [1, 1], color='#ffca28', linewidth=4) 
    ax.text(np.pi, 1.25, "ASC: TAURUS", color='#ffca28', fontweight='bold', ha='right')

    for name, data in results.items():
        rad = np.deg2rad(data['RawDeg']) - rot
        ax.scatter(rad, 0.85, color='white', s=150, edgecolors='#ffca28')
        # LABELS
        ax.text(rad, 0.73, name, color='white', fontsize=10, fontweight='bold', ha='center')

    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # 5. ANALYSIS
    st.header(f"✨ Sanctuary Reading: {user_name}")
    for planet, d in results.items():
        with st.expander(f"{planet} in {d['Constellation']} ({d['Position']})"):
            st.write(f"**House {d['House']}** | **Nakshatra:** {d['Nakshatra']}")
