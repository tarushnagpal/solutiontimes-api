from rest_framework import serializers
from faqs.models import FAQ

class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('id','pub_date','question','answer')
        
