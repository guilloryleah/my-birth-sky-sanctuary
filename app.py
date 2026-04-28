import streamlit as st
from skyfield.api import load
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SANCTUARY CONFIG ---
st.set_page_config(page_title="My Birth Sky", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #004d40; color: #ffffff; }
    h1 { color: #ffca28; font-family: 'Playfair Display', serif; }
    .stButton>button { background-color: #ffca28; color: #004d40; border-radius: 20px; font-weight: bold; }
    .report-box { background-color: #00241f; padding: 20px; border-radius: 15px; border-left: 5px solid #ffca28; margin-bottom: 20px; }
    .poem-box { background-color: #001a17; padding: 30px; border-radius: 20px; border: 1px solid #ffca28; font-style: italic; text-align: center; margin: 20px 0; line-height: 1.6; }
    </style>
    """, unsafe_allow_name_with_html=True)

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
    
    # Calculation Engine
    sidereal_time = t.gmst + (lon / 15.0)
    asc_deg = (sidereal_time * 15 + 90) % 360 
    asc_s = get_sign(asc_deg)
    
    # Celestial Positions
    bodies = {'Sun': 'sun', 'Moon': 'moon', 'Mercury': 'mercury', 'Venus': 'venus', 'Mars': 'mars', 'Jupiter': 'jupiter_barycenter', 'Saturn': 'saturn_barycenter'}
    results = {}
    for name, key in bodies.items():
        p_pos = earth.at(t).observe(planets_data[key]).ecliptic_latlon()[1].degrees
        results[name] = {"deg": p_pos, "sign": get_sign(p_pos)}

    # Nodes
    rahu_s = get_sign((results['Moon']['deg'] + 45) % 360)
    ketu_s = get_sign((rahu_s_deg := (results['Moon']['deg'] + 45) % 360) + 180 % 360)

    # 1. Visualization
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#004d40')
    ax.set_facecolor('#00241f')
    ax.text(0, 0, wisdom[asc_s]['symbol'], color='#ffca28', fontsize=65, ha='center', va='center')
    
    for name, data in results.items():
        rad = np.deg2rad(data['deg'])
        ax.scatter(rad, 0.9, color='#ffca28', s=100)
        ax.text(rad, 1.1, name, color='white', fontsize=8, ha='center')

    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # 2. The Nodal Poem
    st.markdown(f"""
    <div class='poem-box'>
    <h3>A Song for {user_name}</h3>
    In the ancient halls of <b>{ketu_s}</b>, your wisdom was deep,<br>
    A treasure of silence you've chosen to keep.<br>
    But the dragon now turns toward <b>{rahu_s}</b>’s new light,<br>
    To wake up the spirit and dance in the white.<br>
    The Mountain is poised, the blueprint is clear,<br>
    The universe whispers: <i>You belong here.</i>
    </div>
    """, unsafe_allow_name_with_html=True)

    # 3. Integral Analysis
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🧘 Yoga")
        st.write(f"**Pose:** {wisdom[asc_s]['pose']}")
    with col2:
        st.subheader("🌿 Ritual")
        st.write(f"**Aroma:** {wisdom[results['Sun']['sign']]['aroma']}")
    with col3:
        st.subheader("🍲 Ayurveda")
        st.write(f"**Focus:** {wisdom[results['Moon']['sign']]['focus']}")
    
    st.balloons()
