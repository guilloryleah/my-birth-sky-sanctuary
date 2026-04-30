import streamlit as st
import swisseph as swe
import pytz
from datetime import datetime

# --- 1. THE DATA DICTIONARIES ---
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# --- 2. THE CALCULATION ENGINE ---
def get_birth_sky(year, month, day, hour, minute, lat, lon, tzone_str):
    # Points to NASA/Swiss Ephemeris data files
    swe.set_ephe_path('./ephe') 
    
    # LOCKING SIDEREAL MODE (True Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Historical Time Integrity
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
        return {
            "Sign": ZODIAC_SIGNS[int(deg / 30)],
            "Nakshatra": NAKSHATRAS[int(deg / (360/27))],
            "Position": f"{round(deg % 30, 2)}°"
        }

    # Topocentric Ascendant (The Front Door)
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    
    return {
        "Ascendant": {
            "Sign": ZODIAC_SIGNS[int(asc_deg/30)],
            "Nakshatra": NAKSHATRAS[int(asc_deg/(360/27))],
            "Position": f"{round(asc_deg % 30, 2)}°"
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

# --- 3. THE INTERFACE ---
st.set_page_config(page_title="My Birth Sky Sanctuary")
st.title("My Birth Sky Sanctuary")

with st.form("sky_data"):
    client_name = st.text_input("Name")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Birth Date", value=datetime(1957, 5, 10))
    with col2:
        time = st.time_input("Birth Time", value=datetime(1957, 5, 10, 12, 0).time())
    
    tz = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("America/Chicago"))

    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("Latitude", value=41.8722, format="%.4f")
    with col4:
        lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
    
    submitted = st.form_submit_button("Calculate Sky")

# --- 4. THE OUTPUT ---
if submitted:
    try:
        sky = get_birth_sky(date.year, date.month, date.day, time.hour, time.minute, lat, lon, tz)
        
        st.header(f"Birth Sky for {client_name}")
        
        # Ascendant Focus
        asc = sky["Ascendant"]
        st.subheader(f"Ascendant: {asc['Position']} {asc['Sign']} in {asc['Nakshatra']}")
        
        st.divider()
        
        # All Planet/Nakshatra Combos
        for planet, data in sky.items():
            if planet != "Ascendant":
                st.write(f"**{planet}:** {data['Position']} {data['Sign']} — {data['Nakshatra']}")
                
    except Exception as e:
        st.error(f"Error: {e}")
