from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .utils import Github, Google, login_oauth2


class GoogleSignInSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    email = serializers.CharField()
    name = serializers.CharField()


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
