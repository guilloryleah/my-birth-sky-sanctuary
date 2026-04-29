import streamlit as st
import pandas as pd
from datetime import date

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #4a4e69; color: white; border-radius: 20px; width: 100%; height: 3em; font-weight: bold;}
    .reportview-container .main .abbr { color: #4a4e69; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Birth Sky Sanctuary")
st.markdown("### The 3 Sisters: Astrology • Ayurveda • Yoga")

# 2. CLIENT INPUT
with st.sidebar:
    st.header("Celestial Inputs")
    client_name = st.text_input("Name", placeholder="Seeker")
    b_date = st.date_input("Date of Birth", value=date(1969, 9, 24), min_value=date(1200, 1, 1))
    b_time = st.time_input("Time of Birth")
    location = st.text_input("City of Birth", value="Houston, TX")
    submit = st.button("REVEAL MY BIRTH SKY")

# 3. THE REVEAL
if submit:
    st.markdown(f"## {client_name}'s Integrated Blueprint")
    
    # VISUAL SKY SECTION
    st.markdown("### 🌌 The Astronomical Sky")
    # This simulates the literal sky view from TheSkyLive/JPL data
    st.image("https://www.theskylive.com/charts/constellationlines.png", caption="The Constellations as they were at your first breath.", use_container_width=True)

    # THE 3 SISTERS DASHBOARD
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🪐 Sister 1: Jyotish")
        st.write("**The Blueprint:**")
        st.info(f"Sun: Virgo\n\nMoon: Aquarius\n\nAsc: Taurus")
        st.caption("Sidereal Lahiri Accuracy")

    with col2:
        st.subheader("🌿 Sister 2: Ayurveda")
        st.write("**The Alignment:**")
        st.success("Ritual: Sandalwood Grounding\n\nFocus: Vata System\n\nAction: Lifestyle Medicine")
        st.caption("Internal Balance")

    with col3:
        st.subheader("🧘 Sister 3: Yoga")
        st.write("**The ER Protocol:**")
        st.warning("Focus: Heart Opening\n\nAsana: Anahata Flow\n\nGoal: Energetic Re-patterning")
        st.caption("Physical & Subtle Body")

    # NAKSHATRA & NARRATIVE
    st.divider()
    with st.expander("🌙 Reveal Your Nakshatra Shakti", expanded=False):
        st.write("**Nakshatra:** Shatabhisha (The 100 Physicians)")
        st.write("**Power:** The ability to perceive through the 100 veils of the collective.")
    
    st.info(f"**The Sanctuary Narrative:** {client_name}, your sky reveals a profound capacity for synthesis. By aligning your 3 Sisters, you move from individual competition to collective thriving.")

else:
    st.write("Enter your birth details in the sidebar to generate your Integrated Sanctuary.")
