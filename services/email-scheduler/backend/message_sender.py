import smtplib
from database.database import get_db
import dotenv
import os
from email.message import EmailMessage
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from celery import Celery
import asyncio

dotenv.load_dotenv()

app = Celery("celery", "redis://redis:6379/0")


@app.task
def send_message():
    return asyncio.run(async_send_message())


async def async_send_message():
    db: AsyncConnection = get_db()
    token = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SMTP_USER_NAME")

    query = text(
        """SELECT id, receiver_email, subject, message_body, sending_time FROM emails WHERE sending_time <= :now AND is_sent = False"""
    )

    current_time = datetime.now()

    data = await db.execute(query, {"now": current_time})
    emails_to_send = data.all()

    if not emails_to_send:
        return "Нет сообщений для отправки"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, token)

            for row in emails_to_send:
                msg = EmailMessage()
                msg.set_content(row.message_body)
                msg["Subject"] = row.subject
                msg["From"] = sender_email
                msg["To"] = row.receiver_email

                server.send_message(msg)
                print(f"Сообщение было отослано по адресу: {row.receiver_email}")

                query = text("""UPDATE emails SET is_sent = True WHERE id = :id""")
                await db.execute(query, {"id": row.id})

        return 200

    except Exception as e:
        print(f"Ошибка: {e}")
        return 500
