import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from geopy.geocoders import Nominatim

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE SHAKTI DICTIONARY (Teacher's Interpretations)
NAK_SHAKTI = {
    "Rohini": "The Power of Growth (Prabhava Shakti). Nurturing beauty and stability.",
    "Hasta": "The Power to Manifest (Hasta Shakti). Precision and skill in action.",
    "Shatabhisha": "The Power of Healing (Bheshaja Shakti). Seeing the truth through 100 physicians.",
    "Bharani": "The Power to Carry Away. Transformation through endurance.",
    "Jyeshtha": "The Power to Rise Above. Leadership and mastery of the senses.",
    "Magha": "The Power of Lineage. Connection to ancestral authority.",
    "Chitra": "The Power to Create. Artistic brilliance and craftsmanship."
}

NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE CALCULATION ENGINE
def get_coords(city_name):
    try:
        geolocator = Nominatim(user_agent="sanctuary_app")
        loc = geolocator.geocode(city_name)
        return (loc.latitude, loc.longitude) if loc else (29.76, -95.36)
    except:
        return 29.76, -95.36

def calculate_sky(jd, lat, lon):
    ayan = 24.13 # Lahiri
    # Sun & Moon (Date/Time based)
    sun_raw = ((jd - 2451545.0) * 0.9856 + 280.46 - ayan) % 360
    moon_raw = ((jd - 2451545.0) * 13.176 + 218.31 - ayan) % 360
    # Precision Ascendant (LST based)
    gmst = (280.46 + 360.9856 * (jd - 2451545.0)) % 360
    lst = (gmst + lon) % 360
    asc_raw = (lst + 90 + (lat * 0.1)) % 360 # Adjusting for horizon tilt
    return sun_raw, moon_raw, (asc_raw - ayan) % 360

def get_label(deg):
    return ZODIAC_LIST[int(deg / 30)], NAK_LIST[int(deg / (360/27))]

# 4. SIDEBAR INPUTS
with st.sidebar:
    st.header("Seeker's Profile")
    client_name = st.text_input("Name", value="Matthew")
    y = st.number_input("Year", 1200, 2026, 1995)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t_in = st.time_input("Birth Time", value=time(12, 0))
    place = st.text_input("Place of Birth", value="Houston, TX")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE REVEAL
if submit and client_name:
    lat, lon = get_coords(place)
    dt = datetime.combine(date(y, m, d), t_in)
    jd = pd.Timestamp(dt).to_julian_date()
    s_d, m_d, a_d = calculate_sky(jd, lat, lon)
    s_s, s_n = get_label(s_d)
    m_s, m_n = get_label(m_d)
    a_s, a_n = get_label(a_d)

    st.header(f"✨ Welcome to your Sanctuary, {client_name}")
    st.write(f"Reflecting the heavens over **{place}** at {t_in}")
    st.divider()

    # THE 3 SISTERS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.info(f"**Ascendant:** {a_s} ({a_n})\n\n**Sun:** {s_s} ({s_n})\n\n**Moon:** {m_s} ({m_n})")
    
    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**Alignment:** Grounding for your {s_s} nature.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:** Heart-centered flow for {a_n}.")

    # DETAILED ANALYSIS
    st.markdown("---")
    st.subheader(f"Detailed Celestial Analysis for {client_name}")
    st.markdown(f"**Your {a_s} Ascendant in {a_n}:** {NAK_SHAKTI.get(a_n, 'A unique portal of growth.')}")
    st.markdown(f"**Your {s_s} Sun in {s_n}:** {NAK_SHAKTI.get(s_n, 'The core power of your identity.')}")

else:
    st.write("The stars are aligning. Please enter your birth details in the sidebar.")
