from rest_framework import serializers
from problemstatements.models import ProblemStatement
from django.contrib.auth.models import User

class ProblemStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemStatement
        fields = ('id', 'title', 'description', 'submissions', 'videolink', 'title', 'description', 'time_to_show', 'video_id', 'domain')
        
