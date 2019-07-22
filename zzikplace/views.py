from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Place, SearchWord

def around(request):
    return render(request, 'zzikplace/around.html')

def index(request):
	if request.method == "GET":
		return render(request, 'zzikplace/index.html')
	
	elif request.method == "POST":
		title = request.POST['selectedName']
		address = request.POST['selectedAddress']
		Place.objects.create(title=title, address=address)
		return redirect('/zzikplace')
		searchwords = SearchWord.objects.first()
		return render(request, 'zzikplace/findplace.html',{'searchwords': searchwords})

def findplace(request):
	if request.method == "POST":
		searchword = request.POST['search-word']
		SearchWord.objects.all().delete()
		SearchWord.objects.create(searchword=searchword)
		searchwords = SearchWord.objects.first()
	return render(request, 'zzikplace/findplace.html',{'searchwords': searchwords})