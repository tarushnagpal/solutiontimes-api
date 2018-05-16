from rest_framework import serializers
from django.core.validators import validate_email
from users.models import User
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists)
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.base import AuthProcess
from requests.exceptions import HTTPError
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer

from rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'password', 'email', 'name', 'college', 'dob', 'age')
        

class CustomRegisterSerializer(RegisterSerializer):
    
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    college = serializers.CharField(required=True)
    dob = serializers.DateField(required=True)

    def get_cleaned_data(self):
        super(MyRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'college': self.validated_data.get('college', ''),
            'dob': self.validated_data.get('dob', '')
        }

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        # if data['password1'] != data['password2']:
        #     raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'college': self.validated_data.get('college', ''),
            'dob': self.validated_data.get('dob', ''),
        }

    def create(self, validated_data): 
        try:
            return User.objects.create(**validated_data)    
        except (AssertionError):
            raise serializers.ValidationError("Error message")

    def save(self, request):
        adapter = get_adapter()
        
        try: 
            user = adapter.new_user(request)
            self.cleaned_data = self.get_cleaned_data()
            adapter.save_user(request, user, self)
            self.custom_signup(request, user)
            setup_user_email(request, user, [])

        except (AssertionError):
            raise serializers.ValidationError("Error message setup_user_email   ")
        
        return user

    class Meta:
        model = User