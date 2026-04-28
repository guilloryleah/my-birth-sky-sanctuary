from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# 1. Set your birth data
# Replace these with your exact birth time and coordinates
date = Datetime('19XX/XX/XX', 'HH:MM', '+00:00') # YYYY/MM/DD and Time
pos = GeoPos('29n45', '95w21') # Coordinates for Houston, TX

# 2. Generate the Chart using Sidereal (Lahiri) Ayanamsa
# This ensures it aligns with pure astronomical data
chart = Chart(date, pos, hsys=const.HOUSES_PLACIDUS, ayanamsa=const.AYAN_LAHIRI)

# 3. Output your core placements
print(f"{'Planet':<10} | {'Sign':<12} | {'Degree'}")
print("-" * 35)

planets = [
    const.SUN, const.MOON, const.MERCURY, 
    const.VENUS, const.MARS, const.JUPITER, 
    const.SATURN
]

for p in planets:
    obj = chart.get(p)
    print(f"{obj.id:<10} | {obj.sign:<12} | {obj.signlon:.2f}°")
