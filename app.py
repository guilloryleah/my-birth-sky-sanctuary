import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- 1. THE UNIVERSAL NAKSHATRA MEDICINE (POEMS & PROTOCOLS) ---
def get_nakshatra_medicine(nakshatra_name):
    """
    Returns the Astrology, Yoga, and Ayurveda for each Nakshatra.
    These are the foundational 'poems' for each of the 27 stations.
    """
    
    medicine_vault = {
        "Ashwini": {
            "astrology": "The 'Swift Lightning.' Impulsive and moves faster than the mind. It creates 'head-heat' and sudden bursts of energy that can lead to burnout.",
            "yoga": "Savasana with an Eye Pillow — To force the 'Internal Charioteer' to stop and rest the eyes.",
            "ayurveda": "Cranial Pressure. Use Brahmi oil on the scalp to prevent migraines and irritability."
        },
        "Bharani": {
            "astrology": "The 'Volcano in the Vessel.' Under extreme pressure to transform. It represents the 'Fire of Birth' and deep survival instincts.",
            "yoga": "Baddha Konasana (Bound Angle) — To release the deep 'Apana' (downward) energy stored in the pelvic floor.",
            "ayurveda": "Pelvic Inflammation. Cool the 'Yoni/Linga' energy. Drink Aloe Vera juice to soothe the internal heat."
        },
        "Krittika": {
            "astrology": "The 'Commander’s Blade.' The sharpest station. It provides the power to 'cut' through obstacles but can become overly aggressive or critical.",
            "yoga": "Utkatasana (Chair Pose) — To channel the fire into the thighs and stabilize the 'Agnihotra'.",
            "ayurveda": "Blood Purifier. This energy 'boils' the blood. Use Neem or Turmeric to clear toxins (Ama) from the circulatory system."
        },
        "Rohini": {
            "astrology": "The 'Passionate Builder.' Stubborn and highly sensual. It seeks to guard its territory and its beauty with fierce loyalty.",
            "yoga": "Vrksasana (Tree Pose) — To ground aggressive energy into the earth, preventing 'Bull-headed' stubbornness.",
            "ayurveda": "Neck and Throat. Tension often settles here. Use warm Sesame oil massages on the throat."
        },
        "Mrigashira": {
            "astrology": "The 'Restless Hunter.' Searching for a target. This creates nervous energy and a tendency to 'run' away from problems or chase illusions.",
            "yoga": "Garudasana (Eagle Pose) — To bind the limbs and force scattered energy into a single point of focus.",
            "ayurveda": "Sensory Exhaustion. The 'Deer' mind tires the eyes. Use Rosewater compresses to cool the optical nerves."
        },
        "Ardra": {
            "astrology": "The 'Storm Warrior.' Destructive and emotional. It represents the 'teardrop' of the hunter. It fights through chaos and sudden shifts.",
            "yoga": "Simhasana (Lion’s Breath) — To roar out the internal storm and clear the 'Rudra' energy from the chest.",
            "ayurveda": "Lymphatic Flow. Can cause 'stagnant heat.' Use dry brushing to keep the 'storm' moving through the body."
        },
        "Punarvasu": {
            "astrology": "The 'Returning Arrow.' Defensive and protective. It seeks to return to a state of safety and 'Home.'",
            "yoga": "Anjaneyasana (Low Lunge) — To open the chest and 'pull the bow' of the spirit back to its center.",
            "ayurveda": "Shoulder Tension. Carries the weight of the world. Use Mahanarayan oil on the upper back and shoulders."
        },
        "Pushya": {
            "astrology": "The 'Guardian of the Well.' Strength found in vulnerability. It creates a protective, nurturing energy that resists aggressive conflict.",
            "yoga": "Balasana (Child’s Pose) — To surrender the 'sword' and realize that true strength is found in stillness.",
            "ayurveda": "Digestive Agni. This energy 'steams' the stomach. Eat cooling 'Moon-milk' (warm milk with cardamom) to soothe the lining."
        },
        "Ashlesha": {
            "astrology": "The 'Serpent’s Grip.' Strategic, hypnotic, and can be 'poisonous' if provoked. It moves with secret maneuvers and deep intensity.",
            "yoga": "Bhujangasana (Cobra Pose) — To move energy through the spine like a fluid snake, preventing 'joint-locking.'",
            "ayurveda": "Joint Lubrication. Dries out the 'Shleshaka Kapha' (joint fluid). Use Ghee in the diet to keep the 'hinges' moving."
        },
        "Magha": {
            "astrology": "The 'Ancestral King.' Noble and concerned with honor and legacy. It can be overly proud and 'Heart-heavy.'",
            "yoga": "Tadasana (Mountain Pose) — To stand with the weight of the crown without letting the ego collapse the spine.",
            "ayurveda": "The Physical Heart. Can cause 'heart-burn' or palpitations. Use Arjuna bark to strengthen the cardiac muscle."
        },
        "Purva Phalguni": {
            "astrology": "The 'Relaxed Combatant.' Wants to enjoy life and fights for the right to rest and create. It is the 'War for Pleasure.'",
            "yoga": "Natarajasana (Dancer’s Pose) — To turn heat into a creative, rhythmic expression.",
            "ayurveda": "Lower Back. Can 'burn out' the kidneys. Drink plenty of structured water and avoid excess salt."
        },
        "Uttara Phalguni": {
            "astrology": "The 'Soldier of Service.' Disciplined and focused on the 'Work.' It seeks to organize and perfect the environment.",
            "yoga": "Setu Bridge Pose — To support the 'nervous bridge' between the heart and the gut.",
            "ayurveda": "Nervous Digestion. 'Fries' the small intestine. Use cooling Mint or Fennel to calm the gut-brain axis."
        },
        "Hasta": {
            "astrology": "The 'Craftsman’s Fist.' Incredibly dexterous. It works through skill, manipulation, and the 'Magic of the Hand.'",
            "yoga": "Bakasana (Crow Pose) — To put the entire weight into the hands and balance the 'clutched' energy.",
            "ayurveda": "Wrist and Forearm. Tension from 'over-working' shows up here. Use daily hand stretches and Sesame oil."
        },
        "Chitra": {
            "astrology": "The 'Architect of War.' Brilliant and aesthetic. It seeks to create beauty or to 'rebuild' life from the ashes.",
            "yoga": "Sirsasana (Headstand) — To flip the perspective and see the 'structure' of the universe clearly.",
            "ayurveda": "Skin Radiance. Can cause rashes (Pitta). Use Sandalwood paste to cool the skin and lower internal 'glare.'"
        },
        "Swati": {
            "astrology": "The 'Wind-Swept Warrior.' Independent and moves like a kite. It fights for freedom and has a 'restless' independence.",
            "yoga": "Nadi Shodhana Pranayama — Balance the breath to ground the 'Airy' energy.",
            "ayurveda": "Colon Health. In 'Air' signs, causes gas/bloating. Use 'Hing' (Asafoetida) in cooking to ground the 'Vata.'"
        },
        "Vishakha": {
            "astrology": "The 'Two-Branched Path.' At a crossroads. It struggles between worldly ambition and spiritual depth.",
            "yoga": "Parivrtta Trikonasana (Revolved Triangle) — To 'twist' the soul and see both directions at once.",
            "ayurveda": "Bladder and Pelvis. Can cause 'burning' sensations. Drink Cranberry or Coriander water to flush the system."
        },
        "Anuradha": {
            "astrology": "The 'Devoted Knight.' Softened by the 'Star of Success.' It is dedicated to friends, family, and the 'Lotus-path.'",
            "yoga": "Padmasana (Lotus) — To lock energy into a seat of prayer and devotion.",
            "ayurveda": "Circulatory Vitality. Keep the blood moving. Use 'Warm' spices like Cinnamon to ensure energy doesn't become 'cold and dark.'"
        },
        "Jyeshtha": {
            "astrology": "The 'Eldest Protector.' Powerful and 'Psychic.' It works with wisdom, secrets, and the 'Earring of Power.'",
            "yoga": "Matsyendrasana (Seated Twist) — To wring out the 'poison' of the ego and access hidden power.",
            "ayurveda": "Nervous Core. Can be 'highly-strung.' Use Ashwagandha to 'buffer' the nerves against stress."
        },
        "Moola": {
            "astrology": "The 'Uprooter.' Fierce and destructive to illusions. It seeks the 'Root' of the problem, often by burning the house down.",
            "yoga": "Adho Mukha Svanasana (Downward Dog) — To ground the 'Root-striking' energy into the hands and feet.",
            "ayurveda": "The Psoas Muscle. The seat of 'Fight or Flight' trauma. Release it to stop the internal 'panic.'"
        },
        "Purva Ashada": {
            "astrology": "The 'Invincible Invader.' Fueled by 'The Early Victory.' It moves with the fluidity of water and the power of conviction.",
            "yoga": "Virabhadrasana I (Warrior I) — To stand as an 'Invincible' force, lunging toward the goal.",
            "ayurveda": "Liver Heat. 'Angers' the liver. Use 'Dandelion root' or 'Milk Thistle' to keep the blood clean."
        },
        "Uttara Ashada": {
            "astrology": "The 'Eternal Victor.' Controlled, disciplined, and unstoppable. The 'Mountaineer' of the zodiac.",
            "yoga": "Salamba Sarvangasana (Shoulder Stand) — To stabilize the entire 'Kingdom' of the body in a single, focused 'victory.'",
            "ayurveda": "Bone Strength. Builds the 'Asti Dhatu' (Bones). Ensure high mineral intake and Ghee for joint cushioning."
        },
        "Shravana": {
            "astrology": "The 'Silent Soldier.' Acts through 'Listening.' It is the energy of the scout or the monk. It conquers through patience.",
            "yoga": "Viparita Karani (Legs Up the Wall) — To let the blood drain back into the heart and 'listen' to the internal pulse.",
            "ayurveda": "The Ears. Can cause Tinnitus. Keep the ears warm and quiet; avoid loud, 'aggressive' sounds."
        },
        "Dhanishta": {
            "astrology": "The 'Drummer of War.' Rhythmic and communal. It works for the 'Group' and the 'Future.' The 'Electric Warrior.'",
            "yoga": "Ustrasana (Camel Pose) — To open the heart to the 'Cosmic Drum' and release 'future-fear.'",
            "ayurveda": "The Ankles. Puts tension on the 'base of the flow.' Use magnesium oil on the ankles to prevent cramping."
        },
        "Shatabhisha": {
            "astrology": "The 'Healing Rebel.' Unconventional. It works with 'The Hundred Physicians.' Heals the world by breaking the rules.",
            "yoga": "Savasana — To enter the 'Void' and allow the 'Hundred Stars' to heal fatigue.",
            "ayurveda": "Detoxification. Can hold 'stagnant toxins.' Use 'Kitchari' (mung bean and rice) cleanses to reset."
        },
        "Purva Bhadrapada": {
            "astrology": "The 'Two-Faced Fire.' Highly spiritual but 'Dualistic.' It fights for the 'Light' but knows the 'Dark.' The 'Priest-Warrior.'",
            "yoga": "Pincha Mayurasana (Forearm Balance) — To balance the 'Two faces' of the ego on the 'Arms of Truth.'",
            "ayurveda": "The Feet. Can feel 'un-grounded.' Use warm foot baths with Epsom salts to pull the fire down."
        },
        "Uttara Bhadrapada": {
            "astrology": "The 'Deep Sea Guardian.' Quiet and hidden in the 'Deep Water.' It guards the 'Dreaming World.'",
            "yoga": "Ananta Shayanasana (Side Reclining) — To rest like the 'Infinite Serpent' and realize the war is won in the dream.",
            "ayurveda": "Deep Sleep. Can cause insomnia. Use 'Nutmeg' in warm milk before bed to ground the spiritual visions."
        },
        "Revati": {
            "astrology": "The 'Shepherd of Souls.' At the end of the journey. The 'Gentle Warrior.' It guides others to the 'Final Shore.'",
            "yoga": "Yoga Nidra — To dissolve the 'Warrior' entirely into the 'Ocean.'",
            "ayurveda": "Psychological Peace. Use Sandalwood oil on the 'Third Eye' to bring peace to the soul."
        }
    }

    return medicine_vault.get(nakshatra_name, {
        "astrology": "Wisdom ripening...",
        "yoga": "Mindful Presence",
        "ayurveda": "Balance the elements."
    })

