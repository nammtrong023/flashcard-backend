from accounts.models import User
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Class
from .serializer import ClassSerializer, InviteMemberSerializer
from .utils import generate_invite_code


# Create your views here.
class ClassListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()

    def get(self, request, owner_id):
        queryset = Class.objects.filter(owner__id=owner_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, owner_id):
        data = request.data
        data['owner'] = owner_id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            instance.members.add(owner_id)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ClassRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()

    def get(self, request, owner_id, pk):
        queryset = Class.objects.filter(id=pk, owner__id=owner_id)

        if queryset.exists():
            instance = queryset.first()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Class not found'}, status=404)

    def patch(self, request, owner_id, pk):
        queryset = Class.objects.filter(id=pk, owner__id=owner_id)

        if queryset.exists():
            instance = queryset.first()
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )

            if serializer.is_valid():
                flashcard_sets_data = request.data.get('flashcard_sets', [])
                instance.flashcard_sets.clear()

                for flashcard_set_data in flashcard_sets_data:
                    instance.flashcard_sets.add(flashcard_set_data)

                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'detail': 'Class not found'}, status=404)


class InviteMemberAPIView(generics.GenericAPIView):
    serializer_class = InviteMemberSerializer

    def patch(self, request, invite_code):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        try:
            class_instance = Class.objects.get(invite_code=invite_code)
        except Class.DoesNotExist:
            return Response(
                {'message': 'Class not found'}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND
            )

        if class_instance.members.filter(id=user_id).exists():
            return Response(
                {
                    'data': ClassSerializer(class_instance).data,
                },
                status=status.HTTP_200_OK,
            )

        class_instance.members.add(user_id)
        return Response(
            {
                'data': ClassSerializer(class_instance).data,
                'message': 'User added to the class successfully',
            },
            status=status.HTTP_200_OK,
        )
