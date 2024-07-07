import os
import requests
from dotenv import load_dotenv

class FlightData:
    def __init__(self):
        load_dotenv()
        self.sheets_endpoint = f"https://api.sheety.co/{os.getenv('USER_NAME')}/flightDeals/prices"
    def get_flight_data(self):
        sheets_response = requests.get(self.sheets_endpoint)
        sheets_data = sheets_response.json()
        return sheets_data
