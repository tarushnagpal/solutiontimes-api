from django.db import models
import requests    
import json
import dateutil.parser
import humanize
from datetime import datetime,timezone
from urllib.parse import urlparse,parse_qs
from users.models import User
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError

class ProblemStatementPlaylist(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=100, unique=True)
    playlist_url = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if self.playlist_url:
            url = self.playlist_url
            url = url.split('=')
            p_id = url[-1]
            all_playlists = requests.get('https://content.googleapis.com/youtube/v3/playlistItems?playlistId=' + p_id + '&part=snippet%2CcontentDetails&key=AIzaSyDZk4YcpyjFi_05Pic1f46SEGk1bzUa2Jg')
            all_playlists = all_playlists.json()

            for i in all_playlists['items']:
                
                videolink = 'https://www.youtube.com/watch?v=' + i['contentDetails']['videoId']
                print(videolink)
                ProblemStatement.objects.create( videolink = videolink, domain=self.domain )

class ProblemStatement(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    submissions = models.IntegerField(default=0, editable=False)
    videolink = models.CharField(max_length=100)

    video_id = models.TextField(default="8tPnX7OPo0Q", editable=False)
    domain = models.CharField(max_length=20,default= "Enter domain")
    title  = models.TextField(default = "Only change if you want to edit, Will fetch from youtube")
    description = models.TextField(default = "Only change if you want to edit, Will fetch from youtube")
    time_to_show = models.TextField(default = "Only change if you want to edit, Will fetch from youtube")
    
    contestants = models.ManyToManyField(User, through="Solution", related_name="Contestants+")
    mentors = models.ManyToManyField(User, through="Mentor", related_name="Mentors+")
    sponsors = models.ManyToManyField(User, through="Sponsor", related_name="Sponsors+")

    def save(self, *args, **kwargs):
        if self.videolink:
                        
            self.video_id = self.get_id()

            youtube_data = requests.get('https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id=' + self.video_id + '&key=AIzaSyDZk4YcpyjFi_05Pic1f46SEGk1bzUa2Jg')
            youtube_data = youtube_data.json()

            self.title = self.get_title(youtube_data)
            self.description = self.get_description(youtube_data)
            self.time_to_show = self.get_time(youtube_data)

        super(ProblemStatement, self).save(*args, **kwargs)

    def get_id(self):
        url_data = urlparse(self.videolink)
        query = parse_qs(url_data.query)
        return(query["v"][0])

    def get_title(self,youtube_data):
        return(youtube_data['items'][0]['snippet']['title'])
    
    def get_description(self,youtube_data):
        return(youtube_data['items'][0]['snippet']['description'])
    
    def get_time(self,youtube_data):
        youtube_time = dateutil.parser.parse( youtube_data['items'][0]['snippet']['publishedAt'] )
        current_time = datetime.now( timezone.utc )

        return(humanize.naturaltime(current_time - youtube_time))

    def __str__(self):
        return str(self.id)

    # def __unicode__(self):
    #     return '%s %s %s' % (self.title,self.description,self.videolink)

    class Meta:
        ordering = ('created',)

class Solution(models.Model):
 
    contestant = models.ForeignKey(User, on_delete=models.CASCADE )
    problemStatement = models.ForeignKey( ProblemStatement, on_delete=models.CASCADE )
    
    category = models.CharField(choices=(
            ('General', "General"),
            ('Advanced', "Advanced"),
            ('Legendary', "Legendary"),
        ),
        max_length=10, default='General'
    )
    selected = models.BooleanField(default=False, blank=True)
    is_team = models.BooleanField(default=False)
    team_name = models.CharField(max_length=100, blank=True, null=True )
    team_size = models.IntegerField(blank=True, null=True )
    college = models.CharField(max_length=100, null=True, default="Default")

    video_solution = models.CharField(max_length=100, default="default")

    class Meta:
        unique_together = ('contestant','problemStatement')

    def save(self, *args, **kwargs):
    
        this_user = User.objects.get( email = self.contestant )
        this_user_dict = model_to_dict(this_user) 
            
        if( this_user_dict['is_participant'] ):

            this_user.contest_challenge()
            if( self.is_team ):
                print(self.team_name)

            else:            
                self.team_name = this_user_dict['name']

            self.college = this_user_dict['college']

        else:
            raise ValidationError("Not Participant!")

        super(Solution, self).save(*args, **kwargs)

class Mentor(models.Model):

    mentor =  models.ForeignKey(User, on_delete=models.CASCADE )
    problemStatement = models.ForeignKey( ProblemStatement, on_delete=models.CASCADE )

    is_indivisual = models.BooleanField()
    organization_name = models.CharField(max_length=100, blank=True, null=True )
    email = models.EmailField(null=True, blank=True)
    
    class Meta:
        unique_together = ('mentor','problemStatement')
    
    def save(self, *args, **kwargs):
        this_user = User.objects.get( email = self.mentor )
        this_user_dict = model_to_dict(this_user) 

        if( this_user_dict['is_mentor'] ):

            this_user.mentor_challenge()
            if(self.is_indivisual):
                self.organization_name = this_user_dict['name']
            
            self.email = this_user_dict['email']

        else:
            raise ValidationError("Not a Mentor!")
        
        super(Mentor, self).save(*args, **kwargs)

class Sponsor(models.Model):

    sponsor =  models.ForeignKey(User, on_delete=models.CASCADE )
    problemStatement = models.ForeignKey( ProblemStatement, on_delete=models.CASCADE )

    is_indivisual = models.BooleanField()
    organization_name = models.CharField(max_length=100, blank=True, null=True )
    email = models.EmailField(null=True, blank=True)
    
    class Meta:
        unique_together = ('sponsor','problemStatement')

    def save(self, *args, **kwargs):
        this_user = User.objects.get( email = self.sponsor )
        this_user_dict = model_to_dict(this_user) 

        if( this_user_dict['is_sponsor'] ):

            this_user.sponsor_challenge()
            if(self.is_indivisual):
                self.organization_name = this_user_dict['name']
            
            self.email = this_user_dict['email']

        else:
            raise ValidationError("Not a Sponsor!")
        
        super(Sponsor, self).save(*args, **kwargs)
