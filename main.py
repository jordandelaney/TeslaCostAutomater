from models import API, MailMan
from datetime import datetime as dt
import calendar

today = dt.today()
last_day_of_month = calendar.monthrange(today.year, today.month)[1]

if today.day == last_day_of_month:
    api = API()
    mailman = MailMan()

    charge_cost = api.get_charge_cost()
    if charge_cost:
        msg = f"Your total charge expenses for the month are ${charge_cost}"
        mailman.send_mail(msg)


