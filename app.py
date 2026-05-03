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
        "steps": [
            "Start on your hands and knees.",
            "Tuck your toes and lift your hips high.",
            "Press through your palms.",
            "Pedal your feet to stretch the calves.",
            "Let your head hang heavy.",
        ],
    },
    "Mountain Pose": {
        "sanskrit": "Tadasana",
        "focus": "Heart Center & Posture",
        "steps": [
            "Stand tall with feet rooted.",
            "Roll your shoulders back and down.",
            "Palms face forward.",
            "Reach the crown of your head to the sky.",
        ],
    },
    "Bridge Pose": {
        "sanskrit": "Setu Bandhasana",
        "focus": "Nervous System & Digestion",
        "steps": [
            "Lie on your back, knees bent.",
            "Press feet down and lift your hips.",
            "Interlace hands beneath you if possible.",
            "Breathe into the belly.",
        ],
    },
    "Crow Pose": {
        "sanskrit": "Bakasana",
        "focus": "Mental Focus & Wrist Strength",
        "steps": [
            "Squat low, hands flat on the mat.",
            "Place knees against your upper arms.",
            "Lean forward, shifting weight into your hands.",
            "Lift feet one at a time.",
        ],
    },
    "Forearm Stand": {
        "sanskrit": "Pincha Mayurasana",
        "focus": "Perspective Shift & Blood Flow",
        "steps": [
            "Forearms down, elbows shoulder-width apart.",
            "Lift hips and walk feet in toward your face.",
            "Lift one leg, then the other.",
            "Gaze softly between your arms.",
        ],
    },
    "Bound Angle Pose": {
        "sanskrit": "Baddha Konasana",
        "focus": "Pelvic Release & Creative Energy",
        "steps": [
            "Sit tall, soles of feet together.",
            "Lengthen the spine on the inhale.",
            "Fold forward slowly on the exhale.",
        ],
    },
    "Child's Pose": {
        "sanskrit": "Balasana",
        "focus": "Third Eye & Surrender",
        "steps": [
            "Kneel on the floor, big toes touching.",
            "Sit on your heels and separate your knees.",
            "Fold forward, resting forehead on the mat.",
            "Breathe into your back.",
        ],
    },
    "Warrior I": {
        "sanskrit": "Virabhadrasana I",
        "focus": "Sharp Intellect & Inner Fire",
        "steps": [
            "Step one foot forward into a lunge, back foot at 45 degrees.",
            "Bend the front knee to 90 degrees.",
            "Square your hips toward the front.",
            "Raise arms overhead, palms facing each other.",
            "Gaze forward and breathe steadily.",
        ],
    },
    "Warrior II": {
        "sanskrit": "Virabhadrasana II",
        "focus": "Structured Fire & Endurance",
        "steps": [
            "Step feet wide apart.",
            "Turn front foot forward, back foot at 90 degrees.",
            "Bend front knee over ankle.",
            "Extend arms parallel to the floor.",
            "Gaze over your front fingertips.",
        ],
    },
    "Triangle Pose": {
        "sanskrit": "Trikonasana",
        "focus": "Mental Agility & Balance",
        "steps": [
            "Stand with feet wide, front foot forward.",
            "Extend arms wide and hinge at the hip.",
            "Lower front hand to shin, ankle, or the floor.",
            "Reach the top arm toward the sky.",
            "Gaze up toward your top hand.",
        ],
    },
    "Stillness": {
        "sanskrit": "Savasana / Seated Meditation",
        "focus": "Earthing & Deep Presence",
        "steps": [
            "Find a comfortable seated or lying position.",
            "Close your eyes and soften your breath.",
            "Release any effort from the body.",
            "Rest your awareness on the natural rhythm of your breath.",
            "Stay for at least 5 minutes.",
        ],
    },
}

