from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import GithubLoginSerializer, GoogleSignInSerializer

# Create your views here.


class GoogleOauthSignInview(GenericAPIView):
    serializer_class = GoogleSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)['access_token']

        return Response(data, status=status.HTTP_200_OK)


class GithubOauthSignInView(GenericAPIView):
    def post(self, request):
        serializer = GithubLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = (serializer.validated_data)['code']
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )