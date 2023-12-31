import random

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import (
    InvalidToken,
    TokenError,
    TokenUser,
)

from .models import OneTimePassword, User


def sendOtpToUser(email):
    user = User.objects.get(email=email)
    otp = str(random.randint(100000, 999999))

    OneTimePassword.objects.create(user=user, otp=otp)
    email_body = render_to_string('confirmation.html', {'otp': otp})

    send_mail(
        subject=f'Your otp is {otp}',
        message=email_body,
        from_email=settings.EMAIL_HOST,
        recipient_list=[user.email],
        html_message=email_body,
    )


def send_email_reset_pw(data):
    email_body = render_to_string(
        'password-recovery.html', {'url': data['url']}
    )

    send_mail(
        subject='Reset Password',
        message=email_body,
        from_email=settings.EMAIL_HOST,
        recipient_list=data['to_email'],
        html_message=email_body,
    )


def get_current_user_id(access_token):
    try:
        token_user = TokenUser(access_token)
        return token_user.id

    except InvalidToken:
        raise AuthenticationFailed('Invalid token')

    except TokenError:
        raise AuthenticationFailed('Token is invalid or expired')


def public_view(view):
    return view.as_view(authentication_classes=[])
