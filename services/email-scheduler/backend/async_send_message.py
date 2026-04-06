import aiosmtplib
from database.db import engine
import dotenv
import os
from email.message import EmailMessage
from datetime import datetime
from sqlalchemy import text


dotenv.load_dotenv()


async def async_send_message():
    async with engine.connect() as db:
        token = os.getenv("SMTP_PASSWORD")
        sender_email = os.getenv("SMTP_USER_NAME")

        query = text("""SELECT id, receiver_email, subject, message_body 
                     FROM emails WHERE sending_time <= :now AND is_sent = False""")
        current_time = datetime.now()
        data = await db.execute(query, {"now": current_time})
        emails_to_send = data.all()

        if not emails_to_send:
            return

        try:
            async with aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587) as server:
                await server.login(sender_email, token)

                for row in emails_to_send:
                    try:
                        msg = EmailMessage()
                        msg.set_content(row.message_body)
                        msg["Subject"] = row.subject
                        msg["From"] = sender_email
                        msg["To"] = row.receiver_email

                        await server.send_message(msg)
                        print(f"Отправлено на {row.receiver_email}")

                        update_query = text("UPDATE emails SET is_sent = True WHERE id = :id")
                        await db.execute(update_query, {"id": row.id})
                        await db.commit()
                    except Exception as e:
                        print(f"Ошибка при отправке письма {row.id}: {e}")
                        await db.rollback()
        except Exception as e:
            print(f"Ошибка подключения к SMTP: {e}")