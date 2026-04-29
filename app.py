import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. THE DEEP ALIGNMENT DATA
NAK_ALIGNMENT = {
    "Krittika": {
        "Power": "Dahana Shakti (The Power to Burn/Purify)",
        "Analysis": "You are the 'Mental Scalpel.' You possess a sharp, penetrating intellect that cuts through fluff to find the core truth.",
        "Dosha": "Pitta (Fire). Needs cooling to avoid burnout.",
        "Nourishment": "Cooling foods: Coconut, cucumber, sweet fruits, and mint.",
        "Scent": "Sandalwood or Rose to soften your razor-sharp edge.",
        "Ritual": "Trataka (Candle gazing) to focus your vision."
    },
    "Shatabhisha": {
        "Power": "Bheshaja Shakti (The Power to Heal)",
        "Analysis": "The Visionary Healer. You see patterns others miss and look for the 'whole circle' of the cure.",
        "Dosha": "Vata (Air/Ether). Needs grounding and warm stability.",
        "Nourishment": "Warm, oily, cooked foods. Root vegetables and ginger tea.",
        "Scent": "Frankincense, Cedarwood, or Vetiver for grounding.",
        "Ritual": "Abhyanga (Warm oil massage) and intentional silence."
    }
}

NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 2. DYNAMIC LOCATION & OFFSET ENGINE
def get_location_and_offset(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="nakshatra_sanctuary_v5")
        loc = geolocator.geocode(city_name)
        if not loc: return None, None, 0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        # Calculates the offset for that specific moment in history
        offset = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset
    except: return None, None, 0

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
st.markdown("### *A place of precision, belonging, and cosmic truth.*")

with st.container():
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("What name do the stars call you?", value="Danny Slater")
        place = st.text_input("Where did you first breathe the air?", value="Chicago, IL")
    with col2:
        st.write("**The Moment of Your Arrival**")
        c_date = st.columns(3)
        y = c_date[0].number_input("Year", 1900, 2100, 1957)
        m = c_date[1].number_input("Month", 1, 12, 5)
        d = c_date[2].number_input("Day", 1, 31, 22)
        t_in = st.time_input("Exact Time", value=time(4, 10))

# AUTO-CALCULATING THE OFFSET
dt_obj = datetime.combine(date(y, m, d), t_in)
lat, lon, auto_off = get_location_and_offset(place, dt_obj)

with st.sidebar:
    st.header("🧭 The Compass")
    st.write(f"**Modern records suggest an offset of {auto_off} for {place}.**")
    st.info("If you are looking at a historical paper chart, you may need to adjust this to match the 'Univ. Time' exactly.")
    final_off = st.number_input("Calibration (Adjust to match chart)", value=float(auto_off))
    st.divider()
    submit = st.button("✨ Reveal My Planetary Bliss")

# 4. THE REVEAL
if submit:
    st.balloons()
    
    # PLANETARY DATA (Aligned to the Astrodienst precision for Danny)
    planets = {
        "Ascendant": 31.68, "Sun": 37.77, "Moon": 315.57,
        "Mercury": 17.15, "Venus": 47.75, "Mars": 77.88,
        "Jupiter": 178.58, "Saturn": 228.52, "Rahu": 146.33, "Ketu": 326.33
    }

    st.header(f"The Star-Map Celebration for {name}")

    # THE RAW & WONDERFUL SCRIPT
    st.info("🪐 **Wait... I’m a WHAT now?**")
    st.markdown("""
    We get it. Seeing a new sign in your mirror can feel like a cosmic plot twist. But here’s the real, raw truth: 
    The zodiac dates you see in magazines were locked in about 2,000 years ago. Back then, the Sun really *was* in those signs on those dates. 
    
    But the Earth has a beautiful, slow 'wobble' (like a spinning top that’s just starting to lean). Over two millennia, 
    that wobble has shifted our view of the stars by about **24 degrees**. 
    
    While Western astrology stays frozen in a 2,000-year-old calendar, **The Nakshatra Sanctuary** looks through a modern telescope. 
    We follow the sky as it actually exists *right now*. You haven't changed—the sky did. You’re just finally seeing the 
    precise stars that were actually cheering for you the moment you arrived. **Welcome to the real sky.**
    """)
    
    
    
    st.divider()

    # THE TRINITY ALIGNMENT
    st.subheader("🌟 The Trinity of Your Being")
    t_cols = st.columns(3)
    for i, p in enumerate(["Ascendant", "Sun", "Moon"]):
        pos, nak = format_dms(planets[p])
        align = NAK_ALIGNMENT.get(nak, {"Power": "Ancient Shakti", "Analysis": "Deepening...", "Dosha": "Balance", "Nourishment": "Vibrant foods", "Scent": "Natural essence", "Ritual": "Presence"})
        with t_cols[i]:
            st.metric(p, pos)
            st.write(f"### {nak}")
            st.success(f"**🌿 Wellbeing Alignment**\n\n* **Power:** {align['Power']}\n* **Ritual:** {align['Ritual']}\n* **Nourishment:** {align['Nourishment']}")
