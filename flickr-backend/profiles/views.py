from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework import permissions
from project.permissions import IsOwner
# Create your views here.


class ProfileList(ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ProfileDetailList(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Profile.objects.all()
    lookup_field = 'id'
