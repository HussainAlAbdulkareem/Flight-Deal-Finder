from data_manager import DataManager
from flight_data import FlightData
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
data_manager = DataManager()
data_manager.add_iata_codes()
for row in data_manager.sheet_data["prices"]:
    flight_data = FlightData().find_cheapest_flight(row["iataCode"])
    if type(flight_data) is str:
        print(flight_data)
    else:
        trip_price = float(flight_data["price"]["grandTotal"])
        departure_iata = flight_data["itineraries"][0]['segments'][0]['departure']["iataCode"]
        arrival_iata = flight_data["itineraries"][0]['segments'][0]['arrival']["iataCode"]
        outbound_date = flight_data["itineraries"][0]['segments'][0]['departure']["at"].split("T")[0]
        inbound_date = flight_data["itineraries"][1]['segments'][0]['departure']["at"].split("T")[0]

        if trip_price < row["lowestPrice"]:
            client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))
            message = client.messages.create(
                from_=f'whatsapp:{os.getenv("TWILIO_NUM")}',
                body=f"Low Price Found! {trip_price}CAD to fly from {departure_iata} to {arrival_iata}"
                     f", from {outbound_date} until {inbound_date}.",
                to=f'whatsapp:{os.getenv("MY_NUM")}'
            )
            print(message.status)



