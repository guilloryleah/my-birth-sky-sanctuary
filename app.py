import streamlit as st
import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# --- THE SOUL MAP ENGINE ---
def calculate_soul_map(year, month, day, hour, minute, lat, lon):
    # 1. THE INVISIBLE WORLD CLOCK
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=lon, lat=lat)
    timezone = pytz.timezone(tz_name)
    local_dt = timezone.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)

    # 2. TOPOCENTRIC CALIBRATION (Standing on the ground)
    # This ensures we see the stars from Chicago, not the center of the Earth.
    swe.set_topo(lat, lon, 0) 
    
    # 3. REAL-SKY CONSTANT (True Lahiri)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    
    # 4. CALCUL
