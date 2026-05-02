

import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE POETIC NAKSHATRA ENGINE ---
def get_nakshatra_data(sign, degree):
    """Returns the Nakshatra name and poem based on exact degree ranges."""
    poems = {
        "Ashwini": "Heal the ghost of the old self before you try to outrun it. The horse gallops not to flee the past, but to collide with the future. Listen for the medicine that hums in the silence of the dawn. Stop searching for a cure and realize you are the physician of your own wreckage.",
        "Bharani": "Carry the weight of your becoming until it turns into a wing. The dark soil is not a grave for your spirit, but a womb for your power. Hold the tension of the middle path with a grit that tastes like grace. Give birth to the version of you that no longer asks for permission to exist.",
        "Krittika": "Burn away the brush until only the gold has room to breathe. The blade that cuts you open is the same one that sets you free. Seek the heat that transforms your form rather than the fire that feeds your ego. Let your truth be a cauterizing flame that heals the cold world by touch.",
        "Rohini": "Plant your feet where the earth is soft and red with ancient memory. Ascend the heights by sinking deeper into the marrow of your being. Tend to the garden of the heart with hands that have forgotten how to hurry. Beauty is not an ornament; it is the vital oxygen that mends a fractured soul.",
        "Mrigashira": "Stop chasing the horizon and start watching the rhythm of your shadow. The nectar you seek is hidden in the quiet stride of the searcher. Softness is the only armor that the world is unable to pierce or break. Find the sanctuary that exists between the inhale and the exhale.",
        "Ardra": "Let the storm wash the salt from your eyes until you see without filters. The thunder is the sound of the ego’s architecture finally crumbling. Stand naked in the rain until you are nothing but the core of the lightning. Renewal begins only when you stop trying to keep your old life dry.",
        "Punarvasu": "Return to the center after every long wandering through the wild. The arrow finds the mark only when the hand has ceased its trembling. Trust the cycles of the light as deeply as you trust the dark of the moon. You are the destination you have been traveling a thousand lives to find.",
        "Pushya": "Feed the spirit until it is heavy enough to anchor the drifting mind. Flow like the milk of a star through the veins of the heavy night. Stability is found in the absolute surrender to the service of the sacred. Be the hollow bone; let a higher wisdom play its song through your life.",
        "Ashlesha": "Embrace the serpent that guards the gates of your inner temple. The sting is the wake-up call for the god who fell asleep in your skin. Look into the dark until the dark begins to reflect your own inner light. Shed the skin of who you were so the truth can breathe through your pores.",
        "Magha": "Honor the blood that flows through your veins, for it is an ocean of ancestors. The throne is a cage unless the heart is humble enough to serve the lowest. Walk with the kings of the past but dream a dream they were too afraid to see. Noble action is the only currency that buys a seat in the hall of the eternal.",
        "Purva Phalguni": "Dance until the dancer and the dance are swallowed by the movement. The creative spark is the only bridge that spans the gap to the divine. Rest is a sacred prayer; do not apologize for the stillness that restores you. Pour your love into the world like a wine that never runs dry.",
        "Uttara Phalguni": "Extend your hand to the one who walks in the shadow behind you. The healer’s touch is not a technique, but a state of absolute presence. Steady the mind like a flame in a room where the wind has finally died. The path to the stars is paved with the small, quiet stones of kindness.",
        "Hasta": "Create what has never been seen with the magic of your open palms. The power is in the focus of the eye, not in the movement of the hand. Grasp the truth with everything you have, then let the outcome go. Your work is the physical signature of the peace you have found within.",
        "Chitra": "Carve the diamond of the soul out of the rough and heavy stone of habit. The external glow is merely a shadow of the fire burning in your chest. Build a temple out of the ruins of your yesterday and live in its heart. The masterpiece is not what you make, but the life you choose to inhabit.",
        "Swati": "Sway with the wind but never lose the root that holds you to the earth. Freedom is the ability to find your breath in the center of the hurricane. Scatter your seeds without worry; the earth knows exactly where they belong. The spirit travels furthest when it stops carrying the weight of its names.",
        "Vishakha": "Aim for the highest peak but cherish the blood on the jagged path. Patience is the slow fire that tempers the iron of the human soul. Break the old idols of your mind to find the living truth they were hiding. The victory is won the moment you stop fighting yourself for the prize.",
        "Anuradha": "Weave the threads of your devotion into a cloak that can weather any winter. Friendship is the bridge that keeps the soul from drowning in the lonely sea. Look for the blossom that thrives in the mud; that is where the secret lies. Belonging is not a frequency you find, but a frequency you finally learn to tune.",
        "Jyeshtha": "Protect the spark that flickers in the deepest, coldest cave of your being. Wisdom is a shield that only grows thick through the passage of time. Listen to the heavy silence that sits beneath the noise of the world. The elder within you is waiting for you to stop talking and start seeing.",
        "Moola": "Dig past the layers of bone until you strike the primary root of existence. The collapse of your world is the invitation for the truth to be born. Destroy everything that is false so that what is eternal can finally stand. Foundations are only discovered when you have reached the absolute bottom.",
        "Purva Ashada": "Dive into the depths where the light of the sun is a forgotten memory. Surrender to the current and let the great tides decide your direction. The ocean is not an obstacle; it is the vast embrace of the mother. In the middle of the deep water, discover that you are the shore.",
        "Uttara Ashada": "Stand like a mountain of light against the howling wind of the world’s opinion. The sun of the spirit never sets on a heart that has nothing to hide. Commitment is the anchor that holds when the sky turns black with rain. Integrity is the only peak that offers a view of the entire universe.",
        "Shravana": "Listen to the pulse of the stars as it beats inside your own ears. Learning is the art of becoming a mirror that reflects the light of the sun. Walk the earth as if every step were a word in a holy and secret book. Knowledge is a weight you carry; wisdom is the light that carries you.",
        "Dhanishta": "Find the rhythm that beats beneath the skin of the physical world. Abundance flows only to the hand that is open enough to let it go. Let your every movement be a ritual for the gods who live in the silence. The drum of the heart is the only map you need to navigate the divine.",
        "Shatabhisha": "Hide within the hundred veils until you find the eye that never blinks. The mystery is not a problem to be solved, but a reality to be entered. Heal the wounds of the world by mending the fractures in your own soul. The void is not empty; it is the womb of everything that is yet to be.",
        "Purva Bhadrapada": "Face the fire of your own shadow and do not turn your eyes away. Transformation requires the absolute death of the mask you wear for others. Carry the torch of your truth through the longest tunnel of the dark. The warrior’s greatest battle is won the moment the sword is laid down.",
        "Uttara Bhadrapada": "Sleep in the deep, still waters and dream the world back into balance. Peace is the treasure guarded by the mind that has stopped seeking. The end of the journey is the discovery that you never truly left home. Dissolve into the blue of the infinite and realize you are the sky.",
        "Revati": "Walk the final shore and leave no footprints for the world to follow. The traveler is the path, and the path is the goal, and the goal is now. Give everything away until you find the one thing that cannot be lost. Cross the last bridge and wake up to find the sun rising inside of you."
    }

    name = "Unknown"
    # Sidereal degree range logic
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
    
    return {"name": name, "poem": poems.get(name, "Medicine is ripening.")}

