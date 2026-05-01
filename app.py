import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE HOLISTIC NAKSHATRA ENGINE ---
def get_nakshatra_data(sign, degree):
    """Returns the full holistic profile: Poem, Yoga, and Ayurvedic Alignment."""
    
    # We use a dictionary to store the 'Universal' Nakshatra data
    # Some Nakshatras have 'Sign-Specific' Yoga poses which we handle below
    data = {
        "Ashwini": {
            "poem": "Heal the ghost of the old self before you try to outrun it. The horse gallops not to flee the past, but to collide with the future. Listen for the medicine that hums in the silence of the dawn. Stop searching for a cure and realize you are the physician of your own wreckage.",
            "yoga": "Virabhadrasana III (Warrior III) — Channels Ketu’s swift, focused balance.",
            "ayurveda": "Calm the Head and Skull (Prana Vayu). Use Brahmi oil to soothe mental speed."
        },
        "Bharani": {
            "poem": "Carry the weight of your becoming until it turns into a wing. The dark soil is not a grave for your spirit, but a womb for your power. Hold the tension of the middle path with a grit that tastes like grace. Give birth to the version of you that no longer asks for permission to exist.",
            "yoga": "Malasana (Garland Pose) — Connects to the womb and downward-moving energy.",
            "ayurveda": "Support Reproductive Vitality. Focus on warm, grounding foods to balance Vata."
        },
        "Krittika": {
            "poem": "Burn away the brush until only the gold has room to breathe. The blade that cuts you open is the same one that sets you free. Seek the heat that transforms your form rather than the fire that feeds your ego. Let your truth be a cauterizing flame that heals the cold world by touch.",
            "yoga": "Utkatasana (Chair Pose) — Ignites the internal fire (Agni).",
            "ayurveda": "Purify the Blood (Raktha Dhatu). Avoid spicy foods to keep Pitta in check.",
            "special_yoga": {"Taurus": "Bhujangasana (Cobra Pose) — Opens the throat and neck, the Taurus seat of power."},
            "special_ayurveda": {"Taurus": "Balance the Thyroid and Neck. Use cooling herbs like Coriander."}
        },
        "Rohini": {
            "poem": "Plant your feet where the earth is soft and red with ancient memory. Ascend the heights by sinking deeper into the marrow of your being. Tend to the garden of the heart with hands that have forgotten how to hurry. Beauty is not an ornament; it is the vital oxygen that mends a fractured soul.",
            "yoga": "Vrksasana (Tree Pose) — Reflects growth, fertility, and earthy stability.",
            "ayurveda": "Hydrate the Skin and Fluids. Focus on nourishing, Kapha-balancing tonics."
        },
        "Mrigashira": {
            "poem": "Stop chasing the horizon and start watching the rhythm of your shadow. The nectar you seek is hidden in the quiet stride of the searcher. Softness is the only armor that the world is unable to pierce or break. Find the sanctuary that exists between the inhale and the exhale.",
            "yoga": "Paschimottanasana (Seated Forward Fold) — Calms the restless mind.",
            "ayurveda": "Soothe the Senses. Use Nasya (nasal oil) to ground the airy Vata energy.",
            "special_yoga": {"Gemini": "Garudasana (Eagle Pose) — Enhances neuro-muscular coordination and focus."},
            "special_ayurveda": {"Gemini": "Lung Health and Breath (Pranayama). Focus on expansion."}
        },
        "Ardra": {
            "poem": "Let the storm wash the salt from your eyes until you see without filters. The thunder is the sound of the ego’s architecture finally crumbling. Stand naked in the rain until you are nothing but the core of the lightning. Renewal begins only when you stop trying to keep your old life dry.",
            "yoga": "Simhasana (Lion’s Breath) — Releases the 'storm' of pent-up emotions.",
            "ayurveda": "Detoxify the Sweat and Lymph. Use bitter greens to clear Rahu’s intensity."
        },
        "Punarvasu": {
            "poem": "Return to the center after every long wandering through the wild. The arrow finds the mark only when the hand has ceased its trembling. Trust the cycles of the light as deeply as you trust the dark of the moon. You are the destination you have been traveling a thousand lives to find.",
            "yoga": "Dhanurasana (Bow Pose) — Symbolizes the expansion of the chest.",
            "ayurveda": "Strengthen the Shoulders and Upper Arms. Focus on B vitamins for nerve health.",
            "special_yoga": {"Cancer": "Anjaneyasana (Low Lunge) — Opens the heart/lunar connection."},
            "special_ayurveda": {"Cancer": "Support Digestion (Jathara Agni). Eat warm, easily digestible soups."}
        },
        "Pushya": {
            "poem": "Feed the spirit until it is heavy enough to anchor the drifting mind. Flow like the milk of a star through the veins of the heavy night. Stability is found in the absolute surrender to the service of the sacred. Be the hollow bone; let a higher wisdom play its song through your life.",
            "yoga": "Balasana (Child’s Pose) — The pose of ultimate safety and nurturing.",
            "ayurveda": "Nourish the Breast and Chest tissue. Use Shatavari to enhance Ojas."
        },
        "Ashlesha": {
            "poem": "Embrace the serpent that guards the gates of your inner temple. The sting is the wake-up call for the god who fell asleep in your skin. Look into the dark until the dark begins to reflect your own inner light. Shed the skin of who you were so the truth can breathe through your pores.",
            "yoga": "Bhujangasana (Cobra Pose) — Connects to serpent energy and joint power.",
            "ayurveda": "Joints and Synovial Fluid. Avoid inflammatory nightshades."
        },
        "Magha": {
            "poem": "Honor the blood that flows through your veins, for it is an ocean of ancestors. The throne is a cage unless the heart is humble enough to serve the lowest. Walk with the kings of the past but dream a dream they were too afraid to see. Noble action is the only currency that buys a seat in the hall of the eternal.",
            "yoga": "Tadasana (Mountain Pose) — Standing with the dignity of the ancestors.",
            "ayurveda": "Heart Health. Use Arjuna bark tea to strengthen the physical heart."
        },
        "Purva Phalguni": {
            "poem": "Dance until the dancer and the dance are swallowed by the movement. The creative spark is the only bridge that spans the gap to the divine. Rest is a sacred prayer; do not apologize for the stillness that restores you. Pour your love into the world like a wine that never runs dry.",
            "yoga": "Natarajasana (Dancer’s Pose) — Celebrates the Venusian spirit.",
            "ayurveda": "Relax the Spine. Focus on magnesium to prevent muscle tension."
        },
        "Uttara Phalguni": {
            "poem": "Extend your hand to the one who walks in the shadow behind you. The healer’s touch is not a technique, but a state of absolute presence. Steady the mind like a flame in a room where the wind has finally died. The path to the stars is paved with the small, quiet stones of kindness.",
            "yoga": "Setu Bridge Pose — A bridge for supporting others and the self.",
            "ayurveda": "Spinal Alignment. Practice Shavasana daily to reset the Sun's energy.",
            "special_yoga": {"Virgo": "Trikonasana (Triangle Pose) — Brings geometric precision and focus."},
            "special_ayurveda": {"Virgo": "Lower Abdomen. Use Fennel or Cumin to assist digestion."}
        },
        "Hasta": {
            "poem": "Create what has never been seen with the magic of your open palms. The power is in the focus of the eye, not in the movement of the hand. Grasp the truth with everything you have, then let the outcome go. Your work is the physical signature of the peace you have found within.",
            "yoga": "Bakasana (Crow Pose) — Focuses on hand strength and dexterity.",
            "ayurveda": "Hand and Wrist Health. Massage hands with sesame oil."
        },
        "Chitra": {
            "poem": "Carve the diamond of the soul out of the rough and heavy stone of habit. The external glow is merely a shadow of the fire burning in your chest. Build a temple out of the ruins of your yesterday and live in its heart. The masterpiece is not what you make, but the life you choose to inhabit.",
            "yoga": "Sirsasana (Headstand) — The architect's view; perfect structural alignment.",
            "ayurveda": "Metabolism. Enzyme-rich foods for structural 'building.'",
            "special_yoga": {"Libra": "Ardha Chandrasana (Half Moon) — Balancing the internal architect."},
            "special_ayurveda": {"Libra": "Kidneys. Drink pure, structured water to flush toxins."}
        },
        "Swati": {
            "poem": "Sway with the wind but never lose the root that holds you to the earth. Freedom is the ability to find your breath in the center of the hurricane. Scatter your seeds without worry; the earth knows exactly where they belong. The spirit travels furthest when it stops carrying the weight of its names.",
            "yoga": "Pranayama (Nadi Shodhana) — The alignment of the wind.",
            "ayurveda": "Colon Health. Use Triphala to ensure Vata moves downward."
        },
        "Vishakha": {
            "poem": "Aim for the highest peak but cherish the blood on the jagged path. Patience is the slow fire that tempers the iron of the human soul. Break the old idols of your mind to find the living truth they were hiding. The victory is won the moment you stop fighting yourself for the prize.",
            "yoga": "Parivrtta Trikonasana (Revolved Triangle) — Represents mental focus.",
            "ayurveda": "Bladder and Hips. Keep the pelvic region warm and mobile.",
            "special_yoga": {"Scorpio": "Baddha Konasana (Bound Angle) — Directs energy toward the pelvic seat."},
            "special_ayurveda": {"Scorpio": "Hormonal Balance. Support the endocrine system with healthy fats."}
        },
        "Anuradha": {
            "poem": "Weave the threads of your devotion into a cloak that can weather any winter. Friendship is the bridge that keeps the soul from drowning in the lonely sea. Look for the blossom that thrives in the mud; that is where the secret lies. Belonging is not a frequency you find, but a frequency you finally learn to tune.",
            "yoga": "Padmasana (Lotus Pose) — Deep devotion and stillness.",
            "ayurveda": "Blood Circulation. Use Ginger and Turmeric."
        },
        "Jyeshtha": {
            "poem": "Protect the spark that flickers in the deepest, coldest cave of your being. Wisdom is a shield that only grows thick through the passage of time. Listen to the heavy silence that sits beneath the noise of the world. The elder within you is waiting for you to stop talking and start seeing.",
            "yoga": "Matsyendrasana (Seated Twist) — Wrings out toxins from the nervous system.",
            "ayurveda": "Nervous System (Majja Dhatu). Ashwagandha grounds this energy."
        },
        "Moola": {
            "poem": "Dig past the layers of bone until you strike the primary root of existence. The collapse of your world is the invitation for the truth to be born. Destroy everything that is false so that what is eternal can finally stand. Foundations are only discovered when you have reached the absolute bottom.",
            "yoga": "Adho Mukha Svanasana (Downward Dog) — Rooting deep into foundations.",
            "ayurveda": "Thighs and Hips. Stretch the Psoas to release trauma."
        },
        "Purva Ashada": {
            "poem": "Dive into the depths where the light of the sun is a forgotten memory. Surrender to the current and let the great tides decide your direction. The ocean is not an obstacle; it is the vast embrace of the mother. In the middle of the deep water, discover that you are the shore.",
            "yoga": "Virabhadrasana I (Warrior I) — The invincible water warrior.",
            "ayurveda": "Gallbladder and Liver. Use cooling bitters."
        },
        "Uttara Ashada": {
            "poem": "Stand like a mountain of light against the howling wind of the world’s opinion. The sun of the spirit never sets on a heart that has nothing to hide. Commitment is the anchor that holds when the sky turns black with rain. Integrity is the only peak that offers a view of the entire universe.",
            "yoga": "Salamba Sarvangasana (Shoulder Stand) — Total system victory.",
            "ayurveda": "Bone Density. Support with minerals like Calcium/Magnesium.",
            "special_yoga": {"Capricorn": "Phalakasana (Plank Pose) — Builds structural endurance."},
            "special_ayurveda": {"Capricorn": "Knee Health. Lubricate joints with Ghee to prevent dryness."}
        },
        "Shravana": {
            "poem": "Listen to the pulse of the stars as it beats inside your own ears. Learning is the art of becoming a mirror that reflects the light of the sun. Walk the earth as if every step were a word in a holy and secret book. Knowledge is a weight you carry; wisdom is the light that carries you.",
            "yoga": "Viparita Karani (Legs Up Wall) — A pose of receptive listening.",
            "ayurveda": "Hearing and Ears. Use warm oil (Karna Purana) in ears."
        },
        "Dhanishta": {
            "poem": "Find the rhythm that beats beneath the skin of the physical world. Abundance flows only to the hand that is open enough to let it go. Let your every movement be a ritual for the gods who live in the silence. The drum of the heart is the only map you need to navigate the divine.",
            "yoga": "Ustrasana (Camel Pose) — Opens the heart rhythm.",
            "ayurveda": "Ankles. Keep lower legs warm and manage electrolytes.",
            "special_yoga": {"Aquarius": "Marjaryasana/Bitilasana (Cat-Cow) — Rhythmic flow in the spine."},
            "special_ayurveda": {"Aquarius": "Circulation. Dry brushing helps move 'electric' energy."}
        },
        "Shatabhisha": {
            "poem": "Hide within the hundred veils until you find the eye that never blinks. The mystery is not a problem to be solved, but a reality to be entered. Heal the wounds of the world by mending the fractures in your own soul. The void is not empty; it is the womb of everything that is yet to be.",
            "yoga": "Savasana (Corpse Pose) — Entering the void for total healing.",
            "ayurveda": "Detoxification. Fasting or Kitchari cleanses."
        },
        "Purva Bhadrapada": {
            "poem": "Face the fire of your own shadow and do not turn your eyes away. Transformation requires the absolute death of the mask you wear for others. Carry the torch of your truth through the longest tunnel of the dark. The warrior’s greatest battle is won the moment the sword is laid down.",
            "yoga": "Pincha Mayurasana (Forearm Balance) — Balance and fierce focus.",
            "ayurveda": "Feet and Toes. Reflexology grounds this spiritual energy.",
            "special_yoga": {"Pisces": "Janu Sirsasana (Head-to-Knee Pose) — Deep surrender and internal fire."},
            "special_ayurveda": {"Pisces": "Immune System. Strengthen 'Bala' (strength) with Ojas-building foods."}
        },
        "Uttara Bhadrapada": {
            "poem": "Sleep in the deep, still waters and dream the world back into balance. Peace is the treasure guarded by the mind that has stopped seeking. The end of the journey is the discovery that you never truly left home. Dissolve into the blue of the infinite and realize you are the sky.",
            "yoga": "Ananta Shayanasana (Side Reclining) — The pose of the infinite.",
            "ayurveda": "Sleep Quality. Establish a strict daily routine (Dinacharya)."
        },
        "Revati": {
            "poem": "Walk the final shore and leave no footprints for the world to follow. The traveler is the path, and the path is the goal, and the goal is now. Give everything away until you find the one thing that cannot be lost. Cross the last bridge and wake up to find the sun rising inside of you.",
            "yoga": "Yoga Nidra in Savasana — Dissolving into the cosmic ocean.",
            "ayurveda": "Psychological Well-being. Use Rose water or Sandalwood."
        }
    }

    # Identify the Nakshatra name based on Sidereal degrees
    name = "Unknown"
    if sign == "Aries":
        if degree < 13.333: name = "Ashwini"
        elif degree < 26.666: name = "Bharani"
        else: name = "Krittika"
    elif sign == "Taurus":
        if degree < 10.0: name = "Krittika"
        elif degree < 23.333: name = "Rohini"
        else: name = "Mrigashira"
    elif sign == "Gemini":
        if degree < 6.666: name = "Mrigashira"
        elif degree < 20.0: name = "Ardra"
        else: name = "Punarvasu"
    elif sign == "Cancer":
        if degree < 3.333: name = "Punarvasu"
        elif degree < 16.666: name = "Pushya"
        else: name = "Ashlesha"
    elif sign == "Leo":
        if degree < 13.333: name = "Magha"
        elif degree < 26.666: name = "Purva Phalguni"
        else: name = "Uttara Phalguni"
    elif sign == "Virgo":
        if degree < 10.0: name = "Uttara Phalguni"
        elif degree < 23.333: name = "Hasta"
        else: name = "Chitra"
    elif sign == "Libra":
        if degree < 6.666: name = "Chitra"
        elif degree < 20.0: name = "Swati"
        else: name = "Vishakha"
    elif sign == "Scorpio":
        if degree < 3.333: name = "Vishakha"
        elif degree < 16.666: name = "Anuradha"
        else: name = "Jyeshtha"
    elif sign == "Sagittarius":
        if degree < 13.333: name = "Moola"
        elif degree < 26.666: name = "Purva Ashada"
        else: name = "Uttara Ashada"
    elif sign == "Capricorn":
        if degree < 10.0: name = "Uttara Ashada"
        elif degree < 23.333: name = "Shravana"
        else: name = "Dhanishta"
    elif sign == "Aquarius":
        if degree < 6.666: name = "Dhanishta"
        elif degree < 20.0: name = "Shatabhisha"
        else: name = "Purva Bhadrapada"
    elif sign == "Pisces":
        if degree < 3.333: name = "Purva Bhadrapada"
        elif degree < 16.666: name = "Uttara Bhadrapada"
        else: name = "Revati"

    # Get the entry
    entry = data.get(name, {"poem": "Medicine ripening.", "yoga": "N/A", "ayurveda": "N/A"})
    
    # Use sign-specific yoga/ayurveda if available
    final_yoga = entry.get("special_yoga", {}).get(sign, entry["yoga"])
    final_ayur = entry.get("special_ayurveda", {}).get(sign, entry["ayurveda"])

    return {"name": name, "poem": entry["poem"], "yoga": final_yoga, "ayurveda": final_ayur}