# --- 2. THE SOUL MAP REMEDY LIBRARY ---
REMEDY_LIBRARY = {
    "Sun": {
        "Uttara Phalguni": {
            "pose": "Bridge Pose",
            "focus": "Nervous System",
            "ayurveda": "Eat warm, cooked root vegetables.",
            "poem": "The world is a mirror of your kindness. Serve a purpose larger than your name.",
        },
        "Taurus": {
            "pose": "Mountain Pose",
            "focus": "Steadfastness",
            "ayurveda": "Use grounding oils like Vetiver.",
            "poem": "Bright spirit, root into the fertile valley of your own worth.",
        },
    },
    "Moon": {
        "Purva Bhadrapada": {
            "pose": "Forearm Stand",
            "focus": "Perspective",
            "ayurveda": "Prioritize cooling beverages.",
            "poem": "Take off the mask and breathe. Do not fear the fire of truth.",
        },
        "Pisces": {
            "pose": "Child's Pose",
            "focus": "Oceanic Peace",
            "ayurveda": "Warm baths with sea salt.",
            "poem": "The tide comes in, the tide goes out. You are the ocean, not the wave.",
        },
    },
    "Mercury": {
        "Hasta": {
            "pose": "Crow Pose",
            "focus": "Mental Precision",
            "ayurveda": "Practice Nasya (nasal oiling).",
            "poem": "Magic is hidden in the mastery of small details.",
        },
        "Aries": {
            "pose": "Warrior I",
            "focus": "Sharp Intellect",
            "ayurveda": "Minimize screen time before noon.",
            "poem": "Speak with the sharpness of a needle but the intent of a healer.",
        },
    },
    "Venus": {
        "Magha": {
            "pose": "Mountain Pose",
            "focus": "Heart Center",
            "ayurveda": "Warm sesame oil massage.",
            "poem": "You are the living prayer of those who came before you.",
        },
        "Taurus": {
            "pose": "Bound Angle Pose",
            "focus": "Lush Stability",
            "ayurveda": "Favor sweet, juicy fruits.",
            "poem": "Beauty is found in the stillness of stone and the bloom of a flower.",
        },
    },
    "Mars": {
        "Moola": {
            "pose": "Downward-Facing Dog",
            "focus": "Psoas Release",
            "ayurveda": "Daily brisk walking.",
            "poem": "Dig until you find the root of your pain.",
        },
        "Gemini": {
            "pose": "Triangle Pose",
            "focus": "Mental Agility",
            "ayurveda": "Sip ginger tea.",
            "poem": "Your strength is the agility of your mind. Direct your fire toward clarity.",
        },
    },
    "Jupiter": {
        "Punarvasu": {
            "pose": "Warrior I",
            "focus": "Expansive Faith",
            "ayurveda": "Turmeric golden milk before bed.",
            "poem": "Return again and again to the light within you.",
        },
    },
    "Saturn": {
        "Bharani": {
            "pose": "Bound Angle Pose",
            "focus": "Creative Patience",
            "ayurveda": "Drink CCF tea.",
            "poem": "The seed must endure the dark before it becomes a tree.",
        },
        "Aries": {
            "pose": "Warrior II",
            "focus": "Structured Fire",
            "ayurveda": "Warm, grounding soups.",
            "poem": "Discipline is the bridge between the spark and the flame.",
        },
    },
    "Rahu": {
        "Purva Bhadrapada": {
            "pose": "Forearm Stand",
            "focus": "Perspective Shift",
            "ayurveda": "Prioritize cooling beverages.",
            "poem": "Take off the mask and breathe. Do not fear the fire of truth.",
        },
    },
    "Ketu": {
        "General": {
            "pose": "Child's Pose",
            "focus": "Third Eye",
            "ayurveda": "30 minutes of sacred silence.",
            "poem": "You are the empty vessel that the divine wants to fill.",
        },
    },
    "Ascendant": {
        "Ashwini":        {"pose": "Warrior I",           "focus": "Swift Beginnings",    "ayurveda": "Morning movement before sunrise.",           "poem": "You arrived running. Trust the speed of your own spirit."},
        "Bharani":        {"pose": "Bound Angle Pose",    "focus": "Creative Patience",   "ayurveda": "Drink CCF tea.",                              "poem": "What you carry is heavy — and sacred."},
        "Krittika":       {"pose": "Warrior II",          "focus": "Purifying Fire",      "ayurveda": "Warm lemon water each morning.",              "poem": "You are the flame that burns away what is not true."},
        "Rohini":         {"pose": "Stillness",           "focus": "Earthing",            "ayurveda": "Bare feet on the earth for 10 minutes.",      "poem": "Sink your feet into the red earth and listen to the pulse of the soil."},
        "Mrigashira":     {"pose": "Triangle Pose",       "focus": "Seeking Heart",       "ayurveda": "Rosehip tea for the heart.",                  "poem": "The deer seeks what the forest has always held. Look within."},
        "Ardra":          {"pose": "Child's Pose",        "focus": "Grief & Release",     "ayurveda": "Steam inhalation with eucalyptus.",           "poem": "Let the storm move through you. You are the sky, not the rain."},
        "Punarvasu":      {"pose": "Warrior I",           "focus": "Renewal",             "ayurveda": "Turmeric golden milk before bed.",            "poem": "Return again and again. Each sunrise is your second chance."},
        "Pushya":         {"pose": "Bridge Pose",         "focus": "Nourishment",         "ayurveda": "Cook for yourself with love.",                "poem": "You are the flower that blooms in winter. Nourish what is tender."},
        "Ashlesha":       {"pose": "Stillness",           "focus": "Inner Wisdom",        "ayurveda": "Meditate near water.",                       "poem": "The serpent knows the secrets of the deep. So do you."},
        "Magha":          {"pose": "Mountain Pose",       "focus": "Ancestral Power",     "ayurveda": "Warm sesame oil massage.",                    "poem": "You stand on the shoulders of kings. Rise accordingly."},
        "Purva Phalguni": {"pose": "Bound Angle Pose",    "focus": "Creative Joy",        "ayurveda": "Favor sweet, juicy fruits.",                  "poem": "Rest is not laziness. Bloom in the afternoon sun."},
        "Uttara Phalguni":{"pose": "Bridge Pose",         "focus": "Service & Steadiness","ayurveda": "Eat warm, cooked root vegetables.",           "poem": "The sun does not ask permission to shine. Serve with your whole self."},
        "Hasta":          {"pose": "Crow Pose",           "focus": "Skillful Hands",      "ayurveda": "Practice Nasya (nasal oiling).",              "poem": "Everything you need is already in your hands."},
        "Chitra":         {"pose": "Triangle Pose",       "focus": "Beauty & Craft",      "ayurveda": "Rose water for the skin.",                   "poem": "You are the artist. The world is your unfinished canvas."},
        "Swati":          {"pose": "Stillness",           "focus": "Independence",        "ayurveda": "Breathe outdoor air for 20 minutes.",        "poem": "The wind bends the grass but never breaks it. Be supple."},
        "Vishakha":       {"pose": "Warrior II",          "focus": "Focused Ambition",    "ayurveda": "Sip tulsi tea.",                              "poem": "Fix your gaze and walk. The goal is already yours."},
        "Anuradha":       {"pose": "Bound Angle Pose",    "focus": "Devotion",            "ayurveda": "Lotus seed or saffron milk.",                 "poem": "True friendship is the rarest star. You carry it in your chest."},
        "Jyeshtha":       {"pose": "Mountain Pose",       "focus": "Elder Wisdom",        "ayurveda": "Warm, nourishing soups.",                    "poem": "You have earned your authority. Now use it gently."},
        "Moola":          {"pose": "Downward-Facing Dog", "focus": "Root & Release",      "ayurveda": "Daily brisk walking in nature.",              "poem": "Dig until you find the root. Then let it breathe."},
        "Purva Ashada":   {"pose": "Forearm Stand",       "focus": "Invincible Spirit",   "ayurveda": "Coconut water for vitality.",                 "poem": "You have not yet been defeated. Rise and declare yourself."},
        "Uttara Ashada":  {"pose": "Warrior I",           "focus": "Final Victory",       "ayurveda": "Sesame seeds with honey.",                   "poem": "The battle is long but the victory is certain. Stay."},
        "Shravana":       {"pose": "Child's Pose",        "focus": "Listening & Learning","ayurveda": "Oil the ears before sleep.",                 "poem": "The wisest among us learned to listen before they learned to speak."},
        "Dhanishta":      {"pose": "Bridge Pose",         "focus": "Abundance & Rhythm",  "ayurveda": "Drum or move to music daily.",               "poem": "Your life is a song. Play it loud."},
        "Shatabhisha":    {"pose": "Stillness",           "focus": "Healing Vision",      "ayurveda": "Star-gazing meditation at night.",           "poem": "You hold a hundred medicines within you."},
        "Purva Bhadrapada":{"pose": "Forearm Stand",     "focus": "Sacred Fire",         "ayurveda": "Cooling rose or sandalwood oil.",            "poem": "You are the bridge between the seen and unseen. Walk it bravely."},
        "Uttara Bhadrapada":{"pose": "Child's Pose",     "focus": "Oceanic Depth",       "ayurveda": "Warm baths with sea salt.",                  "poem": "Still water runs deep. Trust the wisdom beneath your silence."},
        "Revati":         {"pose": "Child's Pose",        "focus": "Gentle Completion",   "ayurveda": "Jasmine or lotus flower offering.",          "poem": "You are the last light before the dawn. Rest, and begin again."},
    },
}

