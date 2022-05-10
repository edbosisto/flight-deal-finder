# This class is responsible for talking to the Google Sheet.

import requests
import os

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_PRICES_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.environ.get("SHEETY_USERS_ENDPOINT")
SHEETY_HEADERS = {
            "Authorization": f"Bearer {SHEETY_TOKEN}",
            "Content-Type": "application/json",
        }


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=SHEETY_HEADERS)
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_code = {
                "price": {
                    "iataCode": city["iataCode"],
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_code, headers=SHEETY_HEADERS)
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=SHEETY_HEADERS)
        self.customer_data = response.json()["users"]
        return self.customer_data

