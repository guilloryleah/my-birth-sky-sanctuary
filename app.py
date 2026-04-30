import streamlit as st
import swisseph as swe
from datetime import datetime, timedelta

# --- THE COSMOSPOETESS ENGINE ---

def get_real_sky_report(name, year, month, day, hour, minute, lat, lon, utc_offset):
    # 1. THE WORLD CLOCK ANCHOR
    local_time = datetime(year, month, day, hour, minute)
    utc_time = local_time - timedelta(hours=utc_offset)
    julian_day = swe.julday(utc_time.year, utc_time.month, utc_time.day, 
                            utc_time.hour + utc_time.minute/60.0)

    # 2. THE REAL-SKY CONSTANT (Prevents Aries Drift)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0) 
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # 3. LOCAL SIDEREAL TIME (The 1° Taurus Solution)
    cusps, ascmc = swe.houses_ex(julian_day, lat, lon, b'P', flags)
    ascendant_raw = ascmc[0]
    
    sign_index = int(ascendant_raw / 30)
    degrees_in_sign = ascendant_raw % 30
    zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    return degrees_in_sign, zodiac_signs[sign_index]

# --- THE STREAMLIT DISPLAY (Wakes up the screen) ---

st.set_page_config(page_title="Soul Map Truth Receipt", page_icon="✨")

st.title("✨ The Real-Sky Soul Map")
st.subheader("Anchored in the World Clock for Anyone at Any Age")

# Creating the inputs for your clients
with st.sidebar:
    st.header("Birth Details")
    user_name = st.text_input("Name", "Danny")
    b_date = st.date_input("Birth Date", datetime(1957, 5, 10))
    b_time = st.time_input("Birth Time", datetime.strptime("12:00", "%H:%M").time())
    
    st.markdown("---")
    st.header("Location & World Clock")
    lat = st.number_input("Latitude", value=41.8781, format="%.4f")
    lon = st.number_input("Longitude", value=-87.6298, format="%.4f")
    offset = st.number_input("World Clock Offset (UTC)", value=-5.0, step=1.0)

if st.button("Generate Truth Receipt"):
    deg, sign = get_real_sky_report(user_name, b_date.year, b_date.month, b_date.day, 
                                    b_time.hour, b_time.minute, lat, lon, offset)
    
    # This is what stops the "White Screen" and shows the result
    st.success(f"Calculation Complete for {user_name}!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Foundation", f"{deg:.2f}° {sign}")
    with col2:
        st.metric("System", "Sidereal (True Lahiri)")

    st.write("### The Wisdom Library")
    if sign == "Taurus":
        st.info("**Internal Atmosphere:** Kapha (Stability)")
        st.info("**Soulful Movement:** Vrksasana (Tree Pose)")
    else:
        st.info("Wisdom profile is loading based on the astronomical foundation...")

    st.divider()
    st.caption("Note: This report accounts for Earth's wobble to reflect the True Sky stars at the moment of birth.")
