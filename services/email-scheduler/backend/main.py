from fastapi import FastAPI, APIRouter, Form, Request
from message_sender import send_message
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI(redirect_slashes=True)
templates = Jinja2Templates(directory="../frontend")
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/email-scheduler", response_class=HTMLResponse)
def get_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/api/v1")
def handle_email_request(
    receiver_email: str = Form(...),
    subject: str = Form(...),
    message_body: str = Form(...),
):

    code = send_message(receiver_email, subject, message_body)
    if code == 400:
        return {"status": "failure", "description": "unsuitable email"}
    elif code == 200:
        return {"status": "sent"}
    else:
        return {"status": "failure", "description": "undified"}
