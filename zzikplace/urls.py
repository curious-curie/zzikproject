from django.conf.urls import url
from django.urls import path
from zzikplace import views

app_name = 'zzikplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('join', views.join, name='join'),
    path('login', views.login, name='login'),
    path('show', views.show, name='show'),
]