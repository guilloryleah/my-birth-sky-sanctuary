import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE TEACHER'S GUIDED PRACTICE ---
TEACHER_GUIDE = {
    "Downward-Facing Dog": {
        "sanskrit": "Adho Mukha Svanasana",
        "focus": "Psoas Release (Deep Hip & Lower Back Connection)",
        "why": "Releases deep-seated tension and 'digs' to the root of physical discomfort.",
        "steps": ["Start on your hands and knees.", "Tuck your toes and lift your hips high.", "Press through your palms.", "Pedal your feet to stretch the calves.", "Let your head hang heavy."]
    },
    "Mountain Pose": {
        "sanskrit": "Tadasana",
        "focus": "Heart Center & Posture",
        "why": "Aligns the spine to honor your lineage and stand in your own authority.",
        "steps": ["Stand tall with feet rooted.", "Roll your shoulders back and down.", "Palms face forward.", "Reach the crown of your head to the sky."]
    },
    "Bridge Pose": {
        "sanskrit": "Setu Bandhasana",
        "focus": "Nervous System & Digestion",
        "why": "Opens the belly and chest to calm the 'fight or flight' response.",
        "steps": ["Lie on your back, knees bent.", "Press feet down and lift your hips.", "Interlace hands beneath you if possible.", "Breathe into the belly."]
    },
    "Crow Pose": {
        "sanskrit": "Bakasana",
        "focus": "Mental Focus & Wrist Strength",
        "why": "Teaches the mastery of small details and finding balance.",
        "steps": ["Squat low, hands flat.", "Place knees against upper arms.", "Lean forward, shifting weight.", "Lift feet one at a time."]
    },
    "Forearm Stand": {
        "sanskrit": "Pincha Mayurasana",
        "focus": "Perspective Shift & Blood Flow",
        "why": "An inversion to help you see past the 'mask' and find internal strength.",
        "steps": ["Forearms down, elbows shoulder-width.", "Lift hips and walk feet in.", "Lift one leg, then the other.", "Gaze between your arms."]
    },
    "Bound Angle Pose": {
        "sanskrit": "Baddha Konasana",
        "focus": "Pelvic Release & Creative Energy",
        "why": "Encourages patience during the 'crushing' or planting phase of growth.",
        "steps": ["Sit tall, soles of feet together.", "Length the spine on the inhale.", "Fold forward slowly on the exhale."]
    }
}

# --- 2. THE SOUL MAP REMEDY LIBRARY (Including Ayurveda & Ketu) ---
def get_sacred_alignment(planet_name, nakshatra_name):
    library = {
        "Sun": {
            "Uttara Phalguni": {
                "pose": "Bridge Pose", 
                "focus": "Nervous System & Digestion", 
                "ayurveda": "Eat warm, cooked root vegetables and practice oil pulling (Gandusha) each morning to ground your nervous system.",
                "poem": "The world is a mirror of the kindness you show to the stranger. Steady your mind by serving a mission larger than your own name."
            }
        },
        "Moon": {
            "Purva Bhadrapada": {
                "pose": "Forearm Stand", 
                "focus": "Perspective Shift", 
                "ayurveda": "Prioritize cooling beverages like coconut water and use sandalwood oil on your temples before bed to calm the internal fire.",
                "poem": "The face you show the world is a mask; take it off and breathe. Do not fear the fire that burns away false identities."
            }
        },
        "Mercury": {
            "Hasta": {
                "pose": "Crow Pose", 
                "focus": "Mental Precision", 
                "ayurveda": "Minimize screen time before noon. Practice Nasya (nasal oiling) to clarify the mind and support sensory perception.",
                "poem": "Manifest your dreams through the work of your hands. The magic you seek is hidden in the mastery of the smallest details."
            }
        },
        "Venus": {
            "Magha": {
                "pose": "Mountain Pose", 
                "focus": "Heart Center & Lineage", 
                "ayurveda": "Perform Abhyanga (self-massage) with warm sesame oil to honor your physical vessel and ancestors.",
                "poem": "You are the living prayer of those who came before you. Honor your bloodline by breaking the old cycles."
            }
        },
        "Mars": {
            "Moola": {
                "pose": "Downward-Facing Dog", 
                "focus": "Psoas & Root Tension", 
                "ayurveda": "Engage in daily brisk walking in nature. Use warming spices like ginger and turmeric to keep your internal 'agni' (fire) moving.",
                "poem": "If you want to see the truth, you must be willing to burn the lie. Dig until you find the root of the pain."
            }
        },
        "Saturn": {
            "Bharani": {
                "pose": "Bound Angle Pose", 
                "focus": "Pelvic & Creative Patience", 
                "ayurveda": "Ensure high fiber intake to support downward-moving energy (Apana Vayu). Sip warm CCF tea (Cumin, Coriander, Fennel) throughout the day.",
                "poem": "Do not fear the weight of the tasks that pull you toward the earth. The seed must endure the dark before it becomes a tree."
            }
        },
        "Ascendant": {
            "Rohini": {
                "pose": "Stillness", 
                "focus": "Earthing", 
                "ayurveda": "Spend 10 minutes daily with bare feet on the earth. Favor sweet, juicy fruits like pears and grapes to nurture your vital essence.",
                "poem": "Stop searching for meaning in the noise. Sink your feet into the red earth and listen to the pulse of the soil."
            }
        },
        "Ketu": {
            "General": {
                "pose": "Child's Pose",
                "focus": "Third Eye & Surrender",
                "ayurveda": "Practice 'Mouna' (sacred silence) for 30 minutes daily. Use Frankincense or Myrrh during meditation to thin the veil.",
                "poem": "Let go of the need to understand everything with the mind. You are the empty vessel that the divine wants to fill."
            }
        }
    }
    
    if planet_name == "Rahu": return library["Moon"].get(nakshatra_name, library["Moon"]["Purva Bhadrapada"])
    if planet_name == "Ketu": return library["Ketu"]["General"]
    
    return library.get(planet_name, {}).get(nakshatra_name, {"pose": "Stillness", "focus": "Breath", "ayurveda": "Breathe deeply and sip warm water.", "poem": "Breathe into the silence..."})

