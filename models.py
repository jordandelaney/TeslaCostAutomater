from dotenv import load_dotenv
import os
from datetime import datetime
import requests
import smtplib

load_dotenv()

class API:

    def __init__(self):
        self.url = os.getenv('API_ENDPOINT')
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {os.getenv('TOKEN')}"
        }

    def get_charge_cost(self):
        """Takes the longitude and longitude of the charging station and retrieves
        all charging data for that location for the current month to the day."""
        today = datetime.today()
        start = datetime(today.year, today.month, 1)
        end = datetime(today.year, today.month, today.day)
        params = {
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
            "origin_longitude": float(os.getenv("HOME_LONG")),
            "origin_latitude": float(os.getenv("HOME_LAT")),
            "origin_radius": 1500,
        }

        response = requests.get(f"{self.url}/charges", headers=self.headers, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}: {response.reason}")
            return None

        try:
            results = response.json()["results"]
            return round(sum((charge["cost"] for charge in results)), 2)
        except ValueError:
            print("Error: Invalid JSON response")
            return None

class MailMan:

    def __init__(self):
        self.user = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.to_addrs = os.getenv('SEND_TO')
        self.port = int(os.getenv('EMAIL_PORT'))
        self.host = os.getenv('EMAIL_HOST')

    def send_mail(self, message):
        try:
            with smtplib.SMTP(host=self.host, port=self.port) as connection:
                connection.starttls()
                connection.login(
                    user=self.user,
                    password=self.password
                )
                connection.sendmail(
                    from_addr=self.user,
                    to_addrs=self.to_addrs,
                    msg="Subject:This Month's Charging Report\n\n"
                        f"{message}"
                )
        except smtplib.SMTPException as e:
            print(f"Email sending failed: {e}")