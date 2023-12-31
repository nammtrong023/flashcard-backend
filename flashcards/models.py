from accounts.models import User
from django.db import models
from multiselectfield import MultiSelectField


class FlashcardSet(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="flashcard_sets"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def flashcards(self):
        return self.flashcard_set.all()

    @property
    def flashcard_set_viewer(self):
        return self.flashcardsetviewer_set.all()


class Flashcard(models.Model):
    id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=255, blank=True, default='')
    definition = models.CharField(max_length=255, blank=True, default='')
    flashcard_set = models.ForeignKey(
        FlashcardSet, on_delete=models.CASCADE, related_name='flashcards'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


QUESTION_TYPES = [
    ('Multiple Choice', 'Multiple Choice'),
    ('Written', 'Written'),
]


class FlashcardSetViewer(models.Model):
    question_types = MultiSelectField(
        choices=QUESTION_TYPES, default="Multiple Choice"
    )
    is_first_setting = models.BooleanField(default=True)
    flashcard_set = models.OneToOneField(
        FlashcardSet,
        on_delete=models.CASCADE,
        related_name='flashcard_set_viewer',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
