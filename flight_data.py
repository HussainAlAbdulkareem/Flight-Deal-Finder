import os
import requests
from dotenv import load_dotenv
from flight_search import FlightSearch


class FlightData:
    def __init__(self):
        load_dotenv()
        self.sheets_endpoint = f"https://api.sheety.co/{os.getenv('USER_NAME')}/flightDeals/prices"

    def get_flight_data(self):
        sheets_response = requests.get(self.sheets_endpoint)
        sheets_data = sheets_response.json()
        return sheets_data

    def find_cheapest_flight(self, iataCode):
        flight_info = {}
        max_price = 2500
        flight_data = FlightSearch().search_for_flight(iataCode)
        if flight_data is None:
            return ("No flight data available.")
        for flight in flight_data:
            if float(flight["price"]["grandTotal"]) < max_price:
                flight_info = flight
                max_price = float(flight["price"]["grandTotal"])

        if not flight_info:
            return ("No flight data available.")
        return flight_info

