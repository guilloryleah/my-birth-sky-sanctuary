import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE ASANA & AYURVEDA TEACHER GUIDE ---
# Explains the physical 'How-To' for the medicine prescribed in your poems.
TEACHER_GUIDE = {
    "Tadasana": {
        "description": "Mountain Pose: The blueprint for all standing postures.",
        "steps": [
            "Stand with big toes touching, heels slightly apart.",
            "Lift your kneecaps by engaging your thighs.",
            "Roll shoulders back and down, palms facing forward to open the chest.",
            "Lengthen the crown of your head toward the sky."
        ],
        "focus": "Stability, spinal integrity, and heart muscle strengthening."
    },
    "Savasana": {
        "description": "Corpse Pose: Total conscious relaxation.",
        "steps": [
            "Lie flat on your back with arms and legs spread comfortably.",
            "If using an eye pillow, place it gently over the closed eyes.",
            "Let the breath be natural and the body feel heavy on the earth."
        ],
        "focus": "Curing cranial pressure and resetting the nervous system."
    },
    "Adho Mukha Svanasana": {
        "description": "Downward-Facing Dog: A grounding inversion.",
        "steps": [
            "Start on hands and knees, then tuck toes and lift hips high.",
            "Press firmly through the palms, spreading the fingers wide.",
            "Reach heels toward the floor to lengthen the spine and psoas."
        ],
        "focus": "Releasing hip memory and destroying false foundations."
    },
    "Baddha Konasana": {
        "description": "Bound Angle Pose: A deep hip and groin opener.",
        "steps": [
            "Sit with the soles of your feet together, knees dropping to the sides.",
            "Hold your feet or ankles and sit up tall through the spine.",
            "Gently lean forward if the body allows, keeping the back flat."
        ],
        "focus": "Pelvic inflammation and reproductive vitality."
    },
    "Viparita Karani": {
        "description": "Legs-Up-The-Wall: A restorative inversion.",
        "steps": [
            "Sit sideways against a wall and swing your legs up as you lie back.",
            "Rest your arms by your sides, palms up.",
            "Stay for 5-10 minutes to allow fluids to drain from the legs."
        ],
        "focus": "Eye strain, facial lustre, and hormonal flow."
    },
    "Bakasana": {
        "description": "Crow Pose: A balance that builds focus.",
        "steps": [
            "Squat down and place palms flat on the floor, shoulder-width apart.",
            "Place knees against the back of your upper arms.",
            "Lean forward, shifting weight into hands, and lift one or both feet."
        ],
        "focus": "Intestinal transit, wrist strength, and ghost allergies."
    }
}

# --- 2. THE MASTER COSMIC PHARMACOPEIA LIBRARY ---
def get_holistic_medicine(planet_name, nakshatra_name):
    library = {
        "Mars": {
            "Ashwini": {"yoga": "Savasana with Eye Pillow", "ayurveda": "Cranial Pressure", "poem": "Heal the ghost of the old self before you outrun it."},
            "Bharani": {"yoga": "Baddha Konasana", "ayurveda": "Pelvic Inflammation", "poem": "Carry the weight until it turns into a wing."},
            "Krittika": {"yoga": "Utkatasana", "ayurveda": "Blood Purifier", "poem": "Let your truth be a cauterizing flame."},
            "Rohini": {"yoga": "Vrksasana", "ayurveda": "Neck & Throat", "poem": "Plant your feet where the earth is red."},
            "Mrigashira": {"yoga": "Garudasana", "ayurveda": "Sensory Exhaustion", "poem": "Softness is the only armor that never breaks."},
            "Ardra": {"yoga": "Simhasana", "ayurveda": "Lymphatic Flow", "poem": "Renewal begins when the drought of pride ends."},
            "Punarvasu": {"yoga": "Anjaneyasana", "ayurveda": "Shoulder Tension", "poem": "Trust the cycles of the light and the dark."},
            "Pushya": {"yoga": "Balasana", "ayurveda": "Digestive Agni", "poem": "Be the hollow bone through which wisdom sings."},
            "Ashlesha": {"yoga": "Bhujangasana", "ayurveda": "Joint Lubrication", "poem": "Shed the skin that no longer fits the light."},
            "Magha": {"yoga": "Tadasana", "ayurveda": "Heart Muscle", "poem": "Noble action is the only legacy that lives."},
            "Purva Phalguni": {"yoga": "Natarajasana", "ayurveda": "Lower Back", "poem": "Pour your love into the world like vintage wine."},
            "Uttara Phalguni": {"yoga": "Setu Bandhasana", "ayurveda": "Nervous Digestion", "poem": "Steady the mind like a flame in a windless room."},
            "Hasta": {"yoga": "Bakasana", "ayurveda": "Wrist & Forearm", "poem": "Your work is the signature of your inner peace."},
            "Chitra": {"yoga": "Sirsasana", "ayurveda": "Skin Radiance", "poem": "The masterpiece is the life you choose to lead."},
            "Swati": {"yoga": "Nadi Shodhana", "ayurveda": "Colon Health", "poem": "The spirit travels furthest when it carries nothing."},
            "Vishakha": {"yoga": "Parivrtta Trikonasana", "ayurveda": "Bladder & Pelvis", "poem": "The victory is won in the stillness of the mind."},
            "Anuradha": {"yoga": "Padmasana", "ayurveda": "Circulation", "poem": "Belonging is a state of grace, not a place."},
            "Jyeshtha": {"yoga": "Matsyendrasana", "ayurveda": "Nervous Core", "poem": "Listen to the silence that precedes the great word."},
            "Moola": {"yoga": "Adho Mukha Svanasana", "ayurveda": "Psoas Release", "poem": "Destroy what is false to find what is eternal."},
            "Purva Ashada": {"yoga": "Virabhadrasana I", "ayurveda": "Liver Heat", "poem": "Surrender to the flow and let the tides guide you."},
            "Uttara Ashada": {"yoga": "Salamba Sarvangasana", "ayurveda": "Bone Density", "poem": "Integrity is the only mountain worth climbing."},
            "Shravana": {"yoga": "Viparita Karani", "ayurveda": "Hearing/Ears", "poem": "Knowledge is a burden; wisdom is a light."},
            "Dhanishta": {"yoga": "Ustrasana", "ayurveda": "Ankle Strength", "poem": "The drum of the heart is the map to the divine."},
            "Shatabhisha": {"yoga": "Savasana", "ayurveda": "Detoxification", "poem": "The void is not empty; it is full of infinite light."},
            "Purva Bhadrapada": {"yoga": "Pincha Mayurasana", "ayurveda": "Foot Reflexology", "poem": "The warrior’s greatest battle is in the mirror."},
            "Uttara Bhadrapada": {"yoga": "Ananta Shayanasana", "ayurveda": "Deep Sleep", "poem": "Peace is the treasure guarded by the quiet mind."},
            "Revati": {"yoga": "Yoga Nidra", "ayurveda": "Psychological Peace", "poem": "Give everything away to find what is truly yours."}
        },
        "Moon": {
            "Ashwini": {"yoga": "Viparita Karani", "ayurveda": "Eye Strain", "poem": "Drink from the dawn and let the past dissolve."},
            "Bharani": {"yoga": "Pawanmuktasana", "ayurveda": "Hormonal Flow", "poem": "Give birth to the version of you that knows no fear."},
            "Rohini": {"yoga": "Bhujangasana", "ayurveda": "Mucus/Congestion", "poem": "Tend to the garden of the heart with slow hands."},
            "Ardra": {"yoga": "Shashankasana", "ayurveda": "Nerve Grounding", "poem": "Renewal begins when you stop trying to keep the old life dry."},
            "Pushya": {"yoga": "Balasana", "ayurveda": "Digestive Enzymes", "poem": "Stability is found in the service of the sacred."},
            "Hasta": {"yoga": "Bakasana", "ayurveda": "The Bowels", "poem": "The magic is in the focus, not the hand."},
            "Anuradha": {"yoga": "Padmasana", "ayurveda": "Blood Purity", "poem": "Look for the blossom that grows in the mud."},
            "Jyeshtha": {"yoga": "Matsyasana", "ayurveda": "Adrenal Fatigue", "poem": "The elder within you knows the way."},
            "Shatabhisha": {"yoga": "Savasana", "ayurveda": "Varicose Veins", "poem": "Heal the collective by mending your own soul."},
            "Purva Bhadrapada": {"yoga": "Pincha Mayurasana", "ayurveda": "Foot Reflexology", "poem": "The warrior’s greatest battle is in the mirror."}
        },
        "Sun": {
            "Ashwini": {"yoga": "Pranamasana", "ayurveda": "Eye Vitality", "poem": "You are the physician of your own wreckage."},
            "Rohini": {"yoga": "Ustrasana", "ayurveda": "Thyroid/Metabolism", "poem": "Beauty is the vital oxygen of the soul."},
            "Magha": {"yoga": "Tadasana", "ayurveda": "The Heart", "poem": "Noble action is the only currency of the eternal."},
            "Uttara Phalguni": {"yoga": "Setu Bandhasana", "ayurveda": "Nervous Digestion", "poem": "Steady the mind like a flame in a windless room."},
            "Chitra": {"yoga": "Sirsasana", "ayurveda": "Solar Rashes", "poem": "The masterpiece is not what you make, but who you are."},
            "Swati": {"yoga": "Vrksasana", "ayurveda": "Kidney Filtration", "poem": "Find your breath in the center of the hurricane."},
            "Moola": {"yoga": "Adho Mukha Svanasana", "ayurveda": "Hip Flexibility", "poem": "Foundations are only found at the bottom."},
            "Revati": {"yoga": "Yoga Nidra", "ayurveda": "Immune Strength", "poem": "The traveler is the path and the path is the goal."}
        },
        "Mercury": {
            "Ashwini": {"yoga": "Nadi Shodhana", "ayurveda": "Cranial Nerves", "poem": "Stop searching for a cure; you are the medicine."},
            "Rohini": {"yoga": "Simhasana", "ayurveda": "Thyroid/Speech", "poem": "Softness is the armor the world cannot pierce."},
            "Hasta": {"yoga": "Bakasana", "ayurveda": "Intestinal Transit", "poem": "The power is in the focus of the eye."},
            "Jyeshtha": {"yoga": "Ardha Matsyendrasana", "ayurveda": "Adrenal Buffer", "poem": "Listen to the silence beneath the noise."}
        },
        "Venus": {
            "Ashwini": {"yoga": "Viparita Karani", "ayurveda": "Facial Lustre", "poem": "Drink from the dawn of new love."},
            "Bharani": {"yoga": "Baddha Konasana", "ayurveda": "Reproductive Vitality", "poem": "Carry the weight until it turns into a wing."},
            "Magha": {"yoga": "Tadasana", "ayurveda": "Heart Muscle", "poem": "Noble action is the only legacy that lives."},
            "Hasta": {"yoga": "Anjali Mudra/Vrksasana", "ayurveda": "Nervous Digestion", "poem": "Perfection is a myth; presence is a miracle."},
            "Revati": {"yoga": "Yoga Nidra", "ayurveda": "Ojas/Immunity", "poem": "Cross the bridge and wake up in the morning sun."}
        },
        "Jupiter": {
            "Pushya": {"yoga": "Balasana", "ayurveda": "Liver Cooling", "poem": "Stability is found in absolute surrender."},
            "Hasta": {"yoga": "Bakasana", "ayurveda": "Wrist & Forearm", "poem": "Your work is the signature of your inner peace."},
            "Uttara Ashada": {"yoga": "Salamba Sarvangasana", "ayurveda": "Knee Lubrication", "poem": "Integrity is the only peak with a view."},
            "Revati": {"yoga": "Yoga Nidra", "ayurveda": "Foot Grounding", "poem": "The journey is done; the ocean has returned to the drop."}
        },
        "Saturn": {
            "Ashwini": {"yoga": "Tadasana", "ayurveda": "Joint Lubrication", "poem": "Strength is found in the stillness of the mountain."},
            "Bharani": {"yoga": "Baddha Konasana", "ayurveda": "Pelvic Inflammation", "poem": "Carry the weight until it turns into a wing."},
            "Pushya": {"yoga": "Balasana", "ayurveda": "Gut Transit", "poem": "Carry the old man in the mother's lap."},
            "Swati": {"yoga": "Vrksasana", "ayurveda": "Kidney Filtering", "poem": "Freedom is breathing in the middle of chaos."},
            "Shravana": {"yoga": "Salamba Sarvangasana", "ayurveda": "Ear Health", "poem": "Wisdom is the light that carries you."}
        },
        "Rahu": {
            "Ardra": {"yoga": "Savasana", "ayurveda": "Nervous Static", "poem": "Renewal begins in the drenching storm."},
            "Hasta": {"yoga": "Bakasana", "ayurveda": "Ghost Allergies", "poem": "Grasp the truth, then let the outcome go."},
            "Purva Bhadrapada": {"yoga": "Pincha Mayurasana", "ayurveda": "Foot Reflexology", "poem": "The warrior’s greatest battle is in the mirror."}
        },
        "Ketu": {
            "Uttara Phalguni": {"yoga": "Setu Bandhasana", "ayurveda": "Nervous Digestion", "poem": "Steady the mind like a flame in a windless room."},
            "Moola": {"yoga": "Adho Mukha Svanasana", "ayurveda": "Hip Memory", "poem": "Dig past the bone to the primary root."},
            "Revati": {"yoga": "Yoga Nidra", "ayurveda": "Immune Boundary", "poem": "The traveler leave no footprints behind."}
        }
    }
    
    planet_data = library.get(planet_name, {})
    medicine = planet_data.get(nakshatra_name)
    
    # Fallback to the Mars library if specific planet/nakshatra combo is missing
    if not medicine:
        medicine = library["Mars"].get(nakshatra_name, {
            "yoga": "Gentle Mindfulness", "ayurveda": "Prana Flow", "poem": "The stars are weaving a new path for you..."
        })
    return medicine

