import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. CELESTIAL DATA DICTIONARIES
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE INVISIBLE ENGINE (Timezone & Coordinates)
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="birth_sky_sanctuary_final")
        loc = geolocator.geocode(city_name)
        if not loc:
            return 29.76, -95.36, -6.0 # Default Houston
        
        # Determine the timezone and historical offset (DST check)
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_seconds = timezone.utcoffset(birth_dt).total_seconds()
        offset_hours = offset_seconds / 3600
        
        return loc.latitude, loc.longitude, offset_hours
    except:
        return 29.76, -95.36, -6.0

def calculate_precision_sky(jd_local, lat, lon, offset_hours):
    # Convert local time to UTC for astronomical calculation
    jd_utc = jd_local - (offset_hours / 24.0)
    ayan = 24.13 # Lahiri Ayanamsha 
    
    # Sidereal Time Calculation
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.4606 + 360.985647 * (jd_utc - 2451545.0)) % 360
    lst_deg = (gmst + lon) % 360
    
    # Spherical Trigonometry for the Ascendant (Lagna)
    eps = math.radians(23.439) # Earth's Tilt
    phi = math.radians(lat)
    lst_rad = math.radians(lst_deg)
    
    num = -math.cos(lst_rad)
    den = (math.sin(lst_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    
    # Calculate Final Degrees
    sid_asc = (math.degrees(math.atan2(num, den)) - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

# 4. SIDEBAR (The Data Entry)
with st.sidebar:
    st.header("Seeker's Profile")
    name = st.text_input("What is your name?", placeholder="e.g. Matthew")
    y = st.number_input("Year of Birth", 1900, 2026, 1995)
    m = st.number_input("Month of Birth", 1, 12, 9)
    d = st.number_input("Day of Birth", 1, 31, 24)
    t_in = st.time_input("Exact Birth Time", value=time(12, 0))
    place = st.text_input("City of Birth", placeholder="e.g. Houston, TX")
    
    st.divider()
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. MAIN PAGE (The Vibe & The Result)
if not submit:
    st.markdown("# ✨ Welcome to Your Birth Sky Sanctuary")
    st.markdown("""
    ### *“I am because we are.”*
    
    Welcome, Seeker. You have entered a space where the ancient rhythm of the stars meets the interconnected spirit of **Ubuntu**. 
    This sanctuary is designed to help you rediscover your soul’s blueprint—not through a generic lens, but through the precise, 
    astronomical truth of the **Sidereal Sky**.
    
    Here, we honor the three sisters of alignment:
    1.  **Jyotish:** Your celestial architecture.
    2.  **Ayurveda:** Your elemental medicine.
    3.  **Yoga:** Your energetic re-patterning.
    
    **To begin your journey:**
    Please enter your birth details in the sidebar. Ensure your location is accurate so we can map the exact horizon 
    of your arrival. 
    
    *The heavens were singing when you arrived. Let's find out what they were saying.*
    """)
    st.image("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2013&auto=format&fit=crop", caption="Mapping the cosmic interconnectedness of your arrival.")

else:
    # RUN THE CALCULATION
    birth_dt = datetime.combine(date(y, m, d), t_in)
    lat, lon, offset = get_location_details(place, birth_dt)
    jd_local = pd.Timestamp(birth_dt).to_julian_date()
    
    s_d, m_d, a_d = calculate_precision_sky(jd_local, lat, lon, offset)
    
    # Map degrees to Labels
    s_s, s_n = ZODIAC_LIST[int(s_d/30)], NAK_LIST[int(s_d/13.333)]
    m_s, m_n = ZODIAC_LIST[int(m_d/30)], NAK_LIST[int(m_d/13.333)]
    a_s, a_n = ZODIAC_LIST[int(a_d/30)], NAK_LIST[int(a_d/13.333)]

    st.header(f"✨ Welcome to your Sanctuary, {name}")
    st.write(f"Reflecting the heavens over **{place}**—captured through the lens of Sidereal truth.")
    st.divider()

    # THE 3 SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.metric("Ascendant (Lagna)", a_s)
        st.write(f"**Nakshatra:** {a_n}")
        st.write(f"**Sun:** {s_s} ({s_n})")
        st.write(f"**Moon:** {m_s} ({m_n})")
    
    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**The Elemental Path:**\n\nNourishing your {a_s} constitution through grounding rituals and ancestral wisdom.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:**\n\nAligning the energy of **{a_n}** through heart-centered flow and rhythmic breath.")

    st.markdown("---")
    st.info(f"**Teacher's Reflection:** Your {a_s} Ascendant is the gateway to your purpose. In the spirit of Ubuntu, your journey is a vital thread in the collective tapestry.")
