import requests
from flight_data import FlightData
from flight_search import FlightSearch


class DataManager:
    def __init__(self):
        self.sheet_data = FlightData().get_flight_data()
        self.sheet_endpoint = FlightData().sheets_endpoint
    def add_iata_codes(self):
        for city in self.sheet_data["prices"]:
            if city["iataCode"] == "":
                id_params = {
                    "price": {
                        "iataCode": FlightSearch().get_city_code(city_name=city["city"]),
                    }
                }

                id_endpoint = self.sheet_endpoint + "/" + str(city["id"])
                response = requests.put(id_endpoint, json=id_params)
                response.raise_for_status()



