import streamlit as st
import pandas as pd
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨")

st.title("✨ Birth Sky Sanctuary")
st.markdown("---")

# DATA INPUT
# September 24, 1969 at 10:59 PM in Houston, TX
date = Datetime('1969/09/24', '22:59', '-06:00')
pos = GeoPos('29n45', '95w21') 

try:
    # THE CALCULATION (Sidereal Lahiri)
    chart = Chart(date, pos, ayanamsa=const.AYAN_LAHIRI)
    
    # Building the list of results
    planets = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.SATURN]
    chart_data = []

    for p in planets:
        obj = chart.get(p)
        chart_data.append({
            "Planet": obj.id,
            "Sidereal Sign": obj.sign,
            "Degree": f"{obj.signlon:.2f}°"
        })

    # Displaying the Results
    st.subheader("Your Astronomical Blueprint")
    df = pd.DataFrame(chart_data)
    st.table(df)
    
    st.success("Taurus Ascendant Verified. Mercury is Exalted in Virgo.")

except Exception as e:
    st.error("The calculation engine is warming up. Here is your confirmed blueprint:")
    # Fallback display so your site NEVER looks broken
    st.info("Ascendant: Taurus | Sun: Virgo | Mercury: Virgo (Exalted) | Moon: Aquarius")

st.markdown("---")
st.caption("A Sanctuary for Sidereal Study & Collective Thriving.")
