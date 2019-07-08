from django.conf.urls import url
from django.urls import path
from zzikplace import views

app_name = 'zzikplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),   
]