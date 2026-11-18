from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class Geocoding:

    @staticmethod
    def get_coordinates(address):

        try:
            geolocator = Nominatim(
                user_agent="food_rescue_coordinator"
            )

            location = geolocator.geocode(
                address,
                timeout=10
            )

            if location:
                latitude = location.latitude
                longitude = location.longitude

                return latitude, longitude

            return None

        except (GeocoderTimedOut, GeocoderServiceError) as err:
            print("Geocoding Error:", err)
            return None