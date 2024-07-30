import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
HOST = os.getenv("HOST")
PORT_NUMBER = os.getenv("PORT_NUMBER")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


def send_email(new_vehicles):
    msg = set_message_content(new_vehicles)
    with smtplib.SMTP(HOST, PORT_NUMBER) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        smtp.close()


def set_message_content(
    new_vehicles,
) -> EmailMessage:
    msg = EmailMessage()
    msg["To"] = EMAIL_ADDRESS
    msg["From"] = EMAIL_ADDRESS
    msg["Subject"] = "New Posting('s)!"

    msg_content = ""
    for key in new_vehicles:
        msg_content = f"\nLocation: {key}\n"
        for car in new_vehicles[key]:
            msg_content += f'Vehicle: {car["Car"]}\nRow Number: {car["Row Number"]}\nURL: {car["Image URL"]}\nDate Vehicle was Set: {car["Set Date"]}\n\n'

    msg.set_content(msg_content)

    return msg
