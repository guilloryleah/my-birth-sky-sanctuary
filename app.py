import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. DATA
NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE INVISIBLE ENGINE
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_final")
        loc = geolocator.geocode(city_name)
        if not loc: return 29.76, -95.36, -6.0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_seconds = timezone.utcoffset(birth_dt).total_seconds()
        return loc.latitude, loc.longitude, (offset_seconds / 3600)
    except:
        return 29.76, -95.36, -6.0

def calculate_precision_sky(jd_local, lat, lon, offset_hours):
    jd_utc = jd_local - (offset_hours / 24.0)
    ayan = 24.13 
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.4606 + 360.985647 * (jd_utc - 2451545.0)) % 360
    lst_deg = (gmst + lon) % 360
    eps = math.radians(23.439)
    phi = math.radians(lat)
    lst_rad = math.radians(lst_deg)
    num = -math.cos(lst_rad)
    den = (math.sin(lst_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    sid_asc = (math.degrees(math.atan2(num, den)) - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    return sid_sun, sid_moon, sid_asc

# 4. SIDEBAR (The Work)
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("Name", placeholder="Enter your name")
    y = st.number_input("Year", 1200, 2026, 1995)
    m = st.number_input("Month", 1, 12, 9)
    d = st.number_input("Day", 1, 31, 24)
    t_in = st.time_input("Birth Time")
    place = st.text_input("Place of Birth", placeholder="e.g. Houston, TX")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. MAIN PAGE (The Vibe)
if not submit:
    st.markdown("# ✨ Welcome to Your Birth Sky Sanctuary")
    st.markdown("""
    ### *“As above, so below; as within, so without.”*
    
    Welcome, Seeker. You have entered a space designed to bridge the ancient wisdom of the stars 
    with the grounding path of your own life. Here, we don't just calculate signs; we map the 
    **soul's blueprint** using the precise astronomical logic of the Sidereal sky.
    
    Before we begin, take a breath. Release the noise of the day. 
    
    **To reveal your celestial architecture:**
    * Enter your birth details in the sidebar to the left.
    * Ensure your **Birth Place** is specific so we can capture the exact horizon of your arrival.
    * Once submitted, we will weave together your **Jyotish, Ayurveda, and Yoga** alignment.
    
    *The heavens were singing when you arrived. Let's find out what they were saying.*
    """)
    st.image("https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&q=80&w=2070", caption="The stars are a map to your internal sanctuary.")

# 6. OUTPUT (The Reveal)
else:
    birth_dt = datetime.combine(date(y, m, d), t_in)
    lat, lon, offset = get_location_details(place, birth_dt)
    jd_local = pd.Timestamp(birth_dt).to_julian_date()
    s_d, m_d, a_d = calculate_precision_sky(jd_local, lat, lon, offset)
    
    s_s, s_n = ZODIAC_LIST[int(s_d/30)], NAK_LIST[int(s_d/13.333)]
    m_s, m_n = ZODIAC_LIST[int(m_d/30)], NAK_LIST[int(m_d/13.333)]
    a_s, a_n = ZODIAC_LIST[int(a_d/30)], NAK_LIST[int(a_d/13.333)]

    st.header(f"✨ Welcome to your Sanctuary, {name}")
    st.write(f"Reflecting the heavens over **{place}**—precisely as they were at the moment of your breath.")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.metric("Ascendant (Lagna)", a_s)
        st.write(f"**Nakshatra:** {a_n}")
        st.write(f"**Sun:** {s_s} ({s_n})")
        st.write(f"**Moon:** {m_s} ({m_n})")
    
    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**The Elemental Path:** Nourishing your {a_s} constitution.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:** Aligning the energy of {a_n}.")
