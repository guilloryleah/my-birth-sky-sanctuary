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
    
    # Calculate Rahu and Ketu specifically for the axis
    rahu_res, _ = swe.calc_ut(jd, swe.MEAN_NODE, flags)
    rahu_deg = rahu_res[0]
    ketu_deg = (rahu_deg + 180) % 360
    
    return {
        "Ascendant": {
            "Sign": ZODIAC_SIGNS[int(asc_deg/30)],
            "Nakshatra": NAKSHATRAS[int(asc_deg/(360/27))],
            "Position": f"{round(asc_deg % 30, 2)}°"
        },
        "Sun": calc_obj(swe.SUN),
        "Moon": calc_obj(swe.MOON),
        "Mercury": calc_obj(swe.MERCURY),
        "Rahu": {
            "Sign": ZODIAC_SIGNS[int(rahu_deg/30)],
            "Nakshatra": NAKSHATRAS[int(rahu_deg/(360/27))],
            "Position": f"{round(rahu_deg % 30, 2)}°"
        },
        "Ketu": {
            "Sign": ZODIAC_SIGNS[int(ketu_deg/30)],
            "Nakshatra": NAKSHATRAS[int(ketu_deg/(360/27))],
            "Position": f"{round(ketu_deg % 30, 2)}°"
        }
    }

# --- 3. THE FRONTEND ---
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨")
st.title("✨ Birth Sky Sanctuary")
st.markdown("### *A Real-Sky Receipt of Truth*")

with st.form("birth_data"):
    client_name = st.text_input("Client Name", placeholder="Enter full name")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Birth Date", value=datetime(1957, 5, 10))
    with col2:
        time = st.time_input("Birth Time", value=datetime(1957, 5, 10, 12, 0).time())
    
    tz = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index("America/Chicago"))

    col3, col4 = st.columns(2)
    with col3:
        lat = st.number_input("Latitude", value=41.87, format="%.4f")
    with col4:
        lon = st.number_input("Longitude", value=-87.62, format="%.4f")
    
    submitted = st.form_submit_button("Generate Truth Receipt")

if submitted:
    if not client_name:
        st.error("Please enter a name for the report.")
    else:
        try:
            report = get_real_sky_report(date.year, date.month, date.day, time.hour, time.minute, lat, lon, tz)
            
            st.divider()
            st.header(f"Real-Sky Soul Map: {client_name}")
            
            # Displaying the 'Front Door' (Ascendant)
            asc = report["Ascendant"]
            st.subheader(f"The Gateway (Ascendant): {asc['Position']} {asc['Sign']}")
            st.write(f"**Nakshatra:** {asc['Nakshatra']}")
            
            # Creating columns for a clean visual layout
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Sun", f"{report['Sun']['Sign']}")
                st.caption(f"Nakshatra: {report['Sun']['Nakshatra']}")
            with c2:
                st.metric("Moon", f"{report['Moon']['Sign']}")
                st.caption(f"Nakshatra: {report['Moon']['Nakshatra']}")
            with c3:
                st.metric("Mercury", f"{report['Mercury']['Sign']}")
                st.caption(f"Nakshatra: {report['Mercury']['Nakshatra']}")
                
            st.divider()
            st.subheader("The Evolutionary Axis")
            st.write(f"**Rahu (The Challenge):** {report['Rahu']['Position']} {report['Rahu']['Sign']} in {report['Rahu']['Nakshatra']}")
            st.write(f"**Ketu (The Mastery):** {report['Ketu']['Position']} {report['Ketu']['Sign']} in {report['Ketu']['Nakshatra']}")
            
            st.info("Calculation: Sidereal / True Lahiri System")
            
        except Exception as e:
            st.error(f"Engine Error: {e}")
