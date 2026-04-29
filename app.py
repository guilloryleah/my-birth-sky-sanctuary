import streamlit as st
import swisseph as swe
from datetime import datetime, time

# 1. THE DATA REFERENCE
NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def get_nakshatra(deg):
    idx = int(deg / 13.333333) % 27
    return NAK_LIST[idx]

def get_zodiac(deg):
    idx = int(deg / 30) % 12
    d_in_sign = int(deg % 30)
    m_in_sign = int((deg % 1) * 60)
    return f"{d_in_sign}°{m_in_sign}' {ZODIAC_LIST[idx]}"

# 2. THE INTERFACE
st.set_page_config(page_title="The Sanctuary Engine", layout="wide")
st.title("✨ The Sky Sanctuary Engine")
st.markdown("Enter data exactly as it appears on the **Natal Chart Data Sheet**.")

with st.sidebar:
    st.header("🔭 Data Sheet Entry")
    u_name = st.text_input("Client Name", value="Leah G")
    
    st.divider()
    st.subheader("Time & Place")
    # Using Julian Day logic via Univ. Time
    u_date = st.date_input("Birth Date (UT)", value=datetime(1969, 9, 25)) 
    u_ut = st.time_input("Univ. Time (UT)", value=time(3, 59))
    
    st.divider()
    st.subheader("Coordinates")
    u_lat = st.number_input("Latitude (Decimal)", value=29.76, format="%.4f")
    u_lon = st.number_input("Longitude (Decimal)", value=-95.37, format="%.4f")

# 3. THE CALCULATION
if st.button("✨ Reveal the Sky"):
    # Set the Ayanamsha to Lahiri (The 24-degree shift)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Calculate Julian Day from Universal Time
    ut_decimal = u_ut.hour + (u_ut.minute / 60.0) + (u_ut.second / 3600.0)
    jd_ut = swe.julday(u_date.year, u_date.month, u_date.day, ut_decimal)

    # HOUSE CALCULATION (For the Ascendant)
    # Using Whole Sign (b'W') as requested
    cusps, ascmc = swe.houses_ex(jd_ut, u_lat, u_lon, b'W', swe.FLG_SIDEREAL)
    asc_deg = ascmc[0]

    # PLANET CALCULATION
    planets = {"Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN}
    results = {}
    for p_name, p_id in planets.items():
        res, _ = swe.calc_ut(jd_ut, p_id, swe.FLG_SIDEREAL)
        results[p_name] = res[0]

    # 4. THE REVEAL
    st.header(f"The Soul-Map for {u_name}")
    
    # Trinity Row
    t1, t2, t3 = st.columns(3)
    with t1:
        st.metric("Ascendant", get_nakshatra(asc_deg))
        st.caption(get_zodiac(asc_deg))
    with t2:
        st.metric("Sun", get_nakshatra(results["Sun"]))
        st.caption(get_zodiac(results["Sun"]))
    with t3:
        st.metric("Moon", get_nakshatra(results["Moon"]))
        st.caption(get_zodiac(results["Moon"]))

    st.divider()
    
    # Council Row
    c_cols = st.columns(4)
    for i, p in enumerate(["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]):
        with c_cols[i % 4]:
            st.write(f"**{p}**")
            st.info(f"{get_nakshatra(results[p])}\n\n{get_zodiac(results[p])}")
