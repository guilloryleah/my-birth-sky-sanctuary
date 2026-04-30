import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE COMPLETED WISDOM LIBRARY ---
# This ensures "Unknown" is gone and provides the Zodiac anchors.
ZODIAC_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAK_DATA = {
    "Uttara Phalguni": {
        "Essence": "The Star of Patronage. Focused on kindness, leadership, and fulfilling social contracts.",
        "Ayurveda": "Pitta/Vata balance. Use cooling foods and consistent routines to manage your internal fire.",
        "Yoga": "Virabhadrasana (Warrior Pose). Embody the noble leadership and strength of this star."
    },
    "Purva Bhadrapada": {
        "Essence": "The Star of Transformation. Deeply spiritual, often marking a bridge between worlds.",
        "Ayurveda": "Vata/Kapha focus. Prioritize warmth and grounding to support your visionary nature.",
        "Yoga": "Savasana (Corpse Pose). Practice the art of letting go to facilitate deep inner change."
    },
    "Rohini": {
        "Essence": "The Star of Ascent. Soulful magnetism that fosters growth and creative beauty.",
        "Ayurveda": "Dominant Kapha. Prioritize movement to keep your lunar fluidity flowing.",
        "Yoga": "Vrksasana (Tree Pose). Ground through roots to reach your highest potential."
    }
    # (The engine will now default to "Sincere Guidance" for any star not yet detailed)
}

def get_zodiac(deg):
    return ZODIAC_NAMES[int(deg / 30) % 12]

def get_nakshatra_info(deg):
    names = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    name = names[int(deg / 13.333333) % 27]
    reading = NAK_DATA.get(name, {
        "Essence": "A unique celestial path of growth and discovery.",
        "Ayurveda": "Focus on balancing your elemental nature through mindful habits.",
        "Yoga": "Practice rhythmic movement to align your body with the sky."
    })
    return name, reading

# --- THE ENGINE ---
st.set_page_config(page_title="The Sky Sanctuary", layout="centered")
st.title("🧘‍♀️ The Sky Sanctuary")
st.markdown("*Professional alignment of the Real-Sky and the Body.*")

with st.container():
    u_name = st.text_input("Name")
    u_date = st.date_input("Birth Date", value=datetime(1969, 9, 25))
    u_time = st.time_input("Birth Time (Local)")
    u_city = st.text_input("Birth City (e.g., Houston, TX, USA)")

if st.button("Reveal My Alignment"):
    geolocator = Nominatim(user_agent="sky_sanctuary_pro")
    location = geolocator.geocode(u_city)
    
    if location:
        tf = TimezoneFinder()
        tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        timezone = pytz.timezone(tz_str)
        local_dt = timezone.localize(datetime.combine(u_date, u_time))
        utc_dt = local_dt.astimezone(pytz.utc)
        
        swe.set_sid_mode(swe.SIDM_LAHIRI) # Lock to Sidereal/Real-Sky
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
        
        # Calculations
        cusps, ascmc = swe.houses_ex(jd_ut, location.latitude, location.longitude, b'W', swe.FLG_SIDEREAL)
        sun_res, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SIDEREAL)
        moon_res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)
        
        st.header(f"The Soul-Map for {u_name}")
        
        for label, deg in [("🌅 Ascendant", ascmc[0]), ("☀️ Sun Star", sun_res[0]), ("🌙 Moon Star", moon_res[0])]:
            zodiac = get_zodiac(deg)
            nak_name, read = get_nakshatra_info(deg)
            with st.expander(f"{label}: {zodiac} / {nak_name}", expanded=True):
                st.write(f"**Essence:** {read['Essence']}")
                st.write(f"**Ayurvedic Insight:** {read['Ayurveda']}")
                st.write(f"**Yoga Practice:** {read['Yoga']}")
    else:
        st.error("Please enter a valid city to align the horizon.")
