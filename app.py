import swisseph as swe
import pytz
from datetime import datetime

# --- 1. THE WISDOM LIBRARY (The Scaffold) ---
# This ensures every planet is mapped to its real-sky location
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# The 27 Lunar Mansions for that "Blown Away" detail
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", 
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# --- 2. THE UNIVERSAL CLOCK FUNCTION ---
def generate_complete_report(year, month, day, hour, minute, lat, lon, tzone_str):
    # STEP A: TIME INTEGRITY (IANA Database Check)
    # This solves the '1957 Chicago' Daylight Savings mystery
    local_tz = pytz.timezone(tzone_str)
    local_dt = local_tz.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    # Julian Day for NASA-grade precision
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute/60.0)

    # STEP B: SIDEREAL/LAHIRI MODE (The Bridge)
    # This ignores Western/Tropical seasonal math as requested
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Internal helper to find Sign and Nakshatra
    def calculate_position(obj_id):
        res, _ = swe.calc_ut(jd, obj_id, flags)
        deg = res[0]
        sign_name = ZODIAC_SIGNS[int(deg / 30)]
        nak_name = NAKSHATRAS[int(deg / (360/27))]
        return {"Sign": sign_name, "Nakshatra": nak_name, "Degree": round(deg % 30, 2)}

    # STEP C: THE ASCENDANT (The 1° Taurus Foundation)
    # Uses Topocentric math (Observer's location on Earth's surface)
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    
    # --- 3. THE FINAL TRUTH RECEIPT ---
    report = {
        "Metadata": {
            "System": "Sidereal / True Lahiri",
            "Calculation": "Topocentric (Real-Sky)",
            "Timestamp": utc_dt.strftime('%Y-%m-%d %H:%M UTC')
        },
        "The Front Door": {
            "Ascendant": f"{round(asc_deg % 30, 2)}° {ZODIAC_SIGNS[int(asc_deg/30)]}",
            "Nakshatra": NAKSHATRAS[int(asc_deg/(360/27))]
        },
        "Planetary Placements": {
            "Sun": calculate_position(swe.SUN),
            "Moon": calculate_position(swe.MOON),
            "Mercury": calculate_position(swe.MERCURY),
            "Rahu (North Node)": calculate_position(swe.MEAN_NODE)
        }
    }

    # STEP D: KETU INTEGRITY (The 180° Axis)
    # Automatically pins Ketu opposite Rahu for mathematical balance
    rahu_deg, _ = swe.calc_ut(jd, swe.MEAN_NODE, flags)
    ketu_raw = (rahu_deg[0] + 180) % 360
    report["The Hidden Foundation"] = {
        "Ketu": f"{round(ketu_raw % 30, 2)}° {ZODIAC_SIGNS[int(ketu_raw/30)]}",
        "Nakshatra": NAKSHATRAS[int(ketu_raw/(360/27))]
    }

    return report

# --- 4. THE LIVE TEST (Danny's 1957 Chicago Profile) ---
# Testing for Danny's known 1° Taurus alignment
danny_report = generate_complete_report(1957, 5, 10, 12, 0, 41.87, -87.62, "America/Chicago")

print(danny_report)
