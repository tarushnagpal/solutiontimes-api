from django.db import models
import requests    
import json
import dateutil.parser
import humanize
from datetime import datetime,timezone
from urllib.parse import urlparse,parse_qs


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

    class Meta:
        ordering = ('created',)
