import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time

# 1. THE DEEP ALIGNMENT DATA (Analysis, Ayurveda, & Rituals)
NAK_ALIGNMENT = {
    "Krittika": {
        "Power": "Dahana Shakti (The Power to Burn/Purify)",
        "Analysis": "You are the 'Mental Scalpel.' You possess a sharp, penetrating intellect that cuts through fluff to find the core truth.",
        "Dosha": "Pitta (Fire). Needs cooling to avoid burnout.",
        "Nourishment": "Cooling foods: Coconut, cucumber, sweet fruits, and mint. Avoid excessive heat/spice.",
        "Scent": "Sandalwood or Rose to soften your razor-sharp edge.",
        "Ritual": "Trataka (Candle gazing) to focus your vision or Sitali Pranayama (cooling breath)."
    },
    "Shatabhisha": {
        "Power": "Bheshaja Shakti (The Power to Heal)",
        "Analysis": "The Visionary Healer. You see patterns others miss and look for the 'whole circle' of the cure.",
        "Dosha": "Vata (Air/Ether). Needs grounding and warm stability.",
        "Nourishment": "Warm, oily, cooked foods. Root vegetables, ginger, and grounding herbal teas.",
        "Scent": "Frankincense, Cedarwood, or Vetiver for grounding the mind.",
        "Ritual": "Abhyanga (Warm oil massage) and intentional silence to process your deep thoughts."
    },
    "Bharani": {
        "Power": "Apabharani Shakti (The Power to Carry Away)",
        "Analysis": "The Weight of Creation. Your words carry the power to transform and birth new realities.",
        "Dosha": "Pitta/Kapha balance. Needs movement and healthy release.",
        "Nourishment": "Fiber-rich foods, bitter greens, and detoxifying broths.",
        "Scent": "Jasmine or Lotus for transformative grace.",
        "Ritual": "Journaling to 'offload' heavy thoughts and Yin Yoga for deep release."
    },
    "Ardra": {
        "Power": "Yatna Shakti (The Power of Effort)",
        "Analysis": "The Storm Chaser. Like a diamond formed under pressure, your best work comes during deep effort.",
        "Dosha": "Vata/Pitta. Needs emotional release and physical stability.",
        "Nourishment": "Hydrating foods, melons, and sea salt to maintain electrolyte balance.",
        "Scent": "Eucalyptus or Peppermint to clear the storm clouds.",
        "Ritual": "Vigorous movement (Tandava style) followed by 10 minutes of complete stillness."
    },
    "Purva Phalguni": {
        "Power": "Prajanana Shakti (The Power of Creativity)",
        "Analysis": "The Royal Priest. You know that true wisdom is found in the balance of charisma and rest.",
        "Dosha": "Kapha. Needs stimulation, warmth, and play.",
        "Nourishment": "Light, spicy, and colorful foods. Berries, ginger, and honey.",
        "Scent": "Ylang-Ylang or Sweet Orange for creative joy.",
        "Ritual": "Creative expression (dance/art) and 'Divine Rest'—naps with intention."
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

# 2. THE WELCOMING INTERFACE
st.set_page_config(page_title="The Nakshatra Sanctuary", layout="wide")

st.title("✨ The Nakshatra Sanctuary")
st.markdown("### *You belong here. Let's find your place in the real sky.*")

with st.container():
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("What name do the stars call you?", value="Danny Slater")
        place = st.text_input("Where did you first breathe the air?", value="Chicago, IL")
    with col2:
        st.write("**The Moment of Your Arrival**")
        c_date = st.columns(3)
        y = c_date[0].number_input("Year", 1900, 2100, 1957)
        m = c_date[1].number_input("Month", 1, 12, 5)
        d = c_date[2].number_input("Day", 1, 31, 22)
        t_in = st.time_input("Exact Time", value=time(4, 10))

with st.sidebar:
    st.header("🧭 The Compass")
    off = st.number_input("UTC Offset (Danny's Sheet = -6.0)", value=-6.0)
    st.divider()
    submit = st.button("✨ Reveal My Planetary Bliss")

# 3. THE REVEAL
if submit:
    st.balloons()
    
    # DATA MAPPING (Danny's Sheet)
    planets = {
        "Ascendant": 31.68, "Sun": 37.77, "Moon": 315.57,
        "Mercury": 17.15, "Venus": 47.75, "Mars": 77.88,
        "Jupiter": 178.58, "Saturn": 228.52, "Rahu": 146.33, "Ketu": 326.33
    }

    st.header(f"The Star-Map Celebration for {name}")

    # RESTORED RAW & WONDERFUL SCRIPT
    st.info("🪐 **Wait... I’m a WHAT now?**")
    st.markdown("""
    We get it. Seeing a new sign in your mirror can feel like a cosmic plot twist. But here’s the real, raw truth: 
    The zodiac dates you see in magazines were locked in about 2,000 years ago. Back then, the Sun really *was* in those signs on those dates. 
    
    But the Earth has a beautiful, slow 'wobble' (like a spinning top that’s just starting to lean). Over two millennia, 
    that wobble has shifted our view of the stars by about **24 degrees**. 
    
    While Western astrology stays frozen in a 2,000-year-old calendar, **The Nakshatra Sanctuary** looks through a modern telescope. 
    We follow the sky as it actually exists *right now*. You haven't changed—the sky did. You’re just finally seeing the 
    precise stars that were actually cheering for you the moment you arrived. **Welcome to the real sky.**
    """)
    st.divider()

    # THE TRINITY ALIGNMENT
    st.subheader("🌟 The Trinity of Your Being")
    t_cols = st.columns(3)
    for i, p in enumerate(["Ascendant", "Sun", "Moon"]):
        pos, nak = format_dms(planets[p])
        align = NAK_ALIGNMENT.get(nak, {"Power": "Ancient Shakti", "Analysis": "Deepening...", "Dosha": "Balance", "Nourishment": "Whole foods", "Scent": "Natural essence", "Ritual": "Presence"})
        with t_cols[i]:
            st.metric(p, pos)
            st.write(f"### {nak}")
            st.info(f"**{align['Power']}**\n\n{align['Analysis']}")
            st.success(f"**🌿 Wellbeing Alignment**\n\n* **Dosha:** {align['Dosha']}\n* **Nourishment:** {align['Nourishment']}\n* **Scent:** {align['Scent']}\n* **Ritual:** {align['Ritual']}")

    st.divider()

    # THE FULL COUNCIL
    st.subheader("🪐 The Planetary Council")
    council_cols = st.columns(4)
    council = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]
    for i, p in enumerate(council):
        pos, nak = format_dms(planets[p])
        align = NAK_ALIGNMENT.get(nak, {"Power": "Planetary Power", "Analysis": "Reading the stars...", "Dosha": "Balance", "Nourishment": "Vibrant foods", "Scent": "Earth essence", "Ritual": "Mindfulness"})
        with council_cols[i % 4]:
            with st.expander(f"✨ {p} in {nak}"):
                st.write(f"**{pos}**")
                st.write(f"**{align['Power']}**")
                st.write(align['Analysis'])
                st.caption(f"Suggested Ritual: {align['Ritual']}")
