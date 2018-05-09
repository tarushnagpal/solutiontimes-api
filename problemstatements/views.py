from problemstatements.models import ProblemStatement
from problemstatements.serializers import ProblemStatementSerializer
from rest_framework import generics
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
import requests    

class ProblemStatementList(generics.ListCreateAPIView):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer

class ProblemStatementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer