from problemstatements.models import ProblemStatement
from problemstatements.serializers import ProblemStatementSerializer
from rest_framework import generics


class ProblemStatementList(generics.ListCreateAPIView):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer

class ProblemStatementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProblemStatement.objects.all()
    serializer_class = ProblemStatementSerializer