DEFAULT_REMEDY = {
    "pose": "Stillness",
    "focus": "Breath",
    "ayurveda": "Breathe deeply for five minutes.",
    "poem": "The stars are always in alignment with your soul.",
}

def get_sacred_alignment(planet_name, nakshatra, sign):
    """Look up remedy by nakshatra first, then sign, then default."""
    if planet_name == "Ketu":
        return REMEDY_LIBRARY["Ketu"]["General"]

    planet_data = REMEDY_LIBRARY.get(planet_name, {})

    # Try nakshatra first, then sign, then default
    return planet_data.get(nakshatra) or planet_data.get(sign) or DEFAULT_REMEDY

# --- 3. THE CALCULATOR ENGINE ---
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Moola", "Purva Ashada", "Uttara Ashada", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

# IAU constellation boundaries along the ecliptic (J2000), excluding Ophiuchus.
# Each tuple is (ecliptic_longitude_start, sign_name).
# Ophiuchus (roughly 234-266 deg) is absorbed into Scorpio for traditional 12-sign system.
# Source: IAU boundary data as used by TheSkyLive and JPL.
IAU_SIGN_BOUNDARIES = [
    (0.0,   "Aries"),
    (28.0,  "Taurus"),
    (90.0,  "Gemini"),
    (118.0, "Cancer"),
    (138.0, "Leo"),
    (174.0, "Virgo"),
    (218.0, "Libra"),
    (224.0, "Scorpio"),
    (266.0, "Sagittarius"),
    (300.0, "Capricorn"),
    (327.0, "Aquarius"),
    (351.0, "Pisces"),
]

