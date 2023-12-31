from accounts.models import User
from accounts.serializer import UserSerializer
from flashcards.serializers import FlashcardSetSerializer
from rest_framework import serializers

from .models import Class


class ClassSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    members = UserSerializer(many=True, read_only=True, required=False)
    flashcard_sets = FlashcardSetSerializer(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = Class
        fields = '__all__'


class InviteMemberSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
