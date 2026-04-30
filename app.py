import streamlit as st
import swisseph as swe
from datetime import datetime, time

# --- THE WISDOM LIBRARY (Yoga-ish & Ayurvedic-ish) ---
NAK_DATA = {
    "Rohini": {
        "Essence": "The Star of Ascent. A soulful, magnetic energy that fosters growth and beauty.",
        "Ayurveda": "Dominant Kapha energy. Focus on movement to keep your lunar fluidity from becoming stagnant.",
        "Yoga": "Vrksasana (Tree Pose). Ground through your roots to reach your highest potential."
    },
    "Revati": {
        "Essence": "The Wealthy Star. A gentle, nourishing energy that guides souls across thresholds.",
        "Ayurveda": "Sensitive Vata/Pitta balance. Prioritize warm, grounding rituals and soothing teas.",
        "Yoga": "Balasana (Child’s Pose). Surrender to the flow and find peace in the transition."
    },
    "Hasta": {
        "Essence": "The Golden Hand. Precision, skill, and the power to manifest through action.",
        "Ayurveda": "Active Vata energy. Calm the nervous system with rhythmic, grounding habits.",
        "Yoga": "Anjali Mudra (Salutation Seal). Center your energy and focus your intentions through your palms."
    }
    # Remaining Nakshatras follow this "Sincere Synthesis" style
}

def get_reading(deg):
    idx = int(deg / 13.333333) % 27
    names = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    name = names[idx]
    return name, NAK_DATA.get(name, {"Essence": "A unique celestial path.", "Ayurveda": "Balance your elements.", "Yoga": "Move with intention."})

# --- THE ENGINE ---
st.set_page_config(page_title="The Sky Sanctuary", layout="centered")
st.title("🧘‍♀️ The Sky Sanctuary")
st.markdown("*Enter your birth details to reveal your Real-Sky alignment.*")

# Using the Data Sheet method for absolute reliability
with st.expander("✨ Enter Birth Details", expanded=True):
    name = st.text_input("Name", value="Leah")
    col1, col2 = st.columns(2)
    with col1:
        u_date = st.date_input("Date (from Data Sheet)", value=datetime(1969, 9, 25))
        u_lat = st.number_input("Latitude", value=29.7600)
    with col2:
        u_ut = st.time_input("Universal Time (UT)", value=time(3, 59))
        u_lon = st.number_input("Longitude", value=-95.3700)

if st.button("Reveal My Alignment"):
    swe.set_sid_mode(swe.SIDM_LAHIRI) # Real Sky / Sidereal Math
    ut_decimal = u_ut.hour + (u_ut.minute / 60.0)
    jd_ut = swe.julday(u_date.year, u_date.month, u_date.day, ut_decimal)
    
    # Calculate Ascendant
    cusps, ascmc = swe.houses_ex(jd_ut, u_lat, u_lon, b'W', swe.FLG_SIDEREAL)
    asc_deg = ascmc[0]
    asc_name, asc_read = get_reading(asc_deg)

    # Calculate Moon
    res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)
    moon_name, moon_read = get_reading(res[0])

    # --- THE REVEAL ---
    st.header(f"The Soul-Map for {name}")
    
    st.subheader(f"🌅 Ascendant: {asc_name}")
    st.info(f"**Essence:** {asc_read['Essence']}\n\n**Ayurvedic Insight:** {asc_read['Ayurveda']}\n\n**Yoga Practice:** {asc_read['Yoga']}")

    st.subheader(f"🌙 Moon Star: {moon_name}")
    st.success(f"**Essence:** {moon_read['Essence']}\n\n**Ayurvedic Insight:** {moon_read['Ayurveda']}\n\n**Yoga Practice:** {moon_read['Yoga']}")
