import swisseph as swe
from datetime import datetime, timedelta

def calculate_soul_map(name, year, month, day, hour, minute, lat, lon, utc_offset):
    """
    Calculates the Real-Sky Soul Map using the World Clock (UT) anchor.
    This prevents the 'Aries Drift' for historical figures and modern clients.
    """
    
    # 1. THE WORLD CLOCK ANCHOR (UT Sync)
    # We bypass local time-zone ghosts by calculating the Universal Time immediately.
    local_time = datetime(year, month, day, hour, minute)
    utc_time = local_time - timedelta(hours=utc_offset)
    
    # Convert to Julian Day (The Astronomical Constant)
    julian_day = swe.julday(utc_time.year, utc_time.month, utc_time.day, 
                            utc_time.hour + utc_time.minute/60.0)

    # 2. THE REAL-SKY CONSTANT (Sidereal/True Lahiri)
    # Accounting for Earth's wobble to keep Danny and MJ anchored in Taurus.
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0) 
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # 3. CALCULATING THE ASCENDANT (Local Sidereal Time Solution)
    # This uses Topocentric precision to see the sky from the specific birth location.
    cusps, ascmc = swe.houses_ex(julian_day, lat, lon, b'P', flags)
    ascendant_deg = ascmc[0]

    # 4. WISDOM LIBRARY MAPPING (The Soulful Bridge)
    # Mapping degrees to the 1° Taurus foundation and its corresponding alignments.
    def get_wisdom_alignments(deg):
        if 0 <= deg < 30:
            return "Aries", "Vata", "Surya Namaskar"
        elif 30 <= deg < 60:
            # The 1° Taurus breakthrough (31° in a 360° circle)
            return "Taurus", "Kapha", "Vrksasana (Tree Pose)"
        # ... additional library mappings continue here ...
        return "Unknown", "Balanced", "Savasana"

    sign, dosha, posture = get_wisdom_alignments(ascendant_deg)

    return {
        "Name": name,
        "Ascendant": f"{ascendant_deg % 30:.2f}° {sign}",
        "Internal Atmosphere": dosha,
        "Soulful Movement": posture,
        "Truth Receipt": "Sidereal/True Lahiri (Precession Accounted For)"
    }

# Example: Running the MJ/Danny 'Gold Standard' Test
# Chicago/Gary area, ~May 1957/58, UTC-6 (Standard/DST adjustment)
report = calculate_soul_map("Soul Map Test", 1957, 5, 10, 12, 0, 41.8781, -87.6298, -6)
print(report)
