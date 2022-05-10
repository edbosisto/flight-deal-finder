# This class is responsible for sending notifications with the deal flight details.

from twilio.rest import Client
import smtplib
import os

TWILIO_ACCT_SID = os.environ.get("TWILIO_ACCT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.environ.get("TWILIO_VIRTUAL_NUMBER")
MY_LUX_NUMBER = os.environ.get("MY_LUX_NUMBER")

MY_RECEIVING_EMAIL = os.environ.get("MY_RECEIVING_EMAIL")  # smtp.gmail.com
MY_YAHOO_EMAIL = os.environ.get("MY_YAHOO_EMAIL")  # smtp.mail.yahoo.com
YAHOO_EMAIL_PASS = os.environ.get("YAHOO_EMAIL_PASS")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        the_message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=MY_LUX_NUMBER
        )
        print(the_message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=MY_YAHOO_EMAIL, password=YAHOO_EMAIL_PASS)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_YAHOO_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )

