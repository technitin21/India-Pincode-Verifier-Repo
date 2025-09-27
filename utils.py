import pgeocode, math

nomi = pgeocode.Nominatim('IN')

def geocode_pincode(pincode):
    loc = nomi.query_postal_code(str(pincode))
    if loc is None or loc.latitude is None:
        return None
    return (loc.latitude, loc.longitude)

def haversine_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1-a))
