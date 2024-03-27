import random

from geopy.distance import geodesic


def generate_random_coordinates(location, distance_miles):
    latitude = location.lat
    longitude = location.lng

    random_point = geodesic(kilometers=distance_miles * 1.60934).destination((latitude, longitude), bearing=random.uniform(0, 360))

    return random_point.latitude, random_point.longitude


def generate_random_coordinates_not_radius(location, distance_miles):
    latitude = location.lat + 10
    longitude = location.lng + 10

    random_point = geodesic(kilometers=distance_miles * 1.60934).destination((latitude, longitude),
                                                                             bearing=random.uniform(0, 360))

    return random_point.latitude, random_point.longitude
