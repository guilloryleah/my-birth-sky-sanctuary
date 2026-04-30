import streamlit as st
import swisseph as swe
import pytz
from datetime import datetime

# --- 1. THE WISDOM LIBRARY (Zodiac & Nakshatras) ---
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
    # Essential: Points to the folder for NASA/Swiss Ephemeris data
    swe.set_ephe_path('./ephe') 
    
    # LOCKING SIDEREAL MODE (True Lahiri)
    # This is the line that ensures Danny stays at 1° Taurus and avoids 'Aries'
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Time Integrity: Resolving 1957 Chicago historical offsets
    local_tz = pytz.timezone(tzone_str)
    dt = datetime(year, month, day, hour, minute)
    local_dt = local_tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.utc)
    
    # Julian Day for astronomical precision
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute/60.0)

    # Flags for Sidereal/Real-Sky calculation
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    def calc_obj(obj_id):
        res, _ = swe.calc_ut(jd, obj_id, flags)
        deg = res[0]
        return {
            "Sign": ZODIAC_SIGNS[int(deg / 30)],
            "Nakshatra": NAKSHATRAS[int(deg / (360/27))],
            "Position": f"{round(deg % 30, 2)}°"
        }

    # Topocentric Ascendant Calculation
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

# --- 3. THE FRONTEND (Streamlit Sanctuary) ---
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨")
st.title("✨ Birth Sky Sanctuary")
st.markdown("### *A Real-Sky Receipt of Truth*")

with st.form("birth_data"):
    client_name = st.text_input("Client Name", placeholder="Enter full name")
    
    col1, col2 = st.columns(2)
    with col1:
        # Default birth date
        date = st.date_input("Birth Date", value=datetime(1957, 5, 10))
    with col2:
        # Default birth time
        time = st.time_input("Birth Time", value=datetime(1957, 5, 10, 12, 0).time())
    
    # Timezone selection
    tz = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("America/Chicago"))

    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("Latitude", value=41.8722, format="%.4f")
    with col4:
        lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
    
    submitted = st.form_submit_button("Generate Truth Receipt")

# --- 4. THE OUTPUT ---
if submitted:
    if not client_name:
        st.warning("Please enter a name for the report.")
    else:
        try:
            report = get_real_sky_report(date.year, date.month, date.day, time.hour, time.minute, lat, lon, tz)
            
            st.divider()
            st.header(f"Real-Sky Soul Map: {client_name}")
            
            asc = report["Ascendant"]
            st.subheader(f"The Gateway (Ascendant): {asc['Position']} {asc['Sign']}")
            st.write(f"**Nakshatra:** {asc['Nakshatra']}")
            
            # Professional 3-column layout
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Sun", f"{report['Sun']['Position']} {report['Sun']['Sign']}")
                st.caption(f"Nakshatra: {report['Sun']['Nakshatra']}")
            with c2:
                st.metric("Moon", f"{report['Moon']['Position']} {report['Moon']['Sign']}")
                st.caption(f"Nakshatra: {report['Moon']['Nakshatra']}")
            with c3:
                st.metric("Mercury", f"{report['Mercury']['Position']} {report['Mercury']['Sign']}")
                st.caption(f"Nakshatra: {report['Mercury']['Nakshatra']}")
                
            st.divider()
            st.write(f"**Rahu (The North Node):** {report['Rahu']['Position']} {report['Rahu']['Sign']} in {report['Rahu']['Nakshatra']}")
            
            st.info("System: Sidereal / True Lahiri (Astronomical Real-Sky)")
            
        except Exception as e:
            st.error(f"Engine Error: {e}")
