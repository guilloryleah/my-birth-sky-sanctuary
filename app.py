import streamlit as st
from skyfield.api import load
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SANCTUARY STYLE ---
st.set_page_config(page_title="My Birth Sky Sanctuary", layout="wide")

# This restores the deep emerald look without the error-prone CSS
st.title("🏔️ Your Birth Sky Sanctuary")
st.markdown("---")

# --- DATA: THE ANCIENT CORRESPONDENCES ---
wisdom = {
    "Aries": {"pose": "Warrior I", "aroma": "Peppermint", "focus": "Agni", "symbol": "🦅", "essence": "The Spark of Initiation"},
    "Taurus": {"pose": "Tree Pose", "aroma": "Rose", "focus": "Grounding", "symbol": "🌿", "essence": "The Sacred Earth"},
    "Gemini": {"pose": "Cobra", "aroma": "Lavender", "focus": "Nervous System", "symbol": "🌬️", "essence": "The Breath of Connection"},
    "Cancer": {"pose": "Child's Pose", "aroma": "Jasmine", "focus": "Lymphatic", "symbol": "🌊", "essence": "The Deep Waters"},
    "Leo": {"pose": "Lion's Breath", "aroma": "Orange", "focus": "Heart Center", "symbol": "🦁", "essence": "The Solar Heart"},
    "Virgo": {"pose": "Forward Fold", "aroma": "Eucalyptus", "focus": "Pitta Balance", "symbol": "🏔️", "essence": "The Pure Harvest"},
    "Libra": {"pose": "Dancer's Pose", "aroma": "Geranium", "focus": "Symmetry", "symbol": "💎", "essence": "The Harmonic Scale"},
    "Scorpio": {"pose": "Pigeon Pose", "aroma": "Patchouli", "focus": "Detox", "symbol": "🦂", "essence": "The Alchemical Fire"},
    "Sagittarius": {"pose": "Low Lunge", "aroma": "Sage", "focus": "Expansion", "symbol": "🏹", "essence": "The Truth-Seeker's Path"},
    "Capricorn": {"pose": "Mountain Pose", "aroma": "Vetiver", "focus": "Structure", "symbol": "🏛️", "essence": "The Eternal Foundation"},
    "Aquarius": {"pose": "Bridge Pose", "aroma": "Neroli", "focus": "Circulation", "symbol": "🌌", "essence": "The Collective Vision"},
    "Pisces": {"pose": "Savasana", "aroma": "Melissa", "focus": "Immune Rest", "symbol": "🕯️", "essence": "The Ocean of Oneness"}
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
    
    # CALCULATIONS
    sidereal_time = (t.gmst + (lon / 15.0)) % 24
    asc_deg = (sidereal_time * 15 + 90) % 360 
    asc_s = get_sign(asc_deg)
    
    bodies = {'Sun': 'sun', 'Moon': 'moon', 'Mars': 'mars', 'Jupiter': 'jupiter_barycenter', 'Saturn': 'saturn_barycenter', 'Venus': 'venus'}
    results = {}
    for name, key in bodies.items():
        deg = earth.at(t).observe(planets_data[key]).ecliptic_latlon()[1].degrees
        results[name] = {"deg": deg, "sign": get_sign(deg), "house": int((deg - asc_deg) % 360 / 30) + 1}

    # --- 1. THE SACRED CHART ---
    st.subheader("🌌 The Celestial Map")
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#00241f')
    ax.set_facecolor('#00241f')

    # Draw Zodiac Labels
    for i, sign in enumerate(zodiac_signs):
        angle = np.deg2rad(i * 30 + 15)
        ax.text(angle, 1.15, sign, color='#ffca28', ha='center', va='center', fontsize=10, fontweight='bold')
        ax.plot([np.deg2rad(i*30), np.deg2rad(i*30)], [0, 1], color='#ffca28', alpha=0.2)

    # Draw Planets
    for name, data in results.items():
        rad = np.deg2rad(data['deg'])
        ax.scatter(rad, 0.85, color='#ffffff', s=150, alpha=0.8, edgecolors='#ffca28')
        ax.text(rad, 0.7, name, color='white', ha='center', fontsize=9)

    # Center Symbol
    ax.text(0, 0, wisdom[asc_s]['symbol'], color='#ffca28', fontsize=75, ha='center', va='center')
    
    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # --- 2. DEEP SOULFUL ANALYSIS ---
    st.markdown("---")
    st.header(f"✨ The Wayfinder’s Manifesto for {user_name}")
    
    # Nodal Poem
    moon_deg = results['Moon']['deg']
    rahu_s = get_sign((moon_deg + 45) % 360)
    ketu_s = get_sign((moon_deg + 225) % 360)
    
    st.info(f"**The Dragon’s Path:** Your soul arrived with the deep, hidden echoes of **{ketu_s}**, carrying the wisdom of what has already been mastered. But your dharma—your growth—calls you toward the light of **{rahu_s}**. This is the journey from the familiar to the expansive.")

    # Core Pillars
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🧘 The Vital Body")
        st.write(f"**Ascendant:** {asc_s}")
        st.write(f"**Mantra:** {wisdom[asc_s]['essence']}")
        st.success(f"**Yoga:** {wisdom[asc_s]['pose']}")
    with c2:
        st.subheader("🌿 The Psychic Heart")
        sun_s = results['Sun']['sign']
        st.write(f"**Solar Essence:** {sun_s}")
        st.warning(f"**Ritual:** {wisdom[sun_s]['aroma']} aroma")
    with col3 if 'col3' in locals() else c3: # Fix for potential variable drift
        st.subheader("🍲 The Grounded Life")
        moon_s = results['Moon']['sign']
        st.write(f"**Lunar Mind:** {moon_s}")
        st.error(f"**Focus:** {wisdom[moon_s]['focus']}")

    # Deep Analysis Blocks
    st.markdown("### 🏛️ Planetary Placements")
    for planet, data in results.items():
        with st.expander(f"{planet} in {data['sign']} (House {data['house']})"):
            st.write(f"When **{planet}** moves through **{data['sign']}**, it flavors your {data['house']}th House. This suggests a need to integrate **{wisdom[data['sign']]['essence']}** into your daily rhythm.")

    st.balloons()
