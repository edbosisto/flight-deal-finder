# Flight club
A flight deals scanner using Tequila API to search for flights

### data_manager.py
Data is managed using google sheets. An application known as Sheety https://sheety.co/ is responsible for talking to the spreadsheet.
To use the application you must sign up to Sheety an obtain an API token, and create and link your own google spreadsheet with sheety.
- The google sheet stores all relevant data. Price, destination city and user email addresses for notifications.

### flight_data.py
Responsible for structuring the flight data. Data from the API is passed to the FlightData class which sorts the important information for the spreadsheet.

### flight_search.py
Responsible for searching and retreiving flight data information from Tequila API. 
- To use this application, you must sign up for a free API key here https://tequila.kiwi.com/portal/login
Flight search takes all cities from the google spreadsheet and searches for flight details from the origin city (which can be updated in main.py). Paramaters can be set in the function check_flights().

### notification_manager.py
With smtplib and twilio libraries, the NotificationManager() class is responsible for sending notifications either mobile or email recipients.
- Sign up for a trial twilio account to use this application to send automated sms to your own mobile telephone. https://www.twilio.com/try-twilio
- In order to receive email notifications, update your own email contact details into the variables at the top of the page.
- If a flight is found with a price under the preset threshold in the google spreadsheet, automated notifications can be sent to any and all of the specified contacts in notification_manager.py

### main.py
Origin city set by variable ORIGIN_CITY_IATA. The application searches for return flights from this city.
- sheet_data imports and saves data from google spreadsheet.
- destinations are read from the google sheet.
- datetime library is used to determine current date and date range for flight search.
- flight destinations are iterated through, checking flights for each and comparing to the threshold price in the google sheet.
- if a flight is below the threshold, a notification is automatically sent to email or mobile phone as determined in notification_manager.py



