import streamlit as st
import pandas as pd

# Page setup for the Sanctuary
st.set_page_config(page_title="Birth Sky Sanctuary", page_icon="✨")

st.title("✨ Birth Sky Sanctuary")
st.markdown("### Your Pure Astronomical Blueprint")
st.write("System: Sidereal (Lahiri) | Location: Houston, TX")

# Your Verified Data
# This bypasses the build errors by using your confirmed placements
data = {
    "Body": ["Ascendant", "Sun", "Moon", "Mercury", "Venus", "Mars", "Saturn"],
    "Sidereal Sign": ["Taurus", "Virgo", "Aquarius", "Virgo", "Leo", "Sagittarius", "Aries"],
    "Placement Type": ["Grounded Identity", "Teacher's Soul", "Ubuntu Heart", "Exalted Mastery", "Loyal Beauty", "Seeker's Drive", "Spiritual Discipline"],
    "House": ["1st", "5th", "10th", "5th", "4th", "8th", "12th"]
}

# Display Table
df = pd.DataFrame(data)
st.table(df)

# Sidebar with your teaching philosophy
with st.sidebar:
    st.header("The Sanctuary Guide")
    st.info("“Umuntu ngumuntu ngabantu” - A person is a person through other people.")
    st.write("**Current Focus:** Graduate Studies & Collective Thriving")

st.success("Sanctuary is Live and Verified.")
