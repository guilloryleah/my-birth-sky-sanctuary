import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE COMPLETED WISDOM LIBRARY (All 27 Stars) ---
ZODIAC_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

NAK_DATA = {
    "Ashwini": {
        "Essence": "The Star of the Swift Healer. A pioneer spirit moving with the speed of thought and the courage of a new dawn.",
        "Alignment": "Invite warming, steady rituals to ground your fast-moving energy and soothe your internal atmosphere.",
        "Yoga": "Balasana (Child's Pose) to find rest in the midst of your natural movement."
    },
    "Bharani": {
        "Essence": "The Star of Restraint. A powerful, transformative energy that carries the seeds of new life through discipline.",
        "Alignment": "Prioritize grounding, nourishing rhythms to balance your intense internal fire.",
        "Yoga": "Malasana (Yogi Squat) to connect deeply with the Earth's stabilizing force."
    },
    "Krittika": {
        "Essence": "The Star of the Sacred Fire. A sharp, protective intelligence that acts as the flame warming and guarding the hearth.",
        "Alignment": "Use cooling, earthy essences to keep your inner brilliance from burning too bright.",
        "Yoga": "Agni Stambhasana (Fire Log Pose) to consciously channel your internal heat."
    },
    "Rohini": {
        "Essence": "The Star of Ascent. A soulful magnetism that fosters growth, creative beauty, and emotional depth.",
        "Alignment": "Embrace heart-opening movement to keep your lush, steady energy flowing like a clear stream.",
        "Yoga": "Vrksasana (Tree Pose) to root down so your creative branches can reach the sky."
    },
    "Mrigashira": {
        "Essence": "The Searching Star. A curious, gentle energy driven by a deep desire to explore and uncover hidden truths.",
        "Alignment": "Use warm, rhythmic habits to help your searching mind find a sense of home.",
        "Yoga": "Marjaryasana (Cat-Cow) to find grace and flexibility in your exploration."
    },
    "Ardra": {
        "Essence": "The Star of the Storm. Representing the power of transformation and the profound clarity found after a great rain.",
        "Alignment": "Invite cooling, stabilizing rituals to soothe the lightning of your internal atmosphere.",
        "Yoga": "Adho Mukha Svanasana (Downward Dog) to ground your energy while clearing the mind."
    },
    "Punarvasu": {
        "Essence": "The Star of Renewal. Like the return of the light after darkness, you bring a spirit of hope and restoration.",
        "Alignment": "Focus on expansive, airy spaces and light movement to honor your revitalizing nature.",
        "Yoga": "Trikonasana (Triangle Pose) to create space and reach for the light."
    },
    "Pushya": {
        "Essence": "The Star of Nourishment. A deeply caring and protective energy that provides a sanctuary for others to grow.",
        "Alignment": "Prioritize self-care and quiet reflection to replenish your naturally giving spirit.",
        "Yoga": "Setu Bandhasana (Bridge Pose) to support your heart and solar plexus."
    },
    "Ashlesha": {
        "Essence": "The Star of Entwinement. A deep, intuitive wisdom that penetrates the mysteries of the soul and the Earth.",
        "Alignment": "Use grounding rituals and moments of stillness to anchor your profound sensitivity.",
        "Yoga": "Bhujangasana (Cobra Pose) to awaken your intuitive vitality."
    },
    "Magha": {
        "Essence": "The Star of Power. Rooted in ancestral wisdom, you carry a noble dignity and a deep sense of purpose.",
        "Alignment": "Honor your lineage through quiet contemplation and practices that strengthen your core stability.",
        "Yoga": "Tadasana (Mountain Pose) to stand with the unwavering strength of your heritage."
    },
    "Purva Phalguni": {
        "Essence": "The Star of Prosperity. A vibrant, creative energy that celebrates the beauty, love, and joy of the human experience.",
        "Alignment": "Balance your zest for life with grounding practices to maintain your creative longevity.",
        "Yoga": "Anahatasana (Melting Heart Pose) to keep your heart open and receptive."
    },
    "Uttara Phalguni": {
        "Essence": "The Star of the Patron. Leading through service and stability, you act as a pillar for your community.",
        "Alignment": "Maintain a steady internal rhythm to support your role as a provider of strength.",
        "Yoga": "Virabhadrasana II (Warrior II) to focus your gaze and steady your foundation."
    },
    "Hasta": {
        "Essence": "The Star of the Hand. A skillful, manifesting energy that turns dreams into reality through focus and craft.",
        "Alignment": "Engage in tactile activities or crafts to channel your creative dexterity productively.",
        "Yoga": "Adho Mukha Svanasana (Downward Dog) focusing on the grounding of the palms."
    },
    "Chitra": {
        "Essence": "The Star of Opportunity. An artistic and architectural spirit that sees the inherent beauty in structure and design.",
        "Alignment": "Seek out aesthetically pleasing environments to soothe and inspire your internal world.",
        "Yoga": "Natarajasana (Dancer's Pose) to find the balance between structure and grace."
    },
    "Swati": {
        "Essence": "The Star of Independence. Like a young sprout in the wind, you value freedom and the power of the breath.",
        "Alignment": "Use heavy, grounding rituals to stay anchored when life's winds feel fast.",
        "Yoga": "Pranayama (Breathwork) to steady your independent spirit from within."
    },
    "Vishakha": {
        "Essence": "The Star of Purpose. A determined, focused energy that strives for long-term goals with unwavering commitment.",
        "Alignment": "Balance your drive with moments of soft, restorative rest to avoid internal tension.",
        "Yoga": "Garudasana (Eagle Pose) to find focus and concentration."
    },
    "Anuradha": {
        "Essence": "The Star of Devotion. A loyal and resilient spirit that blossoms through deep connection and hidden strength.",
        "Alignment": "Nurture your connections while maintaining a private sanctuary for your own emotional growth.",
        "Yoga": "Padmasana (Lotus Pose) to find the strength that blossoms in stillness."
    },
    "Jyeshtha": {
        "Essence": "The Star of Eldership. Carrying a powerful, protective wisdom that is earned through experience and mastery.",
        "Alignment": "Use grounding practices to manage your intense internal power and stay focused on your mission.",
        "Yoga": "Virabhadrasana I (Warrior I) to stand in your authentic power."
    },
    "Mula": {
        "Essence": "The Star of the Root. A deep, investigative energy that seeks the core truth by unearthing the foundations of life.",
        "Alignment": "Prioritize physical grounding and simple, earthy rituals to anchor your profound inquiries.",
        "Yoga": "Baddha Konasana (Bound Angle Pose) to ground your roots into the Earth."
    },
    "Purva Ashadha": {
        "Essence": "The Star of Invincibility. A spirited, optimistic energy that finds strength in the flow of life's challenges.",
        "Alignment": "Embrace fluid movement and hydration to honor your naturally resilient internal spirit.",
        "Yoga": "Surya Namaskar (Sun Salutations) to find flow in your strength."
    },
    "Uttara Ashadha": {
        "Essence": "The Star of Victory. A principled and disciplined spirit that achieves greatness through steady, ethical action.",
        "Alignment": "Maintain a clear internal structure through consistent, grounding daily rituals.",
        "Yoga": "Utkatasana (Chair Pose) to build steady, enduring strength."
    },
    "Shravana": {
        "Essence": "The Star of Listening. A wise, receptive energy that gains knowledge through silence and deep observation.",
        "Alignment": "Create a quiet internal atmosphere to better hear the subtle wisdom of the universe.",
        "Yoga": "Vrikshasana (Tree Pose) practiced in complete silence."
    },
    "Dhanishta": {
        "Essence": "The Star of Symphony. A rhythmic and resourceful energy that moves in harmony with the heartbeat of the world.",
        "Alignment": "Incorporate music or rhythmic movement into your day to align with your natural internal beat.",
        "Yoga": "Urdhva Dhanurasana (Wheel Pose) to open your heart to the world's rhythm."
    },
    "Shatabhisha": {
        "Essence": "The Star of a Thousand Healers. A visionary, independent soul who values the truth of the big picture and the mystery of the stars.",
        "Alignment": "Prioritize open spaces and silence to keep your vast, airy mind clear and aligned.",
        "Yoga": "Anjaneyasana (Low Lunge) to open your heart to the wide horizon."
    },
    "Purva Bhadrapada": {
        "Essence": "The Star of Transformation. A spiritual bridge between worlds, facilitating the deep cycles of soul-growth.",
        "Alignment": "Use warming, internal rituals to support your visionary and transformative nature.",
        "Yoga": "Savasana (Corpse Pose) to practice the art of letting go and transformation."
    },
    "Uttara Bhadrapada": {
        "Essence": "The Star of the Deep Woods. A steady, compassionate energy that finds strength in stillness and deep reflection.",
        "Alignment": "Prioritize time in nature to ground your profound internal wisdom and steady spirit.",
        "Yoga": "Sukhasana (Easy Pose) to find the depth within the stillness."
    },
    "Revati": {
        "Essence": "The Star of the Voyager. A compassionate, visionary spirit that guides others toward their final homecoming.",
        "Alignment": "Maintain a gentle internal atmosphere through soothing, water-based rituals and soft movement.",
        "Yoga": "Balasana (Child's Pose) to find safety and rest at the end of the journey."
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
    u_date = st.date_input("Birth Date", value=datetime(1957, 5, 22))
    u_time = st.time_input("Birth Time (Local)")
    u_city = st.text_input("Birth Location", placeholder="City, State, Country")

if st.button("Reveal My Alignment"):
    geolocator = Nominatim(user_agent="sky_sanctuary_topocentric")
    location = geolocator.geocode(u_city, language='en')
    
    if location:
        tf = TimezoneFinder()
        tz_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        
        if tz_str:
            timezone = pytz.timezone(tz_str)
            local_dt = timezone.localize(datetime.combine(u_date, u_time))
            utc_dt = local_dt.astimezone(pytz.utc)
            
            # --- THE UNIVERSAL CLOCK (Topocentric + True Lahiri) ---
            swe.set_sid_mode(swe.SIDM_LAHIRI) 
            swe.set_topo(location.longitude, location.latitude, 0) # Surface-level accuracy
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
            Your **Birth Sky** is the physical snapshot of the heavens exactly as they greeted you on the horizon. By utilizing Topocentric data and the Lahiri precision, we return to the light exactly as it was—grounded, accurate, and real. This 'Real-Sky Homecoming' accounts for the Earth's natural 24-degree wobble, providing the most precise foundation for your soulful alignment.
            """)
        else:
            st.error("Could not determine the time zone.")
    else:
        st.error("Location not found.")
