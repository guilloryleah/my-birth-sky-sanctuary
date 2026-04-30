import swisseph as swe
import pytz
from datetime import datetime

# --- 1. DATA DICTIONARIES (The Wisdom Library) ---
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# --- 2. THE CALCULATION ENGINE ---
def get_real_sky_report(year, month, day, hour, minute, lat, lon, tzone_str):
    # Essential for the engine to locate planetary data
    swe.set_ephe_path('./ephe') 

    # Handle Time Integrity (Navigating the 1957 Chicago 'Ghosts')
    local_tz = pytz.timezone(tzone_str)
    local_dt = local_tz.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    # Julian Day for high-level precision
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute/60.0)

    # Set to Sidereal/Lahiri Mode (The Real-Sky Bridge)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Helper function to find the Sign and Nakshatra for any planet
    def calc_obj(obj_id):
        res, _ = swe.calc_ut(jd, obj_id, flags)
        deg = res[0]
        return {
            "Sign": ZODIAC_SIGNS[int(deg / 30)],
            "Nakshatra": NAKSHATRAS[int(deg / (360/27))],
            "Position": f"{round(deg % 30, 2)}°"
        }

    # Calculate Ascendant (Danny's 1° Taurus Foundation)
    # Using Topocentric math for Earth-Surface accuracy
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    
    results = {
        "Ascendant": {
            "Sign": ZODIAC_SIGNS[int(asc_deg/30)],
            "Nakshatra": NAKSHATRAS[int(asc_deg/(360/27))],
            "Position": f"{round(asc_deg % 30, 2)}°"
        },
        "Sun": calc_obj(swe.SUN),
        "Moon": calc_obj(swe.MOON),
        "Mercury": calc_obj(swe.MERCURY),
        "Rahu (North Node)": calc_obj(swe.MEAN_NODE)
    }

    return results

# --- 3. THE LIVE TEST ---
# Testing Danny's Birth: May 10, 1957, Chicago
danny_data = get_real_sky_report(1957, 5, 10, 12, 0, 41.87, -87.62, "America/Chicago")

print("--- SANCTUARY TRUTH RECEIPT ---")
for planet, data in danny_data.items():
    print(f"{planet}: {data}")
