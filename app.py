import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE COMPLETED WISDOM LIBRARY ---
ZODIAC_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAK_DATA = {
    "Uttara Phalguni": {
        "Essence": "The Star of the Noble Patron. This star bridges Leo's leadership and Virgo's service. You lead through organized support, acting as a stable 'throne' for your community.",
        "Ayurveda": "Managing the Solar-Earth Fire. While you are grounded in Earth (Virgo), your star is fueled by the Sun. This creates an internal 'heat' that requires cooling rituals to prevent irritability or burnout.",
        "Yoga": "Virabhadrasana (Warrior Pose). Ground your feet firmly like the Earth, but reach your heart and arms up with noble, solar purpose."
    },
    "Mrigashira": {
        "Essence": "The Searching Star. A curious, gentle energy driven by a deep desire to explore. You are the eternal student, always seeking the next horizon of truth.",
        "Ayurveda": "Sensitive Vata. Your mind moves quickly like a deer in the forest. Use warm, grounding rituals and consistent rhythms to help your searching mind find rest.",
        "Yoga": "Marjaryasana (Cat-Cow). Practice finding grace and flexibility within constant movement and exploration."
    },
    "Swati": {
        "Essence": "The Star of Independence. Like a young sprout swaying in the breeze, you value freedom and the power of the breath (Prana) to move through the world.",
        "Ayurveda": "Air/Vata Management. You are sensitive to the 'winds' of change. Use heavy, grounding foods like root vegetables to stay anchored when life feels scattered.",
        "Yoga": "Pranayama (Breathwork). Use intentional breathing to steady your independent spirit and find your center."
    },
    "Purva Bhadrapada": {
        "Essence": "The Star of Transformation. A deeply spiritual energy that acts as a bridge between the physical and the mystical worlds.",
        "Ayurveda": "Vata/Kapha Focus. Prioritize internal warmth and physical grounding to support your visionary and often intense nature.",
        "Yoga": "Savasana (Corpse Pose). Practice the profound art of letting go to facilitate your soul's natural cycle of change.",
    },
    "Rohini": {
        "Essence": "The Star of Ascent. Soulful magnetism and creative beauty. This star represents the peak of growth and the ability to manifest visions into reality.",
        "Ayurveda": "Dominant Kapha. You have a lush, steady energy; keep it flowing with active, heart-opening movements to avoid stagnation.",
        "Yoga": "Vrksasana (Tree Pose). Root down firmly into your values so your creative branches have the stability to grow toward the sky."
    }
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
st.markdown("*A Global Haven for Real-Sky Alignment.*")

with st.container():
    u_name = st.text_input("Name")
    u_date = st.date_input("Birth Date", value=datetime(1969, 9, 25), min_value=datetime(1900, 1, 1), max_value=datetime.now())
    u_time = st.time_input("Birth Time (Local)")
    u_city = st.text_input("Birth Location", placeholder="City, State, Country (e.g., London, UK)")

if st.button("Reveal My Alignment"):
    geolocator = Nominatim(user_agent="sky_sanctuary_global_final_fix")
    location = geolocator.geocode(u_city, language='en')
    
    if location:
        tf = TimezoneFinder()
        tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        
        if tz_str:
            timezone = pytz.timezone(tz_str)
            local_dt = timezone.localize(datetime.combine(u_date, u_time))
            utc_dt = local_dt.astimezone(pytz.utc)
            
            swe.set_sid_mode(swe.SIDM_LAHIRI) 
            jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
            
            cusps, ascmc = swe.houses_ex(jd_ut, location.latitude, location.longitude, b'W', swe.FLG_SIDEREAL)
            sun_res, _ = swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SIDEREAL)
            moon_res, _ = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)
            
            # THE EDUCATIONAL SCAFFOLD
            st.info("""
            ### **The Science of the Shift**
            If your signs are different than you expected, you aren't alone! Most traditional systems use a 'frozen' map of the stars from 2,000 years ago. 
            
            Because the Earth has a slight **wobble (Precession)**, the constellations have shifted by about 24 degrees. The Sky Sanctuary uses **Real-Sky Astronomy** to align your map with the actual physical horizon as it appeared at your birth.
            """)
            
            st.header(f"The Soul-Map for {u_name}")
            st.caption(f"Aligned to: {location.address}")
            
            for label, deg in [("🌅 Ascendant", ascmc[0]), ("☀️ Sun Star", sun_res[0]), ("🌙 Moon Star", moon_res[0])]:
                zodiac = get_zodiac(deg)
                nak_name, read = get_nakshatra_info(deg)
                with st.expander(f"{label}: {zodiac} / {nak_name}", expanded=True):
                    st.write(f"**Essence:** {read['Essence']}")
                    st.write(f"**Ayurvedic Insight:** {read['Ayurveda']}")
                    st.write(f"**Yoga Practice:** {read['Yoga']}")
        else:
            st.error("Could not determine the time zone for this location.")
    else:
        st.error("Location not found. Please add the Country for better accuracy.")
