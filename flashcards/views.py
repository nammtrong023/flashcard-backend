from accounts.utils import get_current_user_id
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Flashcard, FlashcardSet, FlashcardSetViewer
from .serializers import (
    FlashcardSerializer,
    FlashcardSetSerializer,
    FlashcardSetViewerSerializer,
)


# Create your views here.
class FlashCardCreateApiView(generics.ListCreateAPIView):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer


class FlashcardRetrieveUpdateDestroyApiView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer

    def delete(self, request, *args, **kwargs):
        flashcard_id = self.kwargs.get('pk')

        try:
            flashcard = Flashcard.objects.get(id=flashcard_id)
        except Flashcard.DoesNotExist:
            raise Response(
                "Flashcard not found", status=status.HTTP_404_NOT_FOUND
            )

        flashcard_set = flashcard.flashcard_set

        if flashcard_set and len(flashcard_set.flashcards.all()) == 4:
            raise ValueError('At least 4 flashcards are required')

        flashcard.delete()

        return Response(
            {
                "message": "Delete flashcard successfully",
            },
            status=status.HTTP_200_OK,
        )


# FLASHCARD_SET
class FlashcardSetListCreateApiView(generics.ListCreateAPIView):
    serializer_class = FlashcardSetSerializer
    queryset = FlashcardSet.objects.all()

    def get(self, request, owner_id):
        owner_id = self.kwargs.get('owner_id')
        queryset = FlashcardSet.objects.filter(owner__id=owner_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FlashcardSetRetrieveUpdateDestroyApiView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = FlashcardSet.objects.all()
    serializer_class = FlashcardSetSerializer

    def put(self, request, *args, **kwargs):
        flashcard_set_id = self.kwargs.get('pk')
        flashcard_set = FlashcardSet.objects.get(id=flashcard_set_id)

        flashcard_set.title = request.data.get('title', flashcard_set.title)
        flashcard_set.description = request.data.get(
            'description', flashcard_set.description
        )

        flashcards_data = request.data.get('flashcards', [])
        for flashcard_data in flashcards_data:
            flashcard_id = flashcard_data.get('id')
            flashcard = Flashcard.objects.get(id=flashcard_id)

            flashcard.term = flashcard_data.get('term', flashcard.term)
            flashcard.definition = flashcard_data.get(
                'definition', flashcard.definition
            )
            flashcard.save()

        flashcard_set.save()

        flashcard_set_serializer = FlashcardSetSerializer(flashcard_set)

        return Response(
            {
                "message": "Update flashcard set successfully",
                "data": flashcard_set_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# FLASHCARD_SET_VIEWER
class FlashcardSetViewerListCreateApiView(generics.ListCreateAPIView):
    queryset = FlashcardSetViewer.objects.all()
    serializer_class = FlashcardSetViewerSerializer


class FlashcardSetViewerByFCardSetIdRetrieveUpdateApiView(
    generics.GenericAPIView
):
    queryset = FlashcardSetViewer.objects.all()
    serializer_class = FlashcardSetViewerSerializer

    def get(self, request, *args, **kwargs):
        flashcard_set_id = self.kwargs.get('pk')

        try:
            flashcard_set = FlashcardSet.objects.get(id=flashcard_set_id)
        except FlashcardSet.DoesNotExist:
            raise NotFound("Flashcard Set not found")

        try:
            flashcard_set_viewer = FlashcardSetViewer.objects.get(
                flashcard_set=flashcard_set
            )
        except FlashcardSetViewer.DoesNotExist:
            raise NotFound("Flashcard Viewer not found")

        return Response(
            FlashcardSetViewerSerializer(flashcard_set_viewer).data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        flashcard_set_id = self.kwargs.get('pk')

        try:
            flashcard_set = FlashcardSet.objects.get(id=flashcard_set_id)
        except FlashcardSet.DoesNotExist:
            raise NotFound("Flashcard Set not found")

        try:
            flashcard_set_viewer = FlashcardSetViewer.objects.get(
                flashcard_set=flashcard_set
            )
        except FlashcardSetViewer.DoesNotExist:
            raise NotFound("Flashcard Viewer not found")

        serializer = FlashcardSetViewerSerializer(
            flashcard_set_viewer, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
