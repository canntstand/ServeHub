from fastapi import FastAPI, Form, Request, BackgroundTasks
from .message_sender import send_message
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(redirect_slashes=True, lifespan=lifespan)

templates = Jinja2Templates(directory="services/email-scheduler/frontend")

app.mount(
    "/static", StaticFiles(directory="services/email-scheduler/frontend"), name="static"
)


@app.get("/email-scheduler", response_class=HTMLResponse)
def get_form_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/message-scheduled", response_class=HTMLResponse)
def get_information_page(request: Request):
    return templates.TemplateResponse(request=request, name="info.html")


@app.post("/api/v1", response_class=RedirectResponse)
def handle_email_request(
    background_tasks: BackgroundTasks,
    receiver_email: str = Form(...),
    subject: str = Form(...),
    message_body: str = Form(...),
    sending_time: str = Form(...),
):

    background_tasks.add_task(
        send_message, receiver_email, subject, message_body, sending_time
    )

    return RedirectResponse(url="/message-scheduled", status_code=302)
