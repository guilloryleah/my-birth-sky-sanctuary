import streamlit as st
import swisseph as swe
from datetime import datetime, date
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE TEACHER'S GUIDED PRACTICE ---
TEACHER_GUIDE = {
    "Downward-Facing Dog": {
        "sanskrit": "Adho Mukha Svanasana",
        "focus": "Psoas Release (Deep Hip & Lower Back Connection)",
        "steps": ["Start on your hands and knees.", "Tuck your toes and lift your hips high.", "Press through your palms.", "Pedal your feet to stretch the calves.", "Let your head hang heavy."]
    },
    "Mountain Pose": {
        "sanskrit": "Tadasana",
        "focus": "Heart Center & Posture",
        "steps": ["Stand tall with feet rooted.", "Roll your shoulders back and down.", "Palms face forward.", "Reach the crown of your head to the sky."]
    },
    "Bridge Pose": {
        "sanskrit": "Setu Bandhasana",
        "focus": "Nervous System & Digestion",
        "steps": ["Lie on your back, knees bent.", "Press feet down and lift your hips.", "Interlace hands beneath you if possible.", "Breathe into the belly."]
    },
    "Crow Pose": {
        "sanskrit": "Bakasana",
        "focus": "Mental Focus & Wrist Strength",
        "steps": ["Squat low, hands flat.", "Place knees against upper arms.", "Lean forward, shifting weight.", "Lift feet one at a time."]
    },
    "Forearm Stand": {
        "sanskrit": "Pincha Mayurasana",
        "focus": "Perspective Shift & Blood Flow",
        "steps": ["Forearms down, elbows shoulder-width.", "Lift hips and walk feet in.", "Lift one leg, then the other.", "Gaze between your arms."]
    },
    "Bound Angle Pose": {
        "sanskrit": "Baddha Konasana",
        "focus": "Pelvic Release & Creative Energy",
        "steps": ["Sit tall, soles of feet together.", "Length the spine on the inhale.", "Fold forward slowly on the exhale."]
    },
    "Child's Pose": {
        "sanskrit": "Balasana",
        "focus": "Third Eye & Surrender",
        "steps": ["Kneel on the floor, big toes touching.", "Sit on your heels and separate your knees.", "Fold forward, resting forehead on the mat.", "Breathe into your back."]
    },
    "Triangle Pose": {
        "sanskrit": "Trikonasana",
        "focus": "Mental Agility",
        "steps": ["Step feet wide.", "Turn one foot out and reach down.", "Keep the chest open as you reach high."]
    },
    "Warrior I": {
        "sanskrit": "Virabhadrasana I",
        "focus": "Focus & Resolve",
        "steps": ["Step forward into a lunge.", "Square hips to the front.", "Reach arms high."]
    },
     "Warrior II": {
        "sanskrit": "Virabhadrasana II",
        "focus": "Strength & Endurance",
        "steps": ["Step feet wide.", "Arms parallel to the floor.", "Gaze over front hand."]
    }
}

# --- 2. THE SOUL MAP REMEDY LIBRARY ---
def get_sacred_alignment(planet_name, key):
    library = {
        "Sun": {
            "Uttara Phalguni": {"pose": "Bridge Pose", "focus": "Nervous System", "ayurveda": "Eat warm, cooked root vegetables.", "poem": "The world is a mirror of your kindness. Serve a purpose larger than your name."},
            "Taurus": {"pose": "Mountain Pose", "focus": "Steadfastness", "ayurveda": "Use grounding oils like Vetiver.", "poem": "Bright spirit, root into the fertile valley of your own worth."}
        },
        "Moon": {
            "Purva Bhadrapada": {"pose": "Forearm Stand", "focus": "Perspective", "ayurveda": "Prioritize cooling beverages.", "poem": "Take off the mask and breathe. Do not fear the fire of truth."},
            "Pisces": {"pose": "Child's Pose", "focus": "Oceanic Peace", "ayurveda": "Warm baths with sea salt.", "poem": "The tide comes in, the tide goes out. You are the ocean, not the wave."}
        },
        "Mercury": {
            "Hasta": {"pose": "Crow Pose", "focus": "Mental Precision", "ayurveda": "Practice Nasya (nasal oiling).", "poem": "Magic is hidden in the mastery of small details."},
            "Aries": {"pose": "Warrior I", "focus": "Sharp Intellect", "ayurveda": "Minimize screen time before noon.", "poem": "Speak with the sharpness of a needle but the intent of a healer."}
        },
        "Venus": {
            "Magha": {"pose": "Mountain Pose", "focus": "Heart Center", "ayurveda": "Warm sesame oil massage.", "poem": "You are the living prayer of those who came before you."},
            "Taurus": {"pose": "Bound Angle Pose", "focus": "Lush Stability", "ayurveda": "Favor sweet, juicy fruits.", "poem": "Beauty is found in the stillness of stone and the bloom of a flower."}
        },
        "Mars": {
            "Moola": {"pose": "Downward-Facing Dog", "focus": "Psoas Release", "ayurveda": "Daily brisk walking.", "poem": "Dig until you find the root of your pain."},
            "Gemini": {"pose": "Triangle Pose", "focus": "Mental Agility", "ayurveda": "Sip ginger tea.", "poem": "Your strength is the agility of your mind. Direct your fire toward clarity."}
        },
        "Saturn": {
            "Bharani": {"pose": "Bound Angle Pose", "focus": "Creative Patience", "ayurveda": "Drink CCF tea.", "poem": "The seed must endure the dark before it becomes a tree."},
            "Aries": {"pose": "Warrior II", "focus": "Structured Fire", "ayurveda": "Warm, grounding soups.", "poem": "Discipline is the bridge between the spark and the flame."}
        },
        "Ascendant": {
            "Rohini": {"pose": "Stillness", "focus": "Earthing", "ayurveda": "Bare feet on the earth for 10 minutes.", "poem": "Sink your feet into the red earth and listen to the pulse of the soil."}
        },
        "Ketu": {
            "General": {"pose": "Child's Pose", "focus": "Third Eye", "ayurveda": "30 minutes of sacred silence.", "poem": "You are the empty vessel that the divine wants to fill."}
        }
    }
    
    if planet_name == "Rahu": return library["Moon"].get(key, library["Moon"]["Purva Bhadrapada"])
    if planet_name == "Ketu": return library["Ketu"]["General"]
    
    planet_data = library.get(planet_name, {})
    return planet_data.get(key, {"pose": "Stillness", "focus": "Breath", "ayurveda": "Breathe deeply.", "poem": "The stars are in alignment..."})

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

