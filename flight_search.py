# This class is responsible for talking to the Flight Search API.

import os
import requests
from flight_data import FlightData

TEQUILA_APP_ID = os.environ.get("TEQUILA_APP_ID")
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
TEQUILA_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")
TEQUILA_HEADERS = {
    "apikey": TEQUILA_API_KEY,
}


class FlightSearch:

    def __init__(self):
        self.city_codes = []

    def get_destination_codes(self, city_names):
        print("Getting destination codes...")
        for city in city_names:
            search_query = {"term": city, "location_types": "city"}
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/locations/query",
                params=search_query,
                headers=TEQUILA_HEADERS
            )
            city_code = response.json()["locations"][0]["code"]
            self.city_codes.append(city_code)

    # Change parameters in check_flights method to suit search parameters

    def check_flights(self, origin_city_code, destination_city_code, from_date, to_date):
        print(f"Checking flights for {destination_city_code}...")
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 28,
            "max_fly_duration": 24,
            "flight_type": "round",
            "one_for_city": 1,
            "adults": 1,
            "max_stopovers": 0,
            "curr": "EUR",
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=TEQUILA_HEADERS)
        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=TEQUILA_HEADERS)

            try:
                data = response.json()["data"][0]
                # pprint(data)
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: €{flight_data.price}")
            return flight_data




