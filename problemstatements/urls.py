from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from problemstatements import views

urlpatterns = [
    url(r'^problemstatements/$', views.ProblemStatementList.as_view()),
    url(r'^problemstatements/(?P<pk>[0-9]+)/$', views.ProblemStatementDetail.as_view()),    
]

urlpatterns = format_suffix_patterns(urlpatterns)