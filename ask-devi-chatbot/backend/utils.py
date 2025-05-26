import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime

def calculate_chart(name, date_str, time_str, place):
    geolocator = Nominatim(user_agent="ask-devi")
    location = geolocator.geocode(place)

    if not location:
        raise ValueError("Invalid location")

    lat, lon = location.latitude, location.longitude

    # Get timezone
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    if not timezone_str:
        timezone_str = 'UTC'

    tz = pytz.timezone(timezone_str)
    naive_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    local_dt = tz.localize(naive_dt)
    utc_dt = local_dt.astimezone(pytz.utc)

    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)

    # Set ephemeris path to current dir
    swe.set_ephe_path(".")

    # Get longitudes
    sun = swe.calc_ut(jd, swe.SUN)[0][0]
    moon = swe.calc_ut(jd, swe.MOON)[0][0]
    asc = swe.houses(jd, lat, lon, b'A')[0][0]  # Ascendant

    def zodiac_sign(degree):
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        return signs[int(degree / 30)]

    return {
        "sunSign": zodiac_sign(sun),
        "moonSign": zodiac_sign(moon),
        "ascendant": zodiac_sign(asc)
    }
