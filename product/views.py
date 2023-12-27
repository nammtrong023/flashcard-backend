from django.shortcuts import render
from rest_framework import generics

from .models import Flashcard, Image, Product, Size
from .serializers import ProductSerializer, SizeSerializer, FlashcardSerializer


# Create your views here.
class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SizeListCreateApiView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class FlashcardListCreateApiView(generics.ListCreateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
