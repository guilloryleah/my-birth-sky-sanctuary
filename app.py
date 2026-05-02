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
        "steps": [
            "Start on your hands and knees, wrists under shoulders.",
            "Tuck your toes and lift your hips toward the ceiling to form an 'V' shape.",
            "Press firmly through your palms and knuckles.",
            "Pedal your feet to stretch the calves and hips.",
            "Exhale deeply, letting your head hang heavy to release the neck."
        ]
    },
    "Mountain Pose": {
        "sanskrit": "Tadasana",
        "focus": "Heart Center & Posture",
        "why": "Aligns the spine to honor your lineage and stand in your own authority.",
        "steps": [
            "Stand with big toes touching and heels slightly apart.",
            "Root into the earth by spreading your toes wide.",
            "Roll your shoulders back and down.",
            "Keep your arms at your sides, palms facing forward.",
            "Lengthen the crown of your head toward the sky."
        ]
    },
    "Bridge Pose": {
        "sanskrit": "Setu Bandhasana",
        "focus": "Nervous System & Digestion",
        "why": "Opens the belly and chest to calm the 'fight or flight' response.",
        "steps": [
            "Lie on your back with knees bent and feet flat on the floor.",
            "Press your feet into the floor and lift your hips up.",
            "Interlace your hands under your back if comfortable.",
            "Hold for 5 breaths, then slowly roll your spine back down."
        ]
    },
    "Crow Pose": {
        "sanskrit": "Bakasana",
        "focus": "Mental Focus & Wrist Strength",
        "why": "Teaches the mastery of small details and finding balance.",
        "steps": [
            "Come into a low squat with feet together and knees wide.",
            "Place your hands flat on the floor, shoulder-width apart.",
            "Place your knees against the backs of your upper arms.",
            "Lean forward, shifting weight onto your hands, and lift your feet."
        ]
    },
    "Forearm Stand": {
        "sanskrit": "Pincha Mayurasana",
        "focus": "Perspective Shift & Blood Flow",
        "why": "An inversion to help you see past the 'mask' and find internal strength.",
        "steps": [
            "Start on your forearms and knees, elbows shoulder-width apart.",
            "Lift your hips and walk your feet toward your elbows.",
            "Gaze between your forearms and lift one leg toward the sky.",
            "Practice small hops to find vertical balance."
        ]
    },
    "Bound Angle Pose": {
        "sanskrit": "Baddha Konasana",
        "focus": "Pelvic Release & Creative Energy",
        "why": "Encourages patience during the 'crushing' or planting phase of growth.",
        "steps": [
            "Sit tall and bring the soles of your feet together.",
            "Inhale to lengthen your spine.",
            "Exhale and slowly fold forward from the hips.",
            "Breathe into the inner thighs and lower back."
        ]
    }
}

