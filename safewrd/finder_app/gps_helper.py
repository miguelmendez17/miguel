"""
FLYTBASE INC grants Customer a perpetual, non-exclusive, royalty-free license to use this software.
 All copyrights, patent rights, and other intellectual property rights for this software are retained by FLYTBASE INC.
"""



import math


def dist_ang_betn_coordinates(lat1, lon1, lat2, lon2):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2  # haversine vertical angle
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is 6371
    mtr = 6371000 * c

    # lets find horizontal angle
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) \
        - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    h_ang = math.atan2(y, x)

    return mtr, h_ang


def get_offset_location(lat_h, long_h, lat_t, long_t, offset):
    # offset in meters
    distance, angle = dist_ang_betn_coordinates(lat_h,long_h, lat_t, long_t)
    R = 6378.1  # Radius of the Earth
    brng = angle  # Bearing is 90 degrees converted to radians.
    d = (distance - offset)*0.001  # Distance in km
    # lat2  52.20444 - the lat result I'm hoping for
    # lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(lat_h)  # Current lat point converted to radians
    lon1 = math.radians(long_h)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                     math.cos(lat1) * math.sin(d / R) * math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2, lon2
