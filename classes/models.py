import random
import string

from accounts.models import User
from django.db import models
from flashcards.models import FlashcardSet


# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    invite_code = models.CharField(max_length=10, blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='classes'
    )
    members = models.ManyToManyField(User, related_name='classes_members')
    flashcard_sets = models.ManyToManyField(
        FlashcardSet,
        blank=True,
        related_name='classes',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_default_invite_code():
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(10))

    invite_code = models.CharField(
        max_length=10,
        default=generate_default_invite_code,
        blank=True,
        null=True,
    )
