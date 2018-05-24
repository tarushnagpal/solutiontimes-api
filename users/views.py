from users.models import User
from users.serializers import CustomRegisterSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_auth.registration.views import RegisterView

# Create your views here.
class CustomRegisterView(RegisterView):
    queryset = User.objects.all()

class Logout(APIView):
    queryset = User.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        print(request.user)
        return Response(status=status.HTTP_200_OK)