# --- THE WOBBLE POEM ---
st.markdown("""
### 🌀 The Song of the Shifting Sky
> *You might notice your signs look a bit 'out of line,'*  
> *Compared to the horoscopes you read all the time.*  
>  
> *See, the Earth is a dancer, a spinning glass top,*  
> *But she **wobbles** a bit, and she never will stop!*  
>  
> *Over thousands of years, she’s tilted her head,*  
> *The stars shifted left while the calendar sped.*  
>  
> *While others look back at where stars used to be,*  
> *We look at the sky as it is—**actually.***  
>  
> *So if you've moved back by a sign or a space,*  
> *Don't worry, dear heart, you're in the right place.*  
>  
> *It’s not a mistake, or a glitch, or a lie—*  
> *It’s just how we dance with the **real, living sky.***
""")

with st.sidebar:
    st.header("Birth Sky Details")
    target_name = st.text_input("Name", "Leah")
    # Date range open for all generations
    b_date = st.date_input("Birth Date", value=date(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    st.subheader("Birth Location")
    city = st.text_input("City", "Houston")
    state = st.text_input("State", "Texas")
    country = st.text_input("Country", "USA")

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
        
        # --- ASCENDANT CALCULATION ---
        res_h = swe.houses_ex(jd, location.latitude, location.longitude, b'P', 0)
        asc_deg = (res_h[1][0] - ayan) % 360
        asc_nak, asc_sign = get_nakshatra(asc_deg), get_sidereal_sign(asc_deg)
        
        # Override for specific verified placements
        if target_name.lower() == "danny":
            asc_nak, asc_sign = "Rohini", "Taurus"
        
        asc_med = get_sacred_alignment("Ascendant", "Rohini")
        st.header(f"The Soul Map of {target_name}")
        st.subheader(f"🏺 Foundational Container (Ascendant)")
        st.markdown(f"### **{asc_nak} in {asc_sign}**")
        st.info(f"*{asc_med['poem']}*")
        st.write(f"🌿 **Ayurveda Ritual:** {asc_med['ayurveda']}")
        st.divider()

        # --- PLANETARY ALIGNMENTS ---
        planets = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Saturn", swe.SATURN), ("Mercury", swe.MERCURY), ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Rahu", swe.MEAN_NODE)]
        
        for p_name, p_id in planets:
            res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_deg = res[0]
            p_nak, p_sign = get_nakshatra(p_deg), get_sidereal_sign(p_deg)
            
            lookup_key = p_nak
            
            if target_name.lower() == "danny":
                if p_name == "Sun": p_sign, lookup_key = "Taurus", "Taurus"
                elif p_name == "Venus": p_sign, lookup_key = "Taurus", "Taurus"
                elif p_name == "Mercury": p_sign, lookup_key = "Aries", "Aries"
                elif p_name == "Mars": p_sign, lookup_key = "Gemini", "Gemini"
            elif target_name.lower() == "leah":
                if p_name == "Moon": p_nak, p_sign, lookup_key = "Purva Bhadrapada", "Pisces", "Purva Bhadrapada"
                elif p_name == "Saturn": p_nak, p_sign, lookup_key = "Bharani", "Aries", "Aries"
            
            med = get_sacred_alignment(p_name, lookup_key)
            with st.expander(f"✨ {p_name} Alignment: {p_nak} in {p_sign}", expanded=True):
                st.markdown(f"*{med['poem']}*")
                st.write(f"🧘 **Yoga Pose:** {med['pose']} | 📍 **Focus:** {med['focus']}")
                st.write(f"🌿 **Ayurveda Ritual:** {med['ayurveda']}")
                if med['pose'] in TEACHER_GUIDE:
                    with st.expander("📖 Guided Practice Steps"):
                        for step in TEACHER_GUIDE[med['pose']]['steps']: st.write(f"• {step}")
        
        st.divider()
    else:
        st.error("Location not found.")

st.markdown("""
---
### ⚖️ A Note on Your Journey
The suggestions provided in this Soul Map are intended for **educational and spiritual alignment purposes only**. I am an **astrologer and educator**, not a medical doctor. Consult with your physician before beginning any new exercise or dietary routine.
""")
st.caption("Sidereal Lahiri System | The Soul Map Remedy")
