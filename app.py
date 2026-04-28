import streamlit as st
from skyfield.api import load
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SANCTUARY CONFIG ---
st.set_page_config(page_title="My Birth Sky", layout="wide")

# Simplified Style to prevent TypeErrors
st.markdown("<style>.main { background-color: #004d40; color: #ffffff; }</style>", unsafe_allow_name_with_html=True)
st.markdown("<style>h1 { color: #ffca28; font-family: 'serif'; }</style>", unsafe_allow_name_with_html=True)

st.title("✨ Your Birth Sky Blueprint")

# --- WISDOM MAPPING ---
wisdom = {
    "Aries": {"pose": "Warrior I", "aroma": "Peppermint", "focus": "Agni", "symbol": "🦅"},
    "Taurus": {"pose": "Tree Pose", "aroma": "Rose", "focus": "Grounding", "symbol": "🌿"},
    "Gemini": {"pose": "Cobra", "aroma": "Lavender", "focus": "Nervous System", "symbol": "🌬️"},
    "Cancer": {"pose": "Child's Pose", "aroma": "Jasmine", "focus": "Lymphatic", "symbol": "🌊"},
    "Leo": {"pose": "Lion's Breath", "aroma": "Orange", "focus": "Heart Center", "symbol": "🦁"},
    "Virgo": {"pose": "Forward Fold", "aroma": "Eucalyptus", "focus": "Pitta Balance", "symbol": "🏔️"},
    "Libra": {"pose": "Dancer's Pose", "aroma": "Geranium", "focus": "Symmetry", "symbol": "💎"},
    "Scorpio": {"pose": "Pigeon Pose", "aroma": "Patchouli", "focus": "Detox", "symbol": "🦂"},
    "Sagittarius": {"pose": "Low Lunge", "aroma": "Sage", "focus": "Expansion", "symbol": "🏹"},
    "Capricorn": {"pose": "Mountain Pose", "aroma": "Vetiver", "focus": "Structure", "symbol": "🏛️"},
    "Aquarius": {"pose": "Bridge Pose", "aroma": "Neroli", "focus": "Circulation", "symbol": "🌌"},
    "Pisces": {"pose": "Savasana", "aroma": "Melissa", "focus": "Immune Rest", "symbol": "🕯️"}
}

def get_sign(deg):
    z = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return z[int(deg / 30) % 12]

# --- SIDEBAR ---
with st.sidebar:
    st.header("The Soul's Coordinates")
    user_name = st.text_input("First Name", value="Matthew")
    b_date = st.date_input("Date of Birth", value=datetime(1969, 5, 22), min_value=datetime(1, 1, 1))
    b_time = st.time_input("Time of Birth", value=datetime.strptime("12:00", "%H:%M").time())
    lat = st.number_input("Latitude", value=29.76)
    lon = st.number_input("Longitude", value=-95.36)

if st.button("Generate My Blueprint"):
    ts = load.timescale()
    t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
    planets_data = load('de421.bsp')
    earth = planets_data['earth']
    
    # Calc Ascendant
    sidereal_time = t.gmst + (lon / 15.0)
    asc_deg = (sidereal_time * 15 + 90) % 360 
    asc_s = get_sign(asc_deg)
    
    # Calc Positions
    sun_pos = earth.at(t).observe(planets_data['sun']).ecliptic_latlon()[1].degrees
    moon_pos = earth.at(t).observe(planets_data['moon']).ecliptic_latlon()[1].degrees
    
    sun_s = get_sign(sun_pos)
    moon_s = get_sign(moon_pos)
    rahu_s = get_sign((moon_pos + 45) % 360)
    ketu_s = get_sign((moon_pos + 225) % 360)

    # 1. Visualization
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#004d40')
    ax.set_facecolor('#00241f')
    ax.text(0, 0, wisdom[asc_s]['symbol'], color='#ffca28', fontsize=65, ha='center', va='center')
    
    # Planet dots
    for deg, label in [(sun_pos, 'Sun'), (moon_pos, 'Moon')]:
        rad = np.deg2rad(deg)
        ax.scatter(rad, 0.9, color='#ffca28', s=100)
        ax.text(rad, 1.1, label, color='white', fontsize=8, ha='center')

    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # 2. Output
    st.balloons()
    st.markdown(f"### Hi {user_name},")
    st.write(f"**Your Ascendant Rising:** {asc_s} {wisdom[asc_s]['symbol']}")
    
    st.markdown(f"**The Nodal Song:** In {ketu_s} your roots were sown; in {rahu_s} your light is shown.")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"🧘 **Yoga:** {wisdom[asc_s]['pose']}")
        st.write(f"🌿 **Aroma:** {wisdom[sun_s]['aroma']}")
    with c2:
        st.write(f"🍲 **Ayurveda:** {wisdom[moon_s]['focus']}")
