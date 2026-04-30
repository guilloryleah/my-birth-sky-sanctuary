import streamlit as st
import swisseph as swe
from datetime import datetime, timedelta

# --- THE SOUL MAP ENGINE ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon, utc_offset):
    # Anchor to the World Clock (UT Sync)
    local_dt = datetime(year, month, day, hour, minute)
    utc_dt = local_dt - timedelta(hours=utc_offset)
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # Real-Sky Sidereal Mode (True Lahiri) to prevent Aries Drift
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Calculate the Ascendant (The Soul's Seat)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_raw = ascmc[0]
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return asc_raw % 30, signs[int(asc_raw / 30)]

# --- THE COSMOSPOETESS INTERFACE ---
st.set_page_config(page_title="Soul Map Engine")
st.title("✨ The Real-Sky Soul Map")
st.markdown("### Mapping the Soul for Anyone at Any Age")

# Defaults are set to the 1957 Chicago foundation
name = st.text_input("Name", "Danny")
b_date = st.date_input("Birth Date", datetime(1957, 5, 10))
b_time = st.time_input("Birth Time", datetime.strptime("12:00", "%H:%M").time())
lat = st.number_input("Latitude", value=41.8781, format="%.4f")
lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
utc_off = st.number_input("World Clock Offset (UTC)", value=-5.0)

if st.button("Generate Soul Map"):
    try:
        deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                       b_time.hour, b_time.minute, lat, lon, utc_off)
        
        st.success(f"Soul Map for {name} is Ready.")
        st.metric("Ascendant (Foundation)", f"{deg:.2f}° {sign}")

        # Integrating the Wisdom Library
        if sign == "Taurus":
            st.info("**Internal Atmosphere:** Kapha (Stability)")
            st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
        
        st.divider()
        st.caption("This map accounts for the Earth's wobble to reflect the True Sky stars at the moment of birth.")
    except Exception as e:
        st.error(f"The engine encountered an issue: {e}")
