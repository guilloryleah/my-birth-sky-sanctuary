import streamlit as st
from skyfield.api import load
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SANCTUARY STYLE ---
st.set_page_config(page_title="My Birth Sky Sanctuary", layout="wide")
st.markdown("<style>.main { background-color: #00241f; color: #ffffff; }</style>", unsafe_allow_html=True)
st.title("🏔️ The Wayfinder’s Master Blueprint")

# --- DATA: ZODIAC & NAKSHATRAS ---
zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# --- SIDEBAR ---
with st.sidebar:
    st.header("Soul Coordinates")
    user_name = st.text_input("Name", value="Leah")
    b_date = st.date_input("Date of Birth", value=datetime(1969, 9, 24))
    b_time = st.time_input("Time of Birth", value=datetime.strptime("22:59", "%H:%M").time(), step=60)
    lat = st.number_input("Latitude", value=29.76)
    lon = st.number_input("Longitude", value=-95.36)

def get_nakshatra(deg):
    idx = int(deg / (360/27)) % 27
    return nakshatras[idx]

def format_deg(deg):
    sign_deg = deg % 30
    minutes = int((sign_deg - int(sign_deg)) * 60)
    return f"{int(sign_deg)}° {minutes:02d}'"

if st.button("Generate My Master Blueprint"):
    ts = load.timescale()
    t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
    planets_data = load('de421.bsp')
    earth = planets_data['earth']
    
    # LAHIRI AYANAMSHA 
    lahiri_offset = 23.418 
    
    # ASCENDANT & HOUSES
    sidereal_time = (t.gmst + (lon / 15.0)) % 24
    asc_deg_s = ((sidereal_time * 15 + 90) - lahiri_offset) % 360
    asc_idx = int(asc_deg_s / 30) % 12
    asc_s = zodiac_signs[asc_idx]

    # PLANETS
    bodies = {'Sun': 'sun', 'Moon': 'moon', 'Mercury': 'mercury', 'Venus': 'venus', 'Mars': 'mars', 'Jupiter': 'jupiter_barycenter', 'Saturn': 'saturn_barycenter'}
    results = {}
    for name, key in bodies.items():
        pos = earth.at(t).observe(planets_data[key]).ecliptic_latlon()[1].degrees
        s_deg = (pos - lahiri_offset) % 360
        p_idx = int(s_deg / 30) % 12
        results[name] = {
            "deg": s_deg, "sign": zodiac_signs[p_idx], 
            "house": (p_idx - asc_idx) % 12 + 1,
            "nak": get_nakshatra(s_deg), "pos_str": format_deg(s_deg)
        }

    # NODES (Mean Proxy)
    moon_pos = results['Moon']['deg']
    rahu_deg = (moon_pos + 45) % 360 
    ketu_deg = (rahu_deg + 180) % 360
    for n, d in [('Rahu', rahu_deg), ('Ketu', ketu_deg)]:
        p_idx = int(d / 30) % 12
        results[n] = {"deg": d, "sign": zodiac_signs[p_idx], "house": (p_idx - asc_idx) % 12 + 1, "nak": get_nakshatra(d), "pos_str": format_deg(d)}

    # --- THE CHART ---
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#00241f'); ax.set_facecolor('#00241f')
    rot = np.deg2rad(asc_idx * 30)
    for i, sign in enumerate(zodiac_signs):
        angle = np.deg2rad(i * 30 + 15) - rot
        ax.text(angle, 1.15, sign, color='#ffca28', fontweight='bold', ha='center')
        ax.plot([np.deg2rad(i*30)-rot, np.deg2rad(i*30)-rot], [0, 1], color='#ffca28', alpha=0.2)
    ax.plot([np.pi, 0], [1, 1], color='#ffca28', linewidth=4)
    for name, d in results.items():
        rad = np.deg2rad(d['deg']) - rot
        ax.scatter(rad, 0.85, color='#ffffff', s=120, edgecolors='#ffca28')
    st.pyplot(fig)

    # --- THE SOULFUL READING ---
    st.header(f"✨ The Sanctuary Reading for {user_name}")
    st.subheader(f"Ascendant in {asc_s} ({format_deg(asc_deg_s)})")
    st.write(f"Your path is anchored in **{asc_s}**, the sign of the Sacred Earth. Your 1st House provides the stability of a mountain, allowing you to build a life of enduring beauty and integrity.")

    st.markdown("---")
    cols = st.columns(2)
    for i, (planet, data) in enumerate(results.items()):
        with cols[i % 2]:
            st.markdown(f"### {planet} in {data['sign']}")
            st.write
