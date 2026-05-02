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
        "steps": ["Begin on forearms, elbows shoulder-width.", "Lift hips into a forearm 'down-dog' (Dolphin).", "Kick up or walk feet in to find vertical balance.", "Engage core to remove the 'mask' of effort."],
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
# Integrating your refined, unmistakable poems
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
    
    # Logic to fetch the node alignments (Rahu/Ketu)
    if planet_name == "Rahu": return library["Moon"].get(nakshatra_name, {})
    if planet_name == "Ketu": return library["Sun"].get(nakshatra_name, {})
    
    planet_data = library.get(planet_name, {})
    return planet_data.get(nakshatra_name, {"yoga": "Pranam", "ayurveda": "Prana", "poem": "Listen to the silence..."})

# --- 3. THE ASTRONOMY ENGINE (Summarized for brevity) ---
def calculate_birth_sky(y, m, d, h, mn, lat, lon):
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    jd = swe.julday(y, m, d, h + mn/60.0)
    ayan = swe.get_ayanamsa_ut(jd)
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    # Example calculation for Sun
    res, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
    p_sign = signs[int(res[0] / 30)]
    # In a full app, you'd loop all planets here...
    return {"Sun": {"sign": p_sign, "nak": "Uttara Phalguni"}} # Mock result for structure

# --- 4. THE SOUL MAP REMEDY UI ---
st.set_page_config(page_title="The Soul Map Remedy", page_icon="🌌")
st.title("🌌 The Soul Map Remedy")
st.write("---")

# User Input
with st.sidebar:
    name = st.text_input("Name", "Leah")
    b_date = st.date_input("Birth Date", value=datetime(1975, 9, 20))
    b_time = st.time_input("Birth Time")
    location = st.text_input("Birth Location", "Cypress, TX")

if st.button("Unveil My Alignments"):
    st.header(f"The Sacred Compass of {name}")
    
    # Ascendant Anchor
    asc_med = get_sacred_alignment("Ascendant", "Rohini")
    st.subheader("🏺 Foundational Container: Rohini")
    st.info(asc_med['poem'])
    st.divider()

    # Planary Cards (Example Loop)
    planets = ["Sun", "Moon", "Mercury", "Jupiter", "Venus", "Mars", "Saturn"]
    for p in planets:
        # Mocking data retrieval for this example
        nak = "Hasta" if p in ["Mercury", "Jupiter"] else ("Magha" if p=="Venus" else "Moola")
        # Real code would use calculated values
        
        med = get_sacred_alignment(p, nak)
        
        with st.expander(f"✨ {p} in {nak}", expanded=True):
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown("### Sacred Invitation")
                st.write(f"*{med['poem']}*")
            with col2:
                st.markdown(f"🧘 **Yoga Asana:** {med['yoga']}")
                st.markdown(f"🍃 **Ayurvedic Alignment:** {med['ayurveda']}")
                
                # Teacher's guide lookup
                pose_name = med['yoga'].split(" (")[0]
                if pose_name in TEACHER_GUIDE:
                    with st.expander("📖 How to Align"):
                        st.write(TEACHER_GUIDE[pose_name]['description'])
                        for step in TEACHER_GUIDE[pose_name]['steps']:
                            st.write(f"- {step}")

st.caption("Based on Sidereal Calculations & The Soul Map Remedy Library.")
