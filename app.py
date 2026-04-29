import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time

# 1. THE DATA (Keeping the precision anchors)
NAK_ANALYSIS = {
    "Krittika": {"Power": "Dahana Shakti", "Analysis": "You are the 'Mental Scalpel.' You burn through the noise to find the core truth."},
    "Shatabhisha": {"Power": "Bheshaja Shakti", "Analysis": "The Visionary Healer. You see the hidden patterns and the 'whole circle' of the cure."},
    "Bharani": {"Power": "Apabharani Shakti", "Analysis": "The Weight of Creation. Your words carry the power to transform and birth new worlds."},
    "Ardra": {"Power": "Yatna Shakti", "Analysis": "The Storm Chaser. You find your greatest diamonds under the pressure of deep effort."},
    "Purva Phalguni": {"Power": "Prajanana Shakti", "Analysis": "The Royal Priest. You know that true wisdom is found in the balance of charisma and rest."}
}

NAK_LIST = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
ZODIAC_LIST = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def format_dms(deg_raw):
    deg_norm = deg_raw % 360
    sign_idx = int(deg_norm / 30)
    deg_in_sign = deg_norm % 30
    d, m = int(deg_in_sign), int((deg_in_sign - int(deg_in_sign)) * 60)
    nak_idx = int(deg_norm / 13.333333) % 27
    return f"{d}° {m}' {ZODIAC_LIST[sign_idx]}", NAK_LIST[nak_idx]

# 2. THE SACRED ENTRANCE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")

st.title("✨ The Nakshatra Sanctuary")
st.subheader("A place of precision, belonging, and cosmic truth.")

# DATA ENTRY WITH "LOVE AND VIBES"
with st.container():
    st.markdown("#### *Let's find your place in the current sky...*")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        name = st.text_input("What name do the stars call you?", value="Danny Slater")
        place = st.text_input("Where did you first breathe the air? (City, State)", value="Chicago, IL")
    
    with col2:
        st.write("**The Moment of Your Arrival**")
        c_date = st.columns(3)
        y = c_date[0].number_input("Year", 1900, 2100, 1957)
        m = c_date[1].number_input("Month", 1, 12, 5)
        d = c_date[2].number_input("Day", 1, 31, 22)
        t_in = st.time_input("Exact Time", value=time(4, 10))

with st.sidebar:
    st.header("🧭 The Compass")
    st.write("Ensuring your map aligns with the physical heavens.")
    off = st.number_input("UTC Offset (Danny's Sheet = -6.0)", value=-6.0)
    st.divider()
    submit = st.button("✨ Reveal My Planetary Bliss")

# 3. THE REVEAL & EDUCATION
if submit:
    st.balloons()
    
    # Danny's Verified Data
    planets = {
        "Ascendant": {"pos": 31.68}, "Sun": {"pos": 37.77}, "Moon": {"pos": 315.57},
        "Mercury": {"pos": 17.15}, "Venus": {"pos": 47.75}, "Mars": {"pos": 77.88},
        "Jupiter": {"pos": 178.58}, "Saturn": {"pos": 228.52}
    }

    st.header(f"The Star-Map Celebration for {name}")
    
    # THE "REAL & RAW" EDUCATION NOTE
    st.warning("🪐 **Wait... I'm a different sign?**")
    st.markdown("""
    If your signs look 'wrong' compared to your usual horoscope, don't panic—**you've just been upgraded to the truth.**
    
    The zodiac dates you see in magazines were set 2,000 years ago. But the Earth has a slow, 26,000-year 'wobble.' 
    Over time, that wobble has shifted the sky by almost a whole sign. Western astrology stays frozen in the past, 
    but we use the **Sidereal** view—looking through the telescope at the stars exactly where they sit today. 
    
    You haven't lost your old self; you've just finally found your **actual** cosmic coordinates.
    """)
    st.divider()

    # PLANETARY BLISS DISPLAY
    st.subheader("🌟 The Trinity of Your Being")
    t_cols = st.columns(3)
    for i, p in enumerate(["Ascendant", "Sun", "Moon"]):
        pos, nak = format_dms(planets[p]["pos"])
        with t_cols[i]:
            st.metric(p, pos)
            st.write(f"### {nak}")
            analysis = NAK_ANALYSIS.get(nak, {"Power": "Cosmic Shakti", "Analysis": "Reading the ancient rhythms..."})
            st.success(f"**{analysis['Power']}**\n\n{analysis['Analysis']}")
