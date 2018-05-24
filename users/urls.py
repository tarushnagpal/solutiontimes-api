from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^rest-auth/registration/$', views.CustomRegisterView.as_view(), name='rest_register' )

]
