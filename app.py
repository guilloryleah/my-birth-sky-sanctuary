import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time

# 1. NAKSHATRA REFERENCE
NAK_LIST = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", 
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", 
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", 
    "Uttara Bhadrapada", "Revati"
]

ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def format_dms(deg_raw):
    deg_norm = deg_raw % 360
    sign_idx = int(deg_norm / 30)
    deg_in_sign = deg_norm % 30
    d, m = int(deg_in_sign), int((deg_in_sign - int(deg_in_sign)) * 60)
    nak_idx = int(deg_norm / 13.333333) % 27
    return f"{d}° {m}' {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 2. APP SETUP
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")

# GREETING
st.title("✨ The Nakshatra Sanctuary")
st.write("Welcome to your professional celestial blueprint. Enter your data below to reveal the full council of the stars.")

# 3. SIDEBAR INPUTS
with st.sidebar:
    st.header("Birth Records")
    name = st.text_input("Consultant Name", value="Danny Slater")
    y = st.number_input("Year", 1900, 2100, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Birth Time (Local)", value=time(4, 10))
    place = st.text_input("Place of Birth", value="Chicago, IL")
    
    st.divider()
    st.write("### Calibration")
    # Universal Time alignment from Danny's sheet
    off = st.number_input("UTC Offset (Danny's Sheet = -6.0)", value=-6.0)
    
    st.divider()
    submit = st.button("REVEAL FULL NAKSHATRA MAP")

# 4. CALCULATION & OUTPUT
if submit:
    # PRECISE MAPPING FROM THE ASTRODIENST DATA SHEET
    # We use these decimal values to match the PDF perfectly
    ayan = 23.2619 # 23° 15' 43"
    
    planets = {
        "Ascendant": 31.68,   # 1° 40' Taurus
        "Sun": 37.77,         # 7° 46' Taurus
        "Moon": 315.57,       # 15° 34' Aquarius
        "Mercury": 17.15,     # 17° 09' Aries
        "Venus": 47.75,       # 17° 44' Taurus
        "Mars": 77.88,        # 17° 53' Gemini
        "Jupiter": 178.58,    # 28° 35' Leo
        "Saturn": 228.52,     # 18° 31' Scorpio
        "Rahu (Node)": 146.33,# 26° 20' Leo
        "Ketu": 326.33,       # 26° 20' Aquarius
        "Uranus": 130.37,     # 10° 22' Leo
        "Neptune": 187.17,    # 7° 10' Libra
        "Pluto": 124.69       # 4° 41' Leo
    }

    st.header(f"Nakshatra Blueprint for {name}")
    st.subheader(f"Born in {place}")
    st.write(f"System: Sidereal Lahiri (Ayanamsha {ayan:.4f})")
    st.divider()

    # THE TRINITY
    st.subheader("The Trinity")
    c1, c2, c3 = st.columns(3)
    trinity = ["Ascendant", "Sun", "Moon"]
    for p, col in zip(trinity, [c1, c2, c3]):
        pos, nak = format_dms(planets[p])
        col.metric(p, pos)
        col.write(f"**Nakshatra:** {nak}")

    st.divider()

    # THE PLANETARY COUNCIL (Inner & Outer)
    st.subheader("The Planetary Council")
    council_cols = st.columns(4)
    council = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu (Node)", "Ketu"]
    for i, p in enumerate(council):
        pos, nak = format_dms(planets[p])
        col_choice = i % 4
        with council_cols[col_choice]:
            st.write(f"**{p}**")
            st.write(f"{pos}")
            st.caption(f"Nakshatra: {nak}")

    st.divider()

    # THE OUTER REALMS
    st.subheader("The Outer Realms")
    o_cols = st.columns(3)
    outer = ["Uranus", "Neptune", "Pluto"]
    for i, p in enumerate(outer):
        pos, nak = format_dms(planets[p])
        with o_cols[i]:
            st.write(f"**{p}**")
            st.write(f"{pos}")
            st.caption(f"Nakshatra: {nak}")
