from flask import Flask, render_template, request
import swisseph as swe
import pytz
from datetime import datetime

app = Flask(__name__)

# --- 1. THE WISDOM LIBRARY ---
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
    # Essential: This tells the engine where the NASA data lives
    swe.set_ephe_path('./ephe') 

    # Handle Time Integrity (Navigating the 1957 Chicago 'Ghosts')
    local_tz = pytz.timezone(tzone_str)
    local_dt = local_tz.localize(datetime(year, month, day, hour, minute))
    utc_dt = local_dt.astimezone(pytz.utc)
    
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                    utc_dt.hour + utc_dt.minute/60.0)

    # Set to Sidereal/Lahiri Mode (The Real-Sky Bridge)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    def calc_obj(obj_id):
        res, _ = swe.calc_ut(jd, obj_id, flags)
        deg = res[0]
        return {
            "Sign": ZODIAC_SIGNS[int(deg / 30)],
            "Nakshatra": NAKSHATRAS[int(deg / (360/27))],
            "Position": f"{round(deg % 30, 2)}°"
        }

    # Calculate Ascendant (Topocentric accuracy)
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
    asc_deg = ascmc[0]
    
    return {
        "Ascendant": {
            "Sign": ZODIAC_SIGNS[int(asc_deg/30)],
            "Nakshatra": NAKSHATRAS[int(asc_deg/(360/27))],
            "Position": f"{round(asc_deg % 30, 2)}°"
        },
        "Sun": calc_obj(swe.SUN),
        "Moon": calc_obj(swe.MOON),
        "Mercury": calc_obj(swe.MERCURY),
        "Rahu": calc_obj(swe.MEAN_NODE)
    }

# --- 3. THE WEB ROUTES (The Bridge) ---
@app.route('/')
def home():
    # This renders your main page
    return "<h1>Sanctuary is Live</h1><p>Engine is ready for your input.</p>"

@app.route('/calculate')
def calculate():
    # Example route for testing: /calculate?year=1957&month=5&day=10&hour=12&min=0&lat=41.87&lon=-87.62&tz=America/Chicago
    try:
        y = int(request.args.get('year'))
        m = int(request.args.get('month'))
        d = int(request.args.get('day'))
        h = int(request.args.get('hour'))
        mi = int(request.args.get('min'))
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        tz = request.args.get('tz')
        
        report = get_real_sky_report(y, m, d, h, mi, lat, lon, tz)
        return report
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
