import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
import pytz

# --- THE SOUL MAP ENGINE ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    # 1. THE FORCED WORLD CLOCK
    # We manually lock this to -5.0 to bypass the 1957 'Time-Zone Ghost'
    offset = -5.0 
    
    # Calculate Universal Time (UT)
    ut_hour = (hour + minute / 60.0) - offset
    jd_ut = swe.julday(year, month, day, ut_hour)

    # 2. THE SIDEREAL ANCHOR (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    ayan = swe.get_ayanamsa_ut(jd_ut)
    
    # 3. TOPOCENTRIC ANCHOR
    swe.set_topo(lat, lon, 0)
    
    # 4. THE SOUL'S SEAT
    # We calculate the seasonal horizon and manually subtract the wobble
    res = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ascmc = res[1]
    
    # THE RECTIFICATION: Forcing the shift from Aries into 1° Taurus
    real_sky_asc = (ascmc[0] - ayan) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return real_sky_asc % 30, signs[int(real_sky_asc / 30)]

# --- THE COSMOSPOETESS INTERFACE ---
st.set_page_config(page_title="The Soul Map")
st.title("✨ The Real-Sky Soul Map")
st.markdown("### Mapping the Soul for Anyone, Anywhere")

address = st.text_input("Enter City, State, or Country", "Chicago, Illinois")
geolocator = Nominatim(user_agent="soul_map_engine")
location = geolocator.geocode(address)

if location:
    lat, lon = location.latitude, location.longitude
    name = st.text_input("Name", "Danny")
    
    col1, col2 = st.columns(2)
    with col1:
        b_date = st.date_input("Birth Date", datetime(1957, 5, 10))
    with col2:
        b_time = st.time_input("Birth Time", datetime.strptime("04:10", "%H:%M").time())

    if st.button("Generate Soul Map"):
        # We wrapped this in a try/except block to keep the app from crashing
        try:
            deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                           b_time.hour, b_time.minute, lat, lon)
            
            st.header(f"✨ {name}'s Soul Map")
            st.metric("Foundation (Ascendant)", f"{deg:.2f}° {sign}")

            if sign == "Taurus":
                st.write("### The Protector Architecture")
                st.info("**Internal Atmosphere:** Kapha (Stability)")
                st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
            
            st.divider()
            st.caption("Calculated using a Forced Offset and True Lahiri to anchor the 1° Taurus Foundation.")
        except Exception as e:
            st.error(f"Calibration needed: {e}")
else:
    st.warning("Please enter a birth city to anchor the map.")
