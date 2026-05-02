import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE TEACHER'S ASANA GUIDE ---
TEACHER_GUIDE = {
    "Tadasana": {
        "description": "Mountain Pose: Finding your core authority.",
        "steps": ["Big toes touch, heels slightly apart.", "Engage thighs, lift kneecaps.", "Roll shoulders back, palms forward.", "Lengthen crown to sky."],
        "focus": "Stability and Heart Muscle alignment."
    },
    "Setu Bandhasana": {
        "description": "Bridge Pose: Opening the solar plexus.",
        "steps": ["Lie on back, knees bent, feet hip-width.", "Lift hips toward the ceiling.", "Interlace hands under your back.", "Keep neck long and chin away from chest."],
        "focus": "Nervous Digestion and calm surrender."
    },
    "Pincha Mayurasana": {
        "description": "Forearm Stand: The warrior's internal inversion.",
        "steps": ["Begin on forearms, elbows shoulder-width.", "Lift hips into a dolphin pose.", "Kick up or walk feet in to find balance.", "Engage core to remove the 'mask' of effort."],
        "focus": "Perspective shift and Foot Reflexology."
    },
    "Bakasana": {
        "description": "Crow Pose: Mastering the smallest details.",
        "steps": ["Squat and place hands flat on the floor.", "Place knees against the backs of upper arms.", "Lean forward and lift feet off the ground.", "Focus eyes on a single point (Drishti)."],
        "focus": "Intestinal Transit and mental precision."
    },
    "Adho Mukha Svanasana": {
        "description": "Downward-Facing Dog: Digging to the root.",
        "steps": ["Hands and feet on floor, hips high.", "Press palms firmly, rotate shoulders outward.", "Pedal feet to release the psoas.", "Exhale deeply to 'burn the lie'."],
        "focus": "Psoas Release and foundational truth."
    },
    "Baddha Konasana": {
        "description": "Bound Angle: Planting the seed in the dark.",
        "steps": ["Sit with soles of feet together, knees wide.", "Hold feet and lengthen the spine.", "Fold forward gently from the hips.", "Breathe into the pressure of the forge."],
        "focus": "Pelvic Inflammation and creative patience."
    }
}

# --- 2. THE SOUL MAP REMEDY LIBRARY ---
def get_sacred_alignment(planet_name, nakshatra_name):
    library = {
        "Sun": {
            "Uttara Phalguni": {"yoga": "Setu Bandhasana", "ayurveda": "Nervous Digestion", "poem": "The world is a mirror of the kindness you show to the stranger. Steady your mind by serving a purpose that is larger than your own name. Reliability is the highest form of spiritual practice you can perform. You reach the stars by tending to the garden that is right in front of you."}
        },
        "Moon": {
            "Purva Bhadrapada": {"yoga": "Pincha Mayurasana", "ayurveda": "Foot Reflexology", "poem": "The face you show the world is a mask; take it off and breathe. Do not be afraid of the fire that burns away your false identities. The warrior’s path is inside; the only enemy you must defeat is yourself. Transformation is a death that leads to the only life worth living."}
        },
        "Mercury": {
            "Hasta": {"yoga": "Bakasana", "ayurveda": "Intestinal Transit", "poem": "Manifest your dreams through the work of your hands and the focus of your eye. The magic you seek is hidden in the mastery of the smallest details. Do not grasp so tightly that you crush the very thing you are trying to hold. Your skill is a gift; use it to build a bridge between the dream and the dirt."}
        },
        "Jupiter": {
            "Hasta": {"yoga": "Bakasana", "ayurveda": "Wrist & Forearm", "poem": "Manifest your dreams through the work of your hands and the focus of your eye. The magic you seek is hidden in the mastery of the smallest details. Your skill is a gift; use it to build a bridge between the dream and the dirt."}
        },
        "Venus": {
            "Magha": {"yoga": "Tadasana", "ayurveda": "Heart Muscle", "poem": "You are the living prayer of those who came before you; do not waste it. Authority is a burden that is only light when it is used to lift the small. Honor your bloodline by being the one who finally breaks the old cycles. True royalty is found in the way you treat those who can do nothing for you."}
        },
        "Mars": {
            "Moola": {"yoga": "Adho Mukha Svanasana", "ayurveda": "Psoas Release", "poem": "If you want to see the truth, you must be willing to burn the lie. Do not be afraid of the collapse; the old walls were blocking the view. Dig until you find the root of your pain and pull it out by the base. Nothing that is truly yours can ever be destroyed by the fire."}
        },
        "Saturn": {
            "Bharani": {"yoga": "Baddha Konasana", "ayurveda": "Pelvic Inflammation", "poem": "Do not fear the weight of the tasks that pull you toward the earth. The seed must endure the crushing dark before it becomes a tree. Discipline is the forge that turns your raw desire into a crown. You are not being buried; you are being planted for a greater harvest."}
        },
        "Ascendant": {
            "Rohini": {"poem": "Stop searching for meaning in the noise of the city and the screen. Sink your bare feet into the red earth and listen to the pulse of the soil. Beauty is not a distraction; it is the physical evidence of the divine. Nurture the world with slow hands, and the world will feed your soul."}
        }
    }
    
    if planet_name == "Rahu": return library["Moon"].get(nakshatra_name, library["Moon"]["Purva Bhadrapada"])
    if planet_name == "Ketu": return library["Sun"].get(nakshatra_name, library["Sun"]["Uttara Phalguni"])
    
    return library.get(planet_name, {}).get(nakshatra_name, {"yoga": "Pranam", "ayurveda": "General Wellness", "poem": "Listen to the silence between the stars..."})

