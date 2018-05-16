from rest_framework import serializers
from faqs.models import FAQ

from rest_auth.registration.serializers import RegisterSerializer

class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('id','pub_date','question','answer')
        

