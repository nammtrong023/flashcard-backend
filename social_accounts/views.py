from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import GithubLoginSerializer, GoogleSignInSerializer
from .utils import Github, Google, login_oauth2

# Create your views here.


class GoogleOauthSignInview(GenericAPIView):
    serializer_class = GoogleSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        provider = 'google'
        provider_id = validated_data['user_id']
        email = validated_data['email']
        name = validated_data['name']

        tokens_data = login_oauth2(provider, provider_id, email, name)

        return Response(tokens_data, status=status.HTTP_200_OK)


class GithubOauthSignInView(GenericAPIView):
    def post(self, request):
        serializer = GithubLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = (serializer.validated_data)['code']
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
