import streamlit as st
import swisseph as swe
import pytz
from datetime import datetime

# --- 1. THE WISDOM LIBRARY (Ayurveda & Yoga Integration) ---
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# This library contains the 'essence' you loved: Doshas and Postures
WISDOM_DATA = {
    "Ashwini": {"dosha": "Vata", "yoga": "Setu Bandhasana (Bridge Pose)"},
    "Bharani": {"dosha": "Pitta", "yoga": "Malasana (Garland Pose)"},
    "Krittika": {"dosha": "Pitta", "yoga": "Surya Namaskar (Sun Salutations)"},
    "Rohini": {"dosha": "Kapha", "yoga": "Vrksasana (Tree Pose)"},
    "Mrigashira": {"dosha": "Vata/Pitta", "yoga": "Nadi Shodhana (Alternate Nostril Breathing)"},
    "Ardra": {"dosha": "Vata", "yoga": "Shivasana (Corpse Pose - for release)"},
    "Punarvasu": {"dosha": "Kapha", "yoga": "Tadasana (Mountain Pose)"},
    "Pushya": {"dosha": "Kapha", "yoga": "Balasana (Child's Pose)"},
    "Ashlesha": {"dosha": "Kapha", "yoga": "Bhujangasana (Cobra Pose)"},
    "Magha": {"dosha": "Pitta", "yoga": "Virabhadrasana I (Warrior I)"},
    "Purva Phalguni": {"dosha": "Pitta", "yoga": "Dhanurasana (Bow Pose)"},
    "Uttara Phalguni": {"dosha": "Pitta/Kapha", "yoga": "Gomukhasana (Cow Face Pose)"},
    "Hasta": {"dosha": "Vata", "yoga": "Bakasana (Crow Pose)"},
    "Chitra": {"dosha": "Pitta", "yoga": "Trikonasana (Triangle Pose)"},
    "Swati": {"dosha": "Vata", "yoga": "Anjaneyasana (Crescent Lunge)"},
    "Vishakha": {"dosha": "Pitta/Kapha", "yoga": "Utkatasana (Chair Pose)"},
    "Anuradha": {"dosha": "Pitta/Kapha", "yoga": "Janu Sirsasana (Head-to-Knee Pose)"},
    "Jyeshtha": {"dosha": "Vata/Pitta", "yoga": "Ardha Matsyendrasana (Half Fish Pose)"},
    "Mula": {"dosha": "Vata", "yoga": "Adho Mukha Svanasana (Downward Dog)"},
    "Purva Ashadha": {"dosha": "Pitta", "yoga": "Ustrasana (Camel Pose)"},
    "Uttara Ashadha": {"dosha": "Pitta/Kapha", "yoga": "Paschimottanasana (Seated Forward Fold)"},
    "Shravana": {"dosha": "Kapha", "yoga": "Viparita Karani (Legs up Wall)"},
    "Dhanishta": {"dosha": "Pitta/Kapha", "yoga": "Natarajasana (Dancer Pose)"},
    "Shatabhisha": {"dosha": "Vata", "yoga": "Padmasana (Lotus Pose)"},
    "Purva Bhadrapada": {"dosha": "Vata/Pitta", "yoga": "Urdhva Dhanurasana (Wheel Pose)"},
    "Uttara Bhadrapada": {"dosha": "Kapha", "yoga": "Savasana (Deep Rest)"},
    "Revati": {"dosha": "Kapha", "yoga": "Matsyasana (Fish Pose)"}
}

NAKSHATRAS = list(WISDOM_DATA.keys())

# --- 2. THE CALCULATION ENGINE ---
def get_birth_sky(year, month, day, hour, minute, lat, lon, tzone_str):
    swe.set_ephe_path('./ephe') 
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    local_tz = pytz.timezone(tzone_str)
    dt = datetime(year, month, day, hour, minute)
    local_dt = local_tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute/60.0)

    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    def calc_obj(obj_id):
        res, _ = swe.calc_ut(jd, obj_id, flags)
        deg = res[0]
        nak_idx = int(deg / (360/27))
        nak_name = NAKSHATRAS[nak_idx]
        return {
            "Sign": ZODIAC_SIGNS[int(deg / 30)],
            "Nakshatra": nak_name,
            "Position": f"{round(deg % 30, 2)}°",
            "Dosha": WISDOM_DATA[nak_name]["dosha"],
            "Yoga": WISDOM_DATA[nak_name]["yoga"]
        }

    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    asc_nak = NAKSHATRAS[int(asc_deg / (360/27))]
    
    return {
        "Ascendant": {
            "Sign": ZODIAC_SIGNS[int(asc_deg/30)],
            "Nakshatra": asc_nak,
            "Position": f"{round(asc_deg % 30, 2)}°",
            "Dosha": WISDOM_DATA[asc_nak]["dosha"],
            "Yoga": WISDOM_DATA[asc_nak]["yoga"]
        },
        "Sun": calc_obj(swe.SUN),
        "Moon": calc_obj(swe.MOON),
        "Mercury": calc_obj(swe.MERCURY),
        "Venus": calc_obj(swe.VENUS),
        "Mars": calc_obj(swe.MARS),
        "Jupiter": calc_obj(swe.JUPITER),
        "Saturn": calc_obj(swe.SATURN),
        "Rahu": calc_obj(swe.MEAN_NODE)
    }

# --- 3. THE FRONTEND ---
st.set_page_config(page_title="My Birth Sky Sanctuary", layout="wide")
st.title("🌿 My Birth Sky Sanctuary")
st.write("Merging Astronomical Truth with Ayurvedic Wisdom")

with st.sidebar:
    st.header("Birth Details")
    client_name = st.text_input("Name", value="Danny")
    date = st.date_input("Date", value=datetime(1957, 5, 10))
    time = st.time_input("Time", value=datetime(1957, 5, 10, 12, 0).time())
    tz = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("America/Chicago"))
    lat = st.number_input("Latitude", value=41.8722, format="%.4f")
    lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
    submitted = st.button("Generate Alignment")

if submitted:
    sky = get_birth_sky(date.year, date.month, date.day, time.hour, time.minute, lat, lon, tz)
    
    st.header(f"Soul Alignment for {client_name}")
    
    # The Big Three + Ascendant
    col1, col2, col3, col4 = st.columns(4)
    for i, p in enumerate(["Ascendant", "Sun", "Moon", "Rahu"]):
        with [col1, col2, col3, col4][i]:
            st.metric(p, f"{sky[p]['Sign']}")
            st.write(f"**Nakshatra:** {sky[p]['Nakshatra']}")
            st.caption(f"Dosha: {sky[p]['Dosha']}")
            st.caption(f"Yoga: {sky[p]['Yoga']}")

    st.divider()
    st.subheader("Deep Planetary Narrative")
    
    for planet in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
        data = sky[planet]
        with st.expander(f"Explore {planet} in {data['Nakshatra']}"):
            st.write(f"**Internal Atmosphere (Dosha):** {data['Dosha']}")
            st.write(f"**Soulful Movement (Yoga Pose):** {data['Yoga']}")
            st.write(f"**Position:** {data['Position']} {data['Sign']}")