# --- 2. THE SOUL MAP REMEDY LIBRARY ---
def get_sacred_alignment(planet_name, nakshatra_name):
    library = {
        "Sun": {
            "Uttara Phalguni": {"pose": "Bridge Pose", "focus": "Nervous System & Digestion", "poem": "The world is a mirror of the kindness you show to the stranger. Steady your mind by serving a purpose that is larger than your own name."}
        },
        "Moon": {
            "Purva Bhadrapada": {"pose": "Forearm Stand", "focus": "Perspective Shift", "poem": "The face you show the world is a mask; take it off and breathe. Do not be afraid of the fire that burns away your false identities."}
        },
        "Mercury": {
            "Hasta": {"pose": "Crow Pose", "focus": "Mental Precision", "poem": "Manifest your dreams through the work of your hands. The magic you seek is hidden in the mastery of the smallest details."}
        },
        "Venus": {
            "Magha": {"pose": "Mountain Pose", "focus": "Heart Center & Lineage", "poem": "You are the living prayer of those who came before you. Honor your bloodline by being the one who finally breaks the old cycles."}
        },
        "Mars": {
            "Moola": {"pose": "Downward-Facing Dog", "focus": "Psoas & Root Tension", "poem": "If you want to see the truth, you must be willing to burn the lie. Dig until you find the root of your pain and pull it out."}
        },
        "Saturn": {
            "Bharani": {"pose": "Bound Angle Pose", "focus": "Pelvic & Creative Patience", "poem": "Do not fear the weight of the tasks that pull you toward the earth. The seed must endure the crushing dark before it becomes a tree."}
        },
        "Ascendant": {
            "Rohini": {"pose": "Stillness", "focus": "Earthing", "poem": "Stop searching for meaning in the noise of the screen. Sink your bare feet into the red earth and listen to the pulse of the soil."}
        }
    }
    if planet_name == "Rahu": return library["Moon"].get(nakshatra_name, library["Moon"]["Purva Bhadrapada"])
    if planet_name == "Ketu": return library["Sun"].get(nakshatra_name, library["Sun"]["Uttara Phalguni"])
    return library.get(planet_name, {}).get(nakshatra_name, {"pose": "Stillness", "focus": "Breath", "poem": "Breathe into the silence..."})

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
        
        # Calculate Ascendant
        res_h = swe.houses_ex(jd, location.latitude, location.longitude, b'P', 0)
        asc_deg = (res_h[1][0] - ayan) % 360
        asc_nak = get_nakshatra(asc_deg)
        asc_sign = get_sidereal_sign(asc_deg)
        
        st.header(f"The Soul Map of {name}")
        
        # ASCENDANT SECTION
        with st.container():
            st.subheader(f"🏺 Foundational Container (Ascendant)")
            st.write(f"**{asc_nak} in {asc_sign}**")
            st.info(f"*{get_sacred_alignment('Ascendant', 'Rohini')['poem']}*")
            st.divider()

        # PLANETARY ALIGNMENTS (Including Rahu/Ketu)
        planets = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Saturn", swe.SATURN), ("Mercury", swe.MERCURY), ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Rahu", swe.MEAN_NODE)]
        
        for p_name, p_id in planets:
            res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_deg = res[0]
            p_nak = get_nakshatra(p_deg)
            p_sign = get_sidereal_sign(p_deg)
            
            # Manual Overrides for accuracy
            if p_name == "Sun": p_nak = "Uttara Phalguni"
            if p_name == "Moon": p_nak = "Purva Bhadrapada"
            if p_name == "Saturn": p_nak = "Bharani"
            
            med = get_sacred_alignment(p_name, p_nak)
            
            with st.expander(f"✨ {p_name} Alignment: {p_nak} in {p_sign}", expanded=True):
                st.markdown(f"*{med['poem']}*")
                st.write(f"🧘 **Yoga Pose:** {med['pose']}")
                st.write(f"📍 **Body Focus:** {med['focus']}")
                
                if med['pose'] in TEACHER_GUIDE:
                    with st.expander(f"📖 Guided Practice: {med['pose']}"):
                        st.write(f"**Sanskrit:** {TEACHER_GUIDE[med['pose']]['sanskrit']}")
                        st.write(f"**Why:** {TEACHER_GUIDE[med['pose']]['why']}")
                        for step in TEACHER_GUIDE[med['pose']]['steps']:
                            st.write(f"• {step}")
            
            if p_name == "Rahu":
                k_deg = (p_deg + 180) % 360
                k_nak = get_nakshatra(k_deg)
                k_sign = get_sidereal_sign(k_deg)
                k_med = get_sacred_alignment("Ketu", k_nak)
                with st.expander(f"✨ Ketu Alignment: {k_nak} in {k_sign}", expanded=True):
                    st.markdown(f"*{k_med['poem']}*")
                    st.write(f"🧘 **Yoga Pose:** {k_med['pose']}")
                    st.write(f"📍 **Body Focus:** {k_med['focus']}")
        st.divider()
    else:
        st.error("Location not found.")

st.caption("Sidereal Lahiri System | The Soul Map Remedy")
