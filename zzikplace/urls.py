from django.conf.urls import url
from django.urls import path
from zzikplace import views

app_name = 'zzikplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('around', views.around, name = 'around'),
    path('new/', views.new, name='new'),
    path(r'^detail/?(?P<id>\d+)?/?$', 'detail', name='detail'),  
    path(r'^detail/$', 'detail', name='calculate'),
]

path('<int:id>/', views.detail, name='detail'),