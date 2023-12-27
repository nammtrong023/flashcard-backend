from django.db import models
from rest_framework import serializers

# Create your models here.


class Size(models.Model):
    value = models.CharField(max_length=10)

    def __str__(self):
        return self.value


class Product(models.Model):
    name = models.CharField(max_length=255)
    sizes = models.ManyToManyField(Size, blank=False)

    @property
    def images(self):
        return self.image_set.all()


class Image(models.Model):
    url = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Flashcard(models.Model):
    title = models.CharField(max_length=255)

    @property
    def flashcard_items(self):
        return self.flashcarditem_set.all()


class FlashcardItem(models.Model):
    name = models.CharField(max_length=255)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
