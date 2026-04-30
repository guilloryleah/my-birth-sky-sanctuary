import swisseph as swe
import pytz
from datetime import datetime

# --- 1. THE FOUNDATION: Loading the NASA Data ---
# You must have the ephemeris files (like de431.bsp) in a folder named 'ephe'
# This is the 'Atlas' the engine uses to find the planets.
swe.set_ephe_path('./ephe') 

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

# --- 2. THE CALCULATION LOGIC ---
def get_real_sky_report(year, month, day, hour, minute, lat, lon, tzone_str):
    try:
        # Time Integrity (Handling 1957 Chicago DST)
        local_tz = pytz.timezone(tzone_str)
        local_dt = local_tz.localize(datetime(year, month, day, hour, minute))
        utc_dt = local_dt.astimezone(pytz.utc)
        
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                        utc_dt.hour + utc_dt.minute/60.0)

        # Sidereal/Lahiri Setting (The 'Real-Sky' Bridge)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

        # Helper for individual planets
        def calc_obj(obj_id):
            res, _ = swe.calc_ut(jd, obj_id, flags)
            deg = res[0]
            return {
                "Sign": ZODIAC_SIGNS[int(deg / 30)],
                "Nakshatra": NAKSHATRAS[int(deg / (360/27))],
                "Position": f"{round(deg % 30, 2)}°"
            }

        # Calculate Ascendant (Danny's 1° Taurus Foundation)
        houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
        
        # Build the final 'Truth Receipt'
        report = {
            "Ascendant": f"{round(ascmc[0] % 30, 2)}° {ZODIAC_SIGNS[int(ascmc[0]/30)]}",
            "Sun": calc_obj(swe.SUN),
            "Moon": calc_obj(swe.MOON),
            "Rahu": calc_obj(swe.MEAN_NODE)
        }

        # KETU INTEGRITY (The 180° Rule)
        rahu_deg, _ = swe.calc_ut(jd, swe.MEAN_NODE, flags)
        ketu_raw = (rahu_deg[0] + 180) % 360
        report["Ketu"] = {
            "Sign": ZODIAC_SIGNS[int(ketu_raw / 30)],
            "Nakshatra": NAKSHATRAS[int(ketu_raw / (360/27))],
            "Position": f"{round(ketu_raw % 30, 2)}°"
        }

        return report

    except Exception as e:
        return f"Engine Error: {e}"

# --- 3. THE LIVE TEST ---
# Testing Danny's birth data (May 10, 1957, Chicago)
# Latitude: 41.87, Longitude: -87.62
print(get_real_sky_report(1957, 5, 10, 12, 0, 41.87, -87.62, "America/Chicago"))
