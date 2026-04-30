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
    
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # 2. THE REAL-SKY CALIBRATION (The Aries Drift Cure)
    # We set the mode to Lahiri AND explicitly tell the engine to use Sidereal houses.
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    
    # 3. TOPOCENTRIC ANCHOR
    swe.set_topo(lat, lon, 0)
    
    # 4. THE SOUL'S SEAT (House Calculation)
    # 'sid_ascmc' gives us the Sidereal Ascendant directly, bypassing the "Aries Drift"
    # We use the 'P' (Placidus) or 'W' (Whole Sign) based on your preference
    cusps, ascmc = swe.houses_ex2(jd_ut, lat, lon, b'P', swe.FLG_SIDEREAL)
    
    asc_raw = ascmc[0] # This is the Ascendant
    
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
        # Danny's Birth Time
        b_time = st.time_input("Birth Time", datetime.strptime("04:10", "%H:%M").time())

    if st.button("Generate Soul Map"):
        deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                       b_time.hour, b_time.minute, lat, lon)
        
        st.header(f"✨ {name}'s Soul Map")
        
        # This will now correctly display the Taurus Foundation
        st.metric("Foundation (Ascendant)", f"{deg:.2f}° {sign}")

        if sign == "Taurus":
            st.info("**Internal Atmosphere:** Kapha (Stability)")
            st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
        
        st.divider()
        st.caption("Calculated using the World Clock and True Lahiri to honor your Real-Sky homecoming.")
else:
    st.warning("Please enter a birth city to anchor the map.")
