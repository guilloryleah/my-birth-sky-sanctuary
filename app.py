import streamlit as st
import swisseph as swe
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim # The 'City Search' Engine

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
st.set_page_config(page_title="The Soul Map")
st.title("✨ The Real-Sky Soul Map")
st.markdown("### Mapping the Soul for Anyone, Anywhere, at Any Age")

# 1. THE LOCATION SEARCH (The "Anyone, Anywhere" Key)
st.subheader("Where were you born?")
address = st.text_input("Enter City, State, or Country", "Chicago, Illinois")

geolocator = Nominatim(user_agent="soul_map_engine")
location = geolocator.geocode(address)

if location:
    st.success(f"Location Found: {location.address}")
    lat, lon = location.latitude, location.longitude
else:
    st.warning("Please enter a valid city to anchor the map.")

# 2. BIRTH DETAILS
st.divider()
name = st.text_input("Name", "Danny")
col1, col2 = st.columns(2)
with col1:
    b_date = st.date_input("Birth Date", datetime(1957, 5, 10))
with col2:
    b_time = st.time_input("Birth Time", datetime.strptime("12:00", "%H:%M").time())

# 3. THE WORLD CLOCK OFFSET (Still manual for historical accuracy)
utc_off = st.number_input("World Clock Offset (UTC) for that location", value=-5.0)

# 4. GENERATE
if st.button("Generate Soul Map") and location:
    try:
        deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                       b_time.hour, b_time.minute, lat, lon, utc_off)
        
        st.header(f"✨ {name}'s Soul Map is Ready")
        st.metric("Foundation", f"{deg:.2f}° {sign}")

        if sign == "Taurus":
            st.info("**Internal Atmosphere:** Kapha (Stability)")
            st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
        
        st.divider()
        st.caption("This map accounts for the Earth's wobble to reflect the True Sky stars at the moment of birth.")
    except Exception as e:
        st.error(f"The engine encountered an issue: {e}")
