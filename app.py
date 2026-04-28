import streamlit as st
from skyfield.api import load
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SIMPLE CONFIG ---
st.set_page_config(page_title="My Birth Sky")

st.title("✨ Your Birth Sky Blueprint")
st.write("Welcome to your personal celestial sanctuary.")

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

# --- INPUTS ---
st.sidebar.header("The Soul's Coordinates")
user_name = st.sidebar.text_input("First Name", value="Matthew")
b_date = st.sidebar.date_input("Date of Birth", value=datetime(1969, 5, 22), min_value=datetime(1, 1, 1))
b_time = st.sidebar.time_input("Time of Birth", value=datetime.strptime("12:00", "%H:%M").time())
lat = st.sidebar.number_input("Latitude", value=29.76)
lon = st.sidebar.number_input("Longitude", value=-95.36)

if st.button("Generate My Blueprint"):
    with st.spinner("Consulting the stars..."):
        ts = load.timescale()
        t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
        planets_data = load('de421.bsp')
        earth = planets_data['earth']
        
        # Calc Ascendant
        sidereal_time = t.gmst + (lon / 15.0)
        asc_deg = (sidereal_time * 15 + 90) % 360 
        asc_s = get_sign(asc_deg)
        
        # Calc Nodes (Proxy)
        moon_pos = earth.at(t).observe(planets_data['moon']).ecliptic_latlon()[1].degrees
        rahu_s = get_sign((moon_pos + 45) % 360)
        ketu_s = get_sign((moon_pos + 225) % 360)

        # 1. Visualization
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
        ax.text(0, 0, wisdom[asc_s]['symbol'], fontsize=70, ha='center', va='center')
        ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        # 2. Output
        st.balloons()
        st.subheader(f"A Message for {user_name}")
        st.info(f"In **{ketu_s}** your roots were sown; in **{rahu_s}** your light is shown.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rising Sign", asc_s)
            st.write(f"🧘 **Yoga Pose:** {wisdom[asc_s]['pose']}")
        with col2:
            st.write(f"🌿 **Ritual Aroma:** {wisdom[asc_s]['aroma']}")
            st.write(f"🍲 **Body Focus:** {wisdom[asc_s]['focus']}")
