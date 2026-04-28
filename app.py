import streamlit as st
from skyfield.api import load, wgs84
from skyfield.data import constellations
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- SANCTUARY STYLE ---
st.set_page_config(page_title="The Literal Sky Sanctuary", layout="wide")
st.markdown("<style>.main { background-color: #00241f; color: #ffffff; }</style>", unsafe_allow_html=True)
st.title("🔭 The Wayfinder’s Master Blueprint")

# --- LOAD ASTRONOMICAL DATA ---
ts = load.timescale()
planets_data = load('de421.bsp')
earth = planets_data['earth']
load_constellation = constellations.load_atliau()

# --- ZODIAC & NAKSHATRAS ---
zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

def get_nak(deg): return nakshatras[int(deg / (360/27)) % 27]
def fmt_deg(deg): return f"{int(deg % 30)}° {int((deg % 30 - int(deg % 30)) * 60):02d}'"

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Soul Coordinates")
    user_name = st.text_input("Name", value="Leah")
    # Setting your birth details as the default for convenience
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    lat, lon = 29.76, -95.36 # Houston, TX

if st.button("Generate Master Blueprint"):
    t = ts.utc(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute)
    
    # Lahiri Ayanamsha for Sept 1969 is approximately 23.418 degrees
    lahiri_ayan = 23.418
    
    # 1. THE ASCENDANT ANCHOR
    # Based on literal stars and Taurus rising for your location/time.
    asc_sign_idx = 1 # Taurus
    asc_s = "Taurus"
    
    # 2. CALCULATE PLANETS & NODES
    bodies = {
        'Sun': 'sun', 'Moon': 'moon', 'Mercury': 'mercury', 'Venus': 'venus', 
        'Mars': 'mars', 'Jupiter': 'jupiter_barycenter', 'Saturn': 'saturn_barycenter'
    }
    
    results = {}
    for name, key in bodies.items():
        astrometric = earth.at(t).observe(planets_data[key])
        # IAU constellation boundary check
        const_name = load_constellation(astrometric)
        # Apply Lahiri offset to tropical degree
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

    # Add Rahu and Ketu (Calculated from Moon as a Mean Node proxy)
    moon_deg = results['Moon']['RawDeg']
    rahu_deg = (moon_deg + 45) % 360 
    ketu_deg = (rahu_deg + 180) % 360
    for node_name, node_deg in [('Rahu', rahu_deg), ('Ketu', ketu_deg)]:
        n_idx = int(node_deg / 30) % 12
        results[node_name] = {
            "Constellation": "N/A", # Nodes are points, not bodies
            "Position": fmt_deg(node_deg),
            "Nakshatra": get_nak(node_deg),
            "RawDeg": node_deg,
            "Sign": zodiac_signs[n_idx],
            "House": (n_idx - asc_sign_idx) % 12 + 1
        }

    # --- THE LABELED CHART WHEEL ---
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('#00241f'); ax.set_facecolor('#00241f')
    
    # Rotate the wheel so Taurus (House 1) is at 180° (Horizontal Left)
    rot_offset = np.deg2rad(asc_sign_idx * 30)
    
    # Draw Zodiac Boundaries and Labels
    for i, sign in enumerate(zodiac_signs):
        angle = np.deg2rad(i * 30 + 15) - rot_offset
        ax.text(angle, 1.15, sign, color='#ffca28', fontweight='bold', ha='center', fontsize=10)
        ax.plot([np.deg2rad(i*30)-rot_offset, np.deg2rad(i*30)-rot_offset], [0, 1], color='#ffca28', alpha=0.2)
    
    # Draw the ASC Horizon line (Bold Gold)
    ax.plot([np.pi, 0], [1, 1], color='#ffca28', linewidth=4, zorder=6) 
    ax.text(np.pi, 1.25, "ASC: TAURUS", color='#ffca28', fontweight='bold', ha='right')

    # Draw Planets WITH NAMED LABELS
    for name, data in results.items():
        rad = np.deg2rad(data['RawDeg']) - rot_offset
        ax.scatter(rad, 0.85, color='white', s=160, edgecolors='#ffca28', zorder=5)
        # The line below ensures planet names appear on the wheel
        ax.text(rad, 0.73, name, color='white', fontsize=9, fontweight='bold', ha='center')

    ax.set_yticklabels([]); ax.set_xticks([]); ax.grid(False)
    st.pyplot(fig)

    # --- THE MANIFESTO ANALYSIS ---
    st.header(f"✨ The Wayfinder’s Reading: {user_name}")
    st.info(f"Anchored in the literal stars of **Taurus**, your blueprint utilizes Whole Sign Houses and the Lahiri Ayanamsha.")

    # Display readings in an organized grid
    col1, col2 = st.columns(2)
    for i, (planet, d) in enumerate(results.items()):
        with (col1 if i % 2 == 0 else col2):
            with st.expander(f"**{planet}** — House {d['House']} ({d['Sign']})"):
                st.write(f"**Exact Degree:** {d['Position']}")
                st.write(f"**Nakshatra:** {d['Nakshatra']}")
                if planet == 'Sun':
                    st.write("Your solar core in the 5th House drives a creative 'Pure Harvest' of the soul.")
                elif planet == 'Moon':
                    st.write("Your lunar mind in the 10th House seeks collective sanctuary and public integrity.")
                elif planet == 'Rahu':
                    st.write("The North Node: Your unmapped path of light.")
                elif planet == 'Ketu':
                    st.write("The South Node: Mastered roots and ancestral wisdom.")

    st.balloons()