# --- CALCULATION ENGINE ---
def get_planet_data(jd_ut, planet_id, planet_name):
    res, ret = swe.calc_ut(jd_ut, planet_id, swe.FLG_SIDEREAL)
    long = res[0]
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign = signs[int(long / 30)]
    degree = long % 30
    nak_data = get_nakshatra_data(sign, degree)
    return {"name": planet_name, "deg": degree, "sign": sign, "nakshatra": nak_data['name'], "poem": nak_data['poem']}

def calculate_full_map(year, month, day, hour, minute, lat, lon):
    # Automatic Timezone Detection
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name)
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # True Lahiri Real-Sky Settings
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)

    # Ascendant Calculation
    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    asc_sign = signs[int(asc_raw / 30)]
    asc_deg = asc_raw % 30
    asc_nak_data = get_nakshatra_data(asc_sign, asc_deg)
    
    # Council Members (Planets)
    planets = [(swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"), (swe.VENUS, "Venus"), 
               (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"), (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")]
    birth_planets = [get_planet_data(jd_ut, p_id, p_name) for p_id, p_name in planets]

    return {
        "asc_deg": asc_deg,
        "asc_sign": asc_sign,
        "asc_nakshatra": asc_nak_data['name'],
        "asc_poem": asc_nak_data['poem'],
        "birth_planets": birth_planets
    }

# --- GLOBAL INTERFACE ---
st.set_page_config(page_title="Soul Map Sanctuary", layout="wide", page_icon="✨")
st.title("✨ The Real-Sky Soul Map: Global Edition")

# Updated label to welcome international clients
address = st.text_input("Birth Location (City, State/Province, Country)", "Houston, Texas, USA")
client_name = st.text_input("Client/Seeker Name", "Leah G")

geolocator = Nominatim(user_agent="soul_map_global_engine")
location = geolocator.geocode(address)

if location:
    col1, col2 = st.columns(2)
    with col1:
        # Timeless range for grandchildren and ancestors
        b_date = st.date_input(
            "Birth Date", 
            value=datetime(1969, 9, 24),
            min_value=datetime(1900, 1, 1),
            max_value=datetime(2100, 12, 31)
        )
    with col2:
        b_time = st.time_input("Birth Time", value=datetime.strptime("22:59", "%H:%M").time())

    if st.button("Generate Soul Map"):
        try:
            data = calculate_full_map(b_date.year, b_date.month, b_date.day, b_time.hour, b_time.minute, location.latitude, location.longitude)
            
            st.divider()
            st.header(f"✨ Soul Map for {client_name}")
            st.metric("Ascendant (The Horizon)", f"{data['asc_deg']:.2f}° {data['asc_sign']}")
            
            st.markdown(f"### The Call of {data['asc_nakshatra']}")
            st.info(data['asc_poem'])
            
            st.subheader("The Planetary Council")
            cols = st.columns(4)
            for i, p in enumerate(data['birth_planets']):
                with cols[i % 4]:
                    st.write(f"**{p['name']}**")
                    st.write(f"{p['deg']:.2f}° {p['sign']}")
                    st.caption(f"*{p['nakshatra']}*")
                    with st.expander("Listen to the Medicine"):
                        st.write(p['poem'])
            
            # Auto-calculate Ketu (opposite Rahu)
            rahu = data['birth_planets'][-1]
            signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            ketu_sign_idx = (signs.index(rahu['sign']) + 6) % 12
            ketu_sign = signs[ketu_sign_idx]
            ketu_nak = get_nakshatra_data(ketu_sign, rahu['deg'])
            
            with cols[0]: 
                st.write(f"**Ketu**")
                st.write(f"{rahu['deg']:.2f}° {ketu_sign}")
                st.caption(f"*{ketu_nak['name']}*")
                with st.expander("Listen to the Medicine"):
                    st.write(ketu_nak['poem'])

            st.divider()
            st.caption("Sidereal Lahiri Calculations | Automatic Timezone & Global Geocoding Enabled.")

        except Exception as e:
            st.error(f"Engine calibration needed: {e}")
else:
    st.warning("Please provide a birth location to anchor the sky.")


