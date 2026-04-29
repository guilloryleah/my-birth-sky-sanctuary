import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. NAKSHATRA & SHAKTI DATABASE
NAK_DATA = {
    "Ashwini": "The Power to Reach Quickly (Shidhra Shakti). Healing and rejuvenation.",
    "Bharani": "The Power to Cleanse/Carry Away (Apabharani Shakti). Transformation.",
    "Krittika": "The Power to Burn (Dahana Shakti). Purification and brilliance.",
    "Rohini": "The Power of Growth (Prabhava Shakti). Fertility and creation.",
    "Mrigashira": "The Power of Fulfillment (Prinana Shakti). Seeking and finding.",
    "Ardra": "The Power of Effort (Yatna Shakti). Transformation through storm.",
    "Punarvasu": "The Power of Renewal (Vasutva Shakti). Return of the light.",
    "Pushya": "The Power of Spiritual Energy (Brahmavarchasa Shakti). Nourishment.",
    "Ashlesha": "The Power to Inflict Poison (Vishasleshana Shakti). Paralysis of enemies.",
    "Magha": "The Power of Lineage (Tyage Shepan Shakti). Ancestral pride.",
    "Purva Phalguni": "The Power of Procreation (Prajanana Shakti). Creative union.",
    "Uttara Phalguni": "The Power of Giving (Chayani Shakti). Prosperity through marriage.",
    "Hasta": "The Power to Manifest (Hasta Shakti). Skill and manifestation.",
    "Chitra": "The Power of Merit (Punya Chayani Shakti). Artistic brilliance.",
    "Swati": "The Power to Scatter (Pradhvamsana Shakti). Freedom and movement.",
    "Vishakha": "The Power of Achievement (Vyapana Shakti). Goal-oriented focus.",
    "Anuradha": "The Power of Worship (Radhana Shakti). Devotion and friendship.",
    "Jyeshtha": "The Power to Rise Above (Tarana Shakti). Seniority and courage.",
    "Mula": "The Power to Uproot (Barhana Shakti). Breaking ties and discovery.",
    "Purva Ashadha": "The Power of Invigoration (Varchograhana Shakti). Vitality.",
    "Uttara Ashadha": "The Power of Victory (Apradhrisya Shakti). Unstoppable success.",
    "Shravana": "The Power of Connection (Samhanana Shakti). Listening and learning.",
    "Dhanishta": "The Power of Abundance (Sansiddha Shakti). Fame and wealth.",
    "Shatabhisha": "The Power of Healing (Bheshaja Shakti). Seeing the hidden truth.",
    "Purva Bhadrapada": "The Power of Fire (Yajamana Shakti). Spiritual ascension.",
    "Uttara Bhadrapada": "The Power of Rain (Varshograhana Shakti). Deep stability.",
    "Revati": "The Power of Nourishment (Kshiradyani Shakti). Wealth and protection."
}

NAK_LIST = list(NAK_DATA.keys())
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. ENGINE
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_danny_fix")
        loc = geolocator.geocode(city_name)
        if not loc: return 29.76, -95.36, -6.0
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_hours = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset_hours
    except:
        return 29.76, -95.36, -6.0

def calculate_sky(jd_local, lat, lon, offset):
    jd_utc = jd_local - (offset / 24.0)
    ayan = 24.13 # Lahiri Calibration
    
    # Accurate Sidereal Calculation
    gmst = (280.4606 + 360.985647 * (jd_utc - 2451545.0)) % 360
    lst = (gmst + lon) % 360
    
    # Spherical Trigonometry for Ascendant
    eps, phi, l_rad = math.radians(23.439), math.radians(lat), math.radians(lst)
    num, den = -math.cos(l_rad), (math.sin(l_rad) * math.cos(eps)) + (math.tan(phi) * math.sin(eps))
    
    sid_asc = (math.degrees(math.atan2(num, den)) - ayan) % 360
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

# 4. SIDEBAR
with st.sidebar:
    st.header("Celestial Data Entry")
    name = st.text_input("Seeker Name", value="Danny")
    y = st.number_input("Year", 1900, 2026, 1980)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 20)
    t_in = st.time_input("Birth Time")
    place = st.text_input("Birth City", value="Houston, TX")
    submit = st.button("REVEAL NAKSHATRAS")

# 5. MAIN PAGE
if not submit:
    st.title("✨ The Nakshatra Sanctuary")
    st.markdown("### Dive into the Lunar Mansions and the Power of the Stars.")
    st.write("Enter your birth details to reveal the specific Shakti (power) behind your placement.")
else:
    dt = datetime.combine(date(y, m, d), t_in)
    lat, lon, off = get_location_details(place, dt)
    jd = pd.Timestamp(dt).to_julian_date()
    s_d, m_d, a_d = calculate_sky(jd, lat, lon, off)

    # Labeling
    def get_info(deg):
        z = ZODIAC_LIST[int(deg/30)]
        n = NAK_LIST[int(deg/13.3333)]
        return z, n

    s_z, s_n = get_info(s_d)
    m_z, m_n = get_info(m_d)
    a_z, a_n = get_info(a_d)

    st.header(f"The Star Map for {name}")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🌙 Moon Placement")
        st.info(f"**Sign:** {m_z}\n\n**Nakshatra:** {m_n}")
        st.write(f"*{NAK_DATA.get(m_n)}*")
    
    with col2:
        st.subheader("☀️ Sun Placement")
        st.success(f"**Sign:** {s_z}\n\n**Nakshatra:** {s_n}")
        st.write(f"*{NAK_DATA.get(s_n)}*")

    with col3:
        st.subheader("🌅 Ascendant (Lagna)")
        st.warning(f"**Sign:** {a_z}\n\n**Nakshatra:** {a_n}")
        st.write(f"*{NAK_DATA.get(a_n)}*")
