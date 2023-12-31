from accounts.models import User
from accounts.serializer import UserSerializer
from rest_framework import serializers

from .models import Flashcard, FlashcardSet, FlashcardSetViewer


class FlashcardSerializer(serializers.ModelSerializer):
    flashcard_set = serializers.PrimaryKeyRelatedField(
        queryset=FlashcardSet.objects.all()
    )
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = Flashcard
        fields = ['id', 'flashcard_set', 'term', 'definition', 'quantity']

    def create(self, validated_data):
        flashcard_set_data = validated_data.pop('flashcard_set')
        flashcard_set = FlashcardSet.objects.get(id=flashcard_set_data.id)
        quantity = validated_data.pop('quantity')

        for _ in range(quantity):
            flashcard = Flashcard.objects.create(
                flashcard_set=flashcard_set, **validated_data
            )

        return flashcard


class FlashcardSetViewerSerializer(serializers.ModelSerializer):
    question_types = serializers.ListField()
    flashcard_set = serializers.PrimaryKeyRelatedField(
        queryset=FlashcardSet.objects.all()
    )

    class Meta:
        model = FlashcardSetViewer
        fields = '__all__'

    def validate(self, attrs):
        flashcard_set = attrs.get('flashcard_set')

        try:
            flashcard_set = FlashcardSet.objects.get(id=flashcard_set.id)
        except FlashcardSet.DoesNotExist:
            raise serializers.ValidationError("Flashcard Set does not exist")

        attrs['flashcard_set'] = flashcard_set
        return attrs

    def create(self, validated_data):
        flashcard_set_data = validated_data.pop('flashcard_set')
        flashcard_set = FlashcardSet.objects.get(id=flashcard_set_data.id)

        flashcard_set_viewer = FlashcardSetViewer.objects.create(
            flashcard_set=flashcard_set, **validated_data
        )
        return flashcard_set_viewer


class FlashcardSetSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    flashcards = FlashcardSerializer(many=True, read_only=True)
    flashcard_set_viewer = FlashcardSetViewerSerializer(read_only=True)

    class Meta:
        model = FlashcardSet
        fields = '__all__'

    def create(self, validated_data):
        owner = validated_data.get('owner')
        flashcard_set = FlashcardSet.objects.create(owner_id=owner.id)

        for _ in range(4):
            Flashcard.objects.create(flashcard_set=flashcard_set)

        flashcard_set.save()
        # bulk_create: create multiple records to database

        return flashcard_set
