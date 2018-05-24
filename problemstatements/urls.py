from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from problemstatements import views

urlpatterns = [
    url(r'^problemstatements/$', views.ProblemStatementList.as_view()),
    url(r'^problemstatements/(?P<pk>[0-9]+)/$', views.problemSpecificSolution ),
    url(r'^problemstatements/(?P<pk>[0-9]+)/solution/$', views.postSolution ),
    url(r'^problemstatements/(?P<pk>[0-9]+)/sponsor/$', views.postSponsor ),
    url(r'^problemstatements/(?P<pk>[0-9]+)/mentor/$', views.postMentor )
]

urlpatterns = format_suffix_patterns(urlpatterns)