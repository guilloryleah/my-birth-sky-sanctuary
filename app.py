import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE HOLISTIC MEDICINE ENGINE ---
def get_holistic_medicine(planet_name, sign, nakshatra_name):
    """
    Returns specific 'Medicine' based on the Planet + Nakshatra combination.
    Includes the 'Mars Journey' provided by the user.
    """
    
    # Placeholder for other planets (Sun, Moon, etc.)
    # As you provide them, we will fill these dictionaries.
    generic_data = {
        "astrology": "The light of this planet is ripening in this station.",
        "yoga": "Practice mindful presence.",
        "ayurveda": "Maintain balance through seasonal routine."
    }

    # --- THE MARS JOURNEY DATASET ---
    mars_medicine = {
        "Ashwini": {
            "astrology": "The 'Swift Lightning.' Mars here is impulsive and moves faster than the mind. It creates 'head-heat' and sudden bursts of energy that can lead to burnout.",
            "yoga": "Savasana with an Eye Pillow — To force the 'Internal Charioteer' to stop and rest the eyes.",
            "ayurveda": "Cranial Pressure. Use Brahmi oil on the scalp to prevent 'Mars-brain' (migraines/irritability)."
        },
        "Bharani": {
            "astrology": "The 'Volcano in the Vessel.' Mars here is under extreme pressure to transform. It represents the 'Fire of Birth' and deep survival instincts.",
            "yoga": "Baddha Konasana (Bound Angle) — To release the deep 'Apana' (downward) energy stored in the pelvic floor.",
            "ayurveda": "Pelvic Inflammation. Cool the 'Yoni/Linga' energy. Drink Aloe Vera juice to soothe the internal heat."
        },
        "Krittika": {
            "astrology": "The 'Commander’s Blade.' This is the sharpest Mars. It provides the power to 'cut' through obstacles but can become overly aggressive or critical.",
            "yoga": "Utkatasana (Chair Pose) — To channel the fire into the thighs and stabilize the 'Agnihotra'.",
            "ayurveda": "Blood Purifier. Mars here 'boils' the blood. Use Neem or Turmeric to clear toxins (Ama)."
        },
        "Rohini": {
            "astrology": "The 'Passionate Builder.' Mars here is stubborn and highly sensual. It seeks to guard its territory and its beauty with fierce loyalty.",
            "yoga": "Vrksasana (Tree Pose) — To ground the aggressive Mars energy into the earth.",
            "ayurveda": "Neck and Throat. Tension here often settles in the neck. Use warm Sesame oil massages."
        },
        "Mrigashira": {
            "astrology": "The 'Restless Hunter.' Mars is searching for a target. This creates nervous energy and a tendency to 'run' away from problems.",
            "yoga": "Garudasana (Eagle Pose) — To bind the limbs and force scattered energy into a single point of focus.",
            "ayurveda": "Sensory Exhaustion. The 'Deer' mind tires the eyes. Use Rosewater compresses."
        },
        "Ardra": {
            "astrology": "The 'Storm Warrior.' Mars here is destructive and emotional. It represents the 'teardrop' of the hunter.",
            "yoga": "Simhasana (Lion’s Breath) — To roar out the internal storm and clear the Rudra energy.",
            "ayurveda": "Lymphatic Flow. Use dry brushing to keep the 'storm' moving through the body."
        },
        "Punarvasu": {
            "astrology": "The 'Returning Arrow.' Mars here is defensive and protective. It seeks to return to a state of safety.",
            "yoga": "Anjaneyasana (Low Lunge) — To open the chest and pull the bow of the spirit back to its center.",
            "ayurveda": "Shoulder Tension. Use Mahanarayan oil on the upper back and shoulders."
        },
        "Pushya": {
            "astrology": "The 'Guardian of the Well.' Mars is 'Debilitated' (weakened) here. It creates passive-aggression.",
            "yoga": "Balasana (Child’s Pose) — To surrender the sword and find strength in vulnerability.",
            "ayurveda": "Digestive Agni. Mars 'steams' the stomach. Eat cooling, 'Moon-milk' (warm milk with cardamom)."
        },
        "Ashlesha": {
            "astrology": "The 'Serpent’s Grip.' Mars here is strategic, hypnotic, and can be 'poisonous' if provoked.",
            "yoga": "Bhujangasana (Cobra Pose) — To move energy through the spine like a fluid snake.",
            "ayurveda": "Joint Lubrication. Mars dries out joint fluid. Use Ghee in the diet."
        },
        "Magha": {
            "astrology": "The 'Ancestral King.' Mars here is noble and fights for honor. It can be overly proud and 'Heart-heavy.'",
            "yoga": "Tadasana (Mountain Pose) — To stand with the weight of the crown without letting the ego collapse the spine.",
            "ayurveda": "The Physical Heart. Use Arjuna bark to strengthen the cardiac muscle."
        },
        "Purva Phalguni": {
            "astrology": "The 'Relaxed Combatant.' Mars here wants to enjoy life. It is the 'War for Pleasure.'",
            "yoga": "Natarajasana (Dancer’s Pose) — To turn Mars-heat into creative expression.",
            "ayurveda": "Lower Back. Mars here can burn out the kidneys. Drink structured water."
        },
        "Uttara Phalguni": {
            "astrology": "The 'Soldier of Service.' Mars here is disciplined and focused on the 'Work.'",
            "yoga": "Setu Bandhasana (Bridge Pose) — To support the nervous bridge between heart and gut.",
            "ayurveda": "Nervous Digestion. Use cooling Mint or Fennel to calm the gut-brain axis."
        },
        "Hasta": {
            "astrology": "The 'Craftsman’s Fist.' Mars here is incredibly dexterous. It fights through skill and manipulation.",
            "yoga": "Bakasana (Crow Pose) — To put the Mars weight into the hands and balance 'clutched' energy.",
            "ayurveda": "Wrist and Forearm health. Use daily hand stretches and Sesame oil."
        },
        "Chitra": {
            "astrology": "The 'Architect of War.' Mars here is brilliant and aesthetic. It fights to create beauty.",
            "yoga": "Sirsasana (Headstand) — To flip the perspective and see the structure of the universe.",
            "ayurveda": "Skin Radiance. Mars can cause rashes (Pitta). Use Sandalwood paste."
        },
        "Swati": {
            "astrology": "The 'Wind-Swept Warrior.' Mars here is independent and moves like a kite.",
            "yoga": "Nadi Shodhana Pranayama — Balance the breath to ground the 'Airy Mars.'",
            "ayurveda": "Colon Health. Mars in Air signs causes bloating. Use 'Hing' (Asafoetida) in cooking."
        },
        "Vishakha": {
            "astrology": "The 'Two-Branched Path.' Mars here is at a crossroads between ambition and spiritual depth.",
            "yoga": "Parivrtta Trikonasana (Revolved Triangle) — To twist the soul and see both directions.",
            "ayurveda": "Bladder and Pelvis. Drink Cranberry or Coriander water to flush the system."
        },
        "Anuradha": {
            "astrology": "The 'Devoted Knight.' Mars here fights for friends, family, and the 'Lotus-path.'",
            "yoga": "Padmasana (Lotus) — To lock Mars energy into a seat of prayer.",
            "ayurveda": "Circulatory Vitality. Use warm spices like Cinnamon."
        },
        "Jyeshtha": {
            "astrology": "The 'Eldest Protector.' Mars here is at its most powerful and 'Psychic.'",
            "yoga": "Matsyendrasana (Seated Twist) — To wring out the poison of the ego.",
            "ayurveda": "Nervous Core. Use Ashwagandha to buffer against high-frequency stress."
        },
        "Moola": {
            "astrology": "The 'Uprooter.' Mars here is fierce and destructive to illusions.",
            "yoga": "Adho Mukha Svanasana (Downward Dog) — To ground the root-striking energy.",
            "ayurveda": "The Psoas Muscle. Release it to stop the 'Mars-panic' of fight-or-flight."
        },
        "Purva Ashada": {
            "astrology": "The 'Invincible Invader.' Mars here is fueled by the power of conviction.",
            "yoga": "Virabhadrasana I (Warrior I) — To stand as an invincible force.",
            "ayurveda": "Liver Heat. Use Dandelion root or Milk Thistle to keep the blood clean."
        },
        "Uttara Ashada": {
            "astrology": "The 'Eternal Victor.' Mars is 'Exalted' here. Disciplined and unstoppable.",
            "yoga": "Salamba Sarvangasana (Shoulder Stand) — To stabilize the body in a single victory.",
            "ayurveda": "Bone Strength. High mineral intake and Ghee for joint cushioning."
        },
        "Shravana": {
            "astrology": "The 'Silent Soldier.' Mars here fights through listening and observation.",
            "yoga": "Viparita Karani (Legs Up Wall) — To let the Mars-blood drain back into the heart.",
            "ayurveda": "The Ears. Avoid loud sounds; keep ears warm and quiet."
        },
        "Dhanishta": {
            "astrology": "The 'Drummer of War.' Mars here is rhythmic, communal, and 'Electric.'",
            "yoga": "Ustrasana (Camel Pose) — To open the heart to the Cosmic Drum.",
            "ayurveda": "The Ankles. Use magnesium oil to prevent cramping."
        },
        "Shatabhisha": {
            "astrology": "The 'Healing Rebel.' Mars here is unconventional and heals by breaking rules.",
            "yoga": "Savasana — To enter the Void and allow the stars to heal fatigue.",
            "ayurveda": "Detoxification. Use Kitchari (mung bean and rice) cleanses."
        },
        "Purva Bhadrapada": {
            "astrology": "The 'Two-Faced Fire.' Mars here is a spiritual 'Priest-Warrior.'",
            "yoga": "Pincha Mayurasana (Forearm Balance) — To balance the two faces of the ego.",
            "ayurveda": "The Feet. Use warm foot baths with Epsom salts."
        },
        "Uttara Bhadrapada": {
            "astrology": "The 'Deep Sea Guardian.' Mars here guards the dreaming world.",
            "yoga": "Ananta Shayanasana (Side Reclining) — To rest like the Infinite Serpent.",
            "ayurveda": "Deep Sleep. Use Nutmeg in warm milk to ground spiritual visions."
        },
        "Revati": {
            "astrology": "The 'Shepherd of Souls.' Mars here is at the end of its journey. The Gentle Warrior.",
            "yoga": "Yoga Nidra — To dissolve the Warrior entirely into the Ocean.",
            "ayurveda": "Psychological Peace. Use Sandalwood oil on the Third Eye."
        }
    }

    if planet_name == "Mars":
        return mars_medicine.get(nakshatra_name, generic_data)
    else:
        return generic_data

