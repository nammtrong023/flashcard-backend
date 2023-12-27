from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utils import send_email_reset_pw


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68,
        min_length=6,
        required=False,
        # Password won't be included in serialized output
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["email", 'name', 'password']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)
    email = serializers.EmailField(required=True)


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # decode uid(userId) to b64(base64)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            request = self.context.get('request')

            token = PasswordResetTokenGenerator().make_token(user)
            site = settings.FRONTEND_URL

            abslink = f"{site}/password-recovery/{uidb64}/{token}"
            email_body = f"Hi {user.name} use the link below to reset your password {abslink}"

            attrs = {
                'email_body': email_body,
                'email_subject': "Reset your Password",
                'to_email': user.email,
            }
            send_email_reset_pw(attrs)

            return super().validate(attrs)

        return 'Not exists'


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=100, min_length=6, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=100, min_length=6, write_only=True
    )
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=3, write_only=True)

    def validate(self, data):
        try:
            token = data.get('token')
            uidb64 = data.get('uidb64')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    "reset link is invalid or has expired", 401
                )

            if password != confirm_password:
                raise AuthenticationFailed("passwords do not match")

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            return AuthenticationFailed("link is invalid or has expired")