# IAU constellation boundaries along the ecliptic (tropical longitude, J2000).
# Validated against Astro.com Lahiri sidereal positions + known ayanamsa of ~23-24°.
# Ophiuchus is excluded — its range (~240°–266°) is absorbed into Scorpio.
IAU_SIGN_BOUNDARIES = [
    (  0.0, "Aries"),
    ( 28.0, "Taurus"),
    ( 90.0, "Gemini"),
    (118.0, "Cancer"),
    (138.0, "Leo"),
    (174.0, "Virgo"),
    (218.0, "Libra"),
    (240.0, "Scorpio"),    # moved from 224 — absorbs Ophiuchus cleanly
    (266.0, "Sagittarius"),
    (300.0, "Capricorn"),
    (327.0, "Aquarius"),
    (351.0, "Pisces"),
]

def get_iau_sign(tropical_degree):
    """Return the IAU sign for a tropical ecliptic longitude (0–360°)."""
    d = tropical_degree % 360
    sign = "Pisces"
    for start, name in IAU_SIGN_BOUNDARIES:
        if d >= start:
            sign = name
    return sign

def format_degree(tropical_degree, sign):
    """Return whole degrees within the current IAU sign boundary."""
    d = tropical_degree % 360
    start = next((s for s, n in IAU_SIGN_BOUNDARIES if n == sign), 0.0)
    return f"{int(d - start)}°"

