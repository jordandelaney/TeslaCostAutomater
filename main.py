from models import API, MailMan

api = API()
mailman = MailMan()

charge_cost = api.get_charge_cost()
if charge_cost:
    msg = f"Your total charge expenses for the month are ${charge_cost}"
    mailman.send_mail(msg)