# --- 2. NAKSHATRA MAPPING LOGIC ---
def get_nakshatra_name(sign, degree):
    """Calculates the specific Nakshatra name based on Sidereal degrees."""
    if sign == "Aries":
        if degree < 13.333: return "Ashwini"
        elif degree < 26.666: return "Bharani"
        return "Krittika"
    elif sign == "Taurus":
        if degree < 10.0: return "Krittika"
        elif degree < 23.333: return "Rohini"
        return "Mrigashira"
    elif sign == "Gemini":
        if degree < 6.666: return "Mrigashira"
        elif degree < 20.0: return "Ardra"
        return "Punarvasu"
    elif sign == "Cancer":
        if degree < 3.333: return "Punarvasu"
        elif degree < 16.666: return "Pushya"
        return "Ashlesha"
    elif sign == "Leo":
        if degree < 13.333: return "Magha"
        elif degree < 26.666: return "Purva Phalguni"
        return "Uttara Phalguni"
    elif sign == "Virgo":
        if degree < 10.0: return "Uttara Phalguni"
        elif degree < 23.333: return "Hasta"
        return "Chitra"
    elif sign == "Libra":
        if degree < 6.666: return "Chitra"
        elif degree < 20.0: return "Swati"
        return "Vishakha"
    elif sign == "Scorpio":
        if degree < 3.333: return "Vishakha"
        elif degree < 16.666: return "Anuradha"
        return "Jyeshtha"
    elif sign == "Sagittarius":
        if degree < 13.333: return "Moola"
        elif degree < 26.666: return "Purva Ashada"
        return "Uttara Ashada"
    elif sign == "Capricorn":
        if degree < 10.0: return "Uttara Ashada"
        elif degree < 23.333: return "Shravana"
        return "Dhanishta"
    elif sign == "Aquarius":
        if degree < 6.666: return "Dhanishta"
        elif degree < 20.0: return "Shatabhisha"
        return "Purva Bhadrapada"
    elif sign == "Pisces":
        if degree < 3.333: return "Purva Bhadrapada"
        elif degree < 16.666: return "Uttara Bhadrapada"
        return "Revati"
    return "Unknown"

