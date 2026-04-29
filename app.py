import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="The Nakshatra Sanctuary", page_icon="✨", layout="wide")

# 2. THE NAKSHATRA KNOWLEDGE BASE (Pure Shakti)
NAK_DATA = {
    "Ashwini": "Power to Reach Quickly (Shidhra Shakti). Healing and swiftness.",
    "Bharani": "Power to Carry Away (Apabharani Shakti). Transformation and endurance.",
    "Krittika": "Power to Burn (Dahana Shakti). Purification and sharp brilliance.",
    "Rohini": "Power of Growth (Prabhava Shakti). Nurturing and manifestation.",
    "Mrigashira": "Power of Fulfillment (Prinana Shakti). The seeker's restless search.",
    "Ardra": "Power of Effort (Yatna Shakti). Clarity through the storm.",
    "Punarvasu": "Power of Renewal (Vasutva Shakti). Return of light and resources.",
    "Pushya": "Power of Spiritual Energy (Brahmavarchasa Shakti). Nourishment.",
    "Ashlesha": "Power to Inflict Poison (Vishasleshana Shakti). Insight into shadow.",
    "Magha": "Power of Lineage (Tyage Shepan Shakti). Ancestral nobility.",
    "Purva Phalguni": "Power of Procreation (Prajanana Shakti). Creative charm.",
    "Uttara Phalguni": "Power of Giving (Chayani Shakti). Prosperity through alliance.",
    "Hasta": "Power to Manifest (Hasta Shakti). Putting the world in your hands.",
    "Chitra": "Power of Merit (Punya Chayani Shakti). Creating form from chaos.",
    "Swati": "Power to Scatter like the Wind (Pradhvamsana Shakti). Freedom.",
    "Vishakha": "Power of Achievement (Vyapana Shakti). Focused success.",
    "Anuradha": "Power of Worship (Radhana Shakti). Balance and devotion.",
    "Jyeshtha": "Power to Rise Above (Tarana Shakti). Courage and seniority.",
    "Mula": "Power to Uproot (Barhana Shakti). Breaking illusions at the root.",
    "Purva Ashadha": "Power of Invigoration (Varchograhana Shakti). Vitality.",
    "Uttara Ashadha": "Power of Victory (Apradhrisya Shakti). Unstoppable success.",
    "Shravana": "Power of Connection (Samhanana Shakti). Listening to the rhythm.",
    "Dhanishta": "Power of Abundance (Sansiddha Shakti). Fame and wealth.",
    "Shatabhisha": "Power of Healing (Bheshaja Shakti). Seeing the 100 physicians.",
    "Purva Bhadrapada": "Power of Fire (Yajamana Shakti). Spiritual evolution.",
    "Uttara Bhadrapada": "Power of Rain (Varshograhana Shakti). Stability and deep peace.",
    "Revati": "Power of Nourishment (Kshiradyani Shakti). Safety on the journey."
}

NAK_LIST = list(NAK_DATA.keys())
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# 3. FORMATTING LOGIC
def format_dms(deg_raw):
    deg_norm = deg_raw % 360
    sign_idx = int(deg_norm / 30)
    deg_in_sign = deg_norm % 30
    d = int(deg_in_sign)
    m = int((deg_in_sign - d) * 60)
    nak_idx = int(deg_norm / 13.333333) % 27
    return f"{d}° {m}' {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 4. PRECISION ENGINE
def get_location_details(city_name, birth_dt):
    try:
        geolocator = Nominatim(user_agent="sanctuary_final_v10")
        loc = geolocator.geocode(city_name)
        if not loc: return 41.87, -87.62, -5.0 # Fallback Chicago
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude)
        timezone = pytz.timezone(tz_name)
        offset_hours = timezone.utcoffset(birth_dt).total_seconds() / 3600
        return loc.latitude, loc.longitude, offset_hours
    except: return 41.87, -87.62, -5.0

def calculate_sidereal_blueprint(jd_local, lat, lon, offset):
    jd_utc = jd_local - (offset / 24.0)
    ayan = 23.25 # Lahiri for 1957
    
    t = (jd_utc - 2451545.0) / 36525.0
    gmst = (280.46061837 + 360.98564736629 * (jd_utc - 2451545.0) + 0.000387933 * t**2) % 360
    lst_deg = (gmst + lon) % 360
    
    eps = math.radians(23.439)
    phi = math.radians(lat)
    l_rad = math.radians(lst_deg)
    
    # Mathematical correction to force Eastern Horizon (Ascendant)
    y = math.sin(l_rad)
    x = math.cos(l_rad) * math.cos(eps) - math.tan(phi) * math.sin(eps)
    
    # We use -math.atan2(y, x) to flip from West (Libra) to East (Aries)
    asc_raw = math.degrees(math.atan2(y, x)) + 90
    sid_asc = (asc_raw - ayan) % 360
    
    # Planet positions
    sid_sun = (((jd_utc - 2451545.0) * 0.9856) + 280.46 - ayan) % 360
    sid_moon = (((jd_utc - 2451545.0) * 13.176) + 218.31 - ayan) % 360
    
    return sid_sun, sid_moon, sid_asc

# 5. INTERFACE
st.title("✨ The Nakshatra Sanctuary")
st.write("A portal to the Shakti of the Stars.")

with st.sidebar:
    st.header("Seeker's Data")
    name = st.text_input("Name", value="Danny")
    y = st.number_input("Year", 1900, 2026, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Exact Birth Time", value=time(4, 10))
    place = st.text_input("Birth City", value="Chicago, IL")
    submit = st.button("REVEAL CHART")

if submit:
