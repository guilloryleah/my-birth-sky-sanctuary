import streamlit as st
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨")

st.title("✨ Birth Sky Sanctuary")
st.markdown("### Your Pure Astronomical Blueprint (Sidereal/Lahiri)")

# 2. The Data Input
# Note: Ensure the Time and Date match your birth records.
# Coordinates are set for Houston, TX.
birth_date = '19XX/XX/XX'  # Replace with your YYYY/MM/DD
birth_time = 'HH:MM'        # Replace with your 24-hour time
utc_offset = '-06:00'      # Central Time

date = Datetime(birth_date, birth_time, utc_offset)
pos = GeoPos('29n45', '95w21') 

# 3. The Calculation Engine
# Using Lahiri Ayanamsa to keep Mercury in Virgo and Sun in Taurus.
chart = Chart(date, pos, ayanamsa=const.AYAN_LAHIRI)

# 4. Gathering the Placements
planets_to_show = [
    const.SUN, const.MOON, const.MERCURY, 
    const.VENUS, const.MARS, const.JUPITER, 
    const.SATURN
]

results = []
for p_id in planets_to_show:
    obj = chart.get(p_id)
    results.append({
        "Planet": obj.id,
        "Sidereal Sign": obj.sign,
        "Exact Degree": f"{obj.signlon:.2f}°"
    })

# 5. Visual Display
df = pd.DataFrame(results)

# Create a clean table in the dashboard
st.table(df)

# Sidebar for extra context
with st.sidebar:
    st.header("The Blueprint Guide")
    st.write("**Mercury in Virgo:** Exalted. Your superpower in communication and literature.")
    st.write("**Sun in Taurus:** Grounded, persistent, and values-driven.")
    st.write("**System:** Sidereal (Pure Astronomy)")

st.success("Dashboard loaded successfully from GitHub.")
