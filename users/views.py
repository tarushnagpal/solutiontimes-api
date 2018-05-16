from users.models import User
from users.serializers import UserSerializer
from rest_framework import generics

# Create your views here.
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
