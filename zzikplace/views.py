from django.shortcuts import render
from django.views.generic.base import TemplateView

def index(request):
    return render(request, 'zzikplace/index.html')

def login(request):
    return render(request, 'zzikplace/login.html')

def signup(request):
    return render(request, 'zzikplace/signup.html')

def around(request):
    return render(request, 'zzikplace/around.html')
