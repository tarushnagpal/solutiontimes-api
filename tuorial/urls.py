from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from allauth.account.views import confirm_email

urlpatterns = [

    url(r'^', include('problemstatements.urls')),
    url(r'^', include('faqs.urls')),
    url(r'^', include('users.urls')),

    path('admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^verify-email/(?P<key>\w+)/$',confirm_email, name="account_confirm_email"),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))


]
