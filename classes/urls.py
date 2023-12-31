from django.urls import path

from . import views

urlpatterns = [
    path('by-owner/<int:owner_id>', views.ClassListCreateApiView.as_view()),
    path(
        'by-group-id/<int:pk>/<int:owner_id>',
        views.ClassRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        'invite/<str:invite_code>',
        views.InviteMemberAPIView.as_view(),
    ),
]
