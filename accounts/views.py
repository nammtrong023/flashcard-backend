from api.permission import CustomPermission
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import OneTimePassword, User
from .serializer import (
    PasswordResetRequestSerializer,
    ResendOtpSerializer,
    SetNewPasswordSerializer,
    UserSerializer,
    VerifyEmailSerializer,
)
from .utils import sendOtpToUser


# Create your views here.
class RegisterView(generics.GenericAPIView):
    permission_classes = [CustomPermission]

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            sendOtpToUser(user['email'])

            return Response(
                {'message': 'Check email'},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credential try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        tokens = user.tokens()
        data = {
            "access": str(tokens.get('access')),
            "refresh": str(tokens.get('refresh')),
        }
        return Response(data, status=status.HTTP_200_OK)


class VerifyEmailView(generics.GenericAPIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = request.data.get('otp')
        email = request.data.get('email')

        try:
            user_codes = OneTimePassword.objects.filter(user__email=email)
        except OneTimePassword.DoesNotExist:
            return Response(
                {'message': 'Email not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        for user_code in user_codes:
            is_valid_otp = otp == user_code.otp

            if is_valid_otp and not user_code.has_expired():
                user = user_code.user
                user.is_verified = True
                user.save()
                OneTimePassword.objects.filter(user=user).delete()

                tokens = user.tokens()
                data = {
                    "access": str(tokens.get('access')),
                    "refresh": str(tokens.get('refresh')),
                }

                return Response(
                    {'data': data, 'message': 'Verified email'},
                    status=status.HTTP_200_OK,
                )
            elif is_valid_otp and user_code.has_expired():
                return Response(
                    {'message': 'Otp has expired'},
                    status=status.HTTP_204_NO_CONTENT,
                )

        return Response(
            {'message': 'Invalid code'},
            status=status.HTTP_204_NO_CONTENT,
        )


class ResendOtpView(generics.GenericAPIView):
    def post(self, request):
        serializer = ResendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'message': 'Email not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {'message': 'Email has been verified'},
                status=status.HTTP_204_NO_CONTENT,
            )

        sendOtpToUser(email)
        return Response(
            {'message': 'Resend otp successfully'},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(generics.GenericAPIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {'message': 'we have sent you a link to reset your password'},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirm(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'message': 'token is invalid or has expired'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    'success': True,
                    'message': 'credentials is valid',
                    'uidb64': uidb64,
                    'token': token,
                },
                status=status.HTTP_200_OK,
            )

        except DjangoUnicodeDecodeError:
            return Response(
                {'message': 'token is invalid or has expired'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {'success': True, 'message': "password reset is succesful"},
            status=status.HTTP_200_OK,
        )


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