# --- 3. THE SIDEREAL ASTRONOMY ENGINE ---
def get_nakshatra_name(sign, degree):
    ranges = {
        "Aries": [(13.333, "Ashwini"), (26.666, "Bharani"), (30.0, "Krittika")],
        "Taurus": [(10.0, "Krittika"), (23.333, "Rohini"), (30.0, "Mrigashira")],
        "Gemini": [(6.666, "Mrigashira"), (20.0, "Ardra"), (30.0, "Punarvasu")],
        "Cancer": [(3.333, "Punarvasu"), (16.666, "Pushya"), (30.0, "Ashlesha")],
        "Leo": [(13.333, "Magha"), (26.666, "Purva Phalguni"), (30.0, "Uttara Phalguni")],
        "Virgo": [(10.0, "Uttara Phalguni"), (23.333, "Hasta"), (30.0, "Chitra")],
        "Libra": [(6.666, "Chitra"), (20.0, "Swati"), (30.0, "Vishakha")],
        "Scorpio": [(3.333, "Vishakha"), (16.666, "Anuradha"), (30.0, "Jyeshtha")],
        "Sagittarius": [(13.333, "Moola"), (26.666, "Purva Ashada"), (30.0, "Uttara Ashada")],
        "Capricorn": [(10.0, "Uttara Ashada"), (23.333, "Shravana"), (30.0, "Dhanishta")],
        "Aquarius": [(6.666, "Dhanishta"), (20.0, "Shatabhisha"), (30.0, "Purva Bhadrapada")],
        "Pisces": [(3.333, "Purva Bhadrapada"), (16.666, "Uttara Bhadrapada"), (30.0, "Revati")],
    }
    for limit, name in ranges.get(sign, []):
        if degree < limit: return name
    return "Unknown"

