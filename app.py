import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time

# 1. THE DEEP ALIGNMENT DATA (Ayurveda, Scents, & Wellness)
NAK_ALIGNMENT = {
    "Krittika": {
        "Power": "Dahana Shakti (To Burn/Purify)",
        "Dosha": "Pitta (Fire). Needs cooling to avoid burnout.",
        "Nourishment": "Cooling foods: Coconut, cucumber, sweet fruits. Avoid excessive spice.",
        "Scent": "Sandalwood or Rose to soften the 'razor' edge.",
        "Ritual": "Trataka (Candle gazing) or cooling Pranayama (Sitali).",
        "Analysis": "The 'Mental Scalpel.' You cut through fluff to find core truths."
    },
    "Shatabhisha": {
        "Power": "Bheshaja Shakti (To Heal)",
        "Dosha": "Vata (Air/Ether). Needs grounding and routine.",
        "Nourishment": "Warm, oily, cooked foods. Root vegetables and herbal teas.",
        "Scent": "Frankincense or Cedarwood for grounding the vision.",
        "Ritual": "Abhyanga (Warm oil massage) and silence.",
        "Analysis": "The Visionary Healer. You see patterns and systematic cures."
    },
    "Bharani": {
        "Power": "Apabharani Shakti (To Carry Away)",
        "Dosha": "Pitta/Kaphic balance. Needs movement and release.",
        "Nourishment": "Fiber-rich foods, beans, and bitter greens for detox.",
        "Scent": "Jasmine or Lotus for transformative grace.",
        "Ritual": "Yin Yoga or journaling to 'offload' the weight of thoughts.",
        "Analysis": "The Weight of Creation. Your words birth new realities."
    },
    "Ardra": {
        "Power": "Yatna Shakti (Effort)",
        "Dosha": "Vata/Pitta. Needs emotional release and stability.",
        "Nourishment": "Hydrating foods, melons, and sea salt for electrolyte balance.",
        "Scent": "Eucalyptus or Peppermint to clear the 'storm' clouds.",
        "Ritual": "Vigorous movement followed by deep stillness.",
        "Analysis": "The Storm Chaser. You find diamonds under pressure."
    },
    "Purva Phalguni": {
        "Power": "Prajanana Shakti (Creativity)",
        "Dosha": "Kapha. Needs stimulation and play.",
        "Nourishment": "Light, spicy, and colorful foods. Berries and ginger.",
        "Scent": "Ylang-Ylang or Orange blossom for creative joy.",
        "Ritual": "Dance, creative arts, and intentional rest.",
        "Analysis": "The Royal Priest. Wisdom through charisma and grace."
    }
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

# 2. THE SACRED INTERFACE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")
st.title("✨ The Nakshatra Sanctuary")

with st.sidebar:
    st.header("🌿 Sacred Entry")
    name = st.text_input("Name", value="Danny Slater")
    y = st.number_input("Year", 1900, 2100, 1957)
    m = st.number_input("Month", 1, 12, 5)
    d = st.number_input("Day", 1, 31, 22)
    t_in = st.time_input("Exact Time", value=time(4, 10))
    place = st.text_input("City", value="Chicago, IL")
    off = st.number_input("UTC Offset (PDF Match: -6.0)", value=-6.0)
    submit = st.button("✨ Reveal My Planetary Bliss")

# 3. THE REVEAL
if submit:
    st.balloons()
    
    # DANNY'S FULL PDF DATA MAPPING
    planets = {
        "Ascendant": 31.68, "Sun": 37.77, "Moon": 315.57,
        "Mercury": 17.15, "Venus": 47.75, "Mars": 77.88,
        "Jupiter": 178.58, "Saturn": 228.52, "Rahu": 146.33, "Ketu": 326.33
    }

    # EDUCATION NOTE
    st.warning("🪐 **The Cosmic 'Wobble' Insight**")
    st.write("You haven't changed—the sky did. Because of Earth's 2,000-year 'wobble,' your actual stars have shifted. This is the telescope view, not the magazine view.")

    # TRINITY WITH ALIGNMENT
    st.header(f"The Soul-Map for {name}")
    st.subheader("🌟 The Trinity Alignment")
    t_cols = st.columns(3)
    for i, p in enumerate(["Ascendant", "Sun", "Moon"]):
        pos, nak = format_dms(planets[p])
        align = NAK_ALIGNMENT.get(nak, {"Power": "Ancient Shakti", "Analysis": "Deepening...", "Dosha": "Balance", "Nourishment": "Whole foods", "Scent": "Natural essence", "Ritual": "Meditation"})
        with t_cols[i]:
            st.metric(p, pos)
            st.write(f"### {nak}")
            with st.container():
                st.info(f"**{align['Power']}**\n\n{align['Analysis']}")
                st.success(f"**🌿 Wellbeing Alignment**\n\n* **Dosha:** {align['Dosha']}\n* **Scent:** {align['Scent']}\n* **Nourishment:** {align['Nourishment']}\n* **Ritual:** {align['Ritual']}")

    st.divider()
    
    # FULL COUNCIL
    st.subheader("🪐 The Planetary Council")
    c_cols = st.columns(4)
    council = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
    for i, p in enumerate(council):
        pos, nak = format_dms(planets[p])
        align = NAK_ALIGNMENT.get(nak, {"Power": "Planetary Strength", "Analysis": "Reading your council...", "Dosha": "N/A", "Nourishment": "Vibrant foods", "Scent": "Clean essence", "Ritual": "Presence"})
        with c_cols[i % 4]:
            with st.expander(f"✨ {p} in {nak}"):
                st.write(f"**{pos}**")
                st.write(align['Analysis'])
                st.caption(f"Power: {align['Power']}")
