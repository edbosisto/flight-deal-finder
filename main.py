import datetime
import os
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = os.environ.get("ORIGIN_CITY_IATA")

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()
# print(sheet_data)

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_codes(city_names)
    data_manager.update_destination_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}

tomorrow = datetime.date.today() + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime("%d/%m/%Y")
return_limit = datetime.date.today() + datetime.timedelta(weeks=26)
return_limit_date = return_limit.strftime("%d/%m/%Y")

for destination_code in destinations:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination_code,
        from_date=tomorrow_date,
        to_date=return_limit_date,
    )

    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only EUR {flight.price}\nFrom {flight.origin_city} - {flight.origin_airport}\nTo {flight.destination_city} - {flight.destination_airport}.\nDeparts {flight.out_date}\nReturns {flight.return_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop overs, via {flight.via_city}."
            print(message)

        link = f"https://www.google.com/travel/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

        notification_manager.send_emails(emails, message, link)
