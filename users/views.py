from users.models import User
from users.serializers import CustomRegisterSerializer
from rest_framework import generics

from rest_auth.registration.views import RegisterView

# Create your views here.
class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