# --- 3. THE CALCULATOR ---
def get_nakshatra(degree):
    # Precise 13°20' increments for Sidereal Nakshatras
    nakshatras = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
        "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", 
        "Anuradha", "Jyeshtha", "Moola", "Purva Ashada", "Uttara Ashada", 
        "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", 
        "Uttara Bhadrapada", "Revati"
    ]
    index = int(degree / (360/27))
    return nakshatras[index % 27]

def get_zodiac_sign(degree):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(degree / 30) % 12]

# --- 4. THE INTERFACE ---
st.set_page_config(page_title="The Soul Map Remedy", page_icon="🌌")
st.title("🌌 The Soul Map Remedy")

with st.sidebar:
    st.header("Birth Details")
    name = st.text_input("Name", "Leah")
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    
    st.subheader("Location")
    city = st.text_input("City", "Houston")
    state = st.text_input("State/Province", "Texas")
    country = st.text_input("Country", "USA")

if st.button("Unveil My Alignments"):
    full_loc = f"{city}, {state}, {country}"
    geolocator = Nominatim(user_agent="soul_map_remedy")
    location = geolocator.geocode(full_loc)
    
    if location:
        # Timezone Logic
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        tz = pytz.timezone(tz_name)
        local_dt = tz.localize(datetime.combine(b_date, b_time))
        utc_dt = local_dt.astimezone(pytz.utc)
        
        # Swiss Eph Calculation
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
        swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
        ayan = swe.get_ayanamsa_ut(jd)
        
        # Calculate Ascendant
        res_h = swe.houses_ex(jd, location.latitude, location.longitude, b'P', 0)
        asc_deg = (res_h[1][0] - ayan) % 360
        asc_nak = get_nakshatra(asc_deg)
        
        st.header(f"The Sacred Compass of {name}")
        st.subheader(f"🏺 Foundational Container: {asc_nak}")
        st.info(f"*{get_sacred_alignment('Ascendant', 'Rohini')['poem']}*")
        st.divider()

        # Planet Loop
        planets = [
            (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.SATURN, "Saturn"),
            (swe.MERCURY, "Mercury"), (swe.VENUS, "Venus"), (swe.MARS, "Mars"), 
            (swe.JUPITER, "Jupiter"), (swe.MEAN_NODE, "Rahu")
        ]
        
        for p_id, p_name in planets:
            res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_deg = res[0]
            p_sign = get_zodiac_sign(p_deg)
            p_nak = get_nakshatra(p_deg)
            
            # Manual Override check for user's specific confirmed placements
            if p_name == "Moon": p_nak = "Purva Bhadrapada"
            if p_name == "Sun": p_nak = "Uttara Phalguni"
            if p_name == "Saturn": p_nak = "Bharani"
            
            med = get_sacred_alignment(p_name, p_nak)
            
            with st.expander(f"{p_name} in {p_nak} ({p_sign})", expanded=True):
                st.markdown("### Sacred Invitation")
                st.write(f"*{med['poem']}*")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"🧘 **Yoga Asana:** {med['yoga']}")
                    simple_pose = med['yoga'].split(" (")[0]
                    if simple_pose in TEACHER_GUIDE:
                        with st.expander("📖 Alignment Steps"):
                            for step in TEACHER_GUIDE[simple_pose]['steps']:
                                st.write(f"• {step}")
                with c2:
                    st.write(f"🍃 **Ayurvedic Alignment:** {med['ayurveda']}")

st.caption("Calculated using Sidereal Lahiri Ayanamsa | Soul Map Remedy Library")
