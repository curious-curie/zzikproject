from django.shortcuts import render
from django.views.generic.base import TemplateView

def index(request):
    return render(request, 'zzikplace/index.html')

def signup(request):
    return render(request, 'zzikplace/signup.html')

def login(request):
    return render(request, 'zzikplace/login.html')