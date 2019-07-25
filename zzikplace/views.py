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

def detail(request, id=None):
    if request.method == "POST":
        title = request.POST['place_name']
        address = request.POST['place_addr']
        tip = request.POST['tip']
        photo = request.FILES.get('photo', False)
        time = request.POST['time']
        place, is_place = Place.objects.get_or_create(address=address, title=title)
        id = place.id
        review = Review.objects.create(place_id=id, tip=tip, photo=photo, time=time, author=request.user)
        review.save()
        return render(request, 'zzikplace/detail.html', {'place': place})

    elif request.method == "GET":
        place = Place.objects.get(id=id)
        return render(request, 'zzikplace/detail.html', {'place': place})


def add(request, id=None):
    if id:
        place = Place.objects.get(id=id)
        return render(request, 'zzikplace/add.html', {'place' : place})
    else:
        return render(request, 'zzikplace/new.html')

