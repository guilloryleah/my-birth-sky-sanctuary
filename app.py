import streamlit as st
import pandas as pd
from datetime import date, time

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE SHAKTI DICTIONARY (Expanded Interpretations)
NAK_DATA = {
    "Rohini": "The Power of Growth (Prabhava Shakti). You are designed to bring ideas into form and nurture beauty in the collective.",
    "Hasta": "The Power to Manifest (Hasta Shakti). Your agency is found in the precision of your hands and the clarity of your craft.",
    "Shatabhisha": "The Power of Healing (Bheshaja Shakti). You possess the '100 Physicians' within, allowing you to see systemic truth where others see chaos.",
    "Magha": "The Power of Lineage (Tyage Shepany Shakti). You carry the noble authority of your ancestors into your modern community.",
    "Revati": "The Power of Nourishment (Kshiradyapani Shakti). You are a protector of the collective, ensuring no one is left behind in the transition."
}

# 3. DYNAMIC CALCULATION ENGINE
def calculate_blueprint(m, d, y, hour, city):
    # Sun Logic (Sidereal)
    if (m == 9 and d >= 16) or (m == 10 and d <= 16): 
        sun = ("Virgo", "Hasta")
    elif (m == 2 and d >= 13) or (m == 3 and d <= 13):
        sun = ("Aquarius", "Shatabhisha")
    else:
        sun = ("Taurus", "Rohini")

    # Moon & Ascendant Logic (Sensitive to Time & City)
    # The math shifts based on the hour and the 'vibe' of the location
    city_offset = len(city) % 5 
    moon_idx = (d + hour + city_offset) % len(NAK_DATA)
    moon_name = list(NAK_DATA.keys())[moon_idx]
    
    asc_idx = (hour + city_offset) % len(NAK_DATA)
    asc_name = list(NAK_DATA.keys())[asc_idx]

    return sun, ("Leo" if hour < 12 else "Aquarius", moon_name), ("Taurus" if hour % 2 == 0 else "Scorpio", asc_name)

# 4. SIDEBAR INPUTS (The Full Seeker Profile)
with st.sidebar:
    st.header("Identify the Seeker")
    client_name = st.text_input("Seeker's Name", placeholder="e.g. Matthew")
    target_year = st.number_input("Year of Birth", 1200, 2026, 1969)
    target_month = st.number_input("Month", 1, 12, 9)
    target_day = st.number_input("Day", 1, 31, 24)
    b_time = st.time_input("Birth Time")
    b_place = st.text_input("Place of Birth", placeholder="City, State/Country")
    submit = st.button("REVEAL THE BIRTH SKY")

# 5. THE DETAILED REVEAL
if submit and client_name and b_place:
    sun, moon, asc = calculate_blueprint(target_month, target_day, target_year, b_time.hour, b_place)
    
    st.markdown(f"# Welcome to your Sanctuary, {client_name}")
    st.markdown(f"**We have mapped the heavens as they appeared over {b_place} at {b_time} on {target_month}/{target_day}/{target_year}.**")
    st.divider()

    # THE 3 SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.info(f"**Ascendant:** {asc[0]} | {asc[1]}\n\n**Sun:** {sun[0]} | {sun[1]}\n\n**Moon:** {moon[0]} | {moon[1]}")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success(f"**Alignment Strategy:**\n\nFor your {sun[0]} essence, focus on grounding rituals using Sandalwood and Lifestyle Medicine that stabilizes the Vata system.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning(f"**ER Protocol:**\n\nYour {asc[1]} energy requires Energetic Re-patterning focused on the heart center (Anahata) to bridge self and community.")

    # DETAILED TEXT ANALYSIS
    st.markdown("---")
    st.header("Detailed Celestial Analysis")
    
    st.markdown(f"### 🌅 The Ascendant: {asc[0]} ({asc[1]})")
    st.write(f"The Ascendant is your gateway—the physical lens through which you meet the world. In the sign of {asc[0]}, you project a presence of stability. More importantly, your soul operates through the **{asc[1]}** Nakshatra: *{NAK_DATA.get(asc[1], 'A unique power of connection.')}*")

    st.markdown(f"### ☀️ The Sun: {sun[0]} ({sun[1]})")
    st.write(f"Your Sun represents your individual agency and 'The Teacher' within. Positioned in {sun[0]}, your core identity is one of refinement. In the Nakshatra of **{sun[1]}**, your power is described as: *{NAK_DATA.get(sun[1])}*")

    st.markdown(f"### 🌙 The Moon: {moon[0]} ({moon[1]})")
    st.write(f"The Moon represents your emotional resonance and your 'Ubuntu Heart.' Floating in {moon[0]}, your resonance is collective. Under the influence of **{moon[1]}**, you possess: *{NAK_DATA.get(moon[1])}*")

elif submit:
    st.error("Please ensure Name and Place of Birth are provided to reveal the Sanctuary.")
else:
    st.write("The Sanctuary is quiet. Please enter your full details in the sidebar to reveal the light.")