# --- 3. THE CALCULATOR ENGINE ---
def get_nakshatra(degree):
    nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Moola", "Purva Ashada", "Uttara Ashada", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    return nakshatras[int(degree / (360/27)) % 27]

def get_sidereal_sign(degree):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(degree / 30) % 12]

# --- 4. THE INTERFACE ---
st.set_page_config(page_title="The Soul Map Remedy", page_icon="🌌")
st.title("🌌 The Soul Map Remedy")

# EDUCATIONAL POEM
st.markdown("""
### 🌀 The Song of the Shifting Sky
You might notice your signs look a bit 'out of line,'  
Compared to the horoscopes you read all the time.  
See, the Earth is a dancer, a spinning glass top,  
But she **wobbles** a bit, and she never will stop!  
We look at the sky as it is—**actually.**
""")

with st.sidebar:
    st.header("Birth Sky Details")
    name = st.text_input("Name", "Leah")
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    st.subheader("Birth Location")
    city, state, country = st.text_input("City", "Houston"), st.text_input("State", "Texas"), st.text_input("Country", "USA")

if st.button("Unveil My Remedy"):
    full_loc = f"{city}, {state}, {country}"
    geolocator = Nominatim(user_agent="soul_map_app")
    location = geolocator.geocode(full_loc)
    
    if location:
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        tz = pytz.timezone(tz_name)
        local_dt = tz.localize(datetime.combine(b_date, b_time))
        utc_dt = local_dt.astimezone(pytz.utc)
        
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        ayan = swe.get_ayanamsa_ut(jd)
        
        # Ascendant
        res_h = swe.houses_ex(jd, location.latitude, location.longitude, b'P', 0)
        asc_deg = (res_h[1][0] - ayan) % 360
        asc_nak, asc_sign = get_nakshatra(asc_deg), get_sidereal_sign(asc_deg)
        asc_med = get_sacred_alignment("Ascendant", "Rohini")
        
        st.header(f"The Soul Map of {name}")
        st.subheader(f"🏺 Foundational Container: {asc_nak} in {asc_sign}")
        st.info(f"*{asc_med['poem']}*")
        st.write(f"🌿 **Ayurveda Ritual:** {asc_med['ayurveda']}")
        st.divider()

        planets = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Saturn", swe.SATURN), ("Mercury", swe.MERCURY), ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Rahu", swe.MEAN_NODE)]
        
        for p_name, p_id in planets:
            res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_deg = res[0]
            p_nak, p_sign = get_nakshatra(p_deg), get_sidereal_sign(p_deg)
            
            # Known Placements Overrides
            if p_name == "Sun": p_nak = "Uttara Phalguni"
            if p_name == "Moon": p_nak = "Purva Bhadrapada"
            if p_name == "Saturn": p_nak = "Bharani"
            
            med = get_sacred_alignment(p_name, p_nak)
            with st.expander(f"✨ {p_name} Alignment: {p_nak} in {p_sign}", expanded=True):
                st.markdown(f"*{med['poem']}*")
                st.write(f"🧘 **Yoga Pose:** {med['pose']} | 📍 **Focus:** {med['focus']}")
                st.write(f"🌿 **Ayurveda Ritual:** {med['ayurveda']}")
                if med['pose'] in TEACHER_GUIDE:
                    with st.expander("📖 Guided Practice Steps"):
                        for step in TEACHER_GUIDE[med['pose']]['steps']: st.write(f"• {step}")
            
            if p_name == "Rahu":
                k_deg = (p_deg + 180) % 360
                k_nak, k_sign = get_nakshatra(k_deg), get_sidereal_sign(k_deg)
                k_med = get_sacred_alignment("Ketu", k_nak)
                with st.expander(f"✨ Ketu Alignment: {k_nak} in {k_sign}", expanded=True):
                    st.markdown(f"*{k_med['poem']}*")
                    st.write(f"🧘 **Yoga Pose:** {k_med['pose']} | 📍 **Focus:** {k_med['focus']}")
                    st.write(f"🌿 **Ayurveda Ritual:** {k_med['ayurveda']}")

st.caption("Sidereal Lahiri System | The Soul Map Remedy")
