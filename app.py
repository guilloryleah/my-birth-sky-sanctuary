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
    },
    "Child's Pose": {
        "sanskrit": "Balasana",
        "focus": "Third Eye & Surrender",
        "why": "A pose of complete release to quiet the ego and listen to the soul.",
        "steps": ["Kneel on the floor, big toes touching.", "Sit on your heels and separate your knees.", "Fold forward, resting forehead on the mat.", "Breathe into your back."]
    }
}

# --- 2. THE SOUL MAP REMEDY LIBRARY ---
def get_sacred_alignment(planet_name, nakshatra_name):
    library = {
        "Sun": {
            "Uttara Phalguni": {
                "pose": "Bridge Pose", 
                "focus": "Nervous System & Digestion", 
                "ayurveda": "Eat warm, cooked root vegetables and practice oil pulling each morning.",
                "poem": "The world is a mirror of the kindness you show to the stranger. Steady your mind by serving a purpose larger than your name."
            }
        },
        "Moon": {
            "Purva Bhadrapada": {
                "pose": "Forearm Stand", 
                "focus": "Perspective Shift", 
                "ayurveda": "Prioritize cooling beverages and sandalwood oil on your temples before bed.",
                "poem": "The face you show the world is a mask; take it off and breathe. Do not fear the fire that burns away false identities."
            }
        },
        "Mercury": {
            "Hasta": {
                "pose": "Crow Pose", 
                "focus": "Mental Precision", 
                "ayurveda": "Practice Nasya (nasal oiling) and minimize screen time before noon.",
                "poem": "Manifest your dreams through the work of your hands. The magic you seek is hidden in the mastery of small details."
            }
        },
        "Venus": {
            "Magha": {
                "pose": "Mountain Pose", 
                "focus": "Heart Center & Lineage", 
                "ayurveda": "Perform Abhyanga (self-massage) with warm sesame oil to honor your lineage.",
                "poem": "You are the living prayer of those who came before you. Honor your bloodline by breaking the old cycles."
            }
        },
        "Mars": {
            "Moola": {
                "pose": "Downward-Facing Dog", 
                "focus": "Psoas & Root Tension", 
                "ayurveda": "Engage in daily brisk walking in nature and use warming spices like ginger.",
                "poem": "If you want to see the truth, you must be willing to burn the lie. Dig until you find the root of your pain."
            }
        },
        "Saturn": {
            "Bharani": {
                "pose": "Bound Angle Pose", 
                "focus": "Pelvic & Creative Patience", 
                "ayurveda": "Support downward energy with high fiber intake and warm CCF tea.",
                "poem": "Do not fear the weight of tasks that pull you toward the earth. The seed must endure the dark before it becomes a tree."
            }
        },
        "Ascendant": {
            "Rohini": {
                "pose": "Stillness", 
                "focus": "Earthing", 
                "ayurveda": "Spend 10 minutes daily with bare feet on the earth. Favor juicy fruits like pears and grapes.",
                "poem": "Stop searching for meaning in the noise. Sink your feet into the red earth and listen to the pulse of the soil."
            }
        },
        "Ketu": {
            "General": {
                "pose": "Child's Pose",
                "focus": "Third Eye & Surrender",
                "ayurveda": "Practice 30 minutes of sacred silence (Mouna) daily. Use Frankincense during meditation.",
                "poem": "Let go of the need to understand with the mind. You are the empty vessel that the divine wants to fill."
            }
        }
    }
    
    if planet_name == "Rahu": return library["Moon"].get(nakshatra_name, library["Moon"]["Purva Bhadrapada"])
    if planet_name == "Ketu": return library["Ketu"]["General"]
    
    return library.get(planet_name, {}).get(nakshatra_name, {"pose": "Stillness", "focus": "Breath", "ayurveda": "Breathe deeply.", "poem": "Breathe into the silence..."})

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

# THE EDUCATIONAL POEM
st.markdown("""
### 🌀 The Song of the Shifting Sky
*A little secret for the curious soul...*

You might notice your signs look a bit 'out of line,'  
Compared to the horoscopes you read all the time.  
See, the Earth is a dancer, a spinning glass top,  
But she **wobbles** a bit, and she never will stop!

Over thousands of years, she’s tilted her head,  
The stars shifted left while the calendar sped.  
While others look back at where stars *used* to be,  
We look at the sky as it is—**actually.**

So if you've moved back by a sign or a space,  
Don't worry, dear heart, you're in the right place.  
It’s not a mistake, or a glitch, or a lie—  
It’s just how we dance with the **real, living sky.**
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
        
        # Calculate Ascendant
        res_h = swe.houses_ex(jd, location.latitude, location.longitude, b'P', 0)
        asc_deg = (res_h[1][0] - ayan) % 360
        asc_nak, asc_sign = get_nakshatra(asc_deg), get_sidereal_sign(asc_deg)
        asc_med = get_sacred_alignment("Ascendant", "Rohini")
        
        st.header(f"The Soul Map of {name}")
        
        # ASCENDANT DISPLAY
        st.subheader(f"🏺 Foundational Container (Ascendant)")
        st.markdown(f"### **{asc_nak} in {asc_sign}**")
        st.info(f"*{asc_med['poem']}*")
        st.write(f"🌿 **Ayurveda Ritual:** {asc_med['ayurveda']}")
        st.divider()

        # PLANETARY ALIGNMENTS
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
                    if k_med['pose'] in TEACHER_GUIDE:
                        with st.expander("📖 Guided Practice Steps"):
                            for step in TEACHER_GUIDE[k_med['pose']]['steps']: st.write(f"• {step}")
        st.divider()
    else:
        st.error("Location not found.")

# --- 5. THE SACRED DISCLAIMER ---
st.markdown("""
---
### ⚖️ A Note on Your Journey
The suggestions provided in this Soul Map—including the yoga poses, Ayurvedic rituals, and spiritual poems—are intended for **educational and spiritual alignment purposes only**. 

I am an **astrologer and educator**, not a medical doctor or licensed healthcare professional. These remedies are not meant to diagnose, treat, or cure any physical or mental condition. Please consult with your physician before beginning any new exercise or dietary routine. 

*Honor your body, trust your intuition, and move with grace.*
""")

st.caption("Sidereal Lahiri System | The Soul Map Remedy")