# --- 3. EPHEMERIS CALCULATIONS ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    # Timezone Handling
    if year > 1800:
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)
        timezone = pytz.timezone(tz_name or "UTC")
        local_dt = timezone.localize(datetime(year, month, day, hour, minute))
        utc_dt = local_dt.astimezone(pytz.utc)
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
    else:
        jd_ut = swe.julday(year, month, day, hour + minute/60.0)

    # Sidereal Settings
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)

    # Ascendant
    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    asc_sign = signs[int(asc_raw / 30)]
    asc_deg = asc_raw % 30
    asc_nak = get_nakshatra_name(asc_sign, asc_deg)

    # Planets
    planet_ids = [(swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"), 
                  (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"), 
                  (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")]
    
    results = []
    for p_id, p_name in planet_ids:
        res, ret = swe.calc_ut(jd_ut, p_id, swe.FLG_SIDEREAL)
        long = res[0]
        p_sign = signs[int(long / 30)]
        p_deg = long % 30
        p_nak = get_nakshatra_name(p_sign, p_deg)
        medicine = get_holistic_medicine(p_name, p_sign, p_nak)
        
        results.append({
            "name": p_name,
            "sign": p_sign,
            "deg": p_deg,
            "nakshatra": p_nak,
            "astrology": medicine["astrology"],
            "yoga": medicine["yoga"],
            "ayurveda": medicine["ayurveda"]
        })

    return {"asc_sign": asc_sign, "asc_deg": asc_deg, "asc_nak": asc_nak, "planets": results}

# --- 4. STREAMLIT INTERFACE ---
st.set_page_config(page_title="Real-Sky Soul Map", layout="wide")
st.title("✨ The Real-Sky Soul Map: Eternal Edition")

with st.sidebar:
    st.header("Birth Calibration")
    address = st.text_input("Birth Location", "Houston, USA")
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24), min_value=datetime(1, 1, 1))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    seeker = st.text_input("Seeker Name", "Leah G")

geolocator = Nominatim(user_agent="soul_map_eternal")
location = geolocator.geocode(address)

if location and st.button("Generate Medicine"):
    data = calculate_soul_map(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute, location.latitude, location.longitude)
    
    st.header(f"Soul Map: {seeker}")
    st.subheader(f"Ascendant: {data['asc_deg']:.2f}° {data['asc_sign']} in {data['asc_nak']}")
    st.divider()

    # Layout for Planets
    for p in data['planets']:
        with st.expander(f"{p['name']} in {p['nakshatra']} ({p['sign']})"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**The Astrology:** {p['astrology']}")
                st.markdown(f"🧘 **Yoga:** {p['yoga']}")
            with col2:
                st.info(f"🍃 **Ayurveda:**\n{p['ayurveda']}")

st.caption("A sanctuary built on Real-Sky data and Holistic Wisdom.")
