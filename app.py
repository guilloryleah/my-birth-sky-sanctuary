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
    "Ashwini": {
        "Essence": "The Star of the Swift Healer. A pioneer spirit that moves with the speed of thought and the courage of a new dawn.",
        "Alignment": "Invite warming, steady rituals to ground your fast-moving energy and soothe your 'internal wind.'",
        "Yoga": "Balasana (Child's Pose) to find rest and centering in the midst of your natural movement."
    },
    "Krittika": {
        "Essence": "The Star of the Sacred Fire. A sharp, protective intelligence that acts as the flame warming the hearth of the community.",
        "Alignment": "Use cooling, earthy essences and grounding practices to keep your inner fire from burning too bright.",
        "Yoga": "Agni Stambhasana (Fire Log Pose) to consciously channel and seat your internal heat."
    },
    "Shatabhisha": {
        "Essence": "The Star of a Thousand Healers. A visionary, independent soul who values the truth of the big picture and the mystery of the stars.",
        "Alignment": "Prioritize open spaces, fresh air, and moments of silence to keep your vast, airy mind clear and aligned.",
        "Yoga": "Anjaneyasana (Low Lunge) to open your heart to the wide horizon you naturally seek."
    },
    "Uttara Phalguni": {
        "Essence": "The Star of the Noble Patron. Bridging leadership and service, you lead by acting as a stable 'throne' for those you support.",
        "Alignment": "Managing the Solar-Earth Fire. Your grounded nature is fueled by the Sun; use cooling rituals to prevent burnout.",
        "Yoga": "Virabhadrasana (Warrior Pose). Ground your feet like Earth, but reach your heart up like the Sun."
    },
    "Mrigashira": {
        "Essence": "The Searching Star. A curious, gentle energy driven by a deep desire to explore and uncover hidden truths.",
        "Alignment": "Sensitive Vata. Your mind moves like a deer; use warm, rhythmic rhythms to help your searching mind find rest.",
        "Yoga": "Marjaryasana (Cat-Cow). Find grace and flexibility in your constant search for knowledge."
    },
    "Swati": {
        "Essence": "The Star of Independence. Like a young sprout in the wind, you value freedom and the power of the breath (Prana).",
        "Alignment": "Air/Vata Focus. You can be easily scattered by 'life's winds.' Use heavy, grounding foods to stay anchored.",
        "Yoga": "Pranayama (Breathwork). Use the breath to steady your independent spirit and find your center."
    },
    "Purva Bhadrapada": {
        "Essence": "The Star of Transformation. A spiritual bridge between worlds, facilitating the deep cycles of soul-growth.",
        "Alignment": "Vata/Kapha Focus. Prioritize internal warmth and physical grounding to support your visionary nature.",
        "Yoga": "Savasana (Corpse Pose). Practice the profound art of letting go to facilitate your natural cycle of change."
    },
    "Rohini": {
        "Essence": "The Star of Ascent. Soulful magnetism that fosters growth, creative beauty, and emotional depth.",
        "Alignment": "Dominant Kapha. You have a lush, steady energy; keep it flowing with heart-opening movement to avoid stagnation.",
        "Yoga": "Vrksasana (Tree Pose). Root down firmly so your creative branches have the stability to grow tall."
    }
}

def get_zodiac(deg):
    return ZODIAC_NAMES[int(deg / 30) % 12]

def get_nakshatra_info(deg):
    names = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    name = names[int(deg / 13.333333) % 27]
    reading = NAK_DATA.get(name, {
        "Essence": "A unique celestial path of growth and discovery.",
        "Alignment": "Focus on balancing your internal atmosphere through mindful, rhythmic habits.",
        "Yoga": "Practice rhythmic movement to align your body with the physical sky."
    })
    return name, reading

