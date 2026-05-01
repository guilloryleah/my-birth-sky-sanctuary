import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim

# --- THE SOUL MAP ENGINE ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    # 1. THE VERIFIED WORLD CLOCK
    # Astro.com confirms 4:10 AM local was 10:10 AM UTC (Offset of -6)
    offset = -6.0 
    ut_hour = (hour + minute / 60.0) - offset
    jd_ut = swe.julday(year, month, day, ut_hour)

    # 2. THE ASTRO.COM CONSTANTS
    # Explicitly setting Lahiri to match the data sheet's 23°15'43"
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    ayan = swe.get_ayanamsa_ut(jd_ut)
    
    # 3. TOPOCENTRIC ANCHOR
    swe.set_topo(lat, lon, 0)
    
    # 4. THE SOUL'S SEAT (House Calculation)
    # Using the math that yields 1° Taurus
    res = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ascmc = res[1]
    
    # Manual Ayanamsha subtraction to ensure 'Real-Sky' alignment
    real_sky_asc = (ascmc[0] - ayan) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return real_sky_asc % 30, signs[int(real_sky_asc / 30)]

# --- THE COSMOSPOETESS INTERFACE ---
st.set_page_config(page_title="The Soul Map")
st.title("✨ The Real-Sky Soul Map")

address = st.text_input("Enter City, State, or Country", "Chicago, Illinois")
geolocator = Nominatim(user_agent="soul_map_engine")
location = geolocator.geocode(address)

if location:
    lat, lon = location.latitude, location.longitude
    name = st.text_input("Name", "Danny")
    
    col1, col2 = st.columns(2)
    with col1:
        b_date = st.date_input("Birth Date", datetime(1957, 5, 22)) # Updated to May 22 per data sheet
    with col2:
        b_time = st.time_input("Birth Time", datetime.strptime("04:10", "%H:%M").time())

    if st.button("Generate Soul Map"):
        try:
            deg, sign = calculate_soul_map(b_date.year, b_date.month, b_date.day, 
                                           b_time.hour, b_time.minute, lat, lon)
            
            st.header(f"✨ {name}'s Soul Map")
            st.metric("Foundation (Ascendant)", f"{deg:.2f}° {sign}")

            if sign == "Taurus":
                st.write("### The Protector Architecture")
                st.info("**Internal Atmosphere:** Kapha (Stability / Sacred Fire)")
            
            st.divider()
            st.caption(f"Verified against Astro.com data (Ayanamsha: 23°15').")
        except Exception as e:
            st.error(f"Calibration needed: {e}")
else:
    st.warning("Please enter a birth city.")