# --- 2. NAKSHATRA MAPPING ---
def get_nakshatra_name(sign, degree):
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
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name or "UTC")
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)

    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    asc_sign = signs[int(asc_raw / 30)]
    asc_deg = asc_raw % 30
    asc_nak = get_nakshatra_name(asc_sign, asc_deg)

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
        medicine = get_nakshatra_medicine(p_nak)
        
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
    b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24))
    b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())
    seeker = st.text_input("Seeker Name", "Leah G")

# Robust Geolocation logic
geolocator = Nominatim(user_agent="my_birth_sky_sanctuary_leahg")
location = None
if address:
    try:
        location = geolocator.geocode(address, timeout=10)
    except Exception as e:
        st.error("The map service is currently busy. Please wait a moment and try again.")

if location and st.button("Generate Medicine"):
    data = calculate_soul_map(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute, location.latitude, location.longitude)
    
    st.header(f"Soul Map: {seeker}")
    st.subheader(f"Ascendant: {data['asc_deg']:.2f}° {data['asc_sign']} in {data['asc_nak']}")
    
    asc_med = get_nakshatra_medicine(data['asc_nak'])
    with st.expander(f"Rising Soul Path: {data['asc_nak']}"):
        st.markdown(f"**The Astrology:** {asc_med['astrology']}")
        st.markdown(f"🧘 **Yoga:** {asc_med['yoga']}")
        st.markdown(f"🍃 **Ayurveda:** {asc_med['ayurveda']}")
    
    st.divider()

    for p in data['planets']:
        with st.expander(f"{p['name']} in {p['nakshatra']} ({p['sign']})"):
            st.markdown(f"### The Astrology")
            st.write(p['astrology'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("🧘 **Yoga Pose**")
                st.info(p['yoga'])
            with col2:
                st.markdown("🍃 **Ayurvedic Alignment**")
                st.success(p['ayurveda'])

st.caption("A sanctuary built on Real-Sky data and Holistic Wisdom.")
