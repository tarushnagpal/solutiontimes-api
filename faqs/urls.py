from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from faqs import views

urlpatterns = [
    url(r'^faqs/$', views.FAQList.as_view()),
    url(r'^faqs/(?P<pk>[0-9]+)/$', views.FAQDetail.as_view()),    
]

urlpatterns = format_suffix_patterns(urlpatterns)