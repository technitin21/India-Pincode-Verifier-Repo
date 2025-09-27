# utils.py
import pgeocode
import re
from math import radians, cos, sin, asin, sqrt


PIN_REGEX = re.compile(r'^[1-9][0-9]{5}$')


nom = pgeocode.Nominatim('IN')


def is_valid_pin(pin):
if pin is None:
return False
pin = str(pin).strip()
return bool(PIN_REGEX.match(pin))


def geocode_pin(pin):
"""Return (lat, lon) for a valid Indian PIN code. Returns (None, None) if not found."""
if not is_valid_pin(pin):
return (None, None)
res = nom.query_postal_code(str(pin))
if hasattr(res, 'latitude') and res.latitude is not None and not str(res.latitude).lower().startswith('nan'):
return (float(res.latitude), float(res.longitude))
return (None, None)


# Haversine (km)
def haversine(lat1, lon1, lat2, lon2):
if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
return float('inf')
lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
dlon = lon2 - lon1
dlat = lat2 - lat1
a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
c = 2 * asin(sqrt(a))
km = 6371 * c
return km
