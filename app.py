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
        "focus": "Psoas Release",
        "steps": ["Start on hands and knees.", "Lift hips high, pressing through palms.", "Let the head hang heavy."]
    },
    "Mountain Pose": {
        "sanskrit": "Tadasana",
        "focus": "Heart Center & Grounding",
        "steps": ["Stand tall with feet rooted.", "Roll shoulders back.", "Reach the crown of head to the sky."]
    },
    "Bridge Pose": {
        "sanskrit": "Setu Bandhasana",
        "focus": "Nervous System & Digestion",
        "steps": ["Lie on your back, knees bent.", "Press feet down and lift your hips.", "Interlace hands beneath you.", "Breathe into the belly."]
    },
    "Child's Pose": {
        "sanskrit": "Balasana",
        "focus": "Surrender",
        "steps": ["Kneel, toes touching.", "Fold forward, resting forehead on the mat.", "Breathe into the back."]
    }
}

# --- 2. UNIVERSAL REMEDY LIBRARY ---
def get_sacred_alignment(planet_name, nakshatra, sign):
    # Library based on your specified natal placements
    library = {
        "Sun": {"Taurus": {"pose": "Mountain Pose", "poem": "Root into the fertile valley of your worth.", "ayurveda": "Use grounding oils like Vetiver."}},
        "Moon": {"Pisces": {"pose": "Child's Pose", "poem": "You are the ocean, not the wave.", "ayurveda": "Warm baths with sea salt."}},
        "Mercury": {"Aries": {"pose": "Warrior I", "poem": "Speak with the sharpness of a needle and the intent of a healer.", "ayurveda": "Minimize screen time before noon."}},
        "Venus": {"Taurus": {"pose": "Bound Angle Pose", "poem": "Beauty is found in the stillness of stone.", "ayurveda": "Favor sweet, juicy fruits."}},
        "Mars": {"Gemini": {"pose": "Triangle Pose", "poem": "Your strength is the agility of your mind.", "ayurveda": "Sip ginger tea."}},
        "Saturn": {"Aries": {"pose": "Warrior II", "poem": "Discipline is the bridge between the spark and the flame.", "ayurveda": "Warm, grounding soups."}},
        "Ascendant": {"Rohini": {"pose": "Stillness", "poem": "Sink your feet into the red earth.", "ayurveda": "Bare feet on the soil for 10 minutes."}}
    }
    
    planet_data = library.get(planet_name, {})
    match = planet_data.get(sign) if sign in planet_data else planet_data.get(nakshatra)
    
    if match:
        return match
    else:
        return {
            "pose": "Child's Pose",
            "poem": f"The stars whisper of {nakshatra}. Observe the breath and find your center.",
            "ayurveda": "Drink warm water and practice 5 minutes of silence."
        }

# --- 3. THE CALCULATOR ENGINE ---
def get_nakshatra(degree):
    nakshatras = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Moola", "Purva Ashada", "Uttara Ashada", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    return nakshatras[int(degree / (360/27)) % 27]

def get_sidereal_sign(degree):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(degree / 30) % 12]

def format_dms(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    return f"{d}° {m}'"

# --- 4. THE INTERFACE ---
st.set_page_config(page_title="The Soul Map Remedy", page_icon="🌌")
st.title("🌌 The Soul Map Remedy")

# RESTORED: THE WOBBLE POEM
st.markdown("""
### 🌀 The Song of the Shifting Sky
> *You might notice your signs look a bit 'out of line,'*  
> *Compared to the horoscopes you read all the time.*  
> *See, the Earth is a dancer, a spinning glass top,*  
> *But she **wobbles** a bit, and she never will stop!*  
>  
> *Over thousands of years, she’s tilted her head,*  
> *The stars shifted left while the calendar sped.*  
> *While others look back at where stars used to be,*  
> *We look at the sky as it is—**actually.***  
>  
> *So if you've moved back by a sign or a space,*  
> *Don't worry, dear heart, you're in the right place.*  
> *It’s not a mistake, or a glitch, or a lie—*  
> *It’s just how we dance with the **real, living sky.***
""")

with st.sidebar:
    st.header("Birth Details")
    target_name = st.text_input("Name", "Leah")
    b_date = st.date_input("Birth Date", value=date(1969, 9, 24), min_value=date(1, 1, 1))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    
    st.subheader("Location")
    city = st.text_input("City", "Houston")
    state = st.text_input("State", "Texas")
    # RESTORED: COUNTRY FIELD
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
        
        # HOUSE/ASCENDANT CALCULATION
        res_h = swe.houses_ex(jd, location.latitude, location.longitude, b'P', 0)
        asc_deg = (res_h[1][0] - ayan) % 360
        asc_nak, asc_sign = get_nakshatra(asc_deg), get_sidereal_sign(asc_deg)
        
        st.header(f"The Soul Map of {target_name}")
        st.subheader(f"🏺 Ascendant: {asc_nak} in {asc_sign} ({format_dms(asc_deg % 30)})")
        
        med = get_sacred_alignment("Ascendant", asc_nak, asc_sign)
        st.info(f"*{med['poem']}*")
        st.write(f"🌿 **Ayurveda:** {med['ayurveda']}")
        st.divider()

        # PLANETARY CALCULATIONS
        planets = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Saturn", swe.SATURN), ("Mercury", swe.MERCURY), ("Venus", swe.VENUS), ("Mars", swe.MARS)]
        
        for p_name, p_id in planets:
            res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_deg = res[0]
            p_nak, p_sign = get_nakshatra(p_deg), get_sidereal_sign(p_deg)
            med = get_sacred_alignment(p_name, p_nak, p_sign)
            
            with st.expander(f"✨ {p_name}: {p_nak} in {p_sign} ({format_dms(p_deg % 30)})", expanded=True):
                st.markdown(f"*{med['poem']}*")
                st.write(f"🧘 **Yoga:** {med['pose']} | 🌿 **Ayurveda:** {med['ayurveda']}")
                if med['pose'] in TEACHER_GUIDE:
                    with st.expander("📖 Practice Steps"):
                        for step in TEACHER_GUIDE[med['pose']]['steps']: st.write(f"• {step}")
    else:
        st.error("Location not found.")

# RESTORED: MEDICAL DISCLAIMER
st.markdown("""
---
### ⚖️ A Note on Your Journey
The suggestions provided in this Soul Map are intended for **educational and spiritual alignment purposes only**. I am an **astrologer and educator**, not a medical doctor. Consult with your physician before beginning any new exercise or dietary routine.
""")
st.caption("Sidereal Lahiri System | Educational Purposes Only")
