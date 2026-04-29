import streamlit as st
import pandas as pd
from datetime import date, time

# 1. SANCTUARY UI
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# 2. THE MASTER NAKSHATRA DICTIONARY (Your Interpretations)
NAK_DATA = {
    "Ashwini": "The Power to Reach Quickly. Energetic healing and rapid initiation.",
    "Rohini": "The Power of Growth. Creating beauty, fertility, and stable foundations.",
    "Hasta": "The Power to Manifest. Skill with the hands, craftsmanship, and detail.",
    "Shatabhisha": "The Power of Healing. Perceiving truth through the 100 physicians.",
    "Magha": "The Power of Lineage. Connection to ancestors and noble authority.",
    "Revati": "The Power of Nourishment. Protecting the collective and final transitions."
}

# 3. THE CALCULATION ENGINE (Time & Date sensitive)
def get_detailed_blueprint(m, d, y, hour):
    # This is a simplified astronomical bridge for the 'Big Three'
    # Sun Logic
    if (m == 9 and d >= 16) or (m == 10 and d <= 16): 
        sun = ("Virgo", "Hasta")
    elif (m == 2 and d >= 13) or (m == 3 and d <= 13):
        sun = ("Aquarius", "Shatabhisha")
    else:
        sun = ("Taurus", "Rohini") # Default for demo

    # Moon Logic (Simplified: Moves ~13 deg per day)
    # We use the day of the month to shift the moon nakshatra
    moon_index = (d + m) % len(NAK_DATA)
    moon_name = list(NAK_DATA.keys())[moon_index]
    moon = ("Aquarius" if d % 2 == 0 else "Leo", moon_name)

    # Ascendant Logic (Changes every 2 hours)
    asc_index = (hour // 2) % len(NAK_DATA)
    asc_name = list(NAK_DATA.keys())[asc_index]
    asc = ("Taurus" if hour < 12 else "Scorpio", asc_name)
    
    return sun, moon, asc

# 4. SIDEBAR INPUTS
with st.sidebar:
    st.header("Identify the Seeker")
    client_name = st.text_input("Full Name")
    target_year = st.number_input("Year", 1200, 2026, 1969)
    target_month = st.number_input("Month", 1, 12, 9)
    target_day = st.number_input("Day", 1, 31, 24)
    b_time = st.time_input("Birth Time", value=time(12, 0))
    submit = st.button("REVEAL MY SANCTUARY")

# 5. THE NARRATIVE REVEAL
if submit:
    sun, moon, asc = get_detailed_blueprint(target_month, target_day, target_year, b_time.hour)
    
    st.markdown(f"# Welcome to your Sanctuary, {client_name}")
    st.markdown(f"**Calculated for your birth on {target_month}/{target_day}/{target_year} at {b_time}.**")
    st.divider()

    # THE THREE SISTERS DASHBOARD
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.write(f"**Ascendant (Lagna):** {asc[0]} | {asc[1]}")
        st.write(f"**Sun (Surya):** {sun[0]} | {sun[1]}")
        st.write(f"**Moon (Chandra):** {moon[0]} | {moon[1]}")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.success("**Alignment Strategy:**")
        st.write(f"Since your Sun is in {sun[0]}, we focus on balancing your core energy through **Lifestyle Medicine** specific to Earth/Air synthesis.")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.warning("**Energetic Re-patterning:**")
        st.write(f"For a {asc[1]} Nakshatra, your ER protocol involves grounding the nervous system to allow the Shakti to flow.")

    # DETAILED ANALYSIS SECTION
    st.markdown("---")
    st.header("Detailed Celestial Analysis")
    
    with st.expander("✨ Your Sun (Core Identity)", expanded=True):
        st.write(f"In {sun[0]}, your light is filtered through the Nakshatra **{sun[1]}**. {NAK_DATA.get(sun[1])}")
        st.write("This is where your individual agency meets the needs of the collective.")

    with st.expander("🌙 Your Moon (Emotional Resonance)"):
        st.write(f"Your emotional body resonates with the frequency of **{moon[1]}**. {NAK_DATA.get(moon[1])}")
        st.write("This defines your 'Ubuntu Heart'—how you connect to the thriving of others.")

    with st.expander("🌅 Your Ascendant (The Gateway)"):
        st.write(f"You meet the world through the lens of **{asc[0]}** and the power of **{asc[1]}**. {NAK_DATA.get(asc[1])}")

else:
    st.write("Enter your details in the sidebar to reveal your personal 3-Sisters Blueprint.")
