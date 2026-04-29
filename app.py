import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="The Nakshatra Sanctuary", page_icon="✨", layout="wide")

# 2. NAKSHATRA SHAKTI DATABASE
NAK_DATA = {
    "Ashwini": "The Power to Reach Quickly (Shidhra Shakti). Miracle healing and swift action.",
    "Bharani": "The Power to Carry Away (Apabharani Shakti). Transformation through endurance.",
    "Krittika": "The Power to Burn (Dahana Shakti). Sharp intelligence and purification.",
    "Rohini": "The Power of Growth (Prabhava Shakti). Nurturing beauty and manifestation.",
    "Mrigashira": "The Power of Fulfillment (Prinana Shakti). The restless search for truth.",
    "Ardra": "The Power of Effort (Yatna Shakti). Clarity gained through the storm.",
    "Punarvasu": "The Power of Renewal (Vasutva Shakti). The return of light and resources.",
    "Pushya": "The Power of Spiritual Energy (Brahmavarchasa Shakti). Deep nourishment.",
    "Ashlesha": "The Power to Inflict Poison (Vishasleshana Shakti). Insight into the shadow.",
    "Magha": "The Power of Lineage (Tyage Shepan Shakti). Connection to ancestral nobility.",
    "Purva Phalguni": "The Power of Procreation (Prajanana Shakti). Creative charm and union.",
    "Uttara Phalguni": "The Power of Giving (Chayani Shakti). Prosperity through alliances.",
    "Hasta": "The Power to Manifest (Hasta Shakti). Putting the world in your hands.",
    "Chitra": "The Power of Merit (Punya Chayani Shakti). Creating form out of chaos.",
    "Swati": "The Power to Scatter like the Wind (Pradhvamsana Shakti). Complete freedom.",
    "Vishakha": "The Power of Achievement (Vyapana Shakti). Focused, multi-branched success.",
    "Anuradha": "The Power of Worship (Radhana Shakti). Success through balance and devotion.",
    "Jyeshtha": "The Power to Rise Above (Tarana Shakti). Courage and mental seniority.",
    "Mula": "The Power to Uproot (Barhana Shakti). Destroying illusions at the root.",
    "Purva Ashadha": "The Power of Invigoration (Varchograhana Shakti). Strength and purification.",
    "Uttara Ashadha": "The Power of Victory (Apradhrisya Shakti). Unstoppable, permanent success.",
    "Shravana": "The Power of Connection (Samhanana Shakti). Listening to the cosmic rhythm.",
    "Dhanishta": "The Power of Abundance (Sansiddha Shakti). Fame, music, and wealth.",
    "Shatabhisha": "The Power of Healing (Bheshaja Shakti). Seeing the 100 physicians within.",
    "Purva Bhadrapada": "The Power of Fire (Yajamana Shakti). Spiritual evolution and heat.",
    "Uttara Bhadrapada": "The Power of Rain (Varshograhana Shakti). Stability and deep peace.",
    "Revati": "The Power of Nourishment (Kshiradyani Shakti). Safety on the final journey."
}

NAK_LIST = list(NAK_DATA.keys())
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. THE PRECISION ENGINE
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_v5")
        loc = geolocator.geocode(city_name)
        if not loc: return 29.76, -95.36, -6.0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_hours = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset_hours
    except: return 29.76, -95.36, -6.0

def calculate_sidereal_positions(jd_local, lat, lon, offset):
    jd_utc = jd_local - (offset / 24.0)
    ayan = 24.13 # Lahiri Calibration
    
    # Astronomical Constants
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.4606 + 360.985647 * (jd_utc - 2451545.0)) % 360
    lst_deg = (gmst + lon) % 360
    
    # Lagna (Ascendant) Calculation
    eps, phi, l_rad = math.radians(23.439), math.radians(lat), math.radians(lst_deg)
    num, den = -math.cos(l_rad), (math.sin(l_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    
    sid_asc = (math.degrees(math.atan2(num, den)) - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

# 4. SIDEBAR
with st.sidebar:
    st.header("Celestial Data")
    name = st.text_input("Name", value="Danny")
    y = st.number_input("Year", 1900, 2026, 1980)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 20)
    t_in = st.time_input("Birth Time")
    place = st.text_input("Birth City", value="Houston, TX")
    submit = st.button("REVEAL THE STARS")

# 5. MAIN PAGE
if not submit:
    st.title("✨ The Nakshatra Sanctuary")
    st.markdown("### Enter your data to reveal the Lunar Mansions and the power of your birth sky.")
else:
    dt = datetime.combine(date(y, m, d), t_in)
    lat, lon, off = get_location_details(place, dt)
    jd = pd.Timestamp(dt).to_julian_date()
    s_d, m_d, a_d = calculate_sidereal_positions(jd, lat, lon, off)

    def get_labels(deg):
        z = ZODIAC_LIST[int(deg/30)]
        n = NAK_LIST[int(deg/13.3333)]
        return z, n

    sz, sn = get_labels(s_d)
    mz, mn = get_labels(m_d)
    az, an = get_labels(a_d)

    st.header(f"The Star Map for {name}")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🌙 Moon")
        st.info(f"**{mz}**\n\n{mn}")
        st.caption(NAK_DATA.get(mn))
    with col2:
        st.subheader("☀️ Sun")
        st.success(f"**{sz}**\n\n{sn}")
        st.caption(NAK_DATA.get(sn))
    with col3:
        st.subheader("🌅 Ascendant")
        st.warning(f"**{az}**\n\n{an}")
        st.caption(NAK_DATA.get(an))

    st.markdown("---")
    st.subheader("Detailed Nakshatra Insights")
    st.write(f"**Sun in {sn}:** {NAK_DATA.get(sn)}")
    st.write(f"**Ascendant in {an}:** {NAK_DATA.get(an)}")
