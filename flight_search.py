import os
import requests
from dotenv import load_dotenv
import datetime


class FlightSearch:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.token = self.gen_new_token()
        self.header = {"Authorization": "Bearer " + self.token["access_token"]}

    def gen_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret,
        }
        response = requests.post(url=self.token_endpoint, headers=header, data=body)
        return response.json()

    def get_city_code(self, city_name):
        city_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        params = {
            "keyword": city_name,
            "max": 1
        }
        response = requests.get(url=city_endpoint, params=params, headers=self.header).json()
        iata_code = response['data'][0]["iataCode"]
        return iata_code

    def search_for_flight(self, iata_code):
        flight_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        flight_params = {
            "originLocationCode": "YYC",
            "destinationLocationCode": iata_code,
            "departureDate": datetime.date.today() + datetime.timedelta(days=1),
            "returnDate": datetime.date.today() + datetime.timedelta(days=6 * 30),
            "adults": 1,
            "currencyCode": "CAD",
            "max": 10,
            "nonStop": "true"
        }
        response = requests.get(url=flight_endpoint, params=flight_params, headers=self.header).json()
        return response['data']


