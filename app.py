import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE NAKSHATRA LOOKUP ENGINE ---
def get_nakshatra(sign, degree):
    # This function uses the exact ranges you provided to find the star-home
    if sign == "Aries":
        if degree < 13.333: return "Ashwini"
        if degree < 26.666: return "Bharani"
        return "Krittika"
    elif sign == "Taurus":
        if degree < 10.0: return "Krittika"
        if degree < 23.333: return "Rohini"
        return "Mrigashira"
    elif sign == "Gemini":
        if degree < 6.666: return "Mrigashira"
        if degree < 20.0: return "Ardra"
        return "Punarvasu"
    elif sign == "Cancer":
        if degree < 3.333: return "Punarvasu"
        if degree < 16.666: return "Pushya"
        return "Ashlesha"
    elif sign == "Leo":
        if degree < 13.333: return "Magha"
        if degree < 26.666: return "Purva Phalguni"
        return "Uttara Phalguni"
    elif sign == "Virgo":
        if degree < 10.0: return "Uttara Phalguni"
        if degree < 23.333: return "Hasta"
        return "Chitra"
    elif sign == "Libra":
        if degree < 6.666: return "Chitra"
        if degree < 20.0: return "Swati"
        return "Vishakha"
    elif sign == "Scorpio":
        if degree < 3.333: return "Vishakha"
        if degree < 16.666: return "Anuradha"
        return "Jyeshtha"
    elif sign == "Sagittarius":
        if degree < 13.333: return "Moola"
        if degree < 26.666: return "Purva Ashada"
        return "Uttara Ashada"
    elif sign == "Capricorn":
        if degree < 10.0: return "Uttara Ashada"
        if degree < 23.333: return "Shravana"
        return "Dhanishta"
    elif sign == "Aquarius":
        if degree < 6.666: return "Dhanishta"
        if degree < 20.0: return "Shatabhisha"
        return "Purva Bhadrapada"
    elif sign == "Pisces":
        if degree < 3.333: return "Purva Bhadrapada"
        if degree < 16.666: return "Uttara Bhadrapada"
        return "Revati"
    return "Unknown"

# --- THE UNIVERSAL ENGINE ---
def get_planet_data(jd_ut, planet_id, planet_name):
    res, ret = swe.calc_ut(jd_ut, planet_id, swe.FLG_SIDEREAL)
    long = res[0]
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    sign = signs[int(long / 30)]
    degree = long % 30
    nakshatra = get_nakshatra(sign, degree)
    
    return {
        "name": planet_name,
        "deg": degree,
        "sign": sign,
        "nakshatra": nakshatra
    }

def calculate_full_map(year, month, day, hour, minute, lat, lon, transit_date=None):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name)
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd_ut = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    swe.set_topo(lat, lon, 0)

    res_h = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
    ayan_corr = swe.get_ayanamsa_ut(jd_ut)
    asc_raw = (res_h[1][0] - ayan_corr) % 360
    
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    asc_sign = signs[int(asc_raw / 30)]
    asc_deg = asc_raw % 30
    asc_nakshatra = get_nakshatra(asc_sign, asc_deg)
    
    planets = [
        (swe.SUN, "Sun"), (swe.MOON, "Moon"), (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"), (swe.MARS, "Mars"), (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"), (swe.MEAN_NODE, "Rahu")
    ]

    birth_planets = [get_planet_data(jd_ut, p_id, p_name) for p_id, p_name in planets]

    transit_results = []
    if transit_date:
        jd_transit = swe.julday(transit_date.year, transit_date.month, transit_date.day, 12.0)
        transit_results = [get_planet_data(jd_transit, p_id, p_name) for p_id, p_name in planets]

    return {
        "asc_deg": asc_deg,
        "asc_sign": asc_sign,
        "asc_nakshatra": asc_nakshatra,
        "birth_planets": birth_planets,
        "transit_planets": transit_results
    }

# --- THE INTERFACE ---
st.set_page_config(page_title="The Soul Map", layout="wide")
st.title("✨ The Real-Sky Soul Map: Nakshatra Edition")

address = st.text_input("Location", "Houston, Texas")
geolocator = Nominatim(user_agent="soul_map_nakshatra_v1")
location = geolocator.geocode(address)

if location:
    name = st.text_input("Name", "Leah G")
    col1, col2 = st.columns(2)
    with col1:
        b_date = st.date_input("Birth Date", value=datetime(1969, 9, 24),
                                min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31)) 
    with col2:
        b_time = st.time_input("Birth Time", datetime.strptime("22:59", "%H:%M").time())

    if st.button("Generate Full Soul Map"):
        try:
            data = calculate_full_map(b_date.year, b_date.month, b_date.day, 
                                     b_time.hour, b_time.minute, 
                                     location.latitude, location.longitude, 
                                     transit_date=datetime.now())
            
            st.header(f"✨ {name}'s Complete Soul Map")
            st.metric("Foundation (Ascendant)", f"{data['asc_deg']:.2f}° {data['asc_sign']}")
            st.subheader(f"Star Mansion: {data['asc_nakshatra']}")
            
            tab1, tab2 = st.tabs(["The Inner Council (Birth)", "Current Sky (Transits)"])
            
            with tab1:
                cols = st.columns(4)
                for i, p in enumerate(data['birth_planets']):
                    with cols[i % 4]:
                        st.write(f"**{p['name']}**")
                        st.write(f"{p['deg']:.2f}° {p['sign']}")
                        st.write(f"*{p['nakshatra']}*")
                
                # Ketu Logic
                rahu_data = data['birth_planets'][-1]
                ketu_sign_idx = (["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"].index(rahu_data['sign']) + 6) % 12
                ketu_sign = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][ketu_sign_idx]
                ketu_nak = get_nakshatra(ketu_sign, rahu_data['deg'])
                st.write(f"**Ketu**: {rahu_data['deg']:.2f}° {ketu_sign}")
                st.write(f"*{ketu_nak}*")

            with tab2:
                st.info("Where the stars are moving today.")
                cols_t = st.columns(4)
                for i, p in enumerate(data['transit_planets']):
                    with cols_t[i % 4]:
                        st.write(f"**{p['name']}**")
                        st.write(f"{p['deg']:.2f}° {p['sign']}")
                        st.write(f"*{p['nakshatra']}*")

            st.divider()
            st.caption("Calculated using Automatic Timezone Detection, True Lahiri, and Your Custom Nakshatra Ranges.")
            
        except Exception as e:
            st.error(f"Calibration needed: {e}")
else:
    st.warning("Please enter a birth city.")
