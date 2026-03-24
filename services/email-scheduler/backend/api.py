from typing import Annotated
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database.database import init_db, get_db
from datetime import datetime
import re


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(redirect_slashes=True, lifespan=lifespan)

templates = Jinja2Templates(directory="frontend")

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=RedirectResponse)
def redirect_to_main_page():
    return RedirectResponse(url="/email-scheduler", status_code=303)


@app.get("/email-scheduler", response_class=HTMLResponse)
def get_form_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/message-scheduled", response_class=HTMLResponse)
def get_information_page(request: Request):
    return templates.TemplateResponse(request=request, name="info.html")


@app.post("/api/v1", response_class=RedirectResponse)
async def handle_email_request(
    db: Annotated[AsyncConnection, Depends(get_db)],
    receiver_email: str = Form(...),
    subject: str = Form(...),
    message_body: str = Form(...),
    sending_time: str = Form(...),
):

    if not re.match(r"[^@]+@[^@]+\.[^@]+", receiver_email):
        return 400

    sending_time = datetime.fromisoformat(sending_time)

    query = text("""
    INSERT INTO emails (is_sent, receiver_email, subject, message_body, sending_time)
    VALUES (:is_sent, :receiver_email, :subject, :message_body, :sending_time)
    """)

    await db.execute(
        query,
        {
            "is_sent": False,
            "receiver_email": receiver_email,
            "subject": subject,
            "message_body": message_body,
            "sending_time": sending_time,
        },
    )

    return RedirectResponse(url="/message-scheduled", status_code=303)
