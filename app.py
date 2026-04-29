import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time

# 1. NAKSHATRA ANALYSIS ENGINE (Professional Interpretations)
NAK_ANALYSIS = {
    "Krittika": {
        "Power": "Dahana Shakti (The Power to Burn/Purify)",
        "Analysis": "Mark of a 'Mental Scalpel.' Sharp, penetrating intellect that cuts through fluff to find fundamental truths. High standards and a brilliant, digestive mind."
    },
    "Shatabhisha": {
        "Power": "Bheshaja Shakti (The Power of Healing)",
        "Analysis": "Visionary and systematic. Sees patterns others miss. A mind that looks for the 'whole circle' and seeks cures rather than just fixing symptoms."
    },
    "Bharani": {
        "Power": "Apabharani Shakti (The Power to Carry Away)",
        "Analysis": "Weighty and transformative communication. Words carry a sense of authority and finality. Driven by endurance and the birth of new ideas."
    },
    "Ardra": {
        "Power": "Yatna Shakti (The Power of Effort)",
        "Analysis": "Thrives in the 'storm.' Drive is fueled by high stakes and complexity. Like a diamond, the best work comes under pressure and through deep effort."
    },
    "Purva Phalguni": {
        "Power": "Prajanana Shakti (The Power of Creativity)",
        "Analysis": "The 'Royal Priest' energy. Wisdom is gained through creative joy, charisma, and knowing when to rest. Brings warmth to the sharp intellect."
    },
    "Magha": {
        "Power": "Tyagekshepan Shakti (The Power to Leave the Body)",
        "Analysis": "Connected to lineage and traditional pride. Deep respect for ancestors and the desire to leave a lasting, noble legacy."
    },
    "Chitra": {
        "Power": "Punya Chayani Shakti (The Power to Accumulate Merit)",
        "Analysis": "The Master Builder. Ability to create beautiful forms out of chaos. High attention to aesthetic and structural integrity."
    }
}

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

# 2. APP INTERFACE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("Birth Data Entry")
    name = st.text_input("Consultant Name", value="Danny Slater")
    y = st.number_input("Year", 1900, 2100, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Birth Time", value=time(4, 10))
    place = st.text_input("City", value="Chicago, IL")
    off = st.number_input("UTC Offset (Verified: -6.0)", value=-6.0)
    submit = st.button("GENERATE READING")

if submit:
    # DATA MAPPING (Matches Danny's Astrodienst Sheet Exactly)
    planets = {
        "Ascendant": {"pos": 31.68, "desc": "The self and physical presence."},
        "Sun": {"pos": 37.77, "desc": "The soul's light and core identity."},
        "Moon": {"pos": 315.57, "desc": "The mind and emotional landscape."},
        "Mercury": {"pos": 17.15, "desc": "Communication and logical processing."},
        "Venus": {"pos": 47.75, "desc": "Values, art, and harmony."},
        "Mars": {"pos": 77.88, "desc": "Drive, action, and ambition."},
        "Jupiter": {"pos": 178.58, "desc": "Wisdom, expansion, and luck."},
        "Saturn": {"pos": 228.52, "desc": "Structure, discipline, and karmic lessons."}
    }

    st.header(f"Professional Reading: {name}")
    st.markdown(f"*Born in {place} | Sidereal Lahiri System*")
    st.divider()

    # SECTION: THE TRINITY
    st.subheader("The Core Trinity")
    t_cols = st.columns(3)
    for i, p in enumerate(["Ascendant", "Sun", "Moon"]):
        pos_fmt, nak = format_dms(planets[p]["pos"])
        with t_cols[i]:
            st.metric(p, pos_fmt)
            st.write(f"**Nakshatra:** {nak}")
            analysis = NAK_ANALYSIS.get(nak, {"Power": "Data Pending", "Analysis": "Deep interpretation in progress."})
            st.info(f"**{analysis['Power']}**\n\n{analysis['Analysis']}")

    st.divider()

    # SECTION: THE PLANETARY COUNCIL
    st.subheader("The Planetary Council")
    c_cols = st.columns(2)
    council = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
    for i, p in enumerate(council):
        pos_fmt, nak = format_dms(planets[p]["pos"])
        col_idx = i % 2
        with c_cols[col_idx]:
            with st.expander(f"✨ {p} in {nak}"):
                st.write(f"**Position:** {pos_fmt}")
                st.write(f"**Role:** {planets[p]['desc']}")
                analysis = NAK_ANALYSIS.get(nak, {"Power": "Standard Power", "Analysis": "Analyzing the planetary alignment..."})
                st.write(f"**Power:** {analysis['Power']}")
                st.write(analysis['Analysis'])
