def get_sign(ra_hours):
    # Convert RA hours to degrees (1 hour = 15 degrees)
    total_degrees = ra_hours * 15
    
    # Subtracting the Ayanamsha (approx 24 degrees for the current era)
    # This aligns the Tropical RA with the actual Sidereal constellations
    sidereal_degrees = (total_degrees - 24.0) % 360
    
    signs = [
        ("Aries", 0, 30), ("Taurus", 30, 60), ("Gemini", 60, 90),
        ("Cancer", 90, 120), ("Leo", 120, 150), ("Virgo", 150, 180),
        ("Libra", 180, 210), ("Scorpio", 210, 240), ("Sagittarius", 240, 270),
        ("Capricorn", 270, 300), ("Aquarius", 300, 330), ("Pisces", 330, 360)
    ]
    
    for name, start, end in signs:
        if start <= sidereal_degrees < end:
            # Calculate the exact degree within that sign
            degree_in_sign = sidereal_degrees - start
            return name, degree_in_sign
    return "Unknown", 0
