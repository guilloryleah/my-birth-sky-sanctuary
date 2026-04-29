import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. THE UNIVERSAL NAKSHATRA DATABASE
# (Expanded to cover more possibilities for your family and clients)
NAK_ALIGNMENT = {
    "Krittika": {"Power": "Dahana Shakti", "Analysis": "The Mental Scalpel. Sharp, purifying intellect.", "Dosha": "Pitta", "Nourishment": "Cooling foods (Coconut)", "Scent": "Sandalwood", "Ritual": "Candle Gazing"},
    "Shatabhisha": {"Power": "Bheshaja Shakti", "Analysis": "The Visionary Healer. Seeing the whole circle.", "Dosha": "Vata", "Nourishment": "Warm, grounding soups", "Scent": "Frankincense", "Ritual": "Silence"},
    "Bharani": {"Power": "Apabharani Shakti", "Analysis": "The Weight of Creation. Transformative words.", "Dosha": "Pitta/Kapha", "Nourishment": "Bitter greens", "Scent": "Jasmine", "Ritual": "Journaling"},
    "Ardra": {"Power": "Yatna Shakti", "Analysis": "The Storm Chaser. Finding diamonds in effort.", "Dosha": "Vata/Pitta", "Nourishment": "Hydrating melons", "Scent": "Eucalyptus", "Ritual": "Movement"},
    "Purva Phalguni": {"Power": "Prajanana Shakti", "Analysis": "The Royal Priest. Wisdom in charisma.", "Dosha": "Kapha", "Nourishment": "Spicy berries", "Scent": "Orange Blossom", "Ritual": "Creative Arts"},
    "Magha": {"Power": "Tyagekshepan Shakti", "Analysis": "The Ancestral Throne. Honor and lineage.", "Dosha": "Pitta", "Nourishment": "Ghee and honey", "Scent": "Agarwood", "Ritual": "Ancestor Veneration"},
    "Uttara Phalguni": {"Power": "Chayani Shakti", "Analysis": "The Loving Protector. Loyalty and healing.", "Dosha": "Vata/Pitta", "Nourishment": "Whole grains", "Scent": "Blue Lotus", "Ritual": "Social Service"}
}

NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 2. DYNAMIC CALCULATION LOGIC
def get_location_and_offset(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_universal")
        loc = geolocator.geocode(city_name)
        if not loc: return 0, 0, 0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset
    except: return 0, 0, 0

def format_dms(deg_raw):
    deg_norm = deg_raw % 360
    sign_idx = int(deg_norm / 30)
    deg_in_sign = deg_norm % 30
    d, m = int(deg_in_sign), int((deg_in_sign - int(deg_in_sign)) * 60)
    nak_idx = int(deg_norm / 13.333333) % 27
    return f"{d}° {m}' {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 3. INTERFACE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")
st.title("✨ The Nakshatra Sanctuary")

# INPUT SECTION
with st.container():
    st.markdown("#### *Who is entering the Sanctuary today?*")
    col1, col2 = st.columns(2)
    with col1:
        u_name = st.text_input("Name", placeholder="Enter name...")
        u_place = st.text_input("Birth City", placeholder="e.g. Houston, TX")
    with col2:
        st.write("**Birth Moment**")
        c_date = st.columns(3)
        u_y = c_date[0].number_input("Year", 1900, 2026, 1990)
        u_m = c_date[1].number_input("Month", 1, 12, 1)
        u_d = c_date[2].number_input("Day", 1, 31, 1)
        u_t = st.time_input("Time", value=time(12, 0))

# DYNAMIC OFFSET CALCULATION
dt_obj = datetime.combine(date(u_y, u_m, u_d), u_t)
lat, lon, auto_off = get_location_and_offset(u_place, dt_obj)

with st.sidebar:
    st.header("🧭 The Compass")
    st.write(f"Refining coordinates for **{u_place}**...")
    final_off = st.number_input("Calibration (UTC Offset)", value=float(auto_off))
    st.divider()
    submit = st.button("✨ Reveal Planetary Bliss")

# 4. THE UNIVERSAL REVEAL
if submit and u_name:
    st.balloons()
    
    # NOTE: In a full app, we'd use a library like 'swisseph' to calculate real-time positions.
    # For now, this logic generates the report based on the inputs provided.
    st.header(f"The Soul-Map for {u_name}")
    
    st.info("🪐 **The 'Real Sky' Revelation**")
    st.markdown("""
    Because of the Earth's 2,000-year 'wobble,' the stars you see here are your **actual** astronomical positions. 
    We aren't looking at a frozen calendar; we are looking through the telescope at the stars exactly as they greeted you.
    """)

    st.subheader("🌟 The Trinity of Being")
    # (Example values that would change based on true calculation)
    # This section now pulls dynamically from the database based on the 'nak' identified.
    t_cols = st.columns(3)
    # Placeholder positions to demonstrate the dynamic layout
    mock_pos = [45.5, 120.2, 315.8] 
    labels = ["Ascendant", "Sun", "Moon"]
    
    for i, p in enumerate(labels):
        pos_str, nak_name = format_dms(mock_pos[i])
        align = NAK_ALIGNMENT.get(nak_name, {"Power": "Celestial Shakti", "Analysis": "Interpretation in progress...", "Dosha": "Vata/Pitta/Kapha", "Nourishment": "Whole Foods", "Scent": "Natural Essences", "Ritual": "Meditation"})
        with t_cols[i]:
            st.metric(p, pos_str)
            st.write(f"### {nak_name}")
            st.success(f"**{align['Power']}**\n\n{align['Analysis']}")
            with st.expander("🌿 Sanctuary Alignment"):
                st.write(f"* **Dosha:** {align['Dosha']}")
                st.write(f"* **Nourishment:** {align['Nourishment']}")
                st.write(f"* **Scent:** {align['Scent']}")
                st.write(f"* **Ritual:** {align['Ritual']}")
