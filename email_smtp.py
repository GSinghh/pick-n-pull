import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()


def send_email():
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    msg_content = "These are all of the new vehicles that have been posted recently"

    car = "Acura Integra"
    msg = EmailMessage()
    msg["Subject"] = f"New {car} Posted"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(msg_content)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        smtp.close()


send_email()
