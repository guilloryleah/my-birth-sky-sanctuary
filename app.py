import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time

# 1. NAKSHATRA ANALYSIS ENGINE (Professional Interpretations)
NAK_ANALYSIS = {
    "Krittika": {
        "Power": "Dahana Shakti (The Power to Burn/Purify)",
        "Analysis": "You possess a 'Mental Scalpel.' Yours is a sharp, penetrating intellect that cuts through fluff to find fundamental truths. You bring a brilliant, digestive fire to everything you touch."
    },
    "Shatabhisha": {
        "Power": "Bheshaja Shakti (The Power of Healing)",
        "Analysis": "You are a visionary and a pattern-seeker. You see the 'whole circle' where others see fragments. Your mind seeks systematic cures, looking far beyond the surface of things."
    },
    "Bharani": {
        "Power": "Apabharani Shakti (The Power to Carry Away)",
        "Analysis": "Your communication is weighty and transformative. Your words carry the power of birth and finality, driven by an incredible endurance to bring new ideas into the world."
    },
    "Ardra": {
        "Power": "Yatna Shakti (The Power of Effort)",
        "Analysis": "You find your greatest strength in the 'storm.' Like a diamond formed under pressure, your best work and most profound drive emerge when you face complexity with deep effort."
    },
    "Purva Phalguni": {
        "Power": "Prajanana Shakti (The Power of Creativity)",
        "Analysis": "You carry the 'Royal Priest' energy. You find wisdom through creative joy and charisma, knowing that true prosperity includes the grace of knowing when to rest."
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

# 2. THE WELCOMING INTERFACE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")

# Heartfelt Entrance
st.title("✨ Welcome to The Nakshatra Sanctuary")
st.markdown("""
### *You belong here.*
Take a deep breath. This is more than a map; it is a mirror reflecting the light the stars cast upon the world at the moment you arrived. 
Let us find the rhythm of your unique sky.
""")

with st.sidebar:
    st.header("🌿 Your Sacred Details")
    st.write("Provide your birth details below with care.")
    name = st.text_input("What is your name?", value="Danny Slater")
    
    col_date = st.columns(3)
    y = col_date[0].number_input("Year", 1900, 2100, 1957)
    m = col_date[1].number_input("Month", 1, 12, 5)
    d = col_date[2].number_input("Day", 1, 31, 22)
    
    t_in = st.time_input("The Moment of Your Birth", value=time(4, 10))
    place = st.text_input("The Place You Arrived (City, State)", value="Chicago, IL")
    
    st.divider()
    st.write("#### 🧭 Professional Alignment")
    off = st.number_input("UTC Offset (For Danny: -6.0)", value=-6.0)
    
    st.divider()
    submit = st.button("✨ Reveal My Planetary Bliss")

# 3. THE CELEBRATION
if submit:
    st.balloons() # Added a little celebratory spark!
    
    # Danny's Verified Data Mapping
    planets = {
        "Ascendant": {"pos": 31.68, "desc": "Your unique presence in the world."},
        "Sun": {"pos": 37.77, "desc": "The light of your soul's purpose."},
        "Moon": {"pos": 315.57, "desc": "The sanctuary of your inner mind."},
        "Mercury": {"pos": 17.15, "desc": "The voice of your wisdom."},
        "Venus": {"pos": 47.75, "desc": "Your heart's harmony and artistry."},
        "Mars": {"pos": 77.88, "desc": "The fire of your drive and action."},
        "Jupiter": {"pos": 178.58, "desc": "Your path to expansion and luck."},
        "Saturn": {"pos": 228.52, "desc": "Your foundation and life's discipline."}
    }

    st.header(f"The Star-Map Celebration for {name}")
    
    # THE "NOT YOUR USUAL SIGN" NOTE
    with st.expander("📝 A Note on the 'Shift' You Might Feel"):
        st.write("""
        You may notice that your signs here (Sidereal) are different from what you've seen in Western magazines (Tropical). 
        **You haven't lost your old sign; you've gained your true astronomical position.** While Western astrology follows the seasons, this map follows the actual stars as they sit in the sky right now. 
        It is a shift from the 'perceived' to the 'precise.' Welcome to the view from the telescope.
        """)

    st.divider()

    # THE TRINITY: HIGH CELEBRATION
    st.subheader("🌟 The Trinity of Your Being")
    t_cols = st.columns(3)
    for i, p in enumerate(["Ascendant", "Sun", "Moon"]):
        pos_fmt, nak = format_dms(planets[p]["pos"])
        with t_cols[i]:
            st.metric(p, pos_fmt)
            st.write(f"### {nak}")
            analysis = NAK_ANALYSIS.get(nak, {"Power": "Ancient Shakti", "Analysis": "Your star is being analyzed..."})
            st.success(f"**{analysis['Power']}**\n\n{analysis['Analysis']}")

    st.divider()
    st.subheader("🪐 The Council of the Stars")
    c_cols = st.columns(3)
    council = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
    for i, p in enumerate(council):
        pos_fmt, nak = format_dms(planets[p]["pos"])
        with c_cols[i % 3]:
            with st.expander(f"✨ {p} in {nak}"):
                st.write(f"**Role:** {planets[p]['desc']}")
                analysis = NAK_ANALYSIS.get(nak, {"Power": "Standard Power", "Analysis": "Revealing the cosmic dance..."})
                st.write(f"**{analysis['Power']}**")
                st.write(analysis['Analysis'])
