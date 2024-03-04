from core.celery import app
from decouple import config
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

site_name = config("APP_NAME")
today = date.today()
year = today.strftime("%Y")


# respond_send_contact_form task
@app.task(name="send_respond_contact_form")
def send_respond_contact_form_task(data):
    logger.info("Sent send_respond_contact_form")
    subject = "HotelProxi: Contact Form"
    from_email = config("EMAIL_HOST_USER")
    to_email = (data["email"],)
    body_txt = "respond_contact_form.txt"
    register_message = render_to_string(
        body_txt, {"site_name": site_name, "year": year, "name": data["name"]}
    )
    message = EmailMultiAlternatives(
        subject=subject, body=register_message, from_email=from_email, to=to_email
    )
    html_template = "respond_contact_form.html"
    template = render_to_string(
        html_template, {"site_name": site_name, "year": year, "name": data["name"]}
    )
    message.attach_alternative(template, "text/html")
    message.send()


# send_contact_form task
@app.task(name="send_contact_form")
def send_contact_form_task(data):
    logger.info("Sent send_contact_form")
    subject = "New Entry: Contact Form"
    from_email = config("EMAIL_HOST_USER")
    to_email = (config("MARKETER_EMAIL"),)
    body_txt = "contact_us_form.txt"
    register_message = render_to_string(
        body_txt,
        {
            "subject": data["subject"],
            "name": data["name"],
            "email": data["email"],
            "phone": data["phone"],
            "message": data["message"],
            "year": year,
            "name": data["name"],
        },
    )
    message = EmailMultiAlternatives(
        subject=subject, body=register_message, from_email=from_email, to=to_email
    )
    html_template = "contact_us_form.html"
    template = render_to_string(
        html_template,
        {
            "subject": data["subject"],
            "name": data["name"],
            "email": data["email"],
            "phone": data["phone"],
            "message": data["message"],
            "year": year,
            "name": data["name"],
        },
    )
    message.attach_alternative(template, "text/html")
    message.send()
