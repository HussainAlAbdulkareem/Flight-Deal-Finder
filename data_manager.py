import requests
from flight_data import FlightData
from flight_search import FlightSearch

class DataManager:
    def add_iata_codes(self):
        sheet_data = FlightData().get_flight_data()
        sheet_endpoint = FlightData().sheets_endpoint

        for city in sheet_data["prices"]:
            if city["iataCode"] == "":
                id_params = {
                    "price": {
                        "iataCode": FlightSearch().get_city_code(city_name=city["city"]),
                    }
                }

                id_endpoint = sheet_endpoint + "/" + str(city["id"])
                response = requests.put(id_endpoint, json=id_params)
                response.raise_for_status()

