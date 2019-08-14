from django.conf.urls import url
from django.urls import path
from zzikplace import views

app_name = 'zzikplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('around', views.around, name = 'around'),
    path('new/', views.new, name='new'),
    path('my/', views.my, name='my'),
    path('myposts/', views.myposts, name='myposts'),
    path('places', views.places, name='places'),
    path('detail/', views.detail, name='detail'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('detail/<int:id>/add/', views.add, name='add'),
    path('detail/<int:pk>/save/', views.place_save, name='save'),
    path('detail/<int:pk>/like/', views.review_like, name='like'),
    path('tags/<str:tag>/', views.tag_list, name='tag_list'),
]

