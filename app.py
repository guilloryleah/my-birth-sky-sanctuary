import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# 1. SANCTUARY CONFIG
st.set_page_config(page_title="The Nakshatra Sanctuary", page_icon="✨", layout="wide")

# 2. THE NAKSHATRA KNOWLEDGE BASE (Pure Shakti)
NAK_DATA = {
    "Ashwini": "Power to Reach Quickly (Shidhra Shakti). Healing and swiftness.",
    "Bharani": "Power to Carry Away (Apabharani Shakti). Transformation and endurance.",
    "Krittika": "Power to Burn (Dahana Shakti). Purification and sharp brilliance.",
    "Rohini": "Power of Growth (Prabhava Shakti). Nurturing and manifestation.",
    "Mrigashira": "Power of Fulfillment (Prinana Shakti). The seeker's restless search.",
    "Ardra": "Power of Effort (Yatna Shakti). Clarity through the storm.",
    "Punarvasu": "Power of Renewal (Vasutva Shakti). Return of light and resources.",
    "Pushya": "Power of Spiritual Energy (Brahmavarchasa Shakti). Nourishment.",
    "Ashlesha": "Power to Inflict Poison (Vishasleshana Shakti). Insight into shadow.",
    "Magha": "Power of Lineage (Tyage Shepan Shakti). Ancestral nobility.",
    "Purva Phalguni": "Power of Procreation (Prajanana Shakti). Creative charm.",
    "Uttara Phalguni": "Power of Giving (Chayani Shakti). Prosperity through alliance.",
    "Hasta": "Power to Manifest (Hasta Shakti). Putting the world in your hands.",
    "Chitra": "Power of Merit (Punya Chayani Shakti). Creating form from chaos.",
    "Swati": "Power to Scatter like the Wind (Pradhvamsana Shakti). Freedom.",
    "Vishakha": "Power of Achievement (Vyapana Shakti). Focused success.",
    "Anuradha": "Power of Worship (Radhana Shakti). Balance and devotion.",
    "Jyeshtha": "Power to Rise Above (Tarana Shakti). Courage and seniority.",
    "Mula": "Power to Uproot (Barhana Shakti). Breaking illusions at the root.",
    "Purva Ashadha": "Power of Invigoration (Varchograhana Shakti). Vitality.",
    "Uttara Ashadha": "Power of Victory (Apradhrisya Shakti). Unstoppable success.",
    "Shravana": "Power of Connection (Samhanana Shakti). Listening to the rhythm.",
    "Dhanishta": "Power of Abundance (Sansiddha Shakti). Fame and wealth.",
    "Shatabhisha": "Power of Healing (Bheshaja Shakti). Seeing the 100 physicians.",
    "Purva Bhadrapada": "Power of Fire (Yajamana Shakti). Spiritual evolution.",
    "Uttara Bhadrapada": "Power of Rain (Varshograhana Shakti). Stability and deep peace.",
    "Revati": "Power of Nourishment (Kshiradyani Shakti). Safety
