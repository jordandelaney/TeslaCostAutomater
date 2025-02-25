from dotenv import load_dotenv
import os
from datetime import datetime
import calendar
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

    def get_charges(self):
        today = datetime.today()
        start = datetime(today.year, today.month, 1)
        end = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
        params = {
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
        }
        response = requests.get(f"{self.url}/charges", headers=self.headers, params=params)
        return response.json()

class MailMan:

    def __init__(self):
        self.user = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.to_addrs = os.getenv('SEND_TO')
        self.port = os.getenv('EMAIL_PORT')


api = API()
print(api.get_charges())