def get_nakshatra(tropical_degree, ayan):
    """
    Nakshatra anchored to real stars.
    Subtract Lahiri ayanamsa from tropical degree to get sidereal position,
    then map onto the 27-nakshatra belt.
    """
    sidereal_deg = (tropical_degree - ayan) % 360
    return NAKSHATRAS[int(sidereal_deg / (360 / 27)) % 27]

# --- 4. THE INTERFACE ---
st.set_page_config(page_title="The Soul Map Remedy", page_icon="🌌")
st.title("🌌 The Soul Map Remedy")

st.markdown("""
### 🌀 The Song of the Shifting Sky
> *You might notice your signs look a bit 'out of line,'*  
> *Compared to the horoscopes you read all the time.*  
>  
> *See, the Earth is a dancer, a spinning glass top,*  
> *But she **wobbles** a bit, and she never will stop!*  
>  
> *Over thousands of years, she's tilted her head,*  
> *The stars shifted left while the calendar sped.*  
>  
> *While others look back at where stars used to be,*  
> *We look at the sky as it is—**actually.***  
>  
> *So if you've moved back by a sign or a space,*  
> *Don't worry, dear heart, you're in the right place.*  
>  
> *It's not a mistake, or a glitch, or a lie—*  
> *It's just how we dance with the **real, living sky.***
""")

with st.sidebar:
    st.header("Birth Sky Details")
    target_name = st.text_input("Name", "")
    b_date = st.date_input(
        "Birth Date",
        value=date(1990, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date(2100, 12, 31),
    )
    b_time = st.time_input("Birth Time", value=datetime.strptime("12:00", "%H:%M").time())
    st.subheader("Birth Location")
    city = st.text_input("City", "")
    state = st.text_input("State / Province", "")
    country = st.text_input("Country", "")

if st.button("Unveil My Remedy"):
    if not city or not country:
        st.error("Please enter at least a city and country.")
    else:
        full_loc = ", ".join(filter(None, [city, state, country]))
        geolocator = Nominatim(user_agent="soul_map_app")

        with st.spinner("Reading the sky..."):
            location = geolocator.geocode(full_loc)

        if not location:
            st.error(f"Location '{full_loc}' not found. Please check your spelling.")
        else:
            tf = TimezoneFinder()
            tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
            tz = pytz.timezone(tz_name)
            # localize() correctly applies the historically accurate UTC offset
            # for the given date (e.g. CST vs CDT in pre-1966 US dates)
            local_dt = tz.localize(datetime.combine(b_date, b_time), is_dst=False)
            utc_dt = local_dt.astimezone(pytz.utc)

            st.caption(f"🕐 Timezone: {tz_name} | UTC offset: {local_dt.utcoffset()} | UT: {utc_dt.strftime('%H:%M')}")

            jd = swe.julday(
                utc_dt.year, utc_dt.month, utc_dt.day,
                utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0,
            )

            # Call houses BEFORE set_sid_mode — swe.houses returns tropical longitudes
            # by default. set_sid_mode would shift the output and corrupt the ascendant.
            cusps, ascmc = swe.houses(jd, location.latitude, location.longitude, b"W")
            asc_tropical = ascmc[0]  # true tropical ecliptic longitude of the Ascendant

            # Now set sidereal mode to get the ayanamsa for nakshatra calculation
            swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
            ayan = swe.get_ayanamsa_ut(jd)

            # --- ASCENDANT ---
            # IAU sign from real-sky tropical longitude directly.
            # Nakshatra from same degree minus ayanamsa, anchoring to actual stars.
            asc_nak      = get_nakshatra(asc_tropical, ayan)
            asc_sign     = get_iau_sign(asc_tropical)
            asc_deg_fmt  = format_degree(asc_tropical, asc_sign)
            asc_med      = get_sacred_alignment("Ascendant", asc_nak, asc_sign)

            display_name = target_name.strip() or "You"
            st.header(f"The Soul Map of {display_name}")
            st.subheader("🏺 Foundational Container (Ascendant)")
            st.markdown(f"### **{asc_deg_fmt} {asc_nak} in {asc_sign}**")
            st.info(f"*{asc_med['poem']}*")
            st.write(f"🌿 **Ayurveda Ritual:** {asc_med['ayurveda']}")
            if asc_med["pose"] in TEACHER_GUIDE:
                with st.expander("📖 Guided Practice Steps"):
                    for step in TEACHER_GUIDE[asc_med["pose"]]["steps"]:
                        st.write(f"• {step}")
            st.divider()

            # --- PLANETS ---
            # FLG_SPEED returns tropical ecliptic longitude in res[0] —
            # the real-sky position matching TheSkyLive.
            planets = [
                ("Sun",     swe.SUN),
                ("Moon",    swe.MOON),
                ("Mercury", swe.MERCURY),
                ("Venus",   swe.VENUS),
                ("Mars",    swe.MARS),
                ("Jupiter", swe.JUPITER),
                ("Saturn",  swe.SATURN),
                ("Rahu",    swe.MEAN_NODE),
            ]

            for p_name, p_id in planets:
                res, _    = swe.calc_ut(jd, p_id, swe.FLG_SPEED)
                p_tropical = res[0]
                p_nak      = get_nakshatra(p_tropical, ayan)
                p_sign     = get_iau_sign(p_tropical)
                p_deg_fmt  = format_degree(p_tropical, p_sign)
                med        = get_sacred_alignment(p_name, p_nak, p_sign)

                with st.expander(f"✨ {p_name}: {p_deg_fmt} {p_nak} in {p_sign}", expanded=True):
                    st.markdown(f"*{med['poem']}*")
                    st.write(f"🧘 **Yoga Pose:** {med['pose']} | 📍 **Focus:** {med['focus']}")
                    st.write(f"🌿 **Ayurveda Ritual:** {med['ayurveda']}")
                    if med["pose"] in TEACHER_GUIDE:
                        with st.expander("📖 Guided Practice Steps"):
                            for step in TEACHER_GUIDE[med["pose"]]["steps"]:
                                st.write(f"• {step}")

            # --- KETU (South Node = Rahu + 180°) ---
            rahu_res, _   = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SPEED)
            ketu_tropical = (rahu_res[0] + 180) % 360
            ketu_nak      = get_nakshatra(ketu_tropical, ayan)
            ketu_sign     = get_iau_sign(ketu_tropical)
            ketu_deg_fmt  = format_degree(ketu_tropical, ketu_sign)
            ketu_med      = get_sacred_alignment("Ketu", ketu_nak, ketu_sign)

            with st.expander(f"✨ Ketu: {ketu_deg_fmt} {ketu_nak} in {ketu_sign}", expanded=True):
                st.markdown(f"*{ketu_med['poem']}*")
                st.write(f"🧘 **Yoga Pose:** {ketu_med['pose']} | 📍 **Focus:** {ketu_med['focus']}")
                st.write(f"🌿 **Ayurveda Ritual:** {ketu_med['ayurveda']}")
                if ketu_med["pose"] in TEACHER_GUIDE:
                    with st.expander("📖 Guided Practice Steps"):
                        for step in TEACHER_GUIDE[ketu_med["pose"]]["steps"]:
                            st.write(f"• {step}")

            st.divider()

st.markdown("""
---
### ⚖️ A Note on Your Journey
The suggestions provided in this Soul Map are intended for **educational and spiritual alignment purposes only**.  
I am an **astrologer and educator**, not a medical doctor.  
Consult with your physician before beginning any new exercise or dietary routine.
""")
st.caption("Sidereal Lahiri System | The Soul Map Remedy")
