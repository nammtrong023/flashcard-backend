import random

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

from .models import OneTimePassword, User


def sendOtpToUser(email):
    user = User.objects.get(email=email)
    otp = str(random.randint(100000, 999999))

    OneTimePassword.objects.create(user=user, otp=otp)
    email_body = render_to_string('confirmation.html', {'otp': otp})

    send_mail(
        subject='Verify',
        message=email_body,
        from_email=settings.EMAIL_HOST,
        recipient_list=[user.email],
        html_message=email_body,  # Set the HTML version of the email body
    )


def send_email_reset_pw(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']],
    )
    email.send()