def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name or "UTC")
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    asc_sign = signs[int(asc_raw / 30)]
    asc_nak = get_nakshatra_name(asc_sign, asc_raw % 30)
    
    planets = [(swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"), 
               (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"), 
               (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")]
    
    results = []
    for p_id, p_name in planets:
        res, ret = swe.calc_ut(jd_ut, p_id, swe.FLG_SIDEREAL)
        p_long = res[0]
        p_sign = signs[int(p_long / 30)]
        p_nak = get_nakshatra_name(p_sign, p_long % 30)
        
        if p_name == "Rahu":
            k_long = (p_long + 180) % 360
            k_sign = signs[int(k_long/30)]
            k_nak = get_nakshatra_name(k_sign, k_long % 30)
            k_med = get_holistic_medicine("Ketu", k_nak)
            results.append({"name": "Ketu", "sign": k_sign, "nakshatra": k_nak, "med": k_med})

        med = get_holistic_medicine(p_name, p_nak)
        results.append({"name": p_name, "sign": p_sign, "nakshatra": p_nak, "med": med})

    return {"asc_sign": asc_sign, "asc_nak": asc_nak, "planets": results}

# --- 4. THE STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Cosmic Pharmacopeia Sanctuary", layout="wide")
st.title("⚖️ The Cosmic Pharmacopeia Sanctuary")
st.markdown("---")

with st.sidebar:
    st.header("Seeker Information")
    name = st.text_input("Name", "Danny R Slater")
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    location = st.text_input("Birth Location", "Houston, USA")

# Geolocation Processing
geolocator = Nominatim(user_agent="soul_map_v5")
loc = geolocator.geocode(location) if location else None

if loc and st.button("Generate Sacred Medicine"):
    data = calculate_soul_map(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute, loc.latitude, loc.longitude)
    
    st.header(f"The Soul Map of {name}")
    st.markdown(f"**Foundational Container (Ascendant):** {data['asc_nak']} ({data['asc_sign']})")
    st.divider()

    # THE SOUL CARDS
    for p in data['planets']:
        # Map icons for flair
        icon = {"Sun": "☀️", "Moon": "🌕", "Mars": "🔴", "Mercury": "☿️", "Venus": "♀️", "Jupiter": "♃️", "Saturn": "🪐", "Rahu": "🐲", "Ketu": "🐍"}.get(p['name'], "✨")
        
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.subheader(f"{icon} {p['name']}")
                st.write(f"**{p['nakshatra']}**")
                st.caption(f"in {p['sign']}")
            with col2:
                st.markdown("### Soulful Prescription")
                st.info(f"*{p['med']['poem']}*")
                
                # Holistic Details
                inner_col1, inner_col2 = st.columns(2)
                with inner_col1:
                    yoga_pose = p['med']['yoga']
                    st.markdown(f"🧘 **Yoga Asana:**  \n{yoga_pose}")
                    
                    # TEACHER GUIDE LOOKUP
                    # Cleans pose name (e.g., 'Savasana with Eye Pillow' -> 'Savasana')
                    simple_pose = yoga_pose.split(" with")[0].split("/")[0]
                    if simple_pose in TEACHER_GUIDE:
                        with st.expander(f"📖 How to Perform {simple_pose}"):
                            st.write(TEACHER_GUIDE[simple_pose]['description'])
                            st.markdown("**Steps:**")
                            for step in TEACHER_GUIDE[simple_pose]['steps']:
                                st.write(f"• {step}")
                            st.markdown(f"**Focus:** {TEACHER_GUIDE[simple_pose]['focus']}")
                
                with inner_col2:
                    st.markdown(f"🍃 **Ayurvedic Alignment:**  \n{p['med']['ayurveda']}")
            st.divider()

st.caption("Sidereal Data via Swiss Ephemeris | Holistic Library by User")
