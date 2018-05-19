from rest_framework import serializers
from django.core.validators import validate_email
from users.models import User
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists)
from allauth.account.adapter import get_adapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.base import AuthProcess
from requests.exceptions import HTTPError
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer

from rest_auth.registration.serializers import RegisterSerializer

        

class CustomRegisterSerializer(RegisterSerializer):
    
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    college = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'college': self.validated_data.get('college', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', '')
        }

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','name','college','date_of_birth')
        read_only_fields = ('email',)