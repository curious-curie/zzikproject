from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Place, Review
from django.contrib.auth.models import User

def index(request):
    return render(request, 'zzikplace/index.html')

def around(request):
    return render(request, 'zzikplace/index.html')

def new(request):
    return render(request, 'zzikplace/new.html')

def detail(request, id):
    place = Place.objects.get(id=id)
    return render(request, 'zzikplace/detail.html', {'place': place})