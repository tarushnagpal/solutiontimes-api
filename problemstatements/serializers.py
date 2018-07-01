from rest_framework import serializers
from problemstatements.models import ProblemStatement , Solution, Mentor, Sponsor, ProblemStatementPlaylist
from users.serializers import UserDetailsSerializer

class ProblemStatementPlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemStatementPlaylist
        fields = ('id','domain','playlist_url')

class ProblemStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemStatement
        fields = ('id', 'title', 'description', 'submissions', 'videolink', 'title', 'description', 'time_to_show', 'video_id', 'domain', 'is_today','is_week','is_month','is_year','is_older' ,'is_short' ,'is_medium' ,'is_long', 'thumbnail','duration', 'views' ,'views_number','likes_number','time_number','dislikes_number')
        
class SolutionSerializer(serializers.ModelSerializer):

    problemStatement = ProblemStatementSerializer(read_only=True, many=True )
    user = UserDetailsSerializer(read_only=True, many=True )

    class Meta:
        model = Solution
        fields = ( 'category', 'is_team', 'selected', 'team_name', 'team_size' )

class MentorSerializer(serializers.ModelSerializer):

    problemStatement = ProblemStatementSerializer(read_only=True, many=True )
    user = UserDetailsSerializer(read_only=True, many=True )

    class Meta:
        model = Mentor
        fields = ( 'is_indivisual' , 'organization_name', 'mentored_challenges' )

class SponsorSerializer(serializers.ModelSerializer):

    problemStatement = ProblemStatementSerializer(read_only=True, many=True )
    user = UserDetailsSerializer(read_only=True, many=True )

    class Meta:
        model = Sponsor
        fields = ( 'is_indivisual' , 'organization_name' , 'sponsored_challenges')        