def format_degree(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    return f"{d}° {m:02d}'"

# --- THE ENGINE ---
st.set_page_config(page_title="The Sky Sanctuary", layout="centered")
st.title("🧘‍♀️ The Sky Sanctuary")
st.markdown("*A Global Haven for Real-Sky Alignment.*")

with st.container():
    u_name = st.text_input("Name")
    u_date = st.date_input("Birth Date", value=datetime(1969, 9, 25), min_value=datetime(1900, 1, 1), max_value=datetime.now())
    u_time = st.time_input("Birth Time (Local)")
    u_city = st.text_input("Birth Location", placeholder="City, State, Country (e.g., Chicago, IL, USA)")

if st.button("Reveal My Alignment"):
    geolocator = Nominatim(user_agent="sky_sanctuary_final_pro")
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
            
            # Calculations
            cusps, ascmc = swe.houses_ex(jd_ut, location.latitude, location.longitude, b'W', swe.FLG_SIDEREAL)
            planets = {
                "🌅 Ascendant": ascmc[0],
                "☀️ Sun (The Soul)": swe.calc_ut(jd_ut, swe.SUN, swe.FLG_SIDEREAL)[0][0],
                "🌙 Moon (The Mind)": swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SIDEREAL)[0][0],
                "☿️ Mercury (The Messenger)": swe.calc_ut(jd_ut, swe.MERCURY, swe.FLG_SIDEREAL)[0][0],
                "♀️ Venus (The Harmonizer)": swe.calc_ut(jd_ut, swe.VENUS, swe.FLG_SIDEREAL)[0][0],
                "♂️ Mars (The Protector)": swe.calc_ut(jd_ut, swe.MARS, swe.FLG_SIDEREAL)[0][0],
                "♃ Jupiter (The Guide)": swe.calc_ut(jd_ut, swe.JUPITER, swe.FLG_SIDEREAL)[0][0],
                "♄ Saturn (The Anchor)": swe.calc_ut(jd_ut, swe.SATURN, swe.FLG_SIDEREAL)[0][0],
                "🐉 Rahu (The Destiny)": swe.calc_ut(jd_ut, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0]
            }
            
            st.header(f"The Soul-Map for {u_name}")
            
            # --- SECTION 1: THE SOUL-MAP (BIG THREE) ---
            big_three = ["🌅 Ascendant", "☀️ Sun (The Soul)", "🌙 Moon (The Mind)"]
            for label in big_three:
                deg = planets[label]
                zodiac = get_zodiac(deg)
                nak_name, read = get_nakshatra_info(deg)
                with st.expander(f"{label}: {zodiac} / {nak_name} ({format_degree(deg % 30)})", expanded=True):
                    st.write(f"**Essence:** {read['Essence']}")
                    st.write(f"**Alignment:** {read['Alignment']}")
                    st.write(f"**Yoga Practice:** {read['Yoga']}")

            # --- SECTION 2: DEEP ALIGNMENT ---
            st.divider()
            st.subheader("Deep Alignment: The Planetary Narrative")
            other_planets = [p for p in planets if p not in big_three]
            for label in other_planets:
                deg = planets[label]
                zodiac = get_zodiac(deg)
                nak_name, read = get_nakshatra_info(deg)
                with st.expander(f"{label}: {zodiac} / {nak_name} ({format_degree(deg % 30)})"):
                    st.write(f"**Essence:** {read['Essence']}")
                    st.write(f"**Alignment:** {read['Alignment']}")
                    st.write(f"**Yoga Practice:** {read['Yoga']}")

            # --- FOOTER ---
            st.divider()
            st.markdown("### **The Wisdom of the Birth Sky**")
            st.write("""
            Your **Birth Sky** is the literal, physical snapshot of the heavens as they appeared on the horizon at the moment of your first breath. 
            
            If your stars feel different than you expected, you are experiencing a 'Real-Sky Homecoming.' Over the last 2,000 years, the Earth has gently 'wobbled' in a slow cycle called Precession. This movement has shifted the constellations about 24 degrees from traditional 'frozen' maps. By aligning with your true physical sky, we return to the light exactly as it greeted you—grounded, accurate, and real.
            """)
        else:
            st.error("Could not determine the time zone.")
    else:
        st.error("Location not found.")
