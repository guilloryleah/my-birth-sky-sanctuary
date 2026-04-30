import streamlit as st
import swisseph as swe
import pytz
from datetime import datetime

# --- 1. THE WISDOM LIBRARY ---
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
def get_real_sky_report(year, month, day, hour, minute, lat, lon, tzone_str):
    swe.set_ephe_path('./ephe') 

    local_tz = pytz.timezone(tzone_str)
    dt = datetime(year, month, day, hour, minute)
    local_dt = local_tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute/60.0)

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    def calc_obj(obj_id):
        res, _ = swe.calc_ut(jd, obj_id, flags)
        deg = res[0]
        return {
            "Sign": ZODIAC_SIGNS[int(deg / 30)],
            "Nakshatra": NAKSHATRAS[int(deg / (360/27))],
            "Position": f"{round(deg % 30, 2)}°"
        }

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
        "Rahu": calc_obj(swe.MEAN_NODE)
    }

# --- 3. THE STREAMLIT FRONTEND ---
st.title("My Birth Sky Sanctuary")
st.write("The Universal Clock is ready for your input.")

with st.form("birth_data"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Birth Date", value=datetime(1957, 5, 10))
    with col2:
        time = st.time_input("Birth Time", value=datetime(1957, 5, 10, 12, 0).time())
    with col3:
        tz = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("America/Chicago"))

    lat = st.number_input("Latitude", value=41.87)
    lon = st.number_input("Longitude", value=-87.62)
    
    submitted = st.form_submit_button("Generate Truth Receipt")

if submitted:
    try:
        report = get_real_sky_report(date.year, date.month, date.day, time.hour, time.minute, lat, lon, tz)
        st.success("Analysis Complete")
        st.json(report)
    except Exception as e:
        st.error(f"Engine Error: {e}")
