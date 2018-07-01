from django.db import models
import requests    
import json
import dateutil.parser
import humanize
from datetime import datetime,timezone,timedelta
from urllib.parse import urlparse,parse_qs
from users.models import User
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
import isodate

class ProblemStatementPlaylist(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=100, unique=True)
    playlist_url = models.CharField(max_length=100, unique=True, help_text="In format: https://www.youtube.com/watch?v=ev2SkXJVAbA&list=PLOoogDtEDyvsBG38tzlj1Zkd0PLxgZwXV")

    def save(self, *args, **kwargs):
        if self.playlist_url:
            url = self.playlist_url
            url = url.split('=')
            p_id = url[-1]
            all_playlists = requests.get('https://content.googleapis.com/youtube/v3/playlistItems?playlistId=' + p_id + '&maxResults=50&part=snippet%2CcontentDetails&key=AIzaSyDZk4YcpyjFi_05Pic1f46SEGk1bzUa2Jg')
            all_playlists = all_playlists.json()

            for i in all_playlists['items']:
                
                videolink = 'https://www.youtube.com/watch?v=' + i['contentDetails']['videoId']
                print(videolink)
                ProblemStatement.objects.create( videolink = videolink, domain=self.domain )

        super(ProblemStatementPlaylist, self).save(*args, **kwargs)


