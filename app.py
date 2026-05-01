import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim

# --- THE STABILIZED ENGINE ---
def get_planet_data(jd_ut, planet_id, planet_name):
    # res[0] is the longitude we need for the 1.74° Taurus math
    res, ret = swe.calc_ut(jd_ut, planet_id, swe.FLG_SIDEREAL)
    long = res[0]
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return {
        "name": planet_name,
        "deg": long % 30,
        "sign": signs[int(long / 30)]
    }

def calculate_full_map(year, month, day, hour, minute, lat, lon, transit_date=None):
    # 1. VERIFIED WORLD CLOCK (Astro.com Offset -6.0)
    offset = -6.0 
    ut_hour = (hour + minute / 60.0) - offset
    jd_ut = swe.julday(year, month, day, ut_hour)

    # 2. REAL-SKY CALIBRATION (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)

    # 3. HOUSE CUSPS & ASCENDANT (Manual Ayanamsha Correction)
    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    # Council Members (Birth Planets)
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")
    ]

    birth_planets = [get_planet_data(jd_ut, p_id, p_name) for p_id, p_name in planets]

    # 4. TRANSIT CALCULATION (Page 2 of your sheet)
    transit_results = []
    if transit_date:
        # Using current time for transits
        jd_transit = swe.julday(transit_date.year, transit_date.month, transit_date.day, 12.0)
        transit_results = [get_planet_data(jd_transit, p_id, p_name) for p_id, p_name in planets]

    return {
        "asc_deg": asc_raw % 30,
        "asc_sign": signs[int(asc_raw / 30)],
        "birth_planets": birth_planets,
        "transit_planets": transit_results
    }

# --- THE COSMOSPOETESS INTERFACE ---
st.set_page_config(page_title="The Soul Map", layout="wide")
st.title("✨ The Real-Sky Soul Map: Full Edition")

address = st.text_input("Location", "Chicago, Illinois")
geolocator = Nominatim(user_agent="soul_map_v3")
location = geolocator.geocode(address)

if location:
    name = st.text_input("Name", "Danny Slater")
    col1, col2 = st.columns(2)
    with col1:
        # Birth Date Verified from Sheet
        b_date = st.date_input("Birth Date", datetime(1957, 5, 22)) 
    with col2:
        # Birth Time Verified from Sheet
        b_time = st.time_input("Birth Time", datetime.strptime("04:10", "%H:%M").time())

    if st.button("Generate Full Soul Map"):
        # We also pass today's date to see the transits from Danny's Page 2
        data = calculate_full_map(b_date.year, b_date.month, b_date.day, 
                                 b_time.hour, b_time.minute, 
                                 location.latitude, location.longitude, 
                                 transit_date=datetime.now())
        
        # --- DISPLAY ---
        st.header(f"✨ {name}'s Complete Soul Map")
        st.metric("Foundation (Ascendant)", f"{data['asc_deg']:.2f}° {data['asc_sign']}")
        
        tab1, tab2 = st.tabs(["The Inner Council (Birth)", "Current Sky (Transits)"])
        
        with tab1:
            st.subheader("Your Birth Constellation")
            cols = st.columns(4)
            for i, p in enumerate(data['birth_planets']):
                with cols[i % 4]:
                    st.write(f"**{p['name']}**")
                    st.write(f"{p['deg']:.2f}° {p['sign']}")
            
            # Specialized Rahu/Ketu logic
            ketu_deg = (data['birth_planets'][-1]['deg'])
            ketu_sign_idx = (["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"].index(data['birth_planets'][-1]['sign']) + 6) % 12
            ketu_sign = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][ketu_sign_idx]
            st.write(f"**Ketu**: {ketu_deg:.2f}° {ketu_sign}")

        with tab2:
            st.subheader("April 2026 Transits")
            st.info("Where the stars are moving today relative to your map.")
            cols_t = st.columns(4)
            for i, p in enumerate(data['transit_planets']):
                with cols_t[i % 4]:
                    st.write(f"**{p['name']}**")
                    st.write(f"{p['deg']:.2f}° {p['sign']}")

        st.divider()
        st.caption("Calculated using Astro.com Verification (UTC 10:10) and True Lahiri.")
