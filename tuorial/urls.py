from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from accounts.views import FacebookLogin,TwitterLogin

urlpatterns = [

    url(r'^', include('problemstatements.urls')),
    url(r'^', include('faqs.urls')),

    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/twitter/$', TwitterLogin.as_view(), name='twitter_login')
]