class ProblemStatement(models.Model):
    
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    submissions = models.IntegerField(default=0, editable=False)
    videolink = models.CharField(max_length=100)

    video_id = models.TextField(default="8tPnX7OPo0Q", editable=False)
    domain = models.CharField(max_length=20,default= "Enter domain")
    title  = models.TextField(default = "Only change if you want to edit, Will fetch from youtube" )
    description = models.TextField(default = "Only change if you want to edit, Will fetch from youtube")
    time_to_show = models.TextField(default = "Only change if you want to edit, Will fetch from youtube")
    thumbnail = models.TextField(default = "https://i.ytimg.com/vi/tgbNymZ7vqY/maxresdefault.jpg")
    duration = models.TextField(default= "4:20" )
    views = models.TextField(default="0")

    views_number = models.TextField(default="0")
    likes_number = models.TextField(default="0")
    dislikes_number = models.TextField(default="0")
    time_number = models.TextField(default="0")

    contestants = models.ManyToManyField(User, through="Solution", related_name="Contestants+")
    mentors = models.ManyToManyField(User, through="Mentor", related_name="Mentors+")
    sponsors = models.ManyToManyField(User, through="Sponsor", related_name="Sponsors+")

    is_today  = models.BooleanField(default=False )
    is_week = models.BooleanField(default=False)
    is_month = models.BooleanField(default=False)
    is_year = models.BooleanField(default=False)
    is_older = models.BooleanField(default=False)
    
    is_short = models.BooleanField(default=False)
    is_medium = models.BooleanField(default=False)
    is_long = models.BooleanField(default=False)    

    def save(self, *args, **kwargs):
        if self.videolink:
                        
            self.video_id = self.get_id()

            youtube_data = requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2C+snippet&id=' + self.video_id + '&part=contentDetails&key=AIzaSyDZk4YcpyjFi_05Pic1f46SEGk1bzUa2Jg')
            view_data = requests.get('https://www.googleapis.com/youtube/v3/videos?part=statistics&id=' + self.video_id + '&key=AIzaSyDZk4YcpyjFi_05Pic1f46SEGk1bzUa2Jg')
            view_data = view_data.json()
            youtube_data = youtube_data.json()
            self.title = self.get_title(youtube_data)
            self.description = self.get_description(youtube_data)
            self.time_to_show = self.get_time(youtube_data)
            self.thumbnail = self.get_thumbnail(youtube_data)
            self.duration = self.get_duration(youtube_data)
            self.views = self.get_views(view_data)
            
            # self.views_number = self.get_viewsnumber(view_data)

            self.set_time_stamps(youtube_data)
            self.set_intervals(youtube_data)

        super(ProblemStatement, self).save(*args, **kwargs)

    def get_id(self):
        url_data = urlparse(self.videolink)
        query = parse_qs(url_data.query)
        return(query["v"][0])
    
    def get_views(self, view_data):
        views = view_data['items'][0]['statistics']['viewCount']
        self.views_number = views
        self.likes_number = view_data['items'][0]['statistics']['likeCount']
        self.dislikes_number = view_data['items'][0]['statistics']['dislikeCount']
        views = humanize.intword(views)
        return(views)

    # def get_viewsnumber(self,view_data):
    #     views = view_data['items'][0]['statistics']['viewCount']
    #     return

    def get_duration(self, youtube_data):
        timeD = youtube_data['items'][0]['contentDetails']['duration']
        formattedTime = timeD.replace("PT","").replace("H",":").replace("M",":").replace("S","")
        return(formattedTime)

    def get_title(self,youtube_data):
        return(youtube_data['items'][0]['snippet']['title'])
    
    def get_description(self,youtube_data):
        return(youtube_data['items'][0]['snippet']['description'])
    
    def get_thumbnail(self,youtube_data):
        return(youtube_data['items'][0]['snippet']['thumbnails']['maxres']['url'] )

    def get_time(self,youtube_data):
        youtube_time = dateutil.parser.parse( youtube_data['items'][0]['snippet']['publishedAt'] )
        current_time = datetime.now( timezone.utc )
        self.time_number = youtube_data['items'][0]['snippet']['publishedAt']
        return(humanize.naturaltime(current_time - youtube_time))
    
    def set_intervals(self,youtube_data):
        duration = isodate.parse_duration(youtube_data['items'][0]['contentDetails']['duration'])
        duration = str(duration).split(':')
        if( int(duration[0]) == 1 ):
            self.is_long = True
        else:
            if( int(duration[1]) < 4 ):
                self.is_short = True
            elif( int(duration[1]) < 15 ):
                self.is_medium = True
            else:
                self.is_long = True

    def set_time_stamps(self,youtube_data):
        youtube_time = dateutil.parser.parse( youtube_data['items'][0]['snippet']['publishedAt'] )
        current_time = datetime.now( timezone.utc )

        monday1 = ( youtube_time - timedelta(days=youtube_time.weekday()))
        monday2 = ( current_time - timedelta(days=current_time.weekday()))

        days = (monday2 - monday1).days

        if(days<1):
            self.is_today = True
        if(days<8):
            self.is_week = True
        if(days<32):
            self.is_month = True
        if(days<366):
            self.is_year = True
        else:
            self.is_older = True



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
    no_of_mentors = models.IntegerField(default=0)

    class Meta:
        unique_together = ('mentor','problemStatement')
    
    def save(self, *args, **kwargs):
        this_user = User.objects.get( email = self.mentor )
        this_user_dict = model_to_dict(this_user) 

        if( this_user_dict['is_mentor'] ):

            this_user.mentor_challenge()
            if(self.is_indivisual):
                self.organization_name = this_user_dict['name']
            
            # print(this_user_dict['mentored'])
            self.email = this_user_dict['email']
            self.no_of_mentors = this_user_dict['mentored_challenges']

        else:
            raise ValidationError("Not a Mentor!")
        
        super(Mentor, self).save(*args, **kwargs)

class Sponsor(models.Model):

    sponsor =  models.ForeignKey(User, on_delete=models.CASCADE )
    problemStatement = models.ForeignKey( ProblemStatement, on_delete=models.CASCADE )

    is_indivisual = models.BooleanField()
    organization_name = models.CharField(max_length=100, blank=True, null=True )
    email = models.EmailField(null=True, blank=True)
    no_of_sponsors = models.IntegerField(default=0)
    
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
            self.no_of_sponsors = this_user_dict['sponsored_challenges']

        else:
            raise ValidationError("Not a Sponsor!")
        
        super(Sponsor, self).save(*args, **kwargs)
