import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE SOUL MAP ENGINE ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    # 1. THE INVISIBLE WORLD CLOCK
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name)
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # 2. LOCKING THE FOUNDATION (True Lahiri / Sidereal)
    # This is the "Aries Drift" Cure. It accounts for the 24-degree shift.
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    
    # We use the Sidereal Flag (FLG_SIDEREAL) to ensure we see the REAL stars
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    
    # Calculate the Ascendant (The Soul's Seat)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_raw = ascmc[0]
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return asc_raw % 30, signs[int(asc_raw / 30)]

# --- THE COSMOSPOETESS INTERFACE ---
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
        b_time = st.time_input("Birth Time", datetime.strptime("04:15", "%H:%M").time())

    if st.button("Generate Soul Map"):
        deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                       b_time.hour, b_time.minute, lat, lon)
        
        st.header(f"✨ {name}'s Soul Map")
        # This metric will now show the Taurus Foundation
        st.metric("Foundation", f"{deg:.2f}° {sign}")

        if sign == "Taurus":
            st.info("**Internal Atmosphere:** Kapha (Stability)")
            st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
        
        st.divider()
        st.caption("Calculated using True Lahiri Sidereal math to reflect the actual stars at birth.")
else:
    st.warning("Please enter a birth city to begin.")
