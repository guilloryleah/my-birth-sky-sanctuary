import streamlit as st
import pandas as pd
from datetime import date, time

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE DYNAMIC LOGIC (The "Math Bridge")
# This function calculates the Sidereal Sun based on the Day and Month using Lahiri offsets
def calculate_sidereal_sun(m, d):
    if (m == 4 and d >= 14) or (m == 5 and d <= 14): return "Aries", "Ashwini"
    if (m == 5 and d >= 15) or (m == 6 and d <= 14): return "Taurus", "Rohini"
    if (m == 6 and d >= 15) or (m == 7 and d <= 15): return "Gemini", "Punarvasu"
    if (m == 7 and d >= 16) or (m == 8 and d <= 15): return "Cancer", "Pushya"
    if (m == 8 and d >= 16) or (m == 9 and d <= 15): return "Leo", "Magha"
    if (m == 9 and d >= 16) or (m == 10 and d <= 16): return "Virgo", "Hasta"
    if (m == 10 and d >= 17) or (m == 11 and d <= 15): return "Libra", "Swati"
    if (m == 11 and d >= 16) or (m == 12 and d <= 15): return "Scorpio", "Anuradha"
    if (m == 12 and d >= 16) or (m == 1 and d <= 13): return "Sagittarius", "Mula"
    if (m == 1 and d >= 14) or (m == 2 and d <= 12): return "Capricorn", "Shravana"
    if (m == 2 and d >= 13) or (m == 3 and d <= 13): return "Aquarius", "Shatabhisha"
    if (m == 3 and d >= 14) or (m == 4 and d <= 13): return "Pisces", "Revati"
    return "Searching...", "Unknown"

# 3. CLIENT INPUT
with st.sidebar:
    st.header("Celestial Inputs")
    client_name = st.text_input("Full Name", placeholder="Seeker")
    target_year = st.number_input("Year of Birth", min_value=1200, max_value=2026, value=1969)
    target_month = st.number_input("Month (1-12)", 1, 12, 9)
    target_day = st.number_input("Day (1-31)", 1, 31, 24)
    birth_time = st.time_input("Exact Birth Time", value=time(12, 0))
    location = st.text_input("City/State of Birth", value="Houston, TX")
    submit = st.button("REVEAL MY BIRTH SKY")

# 4. THE REVEAL
if submit:
    # RUN THE DYNAMIC MATH
    sun_sign, sun_nak = calculate_sidereal_sun(target_month, target_day)
    
    st.markdown(f"## {client_name}'s Integrated Blueprint")
    
    # 3 SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.metric("Sun Sign", sun_sign)
        st.write(f"**Nakshatra:** {sun_nak}")
        st.caption(f"Sky Map for {target_year} Active")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        # Dynamic Ayurvedic logic based on Sign Element
        if sun_sign in ["Aries", "Leo", "Sagittarius"]:
            st.success("**Focus:** Pitta/Cooling\n\n**Ritual:** Rose Water Mist")
        elif sun_sign in ["Taurus", "Virgo", "Capricorn"]:
            st.success("**Focus:** Vata/Grounding\n\n**Ritual:** Sandalwood Oil")
        else:
            st.success("**Focus:** Kapha/Invigorating\n\n**Ritual:** Dry Brushing")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:** Energetic Re-patterning aligned to {sun_sign}")

    # NAKSHATRA SHAKTI TABLE
    st.divider()
    st.markdown("### 🌙 The Nakshatra & The Shakti")
    st.write(f"**Primary Influence:** {sun_nak}")
    st.info("The power specifically calculated for this celestial alignment.")

else:
    st.write("Enter your birth details in the sidebar to reveal your unique Sanctuary.")
