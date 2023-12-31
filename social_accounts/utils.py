import requests
from accounts.models import Account, User
from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed


class Google:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(
                access_token, requests.Request()
            )
            if 'accounts.google.com' in id_info['iss']:
                return id_info

        except Exception as e:
            raise ValueError(
                "The token is either invalid or has expired"
            ) from e


class Github:
    @staticmethod
    def exchange_code_for_token(code):
        params_payload = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_SECRET,
            "code": code,
        }

        get_access_token = requests.post(
            "https://github.com/login/oauth/access_token",
            params=params_payload,
            headers={'Accept': 'application/json'},
        )

        payload = get_access_token.json()
        token = payload.get('access_token')

        return token

    @staticmethod
    def get_github_user(access_token):
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            resp = requests.get('https://api.github.com/user', headers=headers)
            user_data = resp.json()
            return user_data
        except Exception as e:
            raise AuthenticationFailed("invalid access_token", 401) from e


def login_oauth2(provider, provider_id, email, name):
    account_exists = Account.objects.filter(user__email=email).exists()

    if account_exists:
        user = User.objects.get(email=email)
        tokens = user.tokens()
        return {
            "access": str(tokens.get('access')),
            "refresh": str(tokens.get('refresh')),
        }

    user_exists = User.objects.filter(email=email).exists()
    if user_exists:
        user = User.objects.get(email=email)

        account = Account.objects.create(
            user=user,
            provider=provider,
            provider_id=provider_id,
        )
        account.save()

    else:
        new_user = User.objects.create(email=email, name=name, is_verified=True)
        new_user.save()

        account = Account.objects.create(
            user=new_user,
            provider=provider,
            provider_id=provider_id,
        )
        account.save()

        tokens = new_user.tokens()
        return {
            "access": str(tokens.get('access')),
            "refresh": str(tokens.get('refresh')),
        }
