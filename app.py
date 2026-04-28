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
    # Using 10:59 PM (22:59) as the default
    b_date = st.date_input("Date of Birth", value=datetime(1975, 1, 1))
    b_time = st.time_input("Time of Birth", value=datetime.strptime("22:59", "%H:%M").time(), step=60)
    lat = st.number_input("Latitude", value=29.76)
    lon = st.number_input("Longitude", value=-95.36)

if st.button("Generate My Blueprint"):
    ts = load.timescale()
    t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
    planets_data = load('de421.bsp')
    earth = planets_data['earth']
    
    # 1. PURE ASTRONOMY CALCULATIONS (No Ayanamsha)
    sidereal_time = (t.gmst + (lon / 15.0)) % 24
    asc_deg = (sidereal_time * 15 + 90) % 360 
    
    bodies = {'Sun': 'sun', 'Moon': 'moon', 'Mars': 'mars', 'Jupiter': 'jupiter_barycenter'}
    results = {}
    for name, key in bodies.items():
        deg = earth.at(t).observe(planets_data[key]).ecliptic_latlon()[1].degrees
        results[name] = {"deg": deg, "sign": get_sign(deg)}

    # 2. THE SACRED CHART (Rotated to Ascendant)
    st.subheader("🌌 The Celestial Map")
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#fdfcf0') # Creamy sanctuary background
    
    # Rotate the wheel so Ascendant is at 180 degrees (Left/West in Polar, but visually East/Left)
    rotation_offset = np.deg2rad(asc_deg)
    
    # Draw Zodiac Labels
    for i, sign in enumerate(zodiac_signs):
        angle = np.deg2rad(i * 30 + 15) - rotation_offset
        ax.text(angle, 1.1, sign, color='#4a4a4a', ha='center', va='center', fontsize=9, fontweight='bold')
        ax.plot([np.deg2rad(i*30)-rotation_offset, np.deg2rad(i*30)-rotation_offset], [0, 1], color='#4a4a4a', alpha=0.1)

    # Draw Ascendant Line (The Horizontal Horizon)
    ax.plot([np.pi, 0], [1, 1], color='#b8860b', linewidth=3, label="ASC")
    ax.text(np.pi, 1.2, "ASCENDANT", color='#b8860b', fontweight='bold', ha='right')

    # Draw Planets
    for name, data in results.items():
        rad = np.deg2rad(data['deg']) - rotation_offset
        ax.scatter(rad, 0.8, color='#004d40', s=150, zorder=5)
        ax.text(rad, 0.65, name, ha='center', fontsize=8)

    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # 3. THE NODAL MANIFESTO (THE POEM)
    st.markdown("---")
    moon_deg = results['Moon']['deg']
    rahu_s = get_sign((moon_deg + 45) % 360)
    ketu_s = get_sign((moon_deg + 225) % 360)
    
    st.header(f"✨ The Wayfinder’s Manifesto")
    st.subheader(f"A Song for {user_name}")
    
    # The Poem
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
    
    st.balloons()
