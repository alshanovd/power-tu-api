from django.shortcuts import render
from rest_framework import generics
from .models import PowerUser
from .serializers import PowerUserSerializer

# Create your views here.

class PowerUserListCreate(generics.ListCreateAPIView):
    queryset = PowerUser.objects.all()
    serializer_class = PowerUserSerializer