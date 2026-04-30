import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE SANCTUARY LIBRARY ---
# I have pre-loaded the specific Nakshatras for your family's alignment.
NAK_DATA = {
    "Rohini": {
        "Zodiac": "Taurus",
        "Essence": "The Star of Ascent. A soulful, magnetic energy that fosters growth and beauty.",
        "Ayurveda": "Dominant Kapha energy. Prioritize movement to keep lunar fluidity flowing.",
        "Yoga": "Vrksasana (Tree Pose). Ground through roots to reach your highest potential."
    },
    "Hasta": {
        "Zodiac": "Virgo",
        "Essence": "The Golden Hand. Precision, skill, and the power to manifest through mindful action.",
        "Ayurveda": "Active Vata energy. Calm the nervous system with rhythmic, grounding habits.",
        "Yoga": "Anjali Mudra (Salutation Seal). Center your energy and focus your intentions."
    },
    "Mrigashira": {
        "Zodiac": "Gemini",
        "Essence": "The Searching Star. A curious, gentle energy always seeking new paths of wisdom.",
        "Ayurveda": "Sensitive Vata balance. Use warming rituals to ground the searching mind.",
        "Yoga": "Marjaryasana (Cat-Cow). Find flexibility and grace in constant movement."
    }
}

def get_nakshatra_info(deg):
    idx = int(deg / 13.333333) % 27
    names = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    name = names[idx]
    return name, NAK_DATA.get(name, {"Zodiac": "Unknown", "Essence": "A unique path.", "Ayurveda": "Balance your elements.", "Yoga": "Move with intention."})

# --- THE ENGINE ---
st.set_page_config(page_title="The Sky Sanctuary", layout="centered")
st.title("🧘‍♀️ The Sky Sanctuary")
st.markdown("*A professional alignment of the Real-Sky, the body, and the breath.*")

with st.container():
    u_name = st.text_input("Name")
    u_date = st.date_input("Birth Date", value=datetime(1969, 9, 25))
    u_time = st.time_input("Birth Time (Local)")
    u_city = st.text_input("Birth City (e.g., Houston, TX, USA)")

if st.button("Reveal My Alignment"):
    geolocator = Nominatim(user_agent="sky_sanctuary")
    location = geolocator.geocode(u_city)
    
    if location:
        # 1. Solve the Time Zone (The 1957/1969 Bridge)
        tf = TimezoneFinder()
        tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        timezone = pytz.timezone(tz_str)
        local_dt = timezone.localize(datetime.combine(u_date, u_time))
        utc_dt = local_dt.astimezone(pytz.utc)
        
        # 2. The Real-Sky Math (Lahiri Sidereal)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
        
        # 3. Calculate Trinity
        cusps, ascmc = swe.houses_ex(jd_ut, location.latitude, location.longitude, b'W', swe.FLG_SIDEREAL)
        sun_res, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SIDEREAL)
        moon_res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)
        
        # --- THE REVEAL ---
        st.header(f"The Soul-Map for {u_name}")
        
        points = [
            ("🌅 Ascendant", ascmc[0]),
            ("☀️ Sun Star", sun_res[0]),
            ("🌙 Moon Star", moon_res[0])
        ]
        
        for label, deg in points:
            name, info = get_nakshatra_info(deg)
            with st.expander(f"{label}: {info['Zodiac']} / {name}", expanded=True):
                st.write(f"**Essence:** {info['Essence']}")
                st.write(f"**Ayurvedic Insight:** {info['Ayurveda']}")
                st.write(f"**Yoga Practice:** {info['Yoga']}")
    else:
        st.error("City not found. Please check the spelling.")
