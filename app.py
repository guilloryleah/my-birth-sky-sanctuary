import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE SOUL MAP ENGINE ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    # 1. THE INVISIBLE WORLD CLOCK (Automatic UTC Sync)
    # This automatically finds the -5.0 offset for Chicago 1957
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name)
    
    # Anchor the local time to the World Clock
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    # Convert to Julian Day for the star engine
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # 2. REAL-SKY CONSTANT (True Lahiri)
    # This accounts for the Earth's 24-degree wobble
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    
    # 3. TOPOCENTRIC CALIBRATION
    # Standing on the ground to see the real horizon
    swe.set_topo(lat, lon, 0)
    
    # 4. CALCULATING THE SOUL'S SEAT
    # We use the Sidereal flag (FLG_SIDEREAL) to bypass the seasonal calendar
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    
    asc_raw = ascmc[0]
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return asc_raw % 30, signs[int(asc_raw / 30)]

# --- THE COSMOSPOETESS INTERFACE ---
st.title("✨ The Real-Sky Soul Map")
st.markdown("### Mapping the Soul for Anyone, Anywhere")

# Location Search
address = st.text_input("Enter City, State, or Country", "Chicago, Illinois")
geolocator = Nominatim(user_agent="soul_map_engine")
location = geolocator.geocode(address)

if location:
    lat, lon = location.latitude, location.longitude
    
    # Birth Details
    name = st.text_input("Name", "Danny")
    col1, col2 = st.columns(2)
    with col1:
        b_date = st.date_input("Birth Date", datetime(1957, 5, 10))
    with col2:
        # Danny's Birth Time
        b_time = st.time_input("Birth Time", datetime.strptime("04:10", "%H:%M").time())

    if st.button("Generate Soul Map"):
        deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                       b_time.hour, b_time.minute, lat, lon)
        
        st.header(f"✨ {name}'s Soul Map")
        
        # This metric is now anchored to the Taurus Foundation
        st.metric("Foundation (Ascendant)", f"{deg:.2f}° {sign}")

        # The Wisdom Library Integration
        if sign == "Taurus":
            st.write("### The Protector Architecture")
            st.info("**Internal Atmosphere:** Kapha (Stability)")
            st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
        
        st.divider()
        st.caption("Calculated using True Lahiri Sidereal math to honor your Real-Sky homecoming.")
else:
    st.warning("Please enter a birth city to anchor the map.")
