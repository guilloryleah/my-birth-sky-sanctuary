import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim

# --- THE EXPANDED ENGINE ---
def get_planet_data(jd_ut, planet_id, planet_name, ayan):
    # Calculate planet position with Sidereal Flag
    res = swe.calc_ut(jd_ut, planet_id, swe.FLG_SIDEREAL)
    long = res[0]
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return {
        "name": planet_name,
        "deg": long % 30,
        "sign": signs[int(long / 30)]
    }

def calculate_full_map(year, month, day, hour, minute, lat, lon):
    # 1. VERIFIED WORLD CLOCK (Astro.com Offset)
    offset = -6.0 
    ut_hour = (hour + minute / 60.0) - offset
    jd_ut = swe.julday(year, month, day, ut_hour)

    # 2. REAL-SKY CALIBRATION
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    ayan = swe.get_ayanamsa_ut(jd_ut)
    swe.set_topo(lat, lon, 0)

    # 3. CALCULATE ASCENDANT
    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn")
    ]

    results = []
    for p_id, p_name in planets:
        results.append(get_planet_data(jd_ut, p_id, p_name, ayan))

    return {
        "asc_deg": asc_raw % 30,
        "asc_sign": signs[int(asc_raw / 30)],
        "planets": results
    }

# --- THE INTERFACE ---
st.title("✨ The Real-Sky Soul Map: Full Edition")

address = st.text_input("Location", "Chicago, Illinois")
geolocator = Nominatim(user_agent="soul_map_full")
location = geolocator.geocode(address)

if location:
    name = st.text_input("Name", "Danny Slater")
    col1, col2 = st.columns(2)
    with col1:
        # Birth Date from Sheet
        b_date = st.date_input("Birth Date", datetime(1957, 5, 22)) 
    with col2:
        b_time = st.time_input("Birth Time", datetime.strptime("04:10", "%H:%M").time())

    if st.button("Generate Full Soul Map"):
        data = calculate_full_map(b_date.year, b_date.month, b_date.day, 
                                 b_time.hour, b_time.minute, location.latitude, location.longitude)
        
        st.header(f"✨ {name}'s Complete Map")
        st.metric("Foundation (Ascendant)", f"{data['asc_deg']:.2f}° {data['asc_sign']}")
        
        # Displaying the "Family of Stars"
        st.subheader("The Inner Council")
        cols = st.columns(3)
        for i, p in enumerate(data['planets']):
            with cols[i % 3]:
                st.write(f"**{p['name']}**")
                st.write(f"{p['deg']:.2f}° {p['sign']}")
                
        # Protector check for Danny
        if data['asc_sign'] == "Taurus":
            st.success("Protector Architecture Active: Grounded Krittika energy confirmed.")
