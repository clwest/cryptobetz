from django.shortcuts import render
from rest_framework import viewsets
from .models import Coindesk
from .serializers import CoindeskSerializer
# Create your views here.


class CoindeskViewSet(viewsets.ModelViewSet):
  queryset = Coindesk.objects.all()
  serializer_class = CoindeskSerializer
