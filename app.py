import streamlit as st
from skyfield.api import load
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SANCTUARY STYLE ---
st.set_page_config(page_title="My Birth Sky Sanctuary", layout="wide")
st.title("🏔️ Your Birth Sky Sanctuary")

# --- DATA: THE ANCIENT CORRESPONDENCES ---
wisdom = {
    "Aries": {"symbol": "🦅", "essence": "Initiation"},
    "Taurus": {"symbol": "🌿", "essence": "Sacred Earth"},
    "Gemini": {"symbol": "🌬️", "essence": "Connection"},
    "Cancer": {"symbol": "🌊", "essence": "Deep Waters"},
    "Leo": {"symbol": "🦁", "essence": "Solar Heart"},
    "Virgo": {"symbol": "🏔️", "essence": "Pure Harvest"},
    "Libra": {"symbol": "💎", "essence": "Harmony"},
    "Scorpio": {"symbol": "🦂", "essence": "Alchemy"},
    "Sagittarius": {"symbol": "🏹", "essence": "Truth-Seeking"},
    "Capricorn": {"symbol": "🏛️", "essence": "Foundation"},
    "Aquarius": {"symbol": "🌌", "essence": "Vision"},
    "Pisces": {"symbol": "🕯️", "essence": "Oneness"}
}

zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def get_sign(deg):
    return zodiac_signs[int(deg / 30) % 12]

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("The Soul's Coordinates")
    user_name = st.text_input("Name", value="Leah")
    b_date = st.date_input("Date of Birth", value=datetime(1975, 1, 1))
    b_time = st.time_input("Time of Birth", value=datetime.strptime("22:59", "%H:%M").time(), step=60)
    lat = st.number_input("Latitude", value=29.76)
    lon = st.number_input("Longitude", value=-95.36)

if st.button("Generate My Blueprint"):
    ts = load.timescale()
    t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
    planets_data = load('de421.bsp')
    earth = planets_data['earth']
    
    # 1. LAHIRI AYANAMSHA CALCULATION
    # The offset for Lahiri is roughly 24.2 degrees for the 1970s
    lahiri_offset = 24.23 + (0.013 * (b_date.year - 1950))
    
    sidereal_time = (t.gmst + (lon / 15.0)) % 24
    # Calculate Ascendant and shift it to Sidereal/Lahiri
    asc_deg_tropical = (sidereal_time * 15 + 90) % 360 
    asc_deg = (asc_deg_tropical - lahiri_offset) % 360
    asc_s = get_sign(asc_deg)
    
    bodies = {'Sun': 'sun', 'Moon': 'moon', 'Mars': 'mars', 'Jupiter': 'jupiter_barycenter', 'Venus': 'venus', 'Saturn': 'saturn_barycenter'}
    results = {}
    for name, key in bodies.items():
        # Get Tropical deg, then subtract Lahiri offset
        deg_tropical = earth.at(t).observe(planets_data[key]).ecliptic_latlon()[1].degrees
        deg_sidereal = (deg_tropical - lahiri_offset) % 360
        results[name] = {"deg": deg_sidereal, "sign": get_sign(deg_sidereal)}

    # 2. THE SACRED CHART (Rotated to Ascendant)
    st.subheader("🌌 The Celestial Map (Lahiri Sidereal)")
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#00241f') 
    ax.set_facecolor('#00241f')

    rotation_offset = np.deg2rad(asc_deg)
    
    # Draw Zodiac Labels
    for i, sign in enumerate(zodiac_signs):
        angle = np.deg2rad(i * 30 + 15) - rotation_offset
        ax.text(angle, 1.15, sign, color='#ffca28', ha='center', va='center', fontsize=10, fontweight='bold')
        ax.plot([np.deg2rad(i*30)-rotation_offset, np.deg2rad(i*30)-rotation_offset], [0, 1], color='#ffca28', alpha=0.2)

    # Draw Ascendant Line (The 9 o'clock Position)
    ax.plot([np.pi, 0], [1, 1], color='#ffca28', linewidth=4)
    ax.text(np.pi, 1.25, "ASCENDANT", color='#ffca28', fontweight='bold', ha='right')

    # Draw Planets
    for name, data in results.items():
        rad = np.deg2rad(data['deg']) - rotation_offset
        ax.scatter(rad, 0.85, color='#ffffff', s=200, edgecolors='#ffca28', zorder=5)
        ax.text(rad, 0.7, name, color='white', ha='center', fontsize=9)

    # Center Symbol
    ax.text(0, 0, wisdom[asc_s]['symbol'], color='#ffca28', fontsize=70, ha='center', va='center')
    
    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # 3. THE MANIFESTO & POEM
    st.markdown("---")
    st.header(f"✨ The Wayfinder’s Manifesto")
    st.subheader(f"A Song for {user_name}")
    
    moon_deg = results['Moon']['deg']
    rahu_s = get_sign((moon_deg + 45) % 360)
    ketu_s = get_sign((moon_deg + 225) % 360)

    poem = f"""
    > In **{ketu_s}** your roots were sown,  
    > In the deep, dark soil of what is known.  
    > An ancient echo, a silent quest,  
    > You carry the wisdom of the West.  
    >  
    > But look to **{rahu_s}**, where the light is shown,  
    > A path of spirit yet unmapped, unknown.  
    > From the master’s root to the seeker’s flower,  
    > This is your dharma, your sovereign hour.
    """
    st.markdown(poem)
    
    # Core Analysis
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Ascendant:** {asc_s} {wisdom[asc_s]['symbol']}")
        st.write(f"**Essence:** {wisdom[asc_s]['essence']}")
    with c2:
        sun_s = results['Sun']['sign']
        st.success(f"**Sun Sign:** {sun_s} {wisdom[sun_s]['symbol']}")
        st.write(f"**Soul Focus:** {wisdom[sun_s]['essence']}")

    st.balloons()
