from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_email_registration_otp(user_email, message):
    subject = "Verify Your Email Address"
    message = f"{message}"

    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(
          subject, 
          message.strip(), 
          from_email, [user_email]
          )