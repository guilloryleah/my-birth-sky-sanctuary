import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE UNIVERSAL ENGINE ---
def get_planet_data(jd_ut, planet_id, planet_name):
    # res[0] is the longitude for the Real-Sky math
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
    # 1. THE AUTOMATIC WORLD CLOCK (Fixes the Leah/Danny offset mismatch)
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name)
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    # This converts local time (10:59 PM) to the correct UTC (3:59 AM) automatically
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # 2. REAL-SKY CALIBRATION (Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)

    # 3. HOUSE CUSPS & ASCENDANT
    # Calculating seasonal houses first, then applying the Ayanamsha shift
    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")
    ]

    birth_planets = [get_planet_data(jd_ut, p_id, p_name) for p_id, p_name in planets]

    # 4. TRANSIT CALCULATION
    transit_results = []
    if transit_date:
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

# Defaulting to Houston for your test
address = st.text_input("Location", "Houston, Texas")
geolocator = Nominatim(user_agent="soul_map_final_v1")
location = geolocator.geocode(address)

if location:
    name = st.text_input("Name", "Leah G")
    col1, col2 = st.columns(2)
    with col1:
        # Unrestricted Calendar
        b_date = st.date_input(
            "Birth Date", 
            value=datetime(1969, 9, 24),
            min_value=datetime(1900, 1, 1),
            max_value=datetime(2100, 12, 31)
        ) 
    with col2:
        # Your birth time
        b_time = st.time_input("Birth Time", datetime.strptime("22:59", "%H:%M").time())

    if st.button("Generate Full Soul Map"):
        try:
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
                
                # Ketu Logic
                rahu_data = data['birth_planets'][-1]
                ketu_sign_idx = (["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"].index(rahu_data['sign']) + 6) % 12
                ketu_sign = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][ketu_sign_idx]
                st.write(f"**Ketu**: {rahu_data['deg']:.2f}° {ketu_sign}")

                if data['asc_sign'] == "Taurus":
                    st.success("Protector Architecture: Grounded Krittika/Rohini energy confirmed.")

            with tab2:
                st.subheader("April 2026 Transits")
                st.info("Where the stars are moving today relative to your birth map.")
                cols_t = st.columns(4)
                for i, p in enumerate(data['transit_planets']):
                    with cols_t[i % 4]:
                        st.write(f"**{p['name']}**")
                        st.write(f"{p['deg']:.2f}° {p['sign']}")

            st.divider()
            st.caption("Calculated using Automatic Timezone Detection and True Lahiri Sidereal.")
            
        except Exception as e:
            st.error(f"Calibration needed: {e}")
else:
    st.warning("Please enter a birth city to anchor the map.")
