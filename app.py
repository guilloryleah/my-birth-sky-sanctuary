from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

# 1. THE DATA
# Enter your Birth Date (YYYY/MM/DD), Time (24hr), and UTC Offset
# Enter your Location (Houston is approximately 29n45, 95w21)
birth_date = Datetime('19XX/XX/XX', 'HH:MM', '-06:00') 
location = GeoPos('29n45', '95w21')

# 2. THE CALCULATION
# We use AYAN_LAHIRI to ensure it is Sidereal/Vedic, not Western Tropical.
chart = Chart(birth_date, location, ayanamsa=const.AYAN_LAHIRI)

# 3. THE OUTPUT
print(f"{'PLANET':<12} | {'SIGN':<15} | {'DEGREE'}")
print("-" * 40)

# List of bodies to check
bodies = [
    const.SUN, const.MOON, const.MERCURY, 
    const.VENUS, const.MARS, const.JUPITER, 
    const.SATURN, const.RAHU, const.KETU
]

for body in bodies:
    p = chart.get(body)
    print(f"{p.id:<12} | {p.sign:<15} | {p.signlon:.2f}°")