# --- THE CALCULATOR ---
def get_planet_data(jd_ut, planet_id, planet_name):
    res, ret = swe.calc_ut(jd_ut, planet_id, swe.FLG_SIDEREAL)
    long = res[0]
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign = signs[int(long / 30)]
    degree = long % 30
    n = get_nakshatra_data(sign, degree)
    return {"name": planet_name, "deg": degree, "sign": sign, "nakshatra": n['name'], "poem": n['poem'], "yoga": n['yoga'], "ayurveda": n['ayurveda']}

def calculate_full_map(year, month, day, hour, minute, lat, lon):
    if year > 1800:
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=lon, lat=lat)
        timezone = pytz.timezone(tz_name or "UTC")
        local_dt = timezone.localize(datetime(year, month, day, hour, minute))
        utc_dt = local_dt.astimezone(pytz.utc)
        jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
    else:
        jd_ut = swe.julday(year, month, day, hour + minute/60.0)

    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)

    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    asc_sign = signs[int(asc_raw / 30)]
    asc_deg = asc_raw % 30
    asc_n = get_nakshatra_data(asc_sign, asc_deg)
    
    planets = [(swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"), (swe.VENUS, "Venus"), 
               (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"), (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")]
    birth_planets = [get_planet_data(jd_ut, p_id, p_name) for p_id, p_name in planets]

    return {"asc_deg": asc_deg, "asc_sign": asc_sign, "asc_nakshatra": asc_n['name'], "asc_poem": asc_n['poem'], "asc_yoga": asc_n['yoga'], "asc_ayur": asc_n['ayurveda'], "birth_planets": birth_planets}

# --- THE INTERFACE ---
st.set_page_config(page_title="Soul Map Sanctuary", layout="wide", page_icon="✨")
st.title("✨ The Real-Sky Soul Map: Eternal Edition")

address = st.text_input("Birth Location (City, Country)", "Houston, USA")
client_name = st.text_input("Seeker Name", "Leah G")

geolocator = Nominatim(user_agent="soul_map_holistic")
location = geolocator.geocode(address)

if location:
    col1, col2 = st.columns(2)
    with col1:
        b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24), min_value=datetime(1, 1, 1), max_value=datetime(2100, 12, 31))
    with col2:
        b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())

    if st.button("Generate Soul Map"):
        try:
            data = calculate_full_map(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute, location.latitude, location.longitude)
            
            st.divider()
            st.header(f"✨ Soul Map for {client_name}")
            st.metric("Foundation (Ascendant)", f"{data['asc_deg']:.2f}° {data['asc_sign']}")
            
            st.markdown(f"### The Call of {data['asc_nakshatra']}")
            st.info(data['asc_poem'])
            
            # The Medicine Tab Layout
            tab1, tab2 = st.tabs(["The Planetary Council", "The Holistic Body"])
            
            with tab1:
                cols = st.columns(4)
                for i, p in enumerate(data['birth_planets']):
                    with cols[i % 4]:
                        st.write(f"**{p['name']}**")
                        st.caption(f"{p['deg']:.2f}° {p['sign']} ({p['nakshatra']})")
                        with st.expander("Read the Medicine"):
                            st.write(p['poem'])
            
            with tab2:
                st.subheader("Yoga & Ayurvedic Prescriptions")
                # Showing the Ascendant's holistic medicine first
                st.write(f"**Ascendant ({data['asc_nakshatra']})**")
                st.write(f"🧘 **Yoga:** {data['asc_yoga']}")
                st.write(f"🍃 **Ayurveda:** {data['asc_ayur']}")
                st.divider()
                
                # Showing medicine for each planet
                for p in data['birth_planets']:
                    st.write(f"**{p['name']} in {p['nakshatra']}**")
                    st.write(f"🧘 {p['yoga']}")
                    st.write(f"🍃 {p['ayurveda']}")
                    st.write("")

            st.divider()
            st.caption("Universal Sidereal Calculations | Swiss Ephemeris | Holistic Well-being Guide")

        except Exception as e:
            st.error(f"Calibration needed: {e}")
