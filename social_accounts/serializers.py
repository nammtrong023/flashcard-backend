from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .utils import Github, Google, login_oauth2


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        user_data = Google.validate(access_token)

        try:
            user_data['sub']
        except Exception as e:
            raise serializers.ValidationError(
                f"{e} this token has expired or invalid please try again"
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('Could not verify user.')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['given_name']
        provider = 'google'

        return login_oauth2(provider, user_id, email, name)


class GithubLoginSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, code):
        access_token = Github.exchange_code_for_token(code)

        if access_token:
            user_data = Github.get_github_user(access_token)

            name = user_data['name']
            email = user_data['email']
            provider = 'github'
            provider_id = 123
            return login_oauth2(provider, provider_id, email, name)

        return Response({'data': 'Invalid Token'})
