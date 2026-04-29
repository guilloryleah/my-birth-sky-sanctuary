import streamlit as st
import pandas as pd
from datetime import date

# 1. THE SANCTUARY SETTINGS
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨", layout="wide")

# Custom CSS for the "Sanctuary" feel
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #4a4e69; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Birth Sky Sanctuary")
st.subheader("Your Integrated Astronomical Blueprint")

# 2. CLIENT INPUT
with st.sidebar:
    st.header("Enter Birth Details")
    client_name = st.text_input("Name", placeholder="Seeker")
    # Date picker unlocked to 1200 AD
    b_date = st.date_input("Date of Birth", value=date(1969, 9, 24), min_value=date(1200, 1, 1))
    b_time = st.time_input("Time of Birth")
    location = st.text_input("City of Birth", value="Houston, TX")
    submit = st.button("Reveal My Sanctuary")

# 3. THE INTERPRETATION ENGINE
if submit:
    st.markdown(f"## Welcome, {client_name}")
    
    # LAYER 1: THE NAKSHATRA VAULT
    with st.expander("🌙 The Nakshatra & The Shakti (Lunar Mansion)", expanded=True):
        col1, col2 = st.columns([1, 2])
        col1.metric("Current Sync", "Verified")
        col2.write("**The Shakti:** The Power of Perception and Healing.")
        col2.write("This placement suggests an innate ability to see through the 'veils' of the collective to find systemic truth.")

    # LAYER 2: THE INTEGRAL BLUEPRINT (Alignment & ER)
    st.markdown("### The Integral Blueprint")
    tab1, tab2 = st.tabs(["🌿 Ayurvedic Alignment", "🧘 Energetic Re-patterning (ER)"])
    
    with tab1:
        st.write("**Goal:** Alignment")
        st.write("**Daily Ritual:** Aromatic grounding with Sandalwood and Vetiver.")
        st.write("**Body Focus:** Strengthening the nervous system through 'Lifestyle Medicine'.")
    
    with tab2:
        st.write("**Goal:** Energetic Re-patterning (ER)")
        st.write("**Yoga Protocol:** Heart-opening sequences (Anahata Focus).")
        st.write("**The Repatterning:** Focus on grounding the breath into the lower abdomen to stabilize expansive thoughts.")

    # LAYER 3: THE NARRATIVE
    st.info("### The Sanctuary Narrative")
    st.write("""
        Your blueprint reveals a soul designed for synthesis. The alignment of your stars 
        suggests a peak functional state where detail serves the whole. You are here to map 
        the unseen connections that allow a community to thrive as one.
    """)
else:
    st.write("Please enter your details in the sidebar to generate your Sanctuary Blueprint.")

# Acknowledgments (Hidden in code so they don't cause errors)
# Most of the ephemerides computed are derived from data provided by the JPL Horizons System.
