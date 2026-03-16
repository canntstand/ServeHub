import smtplib
import dotenv
import os
from email.message import EmailMessage
import re

dotenv.load_dotenv()


def send_message(receiver_email: str, subject: str, message_body: str):
    token = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SMTP_USER_NAME")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", receiver_email):
        return 400

    msg = EmailMessage()
    msg.set_content(message_body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, token)
            server.send_message(msg)
        
        print(f"Сообщение было отослано по адресу: {receiver_email}")
        return 200

    except Exception as e:
        print(f"Ошибка: {e}")
        return 500
